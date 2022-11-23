# example of import: import app.utils.api_events as api_events


"""INFO EVENTS"""
getRequest = 'getRequest'
postRequest = 'postRequest'
authenticatingToLionbridge = 'authenticatingToLionbridge'
creatingItemsOnLionbridge = 'creatingItemsOnLionbridge'
receivedDataFromLionbridge = 'receivedDataFromLionbridge'
masking_PII_data = 'masking_PII_data'
sending_to_slack = 'sending_to_slack'
translating_comment = 'translating_comment'
no_translation_needed = 'no_translation_needed'
found_comment = 'found_comment'
no_config_for_survey = 'no_config_for_survey'
updating_qualtrics = 'updating_qualtrics'
survey_found_on_BQ = 'survey_found_on_BQ'
qualtrics_update_response = 'qualtrics_update_response'
lionbridge_get_outputs = 'lionbridge_get_outputs'
sending_to_tdp_hoarder = 'sending_to_tdp_hoarder'
requesting_theme_prediction = 'requesting_theme_prediction'


"""SUCCESS EVENTS"""
masking_PII_data_succeed = 'masking_PII_data_succeed'
sent_message_to_slack = 'sent_message_to_slack'
comment_translated = 'comment_translated'
#authtentication and authorization
authenticationSucceed = 'authenticationSucceed'
authorizationSucceed = 'authorizationSucceed'
#lionbridge
lionbridgeAuthSucceed = 'lionbridgeAuthSucceed'
lionbridgeAuthFailed = 'lionbridgeAuthFailed'
lionbridgeCreateItemsSucceed = 'lionbridgeCreateItemsSucceed'

"""FAILURE EVENTS"""
DLP_error = 'DLP_error'
could_not_send_message_to_slack = 'could_not_send_message_to_slack'
comment_is_too_short = 'comment_is_too_short'
failed_translating_comment = 'failed_translating_comment'
failed_requesting_theme_prediction = 'failed_requesting_theme_prediction'
# missing stuff
missingEnvVariable = 'missingEnvVariable'
missingRequestBody = 'missingRequestBoddy'
missingAuthIdOrSecret = 'missingAuthIdOrSecret'
missingLionbridgeProjectId = 'missingLionbridgeProjectId'
missingSurveyItems = 'missingSurveyItems'
missing_item_id = 'missing_item_id'
misssing_outputs = 'missing_outputs'
# invalid stuff
invalidCredentials = 'invalidCredentials'
invalidAccessToken = 'invalidAccessToken'
# permissions
notEnoughPermissions = 'notEnoughPermissions'
# lionbridge
lionbridgeCreateItemsFailed = 'lionbridgeCreateItemsFailed'
lionbridgeGetIdFailed = 'lionbridgeGetIdFailed'
invalid_inputs_len = 'invalid_inputs_len'
lionbridge_get_item_failed = 'lionbridge_get_item_failed'
#bigquery
bqErrorSavingSurvey = 'bqErrorSavingSurvey'
bqErrorSavingIdMappingInfo = 'bqErrorSavingIdMappingInfo'
bqErrorSavingAnnotatedData = 'bqErrorSavingAnnotatedData'
#cronjob
checkingRecordsWithoutItemId = 'checkingRecordsWithoutItemId'
checkingRecordsOlderThanFiveDays = 'checkingRecordsOlderThanFiveDays'