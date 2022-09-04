# -*- coding: UTF-8 -*-

import json
import shutil
from typing import List
from config.plugin import PYTHON_PACKAGE_INDEX
from util.plugin import BasePlugin
from util.stage_model import *
from util.install import *
import os
from util.logging import getlogger

logger =  getlogger()

class OneForAllPlugin(BasePlugin):
    stagelist = ['subdomain_collect']
    def subdomain_collect(self, target_list: List[TopdomainCollectModel]) -> List[SubdomainCollectModel]:
        options = self.config.apply_config()
        basedir = os.path.join(os.path.dirname(__file__), "resource")
        tmpdir = os.path.join(basedir, "tmp", self.celery_task_id)
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
        args = ["./venv/bin/python", "oneforall.py", "--fmt", "json", "--path", result_path, "--targets", target_domain_file]
        args += options
        args.append("run")
        process = subprocess.run(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, cwd = basedir)
        output = process.stdout.decode('utf-8')
        self.save_log(' '.join(args))
        self.save_log(output)

        result = []
        try:
            with open(result_path, "r") as f:
                result = json.loads(f.read())
        except FileNotFoundError:
            logger.debug("no oneforall result file")
        return_data = []
        for item in result:
            for i in target_list:
                subdomain = item.get("subdomain", "")
                if i.topdomain not in subdomain:
                    continue
                tmp = SubdomainCollectModel.generate(i, subdomain)
                return_data.append(tmp)
                logger.debug(f"[+] found subdomain: {subdomain}")
                ips = item["ip"].split(',')
                for ip in ips:
                    tmp = IpInfoModel.generate(tmp, item["cdn"] == 1, ip)
                    return_data.append(tmp)
        
        #shutil.rmtree(tmpdir)
        return return_data


    @staticmethod
    def isinstall():
        basedir = os.path.join(os.path.dirname(__file__), "resource")
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        install_python3()
        try:
            p = subprocess.run(["./venv/bin/python", "oneforall.py", "-h"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, cwd=basedir)
        except :
            return False
        return p.returncode == 0

    @staticmethod
    def install():
        basedir = os.path.join(os.path.dirname(__file__), "resource")
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        
        install_python3()
        gitclone("https://github.com/shmilylty/OneForAll.git", basedir, ["--depth", "1"])
        p = subprocess.run([PYTHON3, "-m", "venv", "venv"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, cwd=basedir)
        p.check_returncode()
        cmd = ["./venv/bin/pip", "install", "-r", "./requirements.txt"]
        if PYTHON_PACKAGE_INDEX != "":
            cmd += ["-i", PYTHON_PACKAGE_INDEX]
        p = subprocess.run(cmd, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL, cwd=basedir)
        p.check_returncode()

        