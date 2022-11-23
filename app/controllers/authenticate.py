import jwt

import app.utils.api_events as API_EVENTS

from flask import Blueprint, make_response, jsonify, request
from app.utils.logger import logger
from app.utils.get_config import get_config
from app.utils.exceptions import BadRequest, Unauthorized, InternalServerError

authenticate = Blueprint('authenticate', __name__, url_prefix='/auth')

@authenticate.route('/', strict_slashes=False, methods=['POST'])
def create_token():
    logger.info(f'/auth {API_EVENTS.postRequest}')
    CONFIG = get_config()
    SECRET_KEY=CONFIG['secret_key']
    QUALTRICS_ID=CONFIG['qualtrics_id']
    QUALTRICS_SECRET=CONFIG['qualtrics_secret']
    if (not SECRET_KEY) or (not QUALTRICS_ID) or (not QUALTRICS_SECRET):
        logger.error(API_EVENTS.missingEnvVariable)
        raise InternalServerError(API_EVENTS.missingEnvVariable)

    body = request.get_json()

    if not body:
        logger.error(API_EVENTS.missingRequestBody)
        raise BadRequest(API_EVENTS.missingRequestBody)

    request_id = body.get('id')
    request_secret = body.get('secret')

    if (not request_id) or (not request_secret):
        logger.error(API_EVENTS.missingAuthIdOrSecret)
        raise BadRequest(API_EVENTS.missingAuthIdOrSecret)

    if (request_id != QUALTRICS_ID) or (request_secret  != QUALTRICS_SECRET):
        logger.error(API_EVENTS.invalidCredentials)
        raise Unauthorized(API_EVENTS.invalidCredentials)

    encoded_jwt = jwt.encode({"name": QUALTRICS_ID}, SECRET_KEY, algorithm='HS256')
    logger.info(API_EVENTS.authenticationSucceed)
    return make_response(jsonify({
        "application_status": "success",
        "access_token": encoded_jwt
    }), 200)
