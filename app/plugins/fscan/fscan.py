import json
import shutil
import re
import subprocess
import os
import platform

from util.plugin import BasePlugin
from typing import List
from util.stage_model import BaseModel, FingerprintDetectModel, IpInfoModel, PocScanModel, PortDetectModel, ServiceDetectModel, FinalStepModel
import requests
from util.logging import getlogger

logger = getlogger(__name__)
class FscanPlugin(BasePlugin):
    stagelist = ['port_detect','poc_scan','final_step']
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
    
    def poc_scan(self, target_list: List[FingerprintDetectModel]) -> List[PocScanModel]:
        port_model = []
        temp_dir = os.path.join(os.path.dirname(__file__),'resource','tmp',self.taskid)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        ipfile = 'ip.txt'
        portfile = 'port.txt'
        outputfile = 'output.txt'
        iplist = []
        portlist = []
        for target in target_list:
            iplist.append(target.ip)
            portlist.append(str(target.port))
        with open(os.path.join(temp_dir,ipfile),'w') as f:
            f.write('\n'.join(iplist))
        with open(os.path.join(temp_dir,portfile), 'w') as f:
            f.write('\n'.join(portlist))
        if platform.system() == 'Windows':
            filename = 'fscan.exe'
        else:
            filename = 'fscan'
        args = [os.path.join(os.path.dirname(__file__),'resource',filename)]
        args.append('-hf')
        args.append(os.path.join(temp_dir,ipfile))
        args.append('-portf')
        args.append(os.path.join(temp_dir, ipfile))
        args.append('-o')
        args.append(os.path.join(temp_dir,outputfile))
        args = args + self.config.apply_config()
        logger.debug(f"fscan command line: {' '.join(args)}")
        process = subprocess.run(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = process.stdout.decode('utf-8')
        error = process.stderr.decode('utf-8')
        try:
            with open(os.path.join(temp_dir,outputfile),'r',encoding='utf-8') as f:
                result = f.read()
            self.save_log(output)
            self.save_log(error)
            parsed = self.parse(result)
            logger.debug(f"get result: {json.dumps(parsed)}")
            for ip in parsed['ports'].keys():
                for port in parsed['ports'][ip]:
                    for target in target_list:
                        if target.ip == ip:
                            vul = parsed['vul'].get(f'{ip}:{port}')
                            if vul == None:
                                continue
                            record = PocScanModel.generate(target, vul['title'], vul['vultype'], 'fscan', vul['title'], '', '')
                            if parsed['info'].get(f'{ip}:{port}'):
                                info = parsed['info'].get(f'{ip}:{port}')
                                record = ServiceDetectModel.generate(record, "web", info)
                            
                            port_model.append(record)
                            break
        except FileNotFoundError as e:
            pass
        shutil.rmtree(temp_dir)
        return port_model

        

    def final_step(self, target_list: List[PocScanModel]) -> List[FinalStepModel]:
        return self.poc_scan(target_list)
    def port_detect(self, target_list: List[IpInfoModel]) -> List[PortDetectModel]:
        port_model = []
        temp_dir = os.path.join(os.path.dirname(__file__),'resource','tmp',self.taskid)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        ipfile = 'ip.txt'
        outputfile = 'output.txt'
        iplist = []
        for target in target_list:
            iplist.append(target.ip)
        logger.debug(f"following ip is target: {', '.join(iplist)}")
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
        args.append('-nopoc')
        args = args + self.config.apply_config()
        logger.debug(f"fscan command line: {' '.join(args)}")
        process = subprocess.run(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = process.stdout.decode('utf-8')
        error = process.stderr.decode('utf-8')
        try:
            with open(os.path.join(temp_dir,outputfile),'r',encoding='utf-8') as f:
                result = f.read()
            self.save_log(output)
            self.save_log(error)
            parsed = self.parse(result)
            logger.debug(f"get result: {json.dumps(parsed)}")
            for ip in parsed['ports'].keys():
                for port in parsed['ports'][ip]:
                    for target in target_list:
                        if target.ip == ip:
                            record = PortDetectModel.generate(target, int(port))
                            if parsed['info'].get(f'{ip}:{port}'):
                                info = parsed['info'].get(f'{ip}:{port}')
                                record = ServiceDetectModel.generate(record, "web", info)
                            
                            port_model.append(record)
                            break
        except FileNotFoundError as e:
            pass
        shutil.rmtree(temp_dir)
        return port_model
    @staticmethod
    def parse(result):
        ip_ports = re.findall(r'^(\d+\.\d+\.\d+\.\d+):(\d+) open',result,flags=re.MULTILINE)
        parsed = {
            'ports': {},
            'info': {},
            'vuls': {}
        }
        for i in ip_ports:
            if parsed['ports'].get(i[0]) == None:
                parsed['ports'][i[0]] = []
            parsed['ports'][i[0]].append(i[1])
        
        infolist = re.findall(r'\[\*\] WebTitle:(https?://([^ :]*)(:\d+)?)\s+code:(\d+)\s+len:(\d+)\s+title:(.*)', result)
        for info in infolist:
            url, ip, port, status_code, content_length, title = info
            if port == '':
                if url.startswith('https://'):
                    port = '443'
                else:
                    port = '80'
            port = port.replace(':', '')
            parsed['info'][f"{ip}:{port}"] = {
                'url': url,
                'status_code': status_code,
                'content_length': content_length,
                'title': title
            }
        vullist = re.findall(r'\[\+\] ((([^:]*):(.*(:\d+)?))\s+([^ ]*)\s+([^\[ ]*))',result, re.MULTILINE)
        for vul in vullist:
            title, url, service, ipport, port, vultype, detail = vul
            if port == '':
                if service == 'https':
                    port = '443'
                else:
                    port = '80'
                ipport = f'{ipport}:{port}'
            parsed['vuls'][ipport] = {
                'url': url,
                'service': service,
                'vultype': vultype,
                'detail': detail,
                'title': title
            }


        return parsed