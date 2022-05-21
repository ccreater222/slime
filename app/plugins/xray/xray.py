# -*- coding: UTF-8 -*-

from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource

class XrayPlugin(BasePlugin):
    stagelist = ['poc_scan','final_step']
    def poc_scan(self, target_list: List[FingerprintDetectModel]) -> List[PocScanModel]:
        return []
    def final_step(self, target_list: List[BaseModel]) -> List[FinalStepModel]:
        return []

    @staticmethod
    def isinstall():
        return True
    @staticmethod
    def install():
        pass