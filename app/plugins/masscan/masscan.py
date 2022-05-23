# -*- coding: UTF-8 -*-

import json
import subprocess
import traceback
from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource
import masscan
import netaddr

class MasscanPlugin(BasePlugin):
    stagelist = ['port_detect']
    def port_detect(self, target_list: List[IpInfoModel]) -> List[PortDetectModel]:
        ip_list = []
        for item in target_list:
            ip_list.append(item.ip)
        ip_list = list(set(ip_list))
        ip_list = list(filter(lambda x: x!="", ip_list))
        m = masscan.PortScanner()
        max_items = 150
        splited_iplist = [ip_list[i:i + max_items] for i in range(0, len(ip_list), max_items)] 
        args = self.config.apply_config()
        total_result = {}
        for item in splited_iplist:
            args["hosts"] = ",".join(item).strip(",")
            try:
                result = m.scan(**args)
            except masscan.PortScannerError as e:
                self.save_log(traceback.format_exc(e))
                result = {}
            except masscan.NetworkConnectionError as e:
                self.save_log(e)
                result = {}
            if result == {}:
                continue
            self.save_log(result.get("masscan", {}).get("command_line", ""))
            self.save_log(json.dumps(result.get("scan", {})))
            total_result = {**total_result, **(result.get("scan", {}))}
        return_data = []
        for target in target_list:
            ip = target.ip
            # cidr
            if "/" in ip:
                try:
                    cidr = netaddr.IPNetwork(ip)
                except:
                    cidr = []
                ips = list(cidr)
                for item in ips:
                    ports = total_result.get(str(item), {})
                    ports = list(ports.get("tcp", {}).keys()) + list(ports.get("udp", {}).keys())
                    for port in ports:
                        tmp = PortDetectModel.generate(target, int(port))
                        tmp.ip = str(item)
                        return_data.append(tmp)
            # normal ip
            else:
                ports = total_result.get(str(ip), {})
                ports = list(ports.get("tcp", {}).keys()) + list(ports.get("udp", {}).keys())
                for port in ports:
                    tmp = PortDetectModel.generate(target, int(port))
                    return_data.append(tmp)
        return return_data

    @staticmethod
    def isinstall():
        try:
            p = subprocess.run(["masscan", "--echo"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except:
            return False
        return p.returncode == 0
    @staticmethod
    def install():
        p = subprocess.run(["apt-get", "install", "-y", "--force-yes", "masscan"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        p.check_returncode()
        p = subprocess.run(["apt-get", "install", "-y", "--force-yes", "libpcap-dev"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        p.check_returncode()