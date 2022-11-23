import jwt

import app.utils.api_events as API_EVENTS

from functools import wraps
from flask import request
from app.utils.get_config import get_config
from app.utils.exceptions import Forbidden, Unauthorized
from app.utils.logger import logger
def authorization(name):
    """
        Params:
            name (str): name field inside the jwt payload, to verify it matches
                i.e, to restrict routes only to specific entities
    """
    def inner(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'Authorization' in request.headers.keys():
                token = request.headers.get('Authorization')
            elif 'access_token' in request.args.keys():
                token = request.args.get('access_token')
            else:
                token = ''

            CONFIG = get_config()
            SECRET_KEY = CONFIG['secret_key']

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                if payload['name'] != name:
                    logger.error(API_EVENTS.notEnoughPermissions)
                    raise Forbidden(API_EVENTS.notEnoughPermissions)
            except Forbidden as e:
                raise e
            except jwt.exceptions.InvalidTokenError as e:
                logger.error(API_EVENTS.invalidAccessToken)
                raise Unauthorized(API_EVENTS.invalidAccessToken) from e

            logger.info(API_EVENTS.authorizationSucceed)

            return func(*args, **kwargs)
        return decorated_function
    return inner
