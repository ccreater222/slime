from pymongo import MongoClient
from config.config import MONGODB_URL
from celery import Celery
from celery import Task

mongo_client = MongoClient(MONGODB_URL)
mongo_db = mongo_client.slime
db_resource = mongo_db.resource
db_vuldata = mongo_db.vuldata
db_config = mongo_db.config
db_task = mongo_db.task
db_taskstruct = mongo_db.taskstruct

class SlimeTask(Task):
    def before_start(self, task_id, args, kwargs):
        slime_taskid = ''
        if len(args) > 0:
            slime_taskid = args[0]
        else:
            slime_taskid = kwargs.get('taskid', '')
        db_taskstruct.update_one({"taskid": slime_taskid}, { "$push": {"tasks": task_id } }, upsert=True)

celery_app = Celery(
    task_cls = SlimeTask
)
celery_app.config_from_object("config.celery")
