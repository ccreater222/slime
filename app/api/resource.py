from util.plugin import InputFilter
from util.stage_model import BaseModel, FinalStepModel, FingerprintDetectModel, IpInfoModel, ServiceDetectModel, get_all_stage_model_keys
from util.response import SuccessResponse
from util.client import db_resource
from flask import request
import math

from util.util import hex_objid, objid_hex

def query_resource():
    all_keys = ['id', 'name', 'topdomain', 'subdomain', 'iscdn', 'ip', 'port', 'service', 'tag', 'finger', 'updated', 'taskid']
    
    result = {'columns': all_keys, 'columndatas': []}
    form = request.get_json()
    if form.get('columns', []) != []:
        result['columns'] = form.get('columns')
    input_filter = InputFilter(form, BaseModel, '')
    models, total,size,page = input_filter.filter_by_page()
    for model in models:
        data = model.toDict()
        data['id'] = objid_hex(model._id)
        result['columndatas'].append(data)
    resp = SuccessResponse(result, total, size, page, math.ceil(total / size))
    return resp.toDict()


def create_resource():
    form = request.get_json()
    for item in form.get('data', []):
        if item.get('id', None) != None:
            item["_id"] = item["id"]
            del item["id"]
        model = BaseModel(**item)
        model.save()
    resp = SuccessResponse({}, 0, 0, 0, 0)
    return resp.toDict()

def delete_resource():
    form = request.get_json()
    input_filter = InputFilter(form, BaseModel, '')
    models = input_filter._filter_func()
    for i in models:
        print(i)
        db_resource.delete_one({'_id': i.get('_id')})
    resp = SuccessResponse({}, 0, 0, 0, 0)
    return resp.toDict()
    

def update_resource():
    data = request.get_json().get('data', {})
    id = data.get('id', "")
    if id == "":
        raise ValueError("you must choose a item")
    del data['id']
    model = BaseModel(**data)
    model._id = hex_objid(id)
    model.save()

    resp = SuccessResponse({}, 0, 0, 0, 0)
    return resp.toDict()

def analyze_resource():
    form = request.get_json()
    form['columns'] = get_all_stage_model_keys()
    target = form.get("target", "cidr")
    limit = form.get("limit", -1)


    result = []
    analyze = {}
    if target == "cidr" :
        input_filter = InputFilter(form, IpInfoModel, '')
        models = input_filter.filter()
        for model in models:
            model = model.toDict()
            ip = model.get("ip", None)
            if ip == None:
                continue
            # only ipv4 TODO add ipv6
            ip = ip.split(".")
            ip.pop()
            cidr = ".".join(ip) + ".*"
            if analyze.get(cidr, None) == None:
                if limit != -1 and len(analyze.keys()) > limit:
                    continue
                analyze[cidr] = 0
            analyze[cidr] += 1
    
    if target == "tags":
        input_filter = InputFilter(form, BaseModel, '')
        models = input_filter.filter()
        for model in models:
            model = model.toDict()
            tag = model.get("tag", None)
            if tag == None:
                continue
            for t in tag:
                if analyze.get(t, None) == None:
                    if limit != -1 and len(analyze.keys()) > limit:
                        continue
                    analyze[t] = 0
                analyze[t] += 1
        
    if target == "services":
        input_filter = InputFilter(form, ServiceDetectModel, '')
        models = input_filter.filter()
        for model in models:
            model = model.toDict()
            service = model.get("service", None)
            if service == None:
                continue
            if analyze.get(service, None) == None:
                if limit != -1 and len(analyze.keys()) > limit:
                    continue
                analyze[service] = 0
            analyze[service] += 1
    
    if target == "fingerprints":
        input_filter = InputFilter(form, FingerprintDetectModel, '')
        models = input_filter.filter()
        for model in models:
            model = model.toDict()
            fingerprint = model.get("finger", [])
            for fp in fingerprint:
                if analyze.get(fp, None) == None:
                    if limit != -1 and len(analyze.keys()) > limit:
                        continue
                    analyze[fp] = 0
                analyze[fp] += 1



    # format
    for k,v in analyze.items():
        result.append({"name": k, "value": v})
    
    resp = SuccessResponse(result, 0, 0, 0, 0)
    return resp.toDict()

        