from util.plugin import InputFilter
from util.stage_model import BaseModel, FinalStepModel, get_all_stage_model_keys
from util.response import SuccessResponse
from util.client import db_resource
from flask import request
import math

from util.util import hex_objid, objid_hex

def query_resource():
    result = {'columns': get_all_stage_model_keys(), 'columndatas': []}
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
