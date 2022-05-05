from inspect import getmembers,ismethod,isfunction
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
    
