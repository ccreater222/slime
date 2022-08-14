from util.stage_model import TopdomainCollectModel
from plugins.subfinder.config import SubfinderConfig
from util.plugin import PLUGIN_LIST
from plugins.subfinder.subfinder import SubfinderPlugin
from plugins.subfinder.util import parse_result_file
import os
def test_subfinder_install():
    instance = SubfinderPlugin()
    current_dir = os.path.dirname(__file__)
    os.remove(os.path.join(current_dir, "..", "..", "..", "plugins", "subfinder", "resource", "subfinder"))
    assert instance.isinstall() == False
    instance.install()
    assert instance.isinstall() == True

def test_subfinder_parser():
    current_dir = os.path.dirname(__file__)
    result = parse_result_file(os.path.join(current_dir, "data.json"))
    assert result != []
    assert len(result[0])  == 2
    assert result[0][0] == "site.ccreater.top"

def test_subfinder():
    instance = SubfinderPlugin()
    instance.config = SubfinderConfig()
    instance.taskid = ""
    instance.stage = "subdomain_collect"
    model = TopdomainCollectModel("ccreater.top")
    assert len(instance.subdomain_collect([model])) > 0