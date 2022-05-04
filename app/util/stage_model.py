

# 每个阶段输入至少要有上个阶段的model属性的字段
# 每个阶段输出至少要有这个阶段的model属性的字段
from datetime import datetime
from unicodedata import name


class BaseModel:
    tag: list
    created: datetime
    updated: datetime
    taskid: str
    # TODO
    def save():
        pass
    pass

class InfoCollectModel(BaseModel):
    name: str

class TopdomainCollectModel(InfoCollectModel):
    topdomain: str

class SubdomainCollectModel(TopdomainCollectModel):
    subdomain: str

class IpInfoModel(SubdomainCollectModel):
    iscdn: bool
    ip: str

class PortDetectModel(IpInfoModel):
    port: int

class ServiceDetectModel(PortDetectModel):
    service: str
    info: dict

class FingerprintDetectModel(ServiceDetectModel):
    finger: list

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

class FinalStepModel(FingerprintDetectModel):
    pass

STAGE_MODEL_LIST = [InfoCollectModel,TopdomainCollectModel,SubdomainCollectModel,IpInfoModel,PortDetectModel,ServiceDetectModel,FingerprintDetectModel,PocScanModel,FinalStepModel]