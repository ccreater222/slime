# -*- coding: UTF-8 -*-
import logging
from logging.config import dictConfig
from config.logging import logging_config
# def debug(self, name, value):
#     if name == 'disabled' and value == True:
#         print("fuckyou")
#     else:
#         super(logging.Logger,self).__setattr__(name, value)
# logging.Logger.__setattr__ = debug
dictConfig(logging_config)
def getlogger(*args, **kwargs):
    return logging.getLogger(*args, **kwargs)
logging.debug("start logging")