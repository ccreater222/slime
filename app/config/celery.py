# -*- coding: UTF-8 -*-

import config.development as current_mode
import os
broker_url = current_mode.RABBIT_URL
result_backend = current_mode.REDIS_URL
timezone = "Asia/Shanghai"
result_expires = 3600
task_serializer = "msgpack"
accept_content = ["msgpack", "json"]
result_serializer = "msgpack"

task_create_missing_queues = True
task_acks_late = True
worker_prefetch_multiplier = 1
task_queue_max_priority = 15
broker_connection_timeout = 7200
worker_hijack_root_logger = False
worker_concurrency = os.cpu_count() * 2
broker_heartbeat = 0
# worker_cancel_long_running_tasks_on_connection_loss = False
task_routes = {
    'worker.task.workflow': 'workflow',
    'worker.task.pluginrunner': 'pluginrunner'
}
