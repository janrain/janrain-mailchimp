"""Application configuration"""
import os
import json

# environment variables and their defaults if not defined
ENV_VARS = {
    # change true to false before commit
    'DEBUG': True,
    'LOGGER_NAME': 'janrain_mailchimp',

    'AWS_ACCESS_KEY_ID': '',
    'AWS_SECRET_ACCESS_KEY': '',
    'AWS_DEFAULT_REGION': 'us-west-2',
    'AWS_DYNAMODB_URL': 'http://localhost:8000',
    'AWS_DYNAMODB_TABLE': 'janrain-mailchimp',

    'JANRAIN_URI': '',
    'JANRAIN_SCHEMA_NAME': 'user',
    'JANRAIN_CLIENT_ID': '',
    'JANRAIN_CLIENT_SECRET': '',
    'JANRAIN_BATCH_SIZE': 100,

    'FIELD_MAPPING':{'familyName': "LNAME", "givenName": "FNAME", 'birthday': 'BIRTHDAY'},

    'MC_URI_TEMPLATE':'https://{data_center}.api.mailchimp.com/3.0/',
    'MC_API_KEY': '',
    'MC_LIST_ID': '',
}

def get_config():
    config = {}
    for key, default_value in ENV_VARS.items():
        value = os.getenv(key, '')
        # empty string means use default value
        if value == '':
            value = default_value
        elif isinstance(ENV_VARS[key], bool):
            if value.upper() != 'FALSE':
                value = True
            else:
                value = False
        elif isinstance(ENV_VARS[key], int):
            try:
                value = int(value)
            except ValueError:
                value = default_value
        elif isinstance(ENV_VARS[key], dict):
            try:
                value = json.loads(value)
            except ValueError:
                value = default_value

        config[key] = value

    return config
