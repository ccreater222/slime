# -*- coding: UTF-8 -*-
from util.client import db_vuldata
from datetime import datetime
from util.stage_model import ServiceDetectModel
from util.util import get_all_keys
import re

class VulData:
    name: str
    ip: str
    port: int
    topdomain: str
    subdomain: str
    title: str
    type: str
    plugin: str
    info: str
    req: str
    resp: str
    tag: list
    created: datetime

    def __init__(self, name: str = "", ip: str = "",\
    port: str = "", topdomain: str = "", \
    subdomain: str = "", title: str = "", \
    type: str = "", plugin: str = "", \
    info: str = "", req: str = "", resp: str = "",
    tag: list = [], created: datetime = None, *args, **kwargs) -> None:
        if created == None:
            self.created = datetime.now()
        else:
            self.created = created
        self.name = name
        self.ip = ip
        self.port = port
        self.topdomain = topdomain
        self.subdomain = subdomain
        self.title = title
        self.type = type
        self.plugin = plugin
        self.info = info
        self.req = req
        self.resp = resp
        self.tag = tag
        for k, v in kwargs.items():
            setattr(self, k, v)
        
        
    @classmethod
    def load_from_service(cls, service: ServiceDetectModel, title: str = "", \
    type: str = "", plugin: str = "", info: str = "", req: str = "", resp: str = "", tag:list = []):
        return cls(service.name, service.ip, service.port, service.topdomain, service.subdomain, \
            title, type, plugin, info, req, resp, tag, datetime.now())
    
    def toDict(self):
        result = {}
        all_keys = get_all_keys(self)
        for k in all_keys:
            result[k] = getattr(self, k)
        return result

    def save(self):
        db_vuldata.insert_one(self.toDict())
    
    @classmethod
    def load_from_database(cls, filter:dict):
        condition = filter.get('condition', {})
        for k, v in condition.items():
            if type(v) == str:
                condition[k] = re.compile(re.escape(v))
        data = db_vuldata.find(condition)
        sort_key = filter.get('sort', "")
        desc = filter.get('desc', False)
        if sort_key != "":
            index = 1
            if desc == True:
                index = -1
            data = data.sort([(sort_key, index)])
        total = db_vuldata.count_documents(condition)
        data = data.skip((filter.get('page') -1) * filter.get('size', 20)).limit(filter.get('size', 20))
        result = []
        for item in data:
            result.append(cls(**item))
        return total, result
        
