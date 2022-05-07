from .util.logging import ExceptionDecorator
from flask import Flask
from .worker import cli_bp
from .api import app_bp
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = True
app.register_blueprint(cli_bp, cli_group=None)
app.register_blueprint(app_bp)