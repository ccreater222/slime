# -*- coding: UTF-8 -*-

import os
from util.plugin import BasePlugin
from config.config import *
from config.plugin import PYTHON2, PYTHON3, PROXY
import subprocess
from inspect import getmembers,isclass
from importlib import import_module
import sys
def install_python2():
    p = subprocess.run([PYTHON2, "-h"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run([PYTHON2, "-m", "pip"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run([PYTHON2, "-m", "venv", "-h"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()

def install_python3():
    p = subprocess.run([PYTHON3, "-h"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run([PYTHON3, "-m", "pip"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run([PYTHON3, "-m", "venv", "-h"], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()



def install_plugins():
    current_dir = os.path.dirname(__file__)
    with os.scandir(os.path.join(current_dir,'..','plugins')) as it:
        for entry in it:
            if not entry.name.startswith('.') and not entry.name.startswith('_') and entry.is_dir():
                plugin_name = entry.name
                modulename = f'plugins.{plugin_name}.{plugin_name}'
                if modulename not in sys.modules:
                    module = import_module(modulename)
                else:
                    module = sys.modules[modulename]
                classes = getmembers(module, isclass)
                for clazzname,clazz in classes:
                    if clazz != BasePlugin and issubclass(clazz,BasePlugin):
                        if not getattr(clazz, "isinstall")():
                            getattr(clazz, "install")()

def gitclone(repo: str, directory: str, args = []):
    if PROXY != "":
        p = subprocess.run(["git", "config", "--global", "http.proxy", PROXY], stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        p.check_returncode()
    args = ["git", "clone"] + args
    args = args + [repo, directory]
    p = subprocess.run(args, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    
