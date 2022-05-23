# -*- coding: UTF-8 -*-

import traceback
from typing import List
from util.plugin import BasePlugin
from util.stage_model import *
from util.client import db_resource
import subprocess
import nmap
import netaddr
from util.logging import getlogger
import json

logger = getlogger(__name__)
class NmapPlugin(BasePlugin):
    stagelist = ['port_detect','service_detect', 'poc_scan']

    def port_detect(self, target_list: List[IpInfoModel]) -> List[PortDetectModel]:
        ip_list = []
        for item in target_list:
            ip_list.append(item.ip)
        ip_list = list(set(ip_list))
        m = nmap.PortScanner()
        max_items = 150
        splited_iplist = [ip_list[i:i + max_items] for i in range(0, len(ip_list), max_items)] 
        args = self.config.apply_config()
        total_result = {}
        for item in splited_iplist:
            args["hosts"] = ",".join(item)
            try:
                result = m.scan(**args)
            except nmap.PortScannerError as e:
                self.save_log(traceback.format_exc(e))
                result = {}
            except nmap.NetworkConnectionError as e:
                self.save_log(e)
                result = {}
            if result == {}:
                continue
            self.save_log(result.get("nmap", {}).get("command_line", ""))
            self.save_log(json.dumps(result.get("scan", {})))
            total_result = {**total_result, **(result.get("scan", {}))}
        result = []
        for target in target_list:
            if "/" in target.ip:
                try:
                    cidr = netaddr.IPNetwork(target.ip)
                except:
                    cidr = []
                ips = list(cidr)
                for item in ips:
                    ipinfo = total_result.get(str(item), {})
                    ports = list(ipinfo.get("tcp", {}).keys()) + list(ipinfo.get("udp", {}).keys()) + list(ipinfo.get("sctp", {}).keys())
                    for port in ports:
                        tmp = PortDetectModel.generate(target, int(port))
                        tmp.ip = str(item)
                        result.append(tmp)
            else:
                ipinfo = total_result.get(target.ip, {})
                ports = list(ipinfo.get("tcp", {}).keys()) + list(ipinfo.get("udp", {}).keys()) + list(ipinfo.get("sctp", {}).keys())
                for port in ports:
                    tmp = PortDetectModel.generate(target, int(port))
                    result.append(tmp)
        return result
    def service_detect(self, target_list: List[PortDetectModel]) -> List[ServiceDetectModel]:
        self.config.host_discover_method = "-Pn"
        self.config.scan_method = "-sS"
        ip_list = []
        port_list = []
        for item in target_list:
            ip_list.append(item.ip)
            port_list.append(str(item.port))
        ip_list = list(set(ip_list))
        port_list = list(set(port_list))
        port_list = list(filter(lambda x: x!="", port_list))
        self.config.ports = ",".join(port_list)
        m = nmap.PortScanner()
        logger.debug(ip_list)
        logger.debug(port_list)
        max_items = 150
        splited_iplist = [ip_list[i:i + max_items] for i in range(0, len(ip_list), max_items)] 
        args = self.config.apply_config()
        args["arguments"] += " -sV"
        total_result = {}
        for item in splited_iplist:
            args["hosts"] = " ".join(item)
            try:
                logger.debug(args)
                result = m.scan(**args)
            except nmap.PortScannerError as e:
                self.save_log(traceback.format_exc(e))
                result = {}
            if result == {}:
                continue
            self.save_log(result.get("nmap", {}).get("command_line", ""))
            self.save_log(json.dumps(result.get("scan", {})))
            total_result = {**total_result, **(result.get("scan", {}))}
        result = []
        for target in target_list:
            ipinfo = total_result.get(target.ip, {})
            portinfo = { 
                **(ipinfo.get("udp", {}).get(target.port, {})),
                **(ipinfo.get("sctp", {}).get(target.port, {})),
                **(ipinfo.get("tcp", {}).get(target.port, {})),
                **(ipinfo.get("udp", {}).get(str(target.port), {})),
                **(ipinfo.get("sctp", {}).get(str(target.port), {})),
                **(ipinfo.get("tcp", {}).get(str(target.port), {}))
            }
            if portinfo == {}:
                continue
            service = portinfo.get("name", "")
            if service == "":
                continue
            tmp = ServiceDetectModel.generate(target, service, portinfo)
            result.append(tmp)

        return result

    def poc_scan(self, target_list: List[ServiceDetectModel]) -> List[PocScanModel]:
        return []

    @staticmethod
    def isinstall():
        try:
            p = subprocess.run(["nmap", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            return False
        return p.returncode == 0
    @staticmethod
    def install():
        p = subprocess.run(["apt-get", "install", "-y", "--force-yes", "nmap"])
        p.check_returncode()