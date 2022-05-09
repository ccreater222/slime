from flask import Blueprint
from .dashboard import dashboard
from .task import task_query
from .vuldata import vuldata_query
from .resource import delete_resource, query_resource, create_resource, update_resource
from .plugins import query_plugins

app_bp = Blueprint('app', __name__, url_prefix='/api')
app_bp.add_url_rule('/dashboard',None, dashboard)
app_bp.add_url_rule('/task', None, task_query, methods=['POST'])
app_bp.add_url_rule('/vuldata', None, vuldata_query, methods=['POST'])

# resource

app_bp.add_url_rule('/resource', None, query_resource, methods = ['POST'])
app_bp.add_url_rule('/create/resource', None, create_resource, methods = ['POST'])
app_bp.add_url_rule('/delete/resource', None, delete_resource, methods = ['POST'])
app_bp.add_url_rule('/update/resource', None, update_resource, methods = ['POST'])

# task

app_bp.add_url_rule('/plugins', None, query_plugins, methods = ['GET'])