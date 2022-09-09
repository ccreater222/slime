# -*- coding: UTF-8 -*-

from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource


class SkipPlugin(BasePlugin):
    stagelist = ['info_collect', 'topdomain_collect', 'subdomain_collect', 'ip_info',
                 'port_detect', 'service_detect', 'fingerprint_detect', 'poc_scan', 'final_step']

    def info_collect(self, target_list: List[InfoCollectModel]) -> List[InfoCollectModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition['name'] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            result.append(InfoCollectModel.generate(item, ""))
        return result

    def topdomain_collect(self, target_list: List[InfoCollectModel]) -> List[TopdomainCollectModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["topdomain"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            result.append(TopdomainCollectModel.generate(item, ""))
        return result

    def subdomain_collect(self, target_list: List[TopdomainCollectModel]) -> List[SubdomainCollectModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["subdomain"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            result.append(SubdomainCollectModel.generate(item, ""))
        return result

    def ip_info(self, target_list: List[SubdomainCollectModel]) -> List[IpInfoModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["ip"] = {"$exists": True}
            condition["iscdn"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            result.append(IpInfoModel.generate(item, False, ""))
        return result

    def port_detect(self, target_list: List[IpInfoModel]) -> List[PortDetectModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["port"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            result.append(PortDetectModel.generate(item, 0))
        return result

    def service_detect(self, target_list: List[PortDetectModel]) -> List[ServiceDetectModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["service"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            service_item = ServiceDetectModel.generate(item, "", {})
            service_item.geturl()
            result.append(service_item)
        return result

    def fingerprint_detect(self, target_list: List[ServiceDetectModel]) -> List[FingerprintDetectModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["finger"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            result.append(FingerprintDetectModel.generate(item, []))
        return result

    def poc_scan(self, target_list: List[ServiceDetectModel]) -> List[PocScanModel]:
        return []

    def final_step(self, target_list: List[BaseModel]) -> List[FinalStepModel]:
        return []

    @staticmethod
    def isinstall():
        return True

    @staticmethod
    def install():
        pass
