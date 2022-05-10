import os
from importlib import import_module
from typing import  List
import re
from dateutil import parser
import sys

from pymongo.cursor import Cursor 
from pymongo.typings import _DocumentType
from plugins import *
from inspect import getmembers,isclass
from .stage_model import *
from util.util import get_all_keys, hex_objid
from util.client import db_config, db_task

STAGE_LIST = ["info_collect","topdomain_collect","subdomain_collect","ip_info","port_detect","service_detect","fingerprint_detect","poc_scan","final_step"]
PLUGIN_LIST = {}
class InputFilter:
    
    def __init__(self, filter, model,task_id):
        self._filter = filter
        self._model = model
        self._task_id = task_id
        client = db_resource
        if self._model == PocScanModel:
            client = db_vuldata
        self.client = client
    
    def _get_condition(self):
        condition = {}
        all_keys = get_all_stage_model_keys()

        if self._filter.get('columns',[]) != []:
            for k in self._model.get_need_attr():
                if k not in self._filter.get('columns',[]):
                    raise TypeError(f'{self._model.__name__} need {",".join(self._model.get_need_attr())} but only {k} is not given')

        for key in all_keys:
            if key in ['info', 'created', 'updated']:
                continue
            if key not in self._filter.get('columns',[]) and self._filter.get('columns',[]) != []:
                condition[key] = {'$exists': False}



        for k,v in self._filter.get('condition', {}).items():
            if v.strip() == '' or not k in all_keys:
                continue
            if type(v) != str:
                continue
            
            if k == 'finger' or k == 'tag':
                condition[k] = {'$all': [v]}
            elif k == 'port':
                condition[k] = int(v)
            elif k == 'updated':
                try:
                    condition[k] = parser.parse(v)
                except:
                    pass
            else:
                condition[k] = re.compile(re.escape(v))
        
        if self._filter.get('selected', []) == []:
            self._filter['selectall'] = True
        if not self._filter.get('selectall', False):
            condition = {}
            objid_arrays = []
            for item in self._filter.get('selected', []):
                val = item.get('id',None)
                if val == None:
                    continue
                objid_arrays.append(hex_objid(val))
            condition['_id'] = {"$in": objid_arrays}
        result = {}
        if self._task_id == '' or self._task_id == None:
            result = condition
        else:
            columns = {}
            keys = self._model.get_need_attr()
            for k in keys:
                columns[k] = {'$exists': True}
            columns['taskid'] = self._task_id
            result = {'$or': [condition, columns]}
        return result


    def filter(self)->List[BaseModel]:
        resources = self._filter_func()
        # how to convert resources to Model
        return self.cursor_to_model(resources)
    def cursor_to_model(self, resources):
        result = []
        for i in resources:
            try:
                result.append(self._model(**i))
            except Exception as e:
                print(e)
        return result
    def filter_by_page(self) -> list:
        page = self._filter.get('page', 1)
        size = self._filter.get('size',20)
        resources = self._filter_func()
        condition = self._get_condition()
        total = self.client.count_documents(condition)
        if page > 0 and size > 0:
            skip_num = (page - 1) * size
            resources = resources.skip(skip_num).limit(size)
        return [self.cursor_to_model(resources), total, size, page]

    # TODO: sort page tatal
    def _filter_func(self)->Cursor[_DocumentType]:
        self.client = db_resource
        resources = self.client.find(self._get_condition())
        sort_key = self._filter.get('sort', "")
        desc = self._filter.get('desc', False)
        if sort_key != "":
            index = 1
            if desc == True:
                index = -1
            resources = resources.sort([(sort_key, index)])
        return resources


class PluginConfig:

    _slime_name = ''

    def get_all_keys(cls):
        return get_all_keys(cls)
    
    def load_from_database(self, stage, taskid):
        # task config > global config > default config

        global_config = db_config.find_one({'taskid': 'global','stage': 'global','plugin': self._slime_name})
        task_config = db_config.find_one({'taskid': taskid, 'stage': stage, 'plugin': self._slime_name})

        if global_config == None:
            global_config = {'config': {}}
        if task_config == None:
            task_config = {'config': {}}
        for config in [global_config.get('config', {}), task_config.get('config', {})]:
            for k in self.get_all_keys():
                val = config.get(k, None)
                if val:
                    setattr(self, k, val)
    
    def save_to_database(self, stage, taskid):
        record = {'config': {}}
        if stage == 'global':
            record['taskid'] = 'global'
            record['stage'] = 'global'
        else:
            record['taskid'] = taskid
            record['stage'] = stage
        record['plugin'] = self._slime_name

        for k in self.get_all_keys():
            record['config'][k] = getattr(self, k)
        db_config.update_one({'taskid': record['taskid'], 'stage': record['stage'], 'plugin': record['plugin']}, {'$set': record}, upsert=True)
        


    def apply_config(self):
        raise NotImplementedError()

# TODO: 排除当前任务插入的数据，排除同时运行任务插入的数据，根据created?
class BasePlugin:

    stagelist = []
    config:PluginConfig = None
    task_id = ''
    stage = ''

    _slime_config = None
    _slime_name = ''

    def __init__(self) -> None:
        if not self.__class__.isinstall():
            self.__class__.install()
    # stage: 运行阶段
    # filter: 数据库过滤条件
    # task_id: 用于选择上个阶段新发现的资产 ,根据时间来过滤后来添加的数据
    # TODO : 
    def save_log(self, log: str) -> None:
        db_task.update_one({"taskid": self.task_id}, {"$push": {f"log.{self.stage}.{self._slime_name}": log}})

    @classmethod
    def dispatch(cls, stage, filter, task_id):
        # init instance
        instance = cls()
        cls.task_id = task_id
        # load config
        config = cls._slime_config()
        config.load_from_database(stage, task_id)
        config.apply_config()
        instance.config = config
        instance.stage = stage

        # load target
        filter_instance = InputFilter(filter, instance.getmodel(stage).__base__,task_id)

        # run
        result = getattr(instance,stage)(filter_instance.filter())
        # save result

        list(map(lambda x:x.save(),result))

    @staticmethod
    def getmodel(stage):
        stage = stage.replace('_', '')
        for stage_model in STAGE_MODEL_LIST:
            if stage in stage_model.__name__.lower():
                return stage_model

    @staticmethod
    def install():
        raise NotImplementedError()
    
    @staticmethod
    def isintstall():
        raise NotImplementedError()

    def info_collect(self, target_list: List[InfoCollectModel])->List[InfoCollectModel]:
        raise NotImplementedError()

    def topdomain_collect(self,target_list: List[InfoCollectModel])->List[TopdomainCollectModel]:
        raise NotImplementedError()

    def subdomain_collect(self,target_list: List[TopdomainCollectModel])->List[SubdomainCollectModel]:
        raise NotImplementedError()

    def ip_info(self,target_list: List[SubdomainCollectModel])->List[IpInfoModel]:
        raise NotImplementedError()

    def port_detect(self,target_list: List[IpInfoModel])->List[PortDetectModel]:
        raise NotImplementedError()

    def service_detect(self,target_list: List[PortDetectModel])->List[ServiceDetectModel]:
        raise NotImplementedError()
    
    def fingerprint_detect(self,target_list: List[ServiceDetectModel])->List[FingerprintDetectModel]:
        raise NotImplementedError()
    
    def poc_scan(self,target_list: List[FingerprintDetectModel])->List[PocScanModel]:
        raise NotImplementedError()
    
    def final_step(self,target_list: List[PocScanModel])->List[FinalStepModel]:
        raise NotImplementedError()

def load_plugin(name):    
    plugin_clazz = None
    config_clazz = None
    description = None
    modulename = f'plugins.{name}.{name}'
    if modulename not in sys.modules:
        module = import_module(modulename)
    else:
        module = sys.modules[modulename]
    classes = getmembers(module, isclass)
    for clazzname,clazz in classes:
        if BasePlugin != clazz and issubclass(clazz,BasePlugin):
            plugin_clazz = clazz
            plugin_clazz._slime_name = name
            
    # load config
    modulename = f'plugins.{name}.config'
    if modulename not in sys.modules:
        module = import_module(modulename)
    else:
        module = sys.modules[modulename]
    classes = getmembers(module,isclass)
    description = getattr(module, "description", "")
    for clazzname,clazz in classes:
        if clazz != PluginConfig and issubclass(clazz,PluginConfig):
            config_clazz = clazz
            plugin_clazz._slime_config = config_clazz
            config_clazz._slime_name = name

    return {
        'config': {
            'clazz': config_clazz,
            'description': description
        },
        'plugin': plugin_clazz,
        'name': name
    }

def load_plugins():
    if PLUGIN_LIST != {}:
        return PLUGIN_LIST
    current_dir = os.path.dirname(__file__)
    with os.scandir(os.path.join(current_dir,'..','plugins')) as it:
        for entry in it:
            if not entry.name.startswith('.') and not entry.name.startswith('_') and entry.is_dir():
                plugin_info = load_plugin(entry.name)
                PLUGIN_LIST[plugin_info['name']] = plugin_info


