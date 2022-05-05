

# 每个阶段输入至少要有上个阶段的model属性的字段
# 每个阶段输出至少要有这个阶段的model属性的字段
from datetime import datetime
from bson import ObjectId
from util.util import dotset, get_all_keys
from util.client import db_resource,db_vuldata

class BaseModel:
    _id: ObjectId
    tag: list
    created: datetime
    updated: datetime
    taskid: str
    _index_keys = ['name', 'topdomain', 'subdomain', 'ip', 'port']
    def save(self):
        if not hasattr(self,'created'):
            self.created = datetime.now()
            self.updated = datetime.now()
        else:
            self.updated = datetime.now()
        # prepare index key
        condition = {}
        update = {}
        for key in self._index_keys:
            if hasattr(self, key):
                condition[key] = getattr(self, key)
            else:
                condition[key] = {'$exists': False}
        data = self.toDict()
        array_key = []
        dict_key = []
        # merge list
        for k,v in data.items():
            if type(v) == list:
                array_key.append(k)
            if type(v) == dict:
                dict_key.append(k)

        if len(array_key) > 0:
            update['$push'] = {}
        
        for k in array_key:
            update['$push'][k] = {
                '$each': data[k]
            }
            del data[k]

        # merge dict    
        for k in dict_key:
            result = dotset(data[k])
            for v in result:
                data[f'{k}.'+v[0]] = v[1]
            del data[k]

        update['$set'] = data
        db_resource.update_one(condition,update,upsert=True)
        

    def get_all_keys(self):
        return get_all_keys(self)
    
    @classmethod
    def generate(cls, model,*args, **kwargs):
        model_keys = model.get_all_keys()
        instance = cls(*args, **kwargs)
        for key in model_keys:
            setattr(instance, key, getattr(model, key))
        return instance
    
    def toDict(self):
        obj = {}
        for key in self.get_all_keys():
            val = getattr(self, key)
            if getattr(self.__annotations__, key, None) != None and type(val) != getattr(self.__annotations__, key, None):
                target_type = getattr(self.__annotations__, key, None)
                real_type = type(val)
                if target_type == str:
                    val = str(val)
                elif target_type == int and real_type == str:
                    val = int(val)
                elif target_type == list:
                    val = [val]
                else:
                    raise TypeError()
            obj[key] = val
        return obj

class InfoCollectModel(BaseModel):
    name: str
    def __init__(self, name:str) -> None:
        if type(name) != str:
            raise TypeError()
        self.name = name

class TopdomainCollectModel(InfoCollectModel):
    topdomain: str
    def __init__(self, topdomain:str) -> None:
        if type(topdomain) != str:
            raise TypeError()
        self.topdomain = topdomain

class SubdomainCollectModel(TopdomainCollectModel):
    subdomain: str
    def __init__(self, subdomain:str) -> None:
        if type(subdomain) != str:
            raise TypeError()
        self.subdomain = subdomain

class IpInfoModel(SubdomainCollectModel):
    iscdn: bool
    ip: str
    def __init__(self, iscdn: bool, ip: str) -> None:
        if type(iscdn) != bool:
            raise TypeError()
        if type(ip) != str:
            raise TypeError()
        self.iscdn = iscdn
        self.ip = ip

class PortDetectModel(IpInfoModel):
    port: int
    def __init__(self, port: int) -> None:
        if type(port) != int :
            raise TypeError()
        self.port = port

class ServiceDetectModel(PortDetectModel):
    service: str
    info: dict
    def __init__(self, service: str, info: dict) -> None:
        if type(service) != str:
            raise TypeError()
        if type(info) != dict:
            raise TypeError()
        self.service = service
        self.info = info

class FingerprintDetectModel(ServiceDetectModel):
    finger: list
    def __init__(self, finger:list) -> None:
        if type(finger) != list:
            raise TypeError(finger)
        self.finger = finger
class PocScanModel(PortDetectModel):
    title: str
    type: str
    plugin: str
    info: str
    req: str
    resp: str
    # TODO: pocscan保存到别的地方
    def save(self):
        if not hasattr(self,'created'):
            self.created = datetime.now()
            self.updated = datetime.now()
        else:
            self.updated = datetime.now()
        db_vuldata.insert_one(self.toDict())

    def __init__(self, title, type, plugin, info, req, resp) -> None:
        for i in [title, type, plugin, info, req, resp]:
            if type(i) != str:
                raise TypeError()
        self.title = title
        self.type = type
        self.plugin = plugin
        self.info = info
        self.req = req
        self.resp = resp

class FinalStepModel(FingerprintDetectModel):
    pass

STAGE_MODEL_LIST = [InfoCollectModel,TopdomainCollectModel,SubdomainCollectModel,IpInfoModel,PortDetectModel,ServiceDetectModel,FingerprintDetectModel,PocScanModel,FinalStepModel]