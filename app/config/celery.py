import config.development as current_mode
broker_url = current_mode.RABBIT_URL
result_backend = current_mode.REDIS_URL
timezone = "Asia/Shanghai"
result_expires = 3600
task_serializer = "msgpack"
accept_content = ["msgpack", "json"]
result_serializer = "msgpack"

task_acks_late = True
worker_prefetch_multiplier = 1
task_queue_max_priority = 15
broker_connection_timeout = 7200
worker_hijack_root_logger = False