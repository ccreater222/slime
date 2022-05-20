# -*- coding: UTF-8 -*-
from .plugin import load_plugins
load_plugins()
from flask import Blueprint
from click import command
from .install import install_plugins
cli_bp = Blueprint('install', __name__)
cli_bp.cli.add_command(command("install", help="Install all plugins")(install_plugins))
