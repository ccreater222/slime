from util.response import SuccessResponse
from util.client import db_task
import uuid
def task_query():
    resp = SuccessResponse([], 0, 0 , 0, 0)
    
    return resp.toDict()

def task_create():
    resp = SuccessResponse([], 0, 0 , 0, 0)
    return resp.toDict()
