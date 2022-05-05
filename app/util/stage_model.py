

# 每个阶段输入至少要有上个阶段的model属性的字段
# 每个阶段输出至少要有这个阶段的model属性的字段
from datetime import datetime
from bson import ObjectId
from util.util import get_all_keys


class BaseModel:
    _id: ObjectId
    tag: list
    created: datetime
    updated: datetime
    taskid: str
    # TODO 去重?
    def save(self):
        
        print(self.ip,self.port)

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
            obj[key] = getattr(self, key)
        return obj

class InfoCollectModel(BaseModel):
    name: str
    def __init__(self, name) -> None:
        self.name = name

class TopdomainCollectModel(InfoCollectModel):
    topdomain: str
    def __init__(self, topdomain) -> None:
        self.topdomain = topdomain

class SubdomainCollectModel(TopdomainCollectModel):
    subdomain: str
    def __init__(self, subdomain) -> None:
        self.subdomain = subdomain

class IpInfoModel(SubdomainCollectModel):
    iscdn: bool
    ip: str
    def __init__(self, iscdn, ip) -> None:
        self.iscdn = iscdn
        self.ip = ip

class PortDetectModel(IpInfoModel):
    port: int
    def __init__(self, port) -> None:
        self.port = port

class ServiceDetectModel(PortDetectModel):
    service: str
    info: dict
    def __init__(self, service, info) -> None:
        self.service = service
        self.info = info

class FingerprintDetectModel(ServiceDetectModel):
    finger: list
    def __init__(self, finger) -> None:
        self.finger = finger
class PocScanModel(FingerprintDetectModel):
    title: str
    type: str
    plugin: str
    info: str
    req: str
    resp: str
    # TODO: pocscan保存到别的地方
    def save(self):
        pass
    def __init__(self, title, type, plugin, info, req, resp) -> None:
        self.title = title
        self.type = type
        self.plugin = plugin
        self.info = info
        self.req = req
        self.resp = resp

class FinalStepModel(FingerprintDetectModel):
    pass

STAGE_MODEL_LIST = [InfoCollectModel,TopdomainCollectModel,SubdomainCollectModel,IpInfoModel,PortDetectModel,ServiceDetectModel,FingerprintDetectModel,PocScanModel,FinalStepModel]