import traceback
from celery.result import AsyncResult
from util.client import celery_app
from util.plugin import PLUGIN_LIST
from util.client import db_taskstruct, db_task
import util.logging as logging
import time


logger = logging.getlogger()



# taskstruct

# {"tasks": [], "stage": "", "plugin": ""}

@celery_app.task
def workflow(taskid: str,stageinfo: dict, filter: dict) -> AsyncResult:
    logger.debug(f"run task[{taskid}]")
    start_time = time.time()
    # update status
    db_task.update_one({"taskid": taskid}, {"$set": {"status": "execute"}})

    # execute
    for stagename, plugin_list in stageinfo.items():
        logger.debug(f"{stagename}:{' '.join(plugin_list)}")
        db_taskstruct.update_one({"taskid": taskid}, {"$set": {"stage": stagename}})
        for plugin in plugin_list:
            db_taskstruct.update_one({"taskid": taskid}, {"$set": {"plugin": plugin}})
            try:
                PLUGIN_LIST[plugin]['plugin'].dispatch(stagename, filter, taskid)
            except Exception as e:
                logger.error(traceback.format_exc())

    logger.debug(f"task[{taskid}] after {(time.time() - start_time)} seconds complete")
    # remove task list
    db_taskstruct.delete_one({"taskid": taskid})
    db_task.update_one({"taskid": taskid}, {"$set": {"status": "success"}})




