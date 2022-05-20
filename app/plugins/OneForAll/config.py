# -*- coding: UTF-8 -*-

import os
from util.plugin import PluginConfig
from util.util import get_all_keys

class OneForAllPlugin(PluginConfig):
    # API setting
    censys_api_id = ""
    censys_api_secret = ''
    binaryedge_api = ''
    chinaz_api = ''
    bing_api_id = ''
    bing_api_key = ''
    securitytrails_api = ''
    fofa_api_email = ''  # fofa用户邮箱
    fofa_api_key = ''  # fofa用户key
    google_api_id = ''  # Google API自定义搜索引擎id
    google_api_key = ''  # Google API自定义搜索key
    riskiq_api_username = ''
    riskiq_api_key = ''
    shodan_api_key = ''
    threatbook_api_key = ''
    virustotal_api_key = ''
    zoomeye_api_usermail = ''
    zoomeye_api_password = ''
    spyse_api_token = ''
    circl_api_username = ''
    circl_api_password = ''
    dnsdb_api_key = ''
    ipv4info_api_key = ''
    passivedns_api_addr = ''
    passivedns_api_token = ''
    github_api_user = ''
    github_api_token = ''
    cloudflare_api_token = ''

    proxy = ""

    alive = "False"
    port = "small"
    brute = "True"
    dns = "True"
    req = "True"
    takeover = "False"
    def apply_config(self) -> list:
        # apply api config
        basedir = os.path.dirname(__file__)
        with open(os.path.join(basedir, "template", "api.txt"), "r") as f:
            api_conf = f.read()
        all_keys = get_all_keys(self)
        all_keys = filter(lambda x: "api" in x, all_keys)
        for key in all_keys:
            api_conf = api_conf.replace("{"+key+"}", getattr(self, key, ""))
        with open(os.path.join(basedir, "resource", "config", "api.py"), "w") as f:
            f.write(api_conf)
        
        with open(os.path.join(basedir, "template", "setting.txt"), "r") as f:
            setting_data = f.read()
        
        setting_data = setting_data.replace("{proxy}", getattr(self, "proxy", ""))
        with open(os.path.join(basedir, "resource", "config", "setting.py"), "w") as f:
            f.write(setting_data)
        
        args = []
        # apply cmd config
        bool_map = {
            "false": "False",
            "true": "True"
        }
        if self.alive.lower() in ["true", "false"]:
            args = args + ["--alive", bool_map[self.alive.lower()]]
        if self.port.lower() in ["true", "false"]:
            args = args + ["--port", bool_map[self.port.lower()]]
        if self.brute.lower() in ["true", "false"]:
            args = args + ["--brute", bool_map[self.brute.lower()]]
        if self.dns.lower() in ["true", "false"]:
            args = args + ["--dns", bool_map[self.dns.lower()]]
        if self.req.lower() in ["true", "false"]:
            args = args + ["--req", bool_map[self.req.lower()]]
        if self.takeover.lower() in ["true", "false"]:
            args = args + ["--takeover", bool_map[self.takeover.lower()]]
        
        return args

