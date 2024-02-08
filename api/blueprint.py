from flask import Blueprint, request

import app_properties
from api import stat

api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.get('/servers')
def servers():
    ss = [{'alias': server.get('alias'), 'id': i} for i, server in enumerate(app_properties.servers.values())]
    return {
        'status': 0,
        'data': {'rows': ss}
    }


@api_blueprint.get('/metrics')
def metrics():
    args = request.args
    return {
        'status': 0,
        'data': {"rows": stat.get_metric(server_id=int(args.get('server')), key=args.get('key'))}
    }
