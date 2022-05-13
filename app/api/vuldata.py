import math
from util.vuldata import VulData
from util.response import SuccessResponse
from flask import request
import re
def vuldata_query():
    form = request.get_json()
    total, data = VulData.load_from_database(form)
    result = []
    for item in data:
        result.append(item.toDict())
    resp = SuccessResponse(result, total, form.get("size", 20) , form.get("page", 1), math.ceil(total / form.get("size", 20)))
    return resp.toDict()