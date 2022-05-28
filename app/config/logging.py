# -*- coding: UTF-8 -*-

import dotenv
import os
import logging
dotenv.load_dotenv()
loglevel = os.getenv("LOGLEVEL")
if loglevel == None:
    loglevel = "INFO"
level = getattr(logging, loglevel.upper(), logging.INFO)
try:
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "log"))
except:
    pass
logging_config = {
    'version' : 1,
    'formatters' : {
        'default': {'format':
              "%(name)s-%(module)s-%(funcName)s[%(lineno)d] %(asctime)s: %(message)s"}
        },
    'handlers' : {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': level
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'level': logging.DEBUG,
            'filename': os.path.join(os.path.dirname(__file__), '..', 'log', 'log.txt')
        }
    },
    'root' : {
        'handlers': ['console', 'file'],
        'level': level,
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': level,
        },
    }
}