# -*- coding: UTF-8 -*-
from util.client import *
from datetime import datetime,timedelta

from util.response import SuccessResponse

def countdata(client):
    result = [client.count_documents({}), []]
    now = datetime.now()
    yestoday = now - timedelta(days=1)
    for i in range(7):
        num = client.count_documents({'created': {'$gte': yestoday, '$lt': now}})
        result[1].insert(0, num)
        now = yestoday
        yestoday = now - timedelta(days=1)
    return result

def dashboard():
    result = {
        'countdata': {},
        'comparedata': {}
    }
    # resource
    tmp = countdata(db_resource)
    result['countdata']['resource'] = tmp[0]
    result['comparedata']['resource'] = tmp[1]

    # vul
    tmp = countdata(db_vuldata)
    result['countdata']['vul'] = tmp[0]
    result['comparedata']['vul'] = tmp[1]

    # task
    tmp = countdata(db_task)
    result['countdata']['task'] = tmp[0]
    result['comparedata']['task'] = tmp[1]

    # service
    result['countdata']['service'] = db_resource.count_documents({'service': {'$exists': True}})

    resp = SuccessResponse(result, 1, 1, 1, 1)
    return resp.toDict()

    
    




    