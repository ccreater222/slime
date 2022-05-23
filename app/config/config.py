# -*- coding: UTF-8 -*-


import config.development as current_mode
import dotenv
import os
import importlib
import sys
dotenv.load_dotenv()
mode = os.getenv("MODE")
if mode == "DEVELOP":
    modulename = f'config.development'
else:
    modulename = f'config.production'
if modulename not in sys.modules:
    module = importlib.import_module(modulename)
else:
    module = sys.modules[modulename]

MONGODB_URL = current_mode.MONGODB_URL
PROXY = ""