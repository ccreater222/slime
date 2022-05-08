from util.logging import ExceptionDecorator
from flask import Flask
from worker import cli_bp
from api import app_bp
from flask_cors import CORS
import werkzeug

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = True
app.register_blueprint(cli_bp, cli_group=None)
app.register_blueprint(app_bp)

@app.errorhandler(500)
def handle_bad_request(e):
    print(e)
    return 'bad request!', 500

if __name__ == "__main__":
    app.run()