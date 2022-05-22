# -*- coding: UTF-8 -*-

import shutil
from util.logging import getlogger
from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource
import os
from util.install import *
import requests
import zipfile
import re
import json
import yaml

logger = getlogger()
# requests.exceptions.SSLError
class NucleiPlugin(BasePlugin):
    stagelist = ['fingerprint_detect', 'poc_scan']
    def parse(self) -> dict:
        basedir = os.path.join(os.path.dirname(__file__), "resource", "tmp", self.taskid)
        with open(os.path.join(basedir, "result.json"), "r") as f:
            data = f.read()
        data = re.sub(r"\}\s*\{","},{", data)
        data = f"[{data}]"
        data = json.loads(data)
        result = {}
        for item in data:
            if result.get(item["host"], []) == []:
                result[item["host"]] = []
            result[item["host"]].append(item)
        return result


    def fingerprint_detect(self, target_list: List[ServiceDetectModel]) -> List[FingerprintDetectModel]:
        basedir = os.path.join(os.path.dirname(__file__), "resource", "tmp", self.taskid)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        
        self.config.severity = "info"
        args = self.config.apply_config()
        args.append("-t")
        args.append("technologies")
        url_list = []
        for item in target_list:
            url_list.append(item.geturl())
        with open(os.path.join(basedir, "url.txt"), "w") as f:
            f.write("\n".join(url_list))
        args += ["-o", os.path.join(basedir, "result.json"), "-json", "-l", os.path.join(basedir, "url.txt")]
        self.save_log(" ".join(["./nuclei"] + args))
        p = subprocess.run(["./nuclei"] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.join(os.path.dirname(__file__), "resource"))
        output = p.stdout.decode('utf-8')
        self.save_log(output)
        nuclei_result = self.parse()
        result = []
        for item in target_list:
            nuclei_item = nuclei_result.get(item.geturl(), [])
            fingers = []
            for i in nuclei_item:
                finger = i.get("template-id", "")
                finger = finger.replace("-", "").replace("detect", "")
                match_name = i.get("matcher-name", "")
                if match_name != "":
                    finger += ":" + match_name
                if finger == "":
                    continue
                fingers.append(finger)
            logger.debug(fingers)
            if fingers == []:
                continue
            
            tmp = FingerprintDetectModel.generate(item, fingers)
            result.append(tmp)
        shutil.rmtree(basedir)
        return result
    def poc_scan(self, target_list: List[ServiceDetectModel]) -> List[PocScanModel]:
        basedir = os.path.join(os.path.dirname(__file__), "resource", "tmp", self.taskid)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        
        args = self.config.apply_config()
        url_list = []
        for item in target_list:
            url_list.append(item.geturl())
        with open(os.path.join(basedir, "url.txt"), "w") as f:
            f.write("\n".join(url_list))
        args += ["-o", os.path.join(basedir, "result.json"), "-json", "-l", os.path.join(basedir, "url.txt")]
        self.save_log(" ".join(["./nuclei"] + args))
        p = subprocess.run(["./nuclei"] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.join(os.path.dirname(__file__), "resource"))
        output = p.stdout.decode('utf-8')
        self.save_log(output)
        nuclei_result = self.parse()
        result = []
        for item in target_list:
            nuclei_item = nuclei_result.get(item.geturl(), [])
            for i in nuclei_item:
                title = i.get("info", {}).get("name", "")
                type = title
                plugin = "nuclei"
                info = str(yaml.dump(i.get("info", {})))

                tmp = PocScanModel.generate(item, title, type, plugin, info, "", "")
                result.append(tmp)
        shutil.rmtree(basedir)
        return result



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