# -*- coding: UTF-8 -*-
from util.response import SuccessResponse
from flask import request
def action_schedule(action):
    form = request.get_json()
    if action == "create":
        return create_schedule()
    elif action in ["pause", "start", "execute"]:

        if action == "start":
            pass
        elif action == "pause":
            pass
        elif action == "restart":
            pass
        return SuccessResponse({}, 0,0,0,0).toDict()
        
    elif action == "delete":
        return SuccessResponse({}, 0,0,0,0).toDict()

def query_schedule():
    form = request.get_json()
    # filter
    return SuccessResponse([], 0, 0, 0, 0).toDict()

def create_schedule():
    resp = SuccessResponse([], 0, 0 , 0, 0)
    return resp.toDict()
