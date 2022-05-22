from util.plugin import PLUGIN_LIST
from plugins.nuclei.nuclei import NucleiPlugin
def test_parse():
    instance = NucleiPlugin()
    instance.taskid = ""
    assert type(instance.parse()) == list    
