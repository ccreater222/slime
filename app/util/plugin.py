import os
from importlib import import_module
from typing import List
from plugins import *
from inspect import getmembers,isclass
from .stage_model import *
from util.util import get_all_keys, hex_objid
from util.client import db_config

STAGE_LIST = ["info_collect","topdomain_collect","subdomain_collect","ip_info","port_detect","service_detect","fingerprint_detect","poc_scan","final_step"]
PLUGIN_LIST = {}
class InputFilter:
    
    def __init__(self, filter, model,task_id):
        self._filter = filter
        self._model = model
        self._task_id = task_id

    def filter(self)->List[BaseModel]:
        condition = {}
        all_keys = get_all_stage_model_keys()

        if self._filter.get('columes',[]) != []:
            for k in self._model.get_need_attr():
                if k not in self._filter.get('columes',[]):
                    raise TypeError()

        for key in all_keys:
            if key in ['info', 'created']:
                continue
            if key not in self._filter.get('columes',[]) and self._filter.get('columes',[]) != []:
                condition[key] = {'$exists': False}

        for k,v in self._filter.get('condition', {}).items():
            if v.strip() == '' or not k in all_keys:
                continue
            if type(v) != str:
                continue
            
            if k == 'finger' or k == 'tag':
                condition[k] = {'$all': [v]}
            elif k == 'port':
                condition[k] = int(k)
            elif k == 'updated':
                continue
            else:
                condition[k] = v
        
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
        if self._task_id == '' or self._task_id == None:
            resources = db_resource.find(condition)
        else:
            columes = {}
            keys = self._model.get_need_attr()
            for k in keys:
                columes[k] = {'$exists': True}
            columes['taskid'] = self._task_id
            resources = db_resource.find({'$or': [condition, columes]})
        # how to convert resources to Model
        result = []
        for i in resources:
            try:
                result.append(self._model(**i))
            except Exception as e:
                print(i)
        return result

class PluginConfig:

    _slime_name = ''

    def get_all_keys(cls):
        return get_all_keys(cls)
    
    # TODO
    def load_from_database(self, stage, taskid):
        # task config > global config > default config

        global_config = db_config.find_one({'taskid': 'global','stage': 'global','plugin': self._slime_name})
        task_config = db_config.find_one({'taskid': taskid, 'stage': stage, 'plugin': self._slime_name})

        if global_config == None:
            global_config = {'config': {}}
        if task_config == None:
            global_config = {'config': {}}
        
        for config in [global_config['config'], task_config['config']]:
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
        


    # TODO 将配置引用到插件
    def apply_config(self):
        raise NotImplementedError()

# TODO: 排除当前任务插入的数据，排除同时运行任务插入的数据，根据created?
class BasePlugin:

    stagelist = []
    config:PluginConfig = None
    task_id = ''

    _slime_config = None
    _slime_name = ''

    def __init__(self) -> None:
        pass
    # stage: 运行阶段
    # filter: 数据库过滤条件
    # task_id: 用于选择上个阶段新发现的资产 ,根据时间来过滤后来添加的数据
    def save_log(log: str) -> None:
        pass

    @classmethod
    def dispatch(cls, stage, filter, task_id):
        # is install
        if  not cls.isintstall():
            cls.install()

        # init instance
        instance = cls()
        cls.task_id = task_id
        # load config
        config = cls._slime_config()
        config.load_from_database(stage, task_id)
        config.apply_config()
        instance.config = config

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

    module = import_module(f'plugins.{name}.{name}')
    classes = getmembers(module, isclass)
    for clazzname,clazz in classes:
        if BasePlugin != clazz and issubclass(clazz,BasePlugin):
            plugin_clazz = clazz
            plugin_clazz._slime_name = name
            
    # load config
    module = import_module(f'plugins.{name}.config')
    classes = getmembers(module,isclass)
    description = module.description
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
                
