# -*- coding: UTF-8 -*-
from flask import request
from util.plugin import InputFilter
from util.stage_model import BaseModel, ServiceDetectModel
from util.util import objid_hex
import math
from util.response import SuccessResponse

def query_service():
    all_keys = ["name","topdomain","subdomain","iscdn","ip","port","service","info"]
    
    result = {'columns': all_keys, 'columndatas': []}
    form = request.get_json()
    form['columns'] = []
    input_filter = InputFilter(form, ServiceDetectModel, '')
    models, total,size,page = input_filter.filter_by_page()
    for model in models:
        data = model.toDict()
        data['id'] = objid_hex(model._id)
        result['columndatas'].append(data)
    resp = SuccessResponse(result, total, size, page, math.ceil(total / size))
    return resp.toDict()
