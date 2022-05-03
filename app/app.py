from util.logging import ExceptionDecorator
from flask import Flask

app = Flask(__name__)

@app.cli.command("worker",help="Run the worker")
def run_worker():
    print("run worker")