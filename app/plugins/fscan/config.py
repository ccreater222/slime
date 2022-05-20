# -*- coding: UTF-8 -*-

from util.plugin import PluginConfig


description = {
    'noping': 'the same as -np options',
    'proxy': 'proxy'
}
class FscanConfig(PluginConfig):
    noping='false'
    _proxy=''
    bruteforcerate='1'
    method='all'
    nopoc=''
    port=''
    thread='600'
    @property
    def proxy(self):
        if self._proxy == '':
            return ""
        return self._proxy
    @proxy.setter
    def proxy(self,_proxy):
        self._proxy = _proxy
    
    def apply_config(self):
        args = []
        if self.noping.lower() == 'true':
            args.append('-np')
        
        if self.bruteforcerate.strip() != '':
            args = args + ['-br', self.bruteforcerate]
        
        if self.proxy != '':
            args += ['-proxy', self.proxy]

        args += ['-m', self.method]
        if self.nopoc.lower() == 'true':
            args.append("nopoc")

        if self.port != '':
            args += ['-p', self.port]
        
        args += ['-t' ,self.thread]
        return args