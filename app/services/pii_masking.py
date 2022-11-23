import re
import app.utils.api_events as API_EVENTS

from app.utils.logger import logger
#google-cloud
from google.cloud import dlp_v2 as dlp


def deidentify_string(project, content_string, info_types):
    """Uses the Data Loss Prevention API to analyze strings for protected data.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        content_string: The string to inspect.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
    Returns:
        string: Deidentified version of the content_string.
    """
    logger.info(API_EVENTS.masking_PII_data)
    
    # Instantiate a client.
    client = dlp.DlpServiceClient()

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    deidentify = [{'info_types': [{'name': info_type}],'primitive_transformation': {'replace_config': {'new_value': {'string_value': '[{}]'.format(info_type)}}}} for info_type in info_types]
    deidentify_config = {'info_type_transformations': {'transformations': deidentify}}

    # Construct exclude rule for Person Name
    info_types_to_locate = [{'name': 'PERSON_NAME'}]
    exclusion_list = ['BILL', 'bill', 'Bill', 'Rogers', 'ROGERS', 'rogers']
    rule_set = [{'info_types': info_types_to_locate, 'rules': [{'exclusion_rule': {'dictionary': {'word_list': {'words': exclusion_list},},'matching_type': 1,}}],}] # number 1 means FULL MATCH

    inspect = [{'name': info_type} for info_type in info_types]
    inspect_config = {'info_types': inspect, 'rule_set': rule_set}
    # inspect_config = {'info_types': inspect}

    # Construct the `item`.
    item = {'value': content_string}

    # Convert the project id into a full resource id.
    parent = client.project_path(project)

    # Call the API.
    try:
        response = client.deidentify_content(parent, deidentify_config, inspect_config, item)
        text = response.item.value
        logger.info(API_EVENTS.masking_PII_data_succeed)
    except Exception as e:
        logger.error(f'{API_EVENTS.DLP_error}: {e}')
        text = content_string

    # Additional filtering for phone numbers
    text = re.sub(r'(\d[\s-]?)?[\(\[\s.-]{0,2}?\d{3}[\)\]\s.-]{0,2}?\d{3}[\s.-]?\d{4}', ' [PHONE_NUMBER]', text)

    # Mask Account Number (6-20 numbers side by side)
    text = re.sub(r'[0-9]{5,15}', '[ACCOUNT_NUMBER]', text)

    return(text)
