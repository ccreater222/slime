from util.plugin import InputFilter
from util.stage_model import BaseModel, FinalStepModel
from util.response import SuccessResponse
from flask import request

from util.util import objid_hex

def query_resource():
    result = {'columes': FinalStepModel.get_need_attr(), 'columedatas': []}
    form = request.form.to_dict()
    if form.get('columes', []) != []:
        result['columes'] = form.get('columes')
    input_filter = InputFilter(form, BaseModel, '')
    models = input_filter.filter()
    for model in models:
        data = model.toDict()
        data['id'] = objid_hex(model._id)
        result['columedatas'].append(data)
    resp = SuccessResponse(result, len(result['columedatas']), len(result['columedatas']), 1, 1)
    return resp.toDict()
