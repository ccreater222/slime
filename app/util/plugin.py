import os
from importlib import import_module
from typing import List
from plugins import *
from inspect import getmembers,isclass,ismethod,isfunction
from .stage_model import *

STAGE_LIST = ["info_collect","topdomain_collect","subdomain_collect","ip_info","port_detect","service_detect","fingerprint_detect","poc_scan","final_step"]
PLUGIN_LIST = {}
class InputFilter:
    
    def __init__(self, filter, model,task_id):
        self._filter = filter
        self._model = model
        self._task_id = task_id

    def filter(self)->List[BaseModel]:
        return []

class PluginConfig:

    _slime_name = ''

    @classmethod
    def get_all_keys(cls):
        all_keys = []
        for name,_ in getmembers(cls,lambda x: not ismethod(x) and not isfunction(x)):
            if name.startswith('_'):
                continue
            all_keys.append(name)
        return all_keys
    
    # TODO
    def load_from_database(self, stage, task_id):
        pass

    # TODO 将配置引用到插件
    def apply_config(self):
        raise NotImplementedError()

# TODO: 排除当前任务插入的数据，排除同时运行任务插入的数据，根据created?
class BasePlugin:

    stagelist = []
    config:PluginConfig = None

    _slime_config = None
    _slime_name = ''

    def __init__(self) -> None:
        pass
    # stage: 运行阶段
    # filter: 数据库过滤条件
    # task_id: 用于选择上个阶段新发现的资产 ,根据时间来过滤后来添加的数据
    @classmethod
    def dispatch(cls, stage, filter, task_id):
        # is install
        if  not cls.isintstall():
            cls.install()

        # init instance
        instance = cls()
        # load config
        config = cls._slime_config()
        config.load_from_database(stage, task_id)
        config.apply_config()
        instance.config = config

        # load target
        filter_instance = InputFilter(filter, None,task_id)

        # run
        result = getattr(instance,stage)(filter_instance.filter())

        # save result
        map(lambda x:x.save(),result)

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
                
