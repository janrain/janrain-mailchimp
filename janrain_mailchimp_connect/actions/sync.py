import datetime
import flask
import hashlib
import janrain_datalib
import json
import logging
import requests
from urllib.parse import urljoin
from datetime import datetime


def sync():
    config = flask.current_app.config.copy()
    logger = logging.getLogger(config['LOGGER_NAME'])
    records = load_records(config,logger)
    mc_records = mailchimp_build_batch(config,records)
   # print(mc_records)
    send_to_mailchimp(config, logger, records)
    return "IM at SYNC 4"

#step 2
def load_records(config,logger):
    ### for this we probably dont need to use sqs, we can just return a list of the records
    """grab records from capture and put them in sqs"""
    batch_size = get_int(config['JANRAIN_BATCH_SIZE'])
    kwargs = {
        'batch_size': batch_size,
        'attributes': ['email', 'uuid'],
        'filtering': "lastUpdated > '{}'".format(toRecordDateTime(datetime.utcfromtimestamp(0)))
    }

    logger.info("starting export from capture with batch size %s...", batch_size)

    # need to get each record and add it to a list which we can return
    records = []
    capture_app = janrain_datalib.get_app(config['JANRAIN_URI'], config['JANRAIN_CLIENT_ID'], config['JANRAIN_CLIENT_SECRET'])
    for record_num, record in enumerate(capture_app.get_schema('user').records.iterator(**kwargs), start=1):
        logger.info("fetched record: %d", record_num)
        records.append(record)
        if len(records) > 10:
            break
    logger.info("total records fetched: %d", len(records))
    return records

def mailchimp_build_batch_operation(config, record, ):
    print(record)
    email_md5 = hashlib.md5(record['email'].encode()).hexdigest()
    return {
        "method": "PUT",
        "path": "lists/{list_id}/members/{email_md5}".format(list_id=config['MC_LIST_ID'], email_md5=email_md5),
        "body": json.dumps({
            "email_address": record['email'],
            "status_if_new": "subscribed",
        })
    }

def mailchimp_build_batch(config, records):
    return {
       "operations": [mailchimp_build_batch_operation(config, record) for record in records],
    }

def send_to_mailchimp(config, logger, records):
    """make the post call to mailchimp with the batch, mailchimp will return a batch id which we can use to check
    the status

    mailchimp endpoint: https://<dc>.api.mailchimp.com/3.0/batches

    """
    #conver the records into operations
    batch = mailchimp_build_batch(config, records)
    #make the endpoint
    endpoint = mailchimp_endpoint(config, "/batches")
    print(batch)
    result = requests.post(endpoint, auth=(config['MC_API_USERNAME'], config['MC_API_KEY']), json=batch)

    print(result.text)

def mailchimp_endpoint(config, path=None):
    data_center= config['MC_API_KEY'].split('-')[-1]
    base_endpoint = config["MC_URI_TEMPLATE"].format(data_center=data_center)
    if path is None:
        return base_endpoint
    else:
        return urljoin(base_endpoint, path.lstrip('/'))

def fromRecordDateTime(record_field):
    return datetime.strptime(record_field.replace(' +0000', ''), '%Y-%m-%d %H:%M:%S.%f')

def toRecordDateTime(datetime_object):
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S.%f")
