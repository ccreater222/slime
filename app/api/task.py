# -*- coding: UTF-8 -*-
import math
from util.plugin import PLUGIN_LIST
from util.task import Task, Taskstatus
from util.response import SuccessResponse
from util.client import db_task
from flask import request
def task_action(action):
    form = request.get_json()
    if action == "create":
        return task_create()
    elif action in ["start", "pause", "restart"]:
        tasks = Task.load_all(form)
        if action == "start":
            new_status = Taskstatus.execute.value
        elif action == "pause":
            new_status = Taskstatus.wait.value
        elif action == "restart":
            new_status = Taskstatus.execute.value
        for task in tasks:
            getattr(task, action)()
        taskids = map(lambda x: x.taskid, tasks)
        db_task.update_many({"taskid": {"$in": list(taskids)}}, {"$set": {"status": new_status}})
        return SuccessResponse({}, 0,0,0,0).toDict()
        
    elif action == "stop":
        tasks = Task.load_all(form)
        taskids = map(lambda x: x.taskid, tasks)
        db_task.delete_many({"taskid": {"$in": list(taskids)}})
        return SuccessResponse({}, 0,0,0,0).toDict()

def task_query():
    form = request.get_json()
    # filter
    result = {'taskcolumn': ["taskid","stageinfo","status","log","created"], 'tasklist': []}
    total, tasks = Task.load_by_page(form)
    
    for task in tasks:
        task_dict = task.toDict()
        configs = {}
        for stage in task_dict.get('stageinfo', {}).keys():
            configs[stage] = []
            for plugin in task_dict['stageinfo'][stage]:
                cls = PLUGIN_LIST[plugin]['config']['clazz']
                instance = cls()
                instance.load_from_database(stage, task_dict.get('taskid'))
                configs[stage].append({'name': plugin, 'config': instance.toDict()})
        task_dict['stageinfo'] = configs
        result["tasklist"].append(task_dict)
    
    return SuccessResponse(result, total, form.get("size", 20), form.get("page", 1), math.ceil(total / form.get("size", 20))).toDict()

def task_create():
    resp = SuccessResponse([], 0, 0 , 0, 0)
    form = request.get_json()
    configs = form.get("stageinfo", None)
    del form["stageinfo"]

    task = Task.load_from_request(configs, form)
    task.save()
    return resp.toDict()
