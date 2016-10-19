import datetime
import flask
import hashlib
import janrain_datalib
import json
import logging
import requests
import time
from urllib.parse import urljoin
from datetime import datetime


def sync():
    config = flask.current_app.config.copy()
    logger = logging.getLogger(config['LOGGER_NAME'])
    total_batch_num = 0
    for capture_batch in capture_batch_generator(config, logger):
        mailchimp_batch = send_batch_to_mailchimp(config, logger, capture_batch)
        logger.info("batch:{} started".format(mailchimp_batch['id']))
        while not isMailchimpBatchFinished(config, mailchimp_batch):
            logger.info("batch:{} not complete".format(mailchimp_batch['id']))
            time.sleep(config['MC_TIME_BETWEEN_BATCHES'])
        logger.info("batch:{} complete".format(mailchimp_batch['id']))
        total_batch_num += 1
        if total_batch_num == 2:
            break

    return "IM at SYNC 4"

def isMailchimpBatchFinished(config, mailchimp_batch):
    endpoint = mailchimp_endpoint(config, "/batches/{}".format(mailchimp_batch.get('id')))
    result = requests.get(endpoint, auth=(config['MC_API_USERNAME'], config['MC_API_KEY']))
    # get batch status
    mc_status = result.json()['status']
    # log status
    logging.debug("MC Batch {} Status: {}".format(mailchimp_batch.get('id'), mc_status))
    return mc_status == 'finished'


#step 2
def capture_batch_generator(config, logger):
    ### for this we probably dont need to use sqs, we can just return a list of the records
    """grab records from capture and put them in sqs"""
    batch_size = config['JANRAIN_BATCH_SIZE']
    kwargs = {
        'batch_size': batch_size,
        'attributes': ['email', 'uuid'] + list(config["FIELD_MAPPING"]),
        'filtering': "lastUpdated > '{}'".format(toRecordDateTime(datetime.utcfromtimestamp(0)))
    }

    logger.info("starting export from capture with batch size %s...", batch_size)

    # need to get each record and add it to a list which we can return
    batch = []
    total_record_num = 0
    capture_app = janrain_datalib.get_app(config['JANRAIN_URI'], config['JANRAIN_CLIENT_ID'], config['JANRAIN_CLIENT_SECRET'])
    for record_num, record in enumerate(capture_app.get_schema('user').records.iterator(**kwargs), start=1):
        logger.debug("fetched record: %d", record_num)
        logger.info("fetched record uuid: %s", record.get('uuid', "unknown"))
        batch.append(record)
        if len(batch) == config['JANRAIN_BATCH_SIZE']:
            yield batch
            batch = []
    if len(batch):
        yield batch

    logger.info("total records fetched: %d", total_record_num)

def mailchimp_build_batch_operation(config, record, ):
    email_md5 = hashlib.md5(record['email'].encode()).hexdigest()
    merge_fields = {}

    return {
        "method": "PUT",
        "path": "lists/{list_id}/members/{email_md5}".format(list_id=config['MC_LIST_ID'], email_md5=email_md5),
        "body": json.dumps({
            "email_address": record['email'],
            "status_if_new": "subscribed",
            "merge_fields": {
                mc_field_label: record.get(janrain_attribute)
                for (janrain_attribute, mc_field_label)
                in config["FIELD_MAPPING"].items()
            }

        })
    }

def mailchimp_build_batch(config, records):
    return {
       "operations": [
           mailchimp_build_batch_operation(config, record)
           for record in records
           if record.get('email')
        ],
    }

def send_batch_to_mailchimp(config, logger, records):
    """make the post call to mailchimp with the batch, mailchimp will return a batch id which we can use to check
    the status

    mailchimp endpoint: https://<dc>.api.mailchimp.com/3.0/batches

    """
    #conver the records into operations
    batch = mailchimp_build_batch(config, records)
    #print(batch)
    #make the endpoint
    endpoint = mailchimp_endpoint(config, "/batches")
    result = requests.post(endpoint, auth=(config['MC_API_USERNAME'], config['MC_API_KEY']), json=batch)
    return result.json()

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
