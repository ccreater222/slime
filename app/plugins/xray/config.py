# -*- coding: UTF-8 -*-

import os
from util.plugin import PluginConfig
from util.util import get_all_keys

class XrayConfig(PluginConfig):
    proxy = ""
    timeout = ""
    reverse_server_url = ""
    reverse_server_token = ""
    plugins = ""
    poc = ""

    thread = "30"
    def apply_config(self):
        basedir = os.path.dirname(__file__)
        with open(os.path.join(basedir, "template", "config.yaml"), "r") as f:
            data = f.read()
        keys = get_all_keys(self)
        for key in keys:
            data = data.replace("{"+key.upper()+"}", getattr(self, key))
        if self.reverse_server_token != "" and self.reverse_server_url != "":
            data = data.replace("{REVERSE_ENABLE}", "true")
        else:
            data = data.replace("{REVERSE_ENABLE}", "false")
        
        with open(os.path.join(basedir, "resource", "config.yaml"), "w") as f:
            f.write(data)
        args = []
        if self.poc != "":
            args.append("--poc")
            args.append(self.poc)
        if self.plugins != "":
            args.append("--plugins")
            args.append(self.plugins)
        return args