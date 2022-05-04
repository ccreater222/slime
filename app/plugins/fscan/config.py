
from util.plugin import PluginConfig


description = {
    'noping': 'the same as -np options',
    'proxy': 'proxy'
}
class FscanConfig(PluginConfig):
    noping=False
    _proxy=''
    @property
    def proxy(self):
        if self._proxy == '':
            return "global proxy setting"
        return self._proxy
    @proxy.setter
    def proxy(self,_proxy):
        self._proxy = _proxy