"""Application configuration"""
import boto3
import os
import json

# environment variables and their defaults if not defined
ENV_VARS = {
    # change true to false before commit
    'DEBUG': True,
    'LOGGER_NAME': 'janrain_mailchimp',
    'APP_LOG_FILE': '/opt/python/log/application.log',
    'APP_LOG_FILESIZE': 10000000,
    'APP_LOG_NUM_BACKUPS': 20,
    'AWS_ACCESS_KEY_ID ': '',
    'AWS_SECRET_ACCESS_KEY': '',
    'AWS_DEFAULT_REGION': '',
    'AWS_DYNAMODB_URL': None,
    'AWS_DYNAMODB_TABLE': 'export-service',
    'AWS_S3_KEY_BUCKET': '',
    'AWS_S3_RSA_KEY': '',
    #
    'JANRAIN_URI': '',
    'JANRAIN_CLIENT_ID': '',
    'JANRAIN_CLIENT_SECRET': '',
    'JANRAIN_BATCH_SIZE': 1000,
    'JANRAIN_ATTRIBUTES': '',
    'JANRAIN_QUERY': '',
    'JANRAIN_FULL_EXPORT': False,
    'MC_URI_TEMPLATE':'https://{data_center}.api.mailchimp.com/3.0/',
    'MC_API_USERNAME': '',
    # tell eric we had to use the key for mailchimp
    'MC_API_KEY': '',
    'MC_LIST_ID': '',
    'MC_MAX_RETRIES': 3,
    'MC_RETRY_TIMEOUT': 1,
    'MC_CALL_TIMEOUT': 1,
    ### need to add a mapping between user profile attributes in janrain to attributes in mailchimp (aka merge_field) must be configurable ###
    ## need a list if what we want to export
    'MC_FIELDS_TO_EXPORT': ['email', ]
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
        elif isinstance(ENV_VARS[key], list):
            try:
                value = json.loads(value)
            except ValueError:
                value = default_value

        config[key] = value

    # grab keys from s3
    if all((config['AWS_S3_KEY_BUCKET'], config['AWS_S3_RSA_KEY'])):
        s3_bucket = boto3.resource('s3').Bucket(config['AWS_S3_KEY_BUCKET'])

        obj = s3_bucket.Object(config['AWS_S3_RSA_KEY']).get()
        config['REMOTE_RSA_KEY'] = obj['Body'].read().decode('utf-8')

    return config
