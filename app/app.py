from .util.logging import ExceptionDecorator
from flask import Flask
from .worker import cli_bp
from .api import app_bp

app = Flask(__name__)
app.register_blueprint(cli_bp, cli_group=None)