from celery.result import AsyncResult
from util.client import celery_app
from util.plugin import PLUGIN_LIST
from util.client import db_taskstruct, db_task

# taskstruct

# {"tasks": [], "stage": "", "plugin": ""}

@celery_app.task
def workflow(taskid: str,stageinfo: dict, filter: dict) -> AsyncResult:

    # update status
    db_task.update_one({"taskid": taskid}, {"$set": {"status": "execute"}})

    # execute
    for stagename, plugin_list in stageinfo.items():
        db_taskstruct.update_one({"taskid": taskid}, {"$set": {"stage": stagename}})
        for plugin in plugin_list:
            db_taskstruct.update_one({"taskid": taskid}, {"$set": {"plugin": plugin}})
            PLUGIN_LIST[plugin]['plugin'].dispatch(stagename, filter, taskid)

    # remove task list
    db_taskstruct.delete_one({"taskid": taskid})
    db_task.update_one({"taskid": taskid}, {"$set": {"status": "success"}})




