# -*- coding: UTF-8 -*-

import traceback
from celery.result import AsyncResult
from util.client import celery_app
from util.plugin import PLUGIN_LIST, BaseModel, BasePlugin
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

@celery_app.task(bind=True)
def pluginrunner(self, stage:str, plugin:str, data: dict, taskid: str):
    
    cls = PLUGIN_LIST[plugin]['plugin']
    instance = cls()
    try:
        # init instance
        instance.taskid = taskid
        instance.celery_task_id = self.request.id
        # load config
        config = cls._slime_config()
        config.load_from_database(stage, taskid)
        instance.config = config
        instance.stage = stage

        # get model from stage function param
        func = getattr(BasePlugin, stage, None)
        if func == None:
            raise NotImplementedError(f"{stage} has not been implemented")
        func_annotations = getattr(func, '__annotations__', None)
        if func_annotations == None:
            raise Exception('what happend?')
        inputtype = func_annotations['target_list'].__args__[0]
        data = inputtype.load_from_db(data)

        # run
        result = getattr(instance,stage)([data])

        # save result
        for item in result:
            item.taskid = taskid
            item.save()
    except Exception as e:
        instance.save_log(traceback.format_exc())
        raise e

