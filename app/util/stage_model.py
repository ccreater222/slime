# -*- coding: UTF-8 -*-



# 每个阶段输入至少要有上个阶段的model属性的字段
# 每个阶段输出至少要有这个阶段的model属性的字段
from datetime import datetime
from bson import ObjectId
import requests
from util.util import dotset, get_all_keys
from util.client import db_resource,db_vuldata
from dateutil import parser as dateparser
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class BaseModel:
    _id: ObjectId
    tag: list
    created: datetime
    updated: datetime
    taskid: str
    _index_keys = ['name', 'topdomain', 'subdomain', 'ip', 'port']
    def __init__(self, *args, **kwargs) -> None:
        all_annotations = FinalStepModel.get_all_annotations()
        for k,v in kwargs.items():
            self.__annotations__[k] = all_annotations[k]
            setattr(self, k, v)
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
        
    @classmethod
    def load_from_db(cls, record):
        instance = cls(**record)
    
    def get_all_keys(self):
        return get_all_keys(self)
    
    @classmethod
    def get_all_annotations(cls):
        if getattr(cls, '_all_annotations', None):
            return getattr(cls, '_all_annotations')
        parent = cls
        annotations = {}
        while True:
            if parent == object:
                break
            for k,v in parent.__annotations__.items():
                annotations[k] = v
            parent = parent.__base__
        setattr(cls,'_all_annotations', annotations)
        return annotations

    @classmethod
    def get_need_attr(cls):
        if getattr(cls, '_all_attr', None):
            return getattr(cls, '_all_attr')
        
        parent = cls
        attrs = []
        while True:
            if parent == BaseModel:
                break

            attrs = attrs + list(parent.__annotations__.keys())
            try:
                attrs.remove('_id')
            except:
                pass
            parent = parent.__base__
        setattr(cls, '_all_attr', attrs)
        return attrs
    @classmethod
    def generate(cls, model,*args, **kwargs):
        model_keys = model.get_all_keys()
        instance = cls(*args, **kwargs)
        for key in model_keys:
            if getattr(instance, key, None) != None:
                continue
            setattr(instance, key, getattr(model, key))
        return instance
    
    def toDict(self):
        obj = {}
        for key in self.get_all_keys():
            val = getattr(self, key)
            if val == None:
                continue
            if self.__annotations__.get(key, None) != None and type(val) != self.__annotations__.get(key, None):
                target_type = self.__annotations__.get(key, None)
                real_type = type(val)
                if target_type == str:
                    val = str(val)
                elif target_type == int and real_type == str:
                    val = int(val)
                elif target_type == list:
                    val = [val]
                elif target_type == datetime:
                    val = dateparser.parse(val)
                elif target_type == bool:
                    if type(val) == str:
                        if val.lower() == "true":
                            val = True
                        else:
                            val = False
                else:
                    raise TypeError(f"target type is {target_type.__name__} but real type is {real_type.__name__}({key}:{val})")
            obj[key] = val
        return obj

class InfoCollectModel(BaseModel):
    name: str
    def __init__(self, name:str, *args, **kwargs) -> None:
        if type(name) != str:
            raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.name = name

class TopdomainCollectModel(InfoCollectModel):
    topdomain: str
    def __init__(self, topdomain:str, *args, **kwargs) -> None:
        if type(topdomain) != str:
            raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.topdomain = topdomain
class SubdomainCollectModel(TopdomainCollectModel):
    subdomain: str
    def __init__(self, subdomain:str, *args, **kwargs) -> None:
        if type(subdomain) != str:
            raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.subdomain = subdomain

class IpInfoModel(SubdomainCollectModel):
    iscdn: bool
    ip: str
    def __init__(self, iscdn: bool, ip: str, *args, **kwargs) -> None:
        if type(iscdn) != bool:
            raise TypeError()
        if type(ip) != str:
            raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.iscdn = iscdn
        self.ip = ip

class PortDetectModel(IpInfoModel):
    port: int
    def __init__(self, port: int, *args, **kwargs) -> None:
        if type(port) != int :
            raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.port = port

class ServiceDetectModel(PortDetectModel):
    service: str
    info: dict
    def __init__(self, service: str, info: dict, *args, **kwargs) -> None:
        if type(service) != str:
            raise TypeError()
        if type(info) != dict:
            raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.service = service
        self.info = info
    def geturl(self):
        if self.info.get("isweb", "").lower() == "false":
            return f"{self.ip}:{self.port}"

        url = self.info.get("url", "")
        if url != "":
            return url
        
        if "https" in self.service:
            return f"https://{self.ip}:{self.port}"
        
        scheme = ""
        try:
            r = requests.get(f"https://{self.ip}:{self.port}", verify=False)
            scheme = "https"
        except requests.exceptions.SSLError:
            # not ssl
            pass
        except requests.exceptions.ConnectionError:
            # is ssl but not https
            self.info["isweb"] = "false"
            self.save()
            return f"{self.ip}:{self.port}"
        except:
            pass
        if scheme == "":
            try:
                r = requests.get(f"http://{self.ip}:{self.port}")
                scheme = "http"
            except requests.exceptions.ConnectionError:
                pass
        
        if scheme == "":
            self.info["isweb"] = "false"
            self.save()
            return f"{self.ip}:{self.port}"
        else:
            self.info["isweb"] = "true"
            self.info["url"] = f"{scheme}://{self.ip}:{self.port}"
            self.save()
            return self.info["url"]
        
        

class FingerprintDetectModel(ServiceDetectModel):
    finger: list
    def __init__(self, finger:list, *args, **kwargs) -> None:
        if type(finger) != list:
            raise TypeError(finger)
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.finger = finger
class PocScanModel(ServiceDetectModel):
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

    def __init__(self, title, vultype, plugin, info, req, resp, *args, **kwargs) -> None:
        for i in [title, vultype, plugin, info, req, resp]:
            if type(i) != str:
                raise TypeError()
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e
        self.title = title
        self.type = vultype
        self.plugin = plugin
        self.info = info
        self.req = req
        self.resp = resp

class FinalStepModel(FingerprintDetectModel):
    def __init__(self,  *args, **kwargs) -> None:
        try:
            super().__init__(**kwargs)
        except Exception as e:
            if len(kwargs.keys()) > 0:
                raise e

STAGE_MODEL_LIST = [InfoCollectModel,TopdomainCollectModel,SubdomainCollectModel,IpInfoModel,PortDetectModel,ServiceDetectModel,FingerprintDetectModel,PocScanModel,FinalStepModel]

def get_all_stage_model_keys():
    keys = []
    for stage in STAGE_MODEL_LIST + [BaseModel]:
        if stage == PocScanModel:
            continue
        keys = keys + list(getattr(stage, '__annotations__',{}).keys())
    keys.remove('_id')
    return list(set(keys))