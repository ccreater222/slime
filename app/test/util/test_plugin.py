from plugins.fscan.config import FscanConfig
from util.plugin import BasePlugin, load_plugins,PLUGIN_LIST
from util.stage_model import InfoCollectModel
def test_load_plugins():
    load_plugins()

def test_plugin_config():
    instance = FscanConfig()
    assert instance.get_all_keys() == ['noping', 'proxy']

def test_base_plugin():
    plugin = BasePlugin()
    assert plugin.getmodel('info_collect') == InfoCollectModel
