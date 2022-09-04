# -*- coding: UTF-8 -*-

import os
from util.client import celery_app

def run_worker():
    loglevel = os.getenv("LOGLEVEL")
    queue = os.getenv("CELERY_QUEUE")
    if queue == None:
        queue = "workflow"
    if loglevel == None:
        loglevel = "WARNING"
    
    argv = [
        'worker',
        "-Q",
        queue,
        "-l",
        loglevel
    ]
    celery_app.worker_main(argv)