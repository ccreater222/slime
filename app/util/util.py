from inspect import getmembers,ismethod,isfunction
def get_all_keys(cls):
    all_keys = []
    for name,_ in getmembers(cls,lambda x: not ismethod(x) and not isfunction(x)):
        if name.startswith('_'):
            continue
        all_keys.append(name)
    return all_keys