import requests

import app.utils.api_events as API_EVENTS

from app.utils.get_config import get_config
from app.utils.logger import logger
from app.utils.exceptions import BadGateway

from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token

def theme_prediction(comment):
    CONFIG = get_config()
    nlp_endpoint = CONFIG['theme_prediction_endpoint']

    auth_req = Request()
    sa_token = fetch_id_token(auth_req, nlp_endpoint)

    logger.info(f"{API_EVENTS.requesting_theme_prediction} for comment {comment}")

    body = { "comment": comment }
    headers = { "Authorization": f"Bearer {sa_token}" }
    response = requests.post(nlp_endpoint, headers=headers, json=body)
    if response.status_code != 200:
        logger.error(f"{API_EVENTS.failed_requesting_theme_prediction}: {response.text}")
        raise BadGateway(API_EVENTS.failed_requesting_theme_prediction)

    json_response = response.json()
    experience_theme = json_response.get('category')
    
    if not experience_theme:
        logger.error(f"{API_EVENTS.failed_requesting_theme_prediction}: {response.text}")
        raise BadGateway(API_EVENTS.failed_requesting_theme_prediction)
    
    return experience_theme
    
    