import time
import app.utils.api_events as API_EVENTS

from flask import Blueprint, make_response, jsonify, request
from copy import deepcopy

from app.decorators.authorization import authorization
from app.utils.exceptions import BadRequest, InternalServerError
from app.utils.get_config import get_config
from app.utils.logger import logger
from app.services.pii_masking import deidentify_string
from app.services.slack_bot import send_slack
from app.services.translate_comment import translate_comment
from app.services.theme_prediction import theme_prediction

survey = Blueprint('survey',__name__, url_prefix='/survey')
CONFIG = get_config()
QUALTRICS_ID = CONFIG['qualtrics_id']

@survey.route('/', strict_slashes=False, methods=['POST'])
@authorization(name=QUALTRICS_ID)
def submit_survey():
    survey_body = request.get_json()
    logger.info(f'/survey {API_EVENTS.postRequest}: {survey_body}')

    if not survey_body:
        logger.error(API_EVENTS.missingRequestBody)
        raise BadRequest(API_EVENTS.missingRequestBody)

    # get survey_id to pull the correct config
    survey_id = survey_body['surveyId']
    response_id = survey_body['responseId']
    survey_config = deepcopy(CONFIG['qualtrics'].get(survey_id)) # deep copy to avoid mutating the CONFIG object

    if not survey_config: 
        logger.warn(f'{API_EVENTS.no_config_for_survey}: {survey_id}')
        raise InternalServerError(f'{API_EVENTS.no_config_for_survey}: {survey_id}')

    # check if survey must be sent to slack
    slack_config = survey_config.get('slack')
    if slack_config:
        gcp_project_id = CONFIG['project_id']
        info_types = CONFIG['dlp']['info_types']           

        slack_message_template = slack_config['template']

        # Checking if survey has comments to be added to the template
        comments_items = slack_config.get('comments').items()
        for key, value in comments_items:
            if key in survey_body and survey_body[key] and not str.isspace(survey_body[key]):
                logger.info(f'{API_EVENTS.found_comment} for {key}')

                # Masking PII data
                survey_body[key] = deidentify_string(gcp_project_id, survey_body[key], info_types)
                time.sleep(0.1) # For DLP API Rate Limit
                slack_message_template.append(value)

                # Translating comment if necessary
                new_comment = translate_comment(survey_body[key])

                # checking if comment was translated
                if new_comment != survey_body[key]:
                    slack_message_template.append(f'Translation: ```{{{key}_translated}}```')
                    survey_body[f'{key}_translated'] = new_comment


                slack_message = "\n".join(slack_message_template).format(**survey_body)
                # channels = [
                #     '#general',
                #     '#hello',
                #     '#random',
                #     '#test'
                # ]

                # for channel in channels: 
                #     send_slack(text=slack_message, channel=channel)
                
                # // "commentsTransaction": "commentsTrasactionTest",
                #     "commentsConsumer": "comments consumer test",
                slack_channel_rules = slack_config['channel_rules']
                
                for channel, condition in slack_channel_rules.items():
                    if eval(condition) == True:
                        send_slack(text=slack_message, channel=channel)
              

    # Checking if survey needs theme prediction
    if 'theme_prediction' in survey_config:
        field = survey_config['theme_prediction']['field']
        output_name = survey_config['theme_prediction']['output_name']
        comment = survey_body.get(f'{field}_translated') or survey_body.get(field)

        if comment:
            prediction = theme_prediction(comment)
            survey_body[output_name] = prediction
            
    return make_response(jsonify({
        'application_status': 'success',
        'message': 'survey was processed'
    }),200)
