import requests
import os
import app.utils.api_events as API_EVENTS

from app.utils.logger import logger
from app.utils.get_config import get_config
from slack_sdk import WebClient

from dotenv import load_dotenv
from pathlib import Path

def send_slack(text="", channel=""):

    logger.info(f'{API_EVENTS.sending_to_slack}: channel {channel}')
    env_path = Path('.') / '.env'
    load_dotenv(env_path)

    CONFIG = get_config()
    CLIENT = WebClient(token=os.environ['slack_token'])

    # logger.info(CONFIG)
    # url = CONFIG['slack_bot_url']
    

    # payload = {
    #     "username": "survey-bot",
    #     "channel": channel,
    #     "text": text
    # }
    try:
        CLIENT.chat_postMessage(channel=channel, text=text)
        # response = requests.post(url, json=payload)
        # code = response.status_code
        # if code >= 400:
        #     logger.error(f'{API_EVENTS.could_not_send_message_to_slack}: status code {code}, {response.text}')
        # logger.info(f'{API_EVENTS.sent_message_to_slack}: status code {code}')
    except Exception as e:
        logger.error(f'{API_EVENTS.could_not_send_message_to_slack}: {e}')
