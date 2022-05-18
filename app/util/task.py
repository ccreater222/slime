# 任务连续
# 子任务管理

from datetime import datetime
from enum import Enum
import uuid
from util.client import db_task, db_taskstruct, celery_app
from util.plugin import PLUGIN_LIST
import re
from dateutil import parser
import dateutil


from util.util import get_all_keys
from worker.task import workflow

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
        data.sort([("created", -1)])
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
    
    def start(self):
        if db_taskstruct.count_documents({"taskid": self.taskid}) == 1:
            process = db_taskstruct.find_one({"taskid": self.taskid})
            new_stageinfo = {}
            start = False
            for k, v in self.stageinfo.items():
                if k == process["stage"]:
                    start = True
                    plugin_index = v.index(process["plugin"])
                    new_stageinfo[k] = v[plugin_index:]
                    continue
                if not start :
                    continue
                new_stageinfo[k] = v
            workflow.delay(self.taskid, self.stageinfo, self.filter)
        else:
            workflow.delay(self.taskid, self.stageinfo, self.filter)

    def kill_all_subtask(self):
        process = db_taskstruct.find_one({"taskid": self.taskid})
        if process == None:
            return
        if process.get("stage", "") == "" or process.get("plugin", "") == "":
            return
        for celery_task_id in process.get("tasks", []):
            try:
                celery_app.control.revoke(celery_task_id)
            except Exception:
                pass

    def pause(self):
        self.kill_all_subtask()
        db_task.update_one({"taskid": self.taskid}, {"$set": {"status": Taskstatus.wait.value}})
    
    def restart(self):
        self.kill_all_subtask()
        db_taskstruct.delete_one({"taskid": self.taskid})
        self.start()
    
    def stop(self):
        self.kill_all_subtask()
        db_task.delete_one({"taskid": self.taskid})
            

