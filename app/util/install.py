import os
from config.config import *
from config.plugin import PYTHON2, PYTHON3
import subprocess
def install_python2():
    p = subprocess.run(f"{PYTHON2} -h", stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run(f"{PYTHON2} -m pip", stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run(f"{PYTHON2} -m venv -h", stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()

def install_python3():
    p = subprocess.run(f"{PYTHON3} -h", stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run(f"{PYTHON3} -m pip", stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()
    p = subprocess.run(f"{PYTHON3} -m venv -h", stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p.check_returncode()

