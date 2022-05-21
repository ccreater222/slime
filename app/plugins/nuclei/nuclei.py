# -*- coding: UTF-8 -*-

from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource
import os
from util.install import *
import requests
import zipfile


class NucleiPlugin(BasePlugin):
    stagelist = ['fingerprint_detect', 'poc_scan']
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
    def poc_scan(self, target_list: List[FingerprintDetectModel]) -> List[PocScanModel]:
        return []



    @staticmethod
    def isinstall():
        current_dir = os.path.dirname(__file__)
        return os.path.exists(os.path.join(current_dir,'resource','nuclei'))

    @staticmethod
    def install():
        r = requests.get("https://github.com/projectdiscovery/nuclei/releases/latest/", proxies={"http": PROXY, "https": PROXY})
        version = r.url.split("/v")[1]
        current_dir = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(current_dir, "resource")):
            os.mkdir(os.path.join(current_dir, "resource"))
        download_url = 'https://github.com/projectdiscovery/nuclei/releases/latest/download/'
        filename = ''
        download_url += f'nuclei_{version}_linux_amd64.zip'
        filename = 'nuclei.zip'
        if not os.path.exists(os.path.join(current_dir,'resource')):
            os.mkdir(os.path.join(current_dir,'resource'))
        r = requests.get(download_url, proxies={"http": PROXY, "https": PROXY})
        with open(os.path.join(current_dir,'resource',filename),'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(os.path.join(current_dir,'resource',filename), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(current_dir,'resource'))
        os.remove(os.path.join(current_dir,'resource',filename))
        os.system(f"chmod +x {os.path.join(current_dir,'resource')}/nuclei")
        # template
        r = requests.get("https://github.com/projectdiscovery/nuclei-templates/releases/latest/", proxies={"http": PROXY, "https": PROXY})
        version = r.url.split("/v")[1] 
        r = requests.get(f"https://github.com/projectdiscovery/nuclei-templates/archive/refs/tags/v{version}.zip", proxies={"http": PROXY, "https": PROXY})
        with open(os.path.join(current_dir,'resource',"template.zip"),'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(os.path.join(current_dir,'resource',"template.zip"), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(current_dir,'resource'))
        os.rename(os.path.join(current_dir,'resource',f"nuclei-templates-{version}"), os.path.join(current_dir,'resource',f"nuclei-templates"))
        os.remove(os.path.join(current_dir,'resource',"template.zip"))
        p = subprocess.run(["./nuclei", "-ud", os.path.join(current_dir,'resource',f"nuclei-templates"), "-duc"] ,cwd = os.path.join(current_dir, "resource"))
        p.check_returncode()