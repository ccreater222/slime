from plugins.fscan.config import FscanConfig
from plugins.fscan.fscan import FscanPlugin
from util.plugin import BasePlugin, load_plugins,PLUGIN_LIST
from util.stage_model import InfoCollectModel
import pytest

def test_load_plugins():
    load_plugins()

def test_plugin_config():
    instance = FscanConfig()
    assert instance.get_all_keys() == ['noping', 'proxy']

#@pytest.mark.skip(reason="waste too much time")
def test_base_plugin():
    plugin = FscanPlugin()
    assert plugin.getmodel('info_collect') == InfoCollectModel
    plugin.dispatch('port_detect',{},"asdasdasdas")
