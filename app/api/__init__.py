from flask import Blueprint
from .dashboard import dashboard
from .task import task_query
from .vuldata import vuldata_query
from .resource import query_resource
app_bp = Blueprint('app', __name__, url_prefix='/api')
app_bp.add_url_rule('/dashboard',None, dashboard)
app_bp.add_url_rule('/task', None, task_query, methods=['POST'])
app_bp.add_url_rule('/vuldata', None, vuldata_query, methods=['POST'])
app_bp.add_url_rule('/resource', None, query_resource, methods = ['POST'])