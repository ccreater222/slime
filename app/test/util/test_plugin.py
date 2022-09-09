# -*- coding: UTF-8 -*-

from plugins.fscan.config import FscanConfig
from plugins.fscan.fscan import FscanPlugin
from util.plugin import PluginConfig, load_plugins
from util.stage_model import InfoCollectModel
from util.client import db_config
import pytest


def test_load_plugins():
    load_plugins()


def test_plugin_config():
    _ = FscanConfig()

@pytest.mark.skip(reason="waste too much time")
def test_base_plugin():
    plugin = FscanPlugin()
    assert plugin.getmodel('info_collect') == InfoCollectModel
    plugin.dispatch('port_detect', {}, "")


def test_config_load():
    config = PluginConfig()
    config._slime_name = 'test'
    config.a = 'b'
    config.c = 'cccc'
    config.save_to_database('global', 'global')

    config.a = 'c'
    config.b = 'e'
    config.save_to_database('test', 'test')

    config = PluginConfig()
    config.a = '0'
    config.b = '1'
    config.c = '2'
    config.d = '3'
    config._slime_name = 'test'
    config.load_from_database('test', 'test')
    assert config.a == 'c'
    assert config.b == 'e'
    assert config.c == 'cccc'
    assert config.d == '3'
    db_config.delete_many({'plugin': 'test'})
