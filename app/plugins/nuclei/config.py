# -*- coding: UTF-8 -*-

from util.plugin import PluginConfig

class NucleiConfig(PluginConfig):
    tags = ""
    etags = ""
    rate_limit = "150"
    timeout = "5"
    proxy = ""
    severity = "medium,high,critical"

    def apply_config(self):
        args = []
        if self.tags != "":
            args.append("-tags")
            args.append(self.tags)
        if self.etags != "":
            args.append("-etags")
            args.append(self.etags)
        if self.rate_limit != "":
            args.append("-rate-limit")
            args.append(self.rate_limit)
        if self.timeout != "":
            args.append("-timeout")
            args.append(self.timeout)
        if self.proxy != "":
            if self.proxy.startswith("socks5://"):
                args.append("-proxy-socks-url")
                args.append(self.proxy)
            else:
                args.append("-proxy")
                args.append(self.proxy)
        if self.severity != "":
            args.append("-s") 
            args.append(self.severity)
        return args