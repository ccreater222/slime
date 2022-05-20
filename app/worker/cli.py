# -*- coding: UTF-8 -*-
from util.client import celery_app
def run_worker():
    argv = [
        'worker',
        '-l',
        'DEBUG',
        '-P',
        'solo'
    ]
    celery_app.worker_main(argv)