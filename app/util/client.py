from pymongo import MongoClient
from config.config import MONGODB_URL
from celery import Celery


mongo_client = MongoClient(MONGODB_URL)
mongo_db = mongo_client.slime
db_resource = mongo_db.resource
db_vuldata = mongo_db.vuldata
db_config = mongo_db.config
db_task = mongo_db.task
celery_app = Celery()
celery_app.config_from_object("config.celery")