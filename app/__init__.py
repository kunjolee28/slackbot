import app.utils.api_events as API_EVENTS
import app.utils.exceptions as custom_exceptions

from flask import Flask, make_response, jsonify
from app.utils.logger import logger
# Blueprints to be registered
from app.controllers.version import version
from app.controllers.survey import survey
from app.controllers.authenticate import authenticate
from app.utils.get_config import get_config
from app.services.slack_bot import send_slack
from google.cloud import secretmanager

# Initialize flask decorator to help register blueprints
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    logger.info(f'/ {API_EVENTS.getRequest}')
    return make_response(jsonify({
        'application_status': 'success',
        'response_message': 'Survey Service API running'
    }),200)

@app.route('/test', methods=['GET'])
def test():
    # CONFIG = get_config()


    channels = [
        '#general',
        '#hello',
        '#random',
        '#test'
    ]

    survey = [
        "*New Feedback {startDate}*",
            "*Identifiers*",
            "   uuid: `{evar29}`  ban_type: `{evar37}`  response_id: `{responseId}`",
            "   pageName: `{pageName}`    region: `{evar1}`",
            "   user_agent: `{userAgent}`    survey_type: `{surveyType}`",
            "*Response:*",
            "   lob: `{lob}`    interactionType: `{interactionType}`",
            "   ease: `{ease}`    csat: `{csat}`",
            "   decibel session replay: `{decibelLink}`"
    ]

    client = secretmanager.SecretManagerServiceClient()


    # logger.info(response)
    for channel in channels: 
        text = '\n'.join(survey)
        send_slack(text=text, channel=channel)

    return make_response(jsonify({
        'OK': True,
        'response': 'Message sended correctly',
    }),200)
    
@app.errorhandler(Exception)
def server_error(e):
    # checking if `e` is an unhandled exception so we can log it
    exceptions_list = filter(lambda ex: '__' not in ex, dir(custom_exceptions)) # removing dunder methods
    if not any( isinstance(e, getattr(custom_exceptions, exception)) for exception in exceptions_list ):
        logger.error(e)
    
    code = e.code if hasattr(e, 'code') else 500
    status = e.status if hasattr(e, 'status') else 'internal server error'
    return make_response(jsonify({
        'application_status': status,
        'error': str(e),
    }),code)

# Register blueprint(s)
app.register_blueprint(version)
app.register_blueprint(survey)
app.register_blueprint(authenticate)
