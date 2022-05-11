# 任务连续
# 子任务管理

from datetime import datetime
from enum import Enum
import uuid
from util.client import db_task
from util.plugin import PLUGIN_LIST


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
    def __init__(self, _config, filter) -> None:
        self.taskid = str(uuid.uuid4())
        self.status = Taskstatus.wait
        for stagename, value in _config.items():
            self.stageinfo[stagename] = list(map(lambda x:x['name'], value))
        for stagename, value in self.stageinfo.items():
            self.log[stagename] = {}
            for plugin in value:
                self.log[stagename][plugin] = []
        self.created = datetime.now()
        self.filter = filter

    def save(self):
        db_task.insert_one(self.toDict())
        for stagename, value in self._config.items():
            for plugin in value:
                config_clazz = PLUGIN_LIST[plugin['name']]['config']['clazz']
                instance = config_clazz()
                for k, v in plugin['config']:
                    setattr(instance, k, v)
                instance.save_to_database(stagename, self.taskid)


    def toDict(self):
        result = []
        keys = get_all_keys(self)
        for key in keys:
            result[key] = getattr(self, key)

