import shutil
import re
import subprocess
import os
import platform
from util.plugin import BasePlugin
from typing import List
from util.stage_model import FingerprintDetectModel, IpInfoModel, PocScanModel, PortDetectModel
import requests

class FscanPlugin(BasePlugin):
    stagelist = ['port_detect','service_detect','poc_scan','final_step']
    @staticmethod
    def isinstall():
        current_dir = os.path.dirname(__file__)
        if platform.system() == 'Windows':
            return os.path.exists(os.path.join(current_dir,'resource','fscan.exe'))
        else:
            return os.path.exists(os.path.join(current_dir,'resource','fscan'))

    @staticmethod
    def install():
        current_dir = os.path.dirname(__file__)
        download_url = 'https://github.com/shadow1ng/fscan/releases/latest/download/'
        filename = ''
        if platform.system() == 'Windows':
            download_url += 'fscan64.exe'
            filename = 'fscan.exe'
        else:
            download_url += 'fscan_amd64'
            filename = 'fscan'
        if not os.path.exists(os.path.join(current_dir,'resource')):
            os.mkdir(os.path.join(current_dir,'resource'))
        r = requests.get(download_url)
        with open(os.path.join(current_dir,'resource',filename),'wb') as f:
            f.write(r.content)
    def port_detect(self, target_list: List[IpInfoModel]) -> List[PortDetectModel]:
        port_model = []
        temp_dir = os.path.join(os.path.dirname(__file__),'resource','tmp',self.task_id)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        ipfile = 'ip.txt'
        outputfile = 'output.txt'
        iplist = []
        for target in target_list:
            iplist.append(target.ip)
        with open(os.path.join(temp_dir,ipfile),'w') as f:
            f.write('\n'.join(iplist))
        if platform.system() == 'Windows':
            filename = 'fscan.exe'
        else:
            filename = 'fscan'
        args = [os.path.join(os.path.dirname(__file__),'resource',filename)]
        args.append('-hf')
        args.append(os.path.join(temp_dir,ipfile))
        args.append('-o')
        args.append(os.path.join(temp_dir,outputfile))
        args.append('-nobr')
        process = subprocess.run(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = process.stdout.decode('utf-8')
        try:
            with open(os.path.join(temp_dir,outputfile),'r',encoding='utf-8') as f:
                result = f.read()
            parsed = self.parse(result)
            for ip in parsed['ports'].keys():
                for port in parsed['ports'][ip]:
                    for target in target_list:
                        if target.ip == ip:
                            port_model.append(PortDetectModel.generate(target, int(port)))
                            break
        except FileNotFoundError:
            pass
        
        shutil.rmtree(temp_dir)
        return port_model
    @staticmethod
    def parse(result):
        ip_ports = re.findall(r'^(\d+\.\d+\.\d+\.\d+):(\d+) open',result,flags=re.MULTILINE)
        parsed = {
            'ports': {}
        }
        for i in ip_ports:
            if parsed['ports'].get(i[0]) == None:
                parsed['ports'][i[0]] = []
            parsed['ports'][i[0]].append(i[1])
        return parsed