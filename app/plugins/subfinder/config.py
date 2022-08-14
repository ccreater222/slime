# -*- coding: UTF-8 -*-

from typing import List
from util.plugin import PluginConfig
from util.util import get_all_keys

class SubfinderConfig(PluginConfig):
    recursive = "False"
    exclude_sources = ""
    sources = ""
    rate_limit = "0"
    all = ""
    proxy = ""
    resolvers = ""
    api_bufferover = ""
    api_binaryedge = ""
    api_c99 = ""
    api_censys = ""
    api_certspotter = ""
    api_chaos = ""
    api_chinaz = ""
    api_dnsdb = ""
    api_fofa = ""
    api_fullhunt = ""
    api_github = ""
    api_intelx = ""
    api_passivetotal = ""
    api_robtex = ""
    api_securitytrails = ""
    api_shodan = ""
    api_threatbook = ""
    api_urlscan = ""
    api_virustotal = ""
    api_whoisxmlapi = ""
    api_zoomeye = ""
    api_zoomeyeapi = ""
    def apply_config(self) -> List:
        all_keys = get_all_keys(self)
        all_keys = filter(lambda x: "api_" in x, all_keys)
        api_config = {}
        for key in all_keys:
            api_config[key.replace("api_", "")] = getattr(self, key, "")
            
        return []