# 任务连续
# 子任务管理

from datetime import datetime
from enum import Enum
import uuid
from util.client import db_task
from util.plugin import PLUGIN_LIST
import re
from dateutil import parser
import dateutil

from util.util import get_all_keys

class Taskstatus(Enum):
    wait="wait"
    execute="execute"
    failed="failed"
    success="success"
class Task:
    taskid: str
    stageinfo: dict
    status: str
    log: dict
    created: datetime
    filter: dict
    _config: dict
    
    

    @classmethod
    def load_all(cls, filter):
        condition = cls.get_condition(filter.get("condition", {}))
        select_all = filter.get("selectall", False)
        if filter.get("selected", []) == []:
            select_all = True
        if select_all == False:
            condition = {"taskid": {"$in": filter.get("selected", [])}}
        tasks = db_task.find(condition)
        result = []
        for item in tasks:
            result.append(cls(**item))
        return result
        

    @staticmethod
    def get_condition(condition):
        result = {}
        for k, v in condition.items():
            if k == "created":
                try:
                    result[k] = parser.parse(v)
                except dateutil.parser._parser.ParserError:
                    continue
            else:
                result[k] =  re.compile(re.escape(v))
        return result

    @classmethod
    def load_by_page(cls, filter) -> list:
        data = db_task.find(cls.get_condition(filter.get('condition', {})))
        sort_key = filter.get('sort', "")
        if sort_key != "":
            index = 1
            if filter.get('desc', False):
                index = -1
            data = data.sort([(sort_key, index)])
        total = db_task.count_documents({})
        data = data.skip((filter.get('page') -1) * filter.get('size', 20)).limit(filter.get('size', 20))
        result = []
        for item in data:
            result.append(cls(**item))
        return total, result
    def __init__(self, *args, **kwargs) -> None:
        for k,v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def load_from_request(cls, _config, filter):
        self = cls()
        self.taskid = str(uuid.uuid4())
        self.status = Taskstatus.wait.value
        self.stageinfo = {}
        self.log = {}
        for stagename, value in _config.items():
            self.stageinfo[stagename] = list(value.keys())
        for stagename, value in self.stageinfo.items():
            self.log[stagename] = {}
            for plugin in value:
                self.log[stagename][plugin] = []
        self.created = datetime.now()
        self.filter = filter
        self._config = _config
        return self

    def save(self):
        db_task.insert_one(self.toDict())
        for stagename, value in self._config.items():
            for plugin in value.keys():
                config_clazz = PLUGIN_LIST[plugin]['config']['clazz']
                instance = config_clazz()
                for k, v in value[plugin].items():
                    setattr(instance, k, v)
                instance.save_to_database(stagename, self.taskid)


    def toDict(self) -> dict:
        result = {}
        keys = get_all_keys(self)
        for key in keys:
            result[key] = getattr(self, key)
        return result

