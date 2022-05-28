# -*- coding: UTF-8 -*-

import json
import shutil
import subprocess
from typing import List

import yaml
from util.plugin import BasePlugin
from util.stage_model import *
import os
import zipfile
from config.plugin import PROXY

class XrayPlugin(BasePlugin):
    stagelist = ['poc_scan','final_step']
    def poc_scan(self, target_list: List[ServiceDetectModel]) -> List[PocScanModel]:
        basedir = os.path.join(os.path.dirname(__file__), "resource")
        tmpdir = os.path.join(os.path.dirname(__file__), "resource", "tmp", self.taskid)
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        url_list = []
        for item in target_list:
            url_list.append(f"{item.ip}:{item.port}")
        with open(os.path.join(tmpdir, "url.txt"), "w") as f:
            f.write("\n".join(url_list))
        
        self.config.plugins = "phantasm"
        args = self.config.apply_config()
        args = ["./xray", "webscan", "--uf", os.path.join(tmpdir, "url.txt"), "--json-output", os.path.join(tmpdir, "result.json")] + args
        self.save_log(" ".join(args))
        p = subprocess.run(args, cwd=basedir, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        output = p.stdout.decode("utf-8")
        self.save_log(output)
        try:
            with open(os.path.join(tmpdir, "result.json"), "r") as f:
                data = f.read()
        except Exception:
            shutil.rmtree(tmpdir)
            return
        data = json.loads(data)
        result = []
        for item in data:
            for target in target_list:
                if f"{target.ip}:{target.port}" in item.get("target", {}).get("url", ""):
                    detail = item.get("detail", {})
                    title = item.get("plugin", "")
                    req, resp = detail.get("snapshot", [["", ""]])[0]
                    tmp = PocScanModel.generate(target, title, title, "xray", yaml.dump(detail), req, resp)
                    result.append(tmp)
        shutil.rmtree(tmpdir)
        return result
    def final_step(self, target_list: List[BaseModel]) -> List[FinalStepModel]:
        basedir = os.path.join(os.path.dirname(__file__), "resource")
        tmpdir = os.path.join(os.path.dirname(__file__), "resource", "tmp", self.taskid)
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        url_list = []
        for item in target_list:
            if getattr(item, "ip", "") == "" or getattr(item, "port", "") == "":
                continue
            url_list.append(f"{item.ip}:{item.port}")
        with open(os.path.join(tmpdir, "url.txt"), "w") as f:
            f.write("\n".join(url_list))
        
        args = self.config.apply_config()
        args = ["./xray", "webscan", "--uf", os.path.join(tmpdir, "url.txt"), "--json-output", os.path.join(tmpdir, "result.json")] + args
        self.save_log(" ".join(args))
        p = subprocess.run(args, cwd=basedir, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        output = p.stdout.decode("utf-8")
        self.save_log(output)
        try:
            with open(os.path.join(tmpdir, "result.json"), "r") as f:
                data = f.read()
        except Exception:
            shutil.rmtree(tmpdir)
            return
        data = json.loads(data)
        result = []
        for item in data:
            for target in target_list:
                if getattr(target, "ip", "") == "" or getattr(target, "port", "") == "":
                    continue
                if f"{target.ip}:{target.port}" in item.get("target", {}).get("url", ""):
                    detail = item.get("detail", {})
                    title = item.get("plugin", "")
                    req, resp = detail.get("snapshot", [["", ""]])[0]
                    tmp = PocScanModel.generate(target, title, title, "xray", yaml.dump(detail), req, resp)
                    result.append(tmp)
        shutil.rmtree(tmpdir)
        return result

    @staticmethod
    def isinstall():
        current_dir = os.path.dirname(__file__)
        return os.path.exists(os.path.join(current_dir,'resource','xray'))
    @staticmethod
    def install():
        current_dir = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(current_dir, "resource")):
            os.mkdir(os.path.join(current_dir, "resource"))
        download_url = 'https://github.com/chaitin/xray/releases/latest/download/'
        download_url += f'xray_linux_amd64.zip'
        filename = 'xray.zip'
        if not os.path.exists(os.path.join(current_dir,'resource')):
            os.mkdir(os.path.join(current_dir,'resource'))
        r = requests.get(download_url, proxies={"http": PROXY, "https": PROXY})
        with open(os.path.join(current_dir,'resource',filename),'wb') as f:
            f.write(r.content)

        with zipfile.ZipFile(os.path.join(current_dir,'resource',filename), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(current_dir,'resource'))
        os.remove(os.path.join(current_dir,'resource',filename))
        os.rename(os.path.join(current_dir,'resource',"xray_linux_amd64"), os.path.join(current_dir,'resource',"xray"))
        os.system(f"chmod +x {os.path.join(current_dir,'resource')}/xray")