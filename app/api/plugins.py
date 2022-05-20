# -*- coding: UTF-8 -*-
from util.plugin import PLUGIN_LIST,STAGE_LIST
from util.response import SuccessResponse
from util.util import get_all_keys
def query_plugins():
    result = {
        'stage': {},
        'plugins': {},
        'stagelist': STAGE_LIST
    }
    for stage in STAGE_LIST:
        result['plugins'][stage] = []
        result['stage'][stage] = {'display': stage, 'description': stage}
    for k,v in PLUGIN_LIST.items():
        plugin = {}
        plugin['name'] = k
        plugin['config'] = get_all_keys(v['config']['clazz'])
        for stage in v['plugin'].stagelist:
            result['plugins'][stage].append(plugin)
    return SuccessResponse(result, 0, 0, 0, 0).toDict()
