# -*- coding: UTF-8 -*-

from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource
from util.util import get_ipv4_by_hostname
class IPInfoPlugin(BasePlugin):
    stagelist = ['ip_info']
    def ip_info(self, target_list: List[SubdomainCollectModel]) -> List[IpInfoModel]:
        result = []
        for item in target_list:
            condition = item.toDict()
            condition["ip"] = {"$exists": True}
            condition["iscdn"] = {"$exists": True}
            data = db_resource.find_one(condition)
            if data != None:
                continue
            ips = get_ipv4_by_hostname(item.subdomain)
            for ip in ips:
                result.append(IpInfoModel.generate(item, False, ip))
        return result

    @staticmethod
    def isinstall():
        return True
    @staticmethod
    def install():
        pass