# -*- coding: UTF-8 -*-

from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource
import os
from config.plugin import PROXY
import zipfile
import subprocess
from util.logging import getlogger
import json
from .util import parse_result_file

logger =  getlogger()
class SubfinderPlugin(BasePlugin):
    stagelist = ['subdomain_collect']
    def subdomain_collect(self, target_list: List[TopdomainCollectModel]) -> List[SubdomainCollectModel]:
        options = self.config.apply_config()
        basedir = os.path.join(os.path.dirname(__file__), "resource")
        tmpdir = os.path.join(basedir, "tmp", self.taskid)
        target_domain_file = os.path.join(tmpdir, "target.txt")
        result_path = os.path.join(tmpdir, "result.json")
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        

        domains = []
        for item in target_list:
            domains.append(item.topdomain)
        domains = list(set(domains))
        logger.debug(" ".join(domains))
        with open(target_domain_file, "w") as f:
            f.write("\n".join(domains))
        args = ["./subfinder", "-dL", target_domain_file, "-oJ", "-o", result_path]
        args += options
        process = subprocess.run(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, cwd = basedir)
        output = process.stdout.decode('utf-8')
        self.save_log(' '.join(args))
        self.save_log(output)
        return_data = []
        result = parse_result_file(result_path)
        for subdomain, topdomain in result:
            for i in target_list:
                if i.topdomain != topdomain:
                    continue
                tmp = SubdomainCollectModel.generate(i, subdomain)
                return_data.append(tmp)
                logger.debug(f"[+] found subdomain: {subdomain}")

        return return_data


    @staticmethod
    def isinstall():
        current_dir = os.path.dirname(__file__)
        return os.path.exists(os.path.join(current_dir,'resource','subfinder'))
    @staticmethod
    def install():
        current_dir = os.path.dirname(__file__)
        download_url = 'https://github.com/projectdiscovery/subfinder/releases/latest/download/'
        r = requests.get(download_url, allow_redirects=False)
        latest_version = r.headers.get("Location").split("/")[-1][1:]
        download_url += f'subfinder_{latest_version}_linux_amd64.zip'
        filename = 'subfinder.zip'
        if not os.path.exists(os.path.join(current_dir,'resource')):
            os.mkdir(os.path.join(current_dir,'resource'))
        r = requests.get(download_url, proxies={"http": PROXY, "https": PROXY})
        with open(os.path.join(current_dir,'resource',filename),'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(os.path.join(current_dir,'resource',filename), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(current_dir,'resource'))
        os.remove(os.path.join(current_dir,'resource',filename))
        os.system(f"chmod +x {os.path.join(current_dir,'resource','subfinder')}")