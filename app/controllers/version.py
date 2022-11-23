import time
from flask import Blueprint, jsonify, make_response


#Define the blueprint: 'version', set its url prefix: app.url/version
version = Blueprint('version', __name__, url_prefix='/version')

@version.route('/', strict_slashes=False, methods=['GET'])
def version_running():
    """
    Displays the version of the live application
    """
    run_time = int(time.time())
    current_version = 1.0

    # Dict for response message
    req_response = {}
    req_response['application_status'] = 'Success'
    req_response['response_message'] = f'version {current_version} of Survey Service is live as at {run_time}'
    req_response['status_code'] = 200
    return make_response(jsonify(req_response), 200)
