# -*- coding: UTF-8 -*-
from flask import Blueprint
from click import command
from .cli import run_worker
cli_bp = Blueprint('worker', __name__)
cli_bp.cli.add_command(command("worker", help="Run the worker")(run_worker))
