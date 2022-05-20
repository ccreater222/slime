# -*- coding: UTF-8 -*-
from inspect import getmembers,ismethod,isfunction

from bson import ObjectId
def get_all_keys(cls):
    all_keys = []
    for name,_ in getmembers(cls,lambda x: not ismethod(x) and not isfunction(x)):
        if name.startswith('_'):
            continue
        all_keys.append(name)
    return all_keys

def dotset(v: dict):
    dot_array = []
    keys = v.keys()
    result = map(lambda k: [k, dotset(v[k])] if type(v[k]) == dict else [k, None] ,keys)
    for i in result:
        key, val = i
        if val == None:
            dot_array.append([key,v[key]])
        else:
            for ii in val:
                dot_array.append([key+'.'+ii[0], ii[1]])
    return dot_array
    
def objid_hex(objid: ObjectId):
    return objid.binary.hex()

def hex_objid(s: str):
    return ObjectId(s)
