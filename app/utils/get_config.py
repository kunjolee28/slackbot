from os import getenv
from json import load
from google.cloud import secretmanager

def get_config():
    env = getenv('ENV')
    with open('app/config.json') as f:
        CONFIG = load(f)
        CONFIG = CONFIG[env]
        f.close()
    CONFIG['env'] = env

    client = secretmanager.SecretManagerServiceClient()

    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/SECRET_KEY/versions/latest"})
    CONFIG['secret_key'] = response.payload.data.decode('UTF-8')

    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/QUALTRICS_ID/versions/latest"})
    CONFIG['qualtrics_id'] = response.payload.data.decode('UTF-8')

    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/QUALTRICS_SECRET/versions/latest"})
    CONFIG['qualtrics_secret'] = response.payload.data.decode('UTF-8')

    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/lionbridge-client-id/versions/latest"})
    CONFIG['lionbridge_client'] = response.payload.data.decode('UTF-8')

    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/lionbridge-client-secret/versions/latest"})
    CONFIG['lionbridge_secret'] = response.payload.data.decode('UTF-8')

    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/slack_bot_url/versions/latest"})
    CONFIG['slack_bot_url'] = response.payload.data.decode('UTF-8')
    
    response = client.access_secret_version(request={"name": f"projects/{CONFIG['project_id']}/secrets/qualtrics_access_token/versions/latest"})
    CONFIG['qualtrics_access_token'] = response.payload.data.decode('UTF-8')


    return CONFIG
