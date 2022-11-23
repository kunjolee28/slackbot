import requests
import app.utils.api_events as API_EVENTS

from app.utils.get_config import get_config
from app.utils.logger import logger

def update_qualtrics(survey_id='', response_id='', annotated_data={}):
    """Function to update qualtrics with annotated data
    Args:
        survey_id(string)
        response_id(string)
        annotated_data(dict)
    """

    logger.info(f'{API_EVENTS.updating_qualtrics}: Survey {survey_id} response {response_id}')

    CONFIG = get_config()
    qualtrisc_endpoint = CONFIG['qualtrics']['api_endpoint']
    api_token = CONFIG['qualtrics_access_token']

    headers = {
        "Content-Type": "application/json",
        "x-api-token": api_token
    }

    payload = {
        "surveyId": survey_id,
        "resetRecordedDate": False,
        "embeddedData": annotated_data
    }

    response = requests.put(f'{qualtrisc_endpoint}/responses/{response_id}', headers=headers, json=payload)
    
    return response