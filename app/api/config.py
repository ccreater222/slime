# -*- coding: UTF-8 -*-
from util.plugin import PLUGIN_LIST,STAGE_LIST,PluginConfig
from util.response import SuccessResponse
from flask import request

def query_config():
    form = request.get_json()
    taskid = form.get("taskid", "global")
    result = {
        'global': {},
        'plugins': {}
    }
    for stage in STAGE_LIST:
        result['plugins'][stage] = []
    global_config = PluginConfig()
    global_config.load_from_database('global', taskid)
    result['global'] = global_config.toDict()

    for plugin, info in PLUGIN_LIST.items():
        if plugin == 'skip' :
            continue
        plugin_clazz = info['plugin']
        config_clazz = info['config']['clazz']
        
        stages = getattr(plugin_clazz, 'stagelist', [])
        for stage in stages:
            config = config_clazz()
            config.load_from_database(stage, taskid)
            result['plugins'][stage].append({"name": plugin, "config": config.toDict()})
    resp = SuccessResponse(result, 0, 0, 0, 0)
    return resp.toDict()
    

def save_config():
    form = request.get_json()
    taskid = form.get("taskid", "global")
    config_list = form.get("config", {})
    stage = form.get("type", "global")
    for item in config_list:
        plugin = item['name']
        config = item['config']
        plugin_info = PLUGIN_LIST.get(plugin, None)
        if plugin_info == None:
            continue
        config_instance = plugin_info['config']['clazz']()
        for k, v in config.items():
            setattr(config_instance, k, v)
        config_instance.save_to_database(stage, taskid)
    return SuccessResponse({}, 0, 0, 0, 0).toDict()
