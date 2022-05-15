
from util.plugin import PluginConfig


description = {
    'noping': 'the same as -np options',
    'proxy': 'proxy'
}
class FscanConfig(PluginConfig):
    noping='false'
    _proxy=''
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
        
        return args