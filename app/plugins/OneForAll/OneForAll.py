from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.install import *
import os

class OneForAllPlugin(BasePlugin):
    stagelist = ['subdomain_collect']
    def subdomain_collect(self, target_list: List[TopdomainCollectModel]) -> List[SubdomainCollectModel]:
        result = []
        for item in target_list:
            result.append(SubdomainCollectModel.generate(item, ""))
        return result

    @staticmethod
    def isinstall():
        return True

    @staticmethod
    def install():
        install_python3()
        