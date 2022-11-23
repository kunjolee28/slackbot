import app.utils.api_events as API_EVENTS

from app.utils.logger import logger
from app.utils.get_config import get_config
from google.cloud import translate

def translate_comment(comment):
    CONFIG = get_config()
     #Create the translation client
    translateClient = translate.TranslationServiceClient()
    project_id = CONFIG['project_id']
    location = 'global'

    parent = f"projects/{project_id}/locations/{location}"

    translated_comment = ''
    if len(comment) >= 10:
        #Call the translation api to detect the language of the comment
        response = translateClient.detect_language(
            parent=parent,
            content=comment,
            mime_type='text/plain')

        #Set langauge_code and language_confidence based on translation api return
        language_code = response.languages[0].language_code
        language_confidence = response.languages[0].confidence

        #If language is french, send comment to translation api, else
        if language_code == 'fr' and language_confidence >= 0.75:
            logger.info(f'{API_EVENTS.translating_comment}: {comment}')

            response = translateClient.translate_text(
                parent=parent,
                contents=[comment],
                mime_type='text/plain',
                source_language_code='fr',
                target_language_code='en')

            try:
                translated_comment = response.translations[0].translated_text
                logger.info(f'{API_EVENTS.comment_translated}: {translated_comment}')

            except Exception as e:
                logger.info(f'{API_EVENTS.failed_translating_comment}: {e}')
        else:
            logger.info(API_EVENTS.no_translation_needed)
    else:
        logger.error(API_EVENTS.comment_is_too_short)
        
    return translated_comment if translated_comment else comment