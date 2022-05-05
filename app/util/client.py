from pymongo import MongoClient
from config.config import MONGODB_URL

mongo_client = MongoClient(MONGODB_URL)
mongo_db = mongo_client.slime
db_resource = mongo_db.resource
db_vuldata = mongo_db.vuldata