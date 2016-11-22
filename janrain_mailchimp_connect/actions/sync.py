import datetime
import flask
import hashlib
import janrain_datalib
import json
import logging
import requests
import time
import sys
from urllib.parse import urljoin
from datetime import datetime
from ..date_utils import toRecordDateTime, fromRecordDateTime

def sync():
    """ Function attached to the Flask route '/sync' which kicks of job in thread. """

    app = flask.current_app
    config = flask.current_app.config.copy()
    logger = logging.getLogger(config['LOGGER_NAME'])
    job = app.JobModel.get(config)
    executor = app.executor

    executor.submit(_sync, config, logger, job)

    return "OK"

def _sync(config, logger, job):
    """ Private function which is meant to be ran in a thread.

    This function downloads records from Capture, sends those records in batches to MailChimp,
    and waits for thoes MailChimp batches to finish.
    """
    job.start()
    total_batch_num = 0
    logger.info("Job started at {}".format(job.started))
    try:
        for capture_batch in capture_batch_generator(config, logger, job):
            mailchimp_batch = send_batch_to_mailchimp(config, logger, capture_batch)
            logger.info("MailChimp Batch: {} Started".format(mailchimp_batch['id']))
            while not is_mailchimp_batch_finished(config, logger, mailchimp_batch):
                logger.info("MailChimp Batch: {} Not Finished".format(mailchimp_batch['id']))
                logger.debug('Sleeping %d seconds', config['MC_TIME_BETWEEN_BATCHES'])
                time.sleep(config['MC_TIME_BETWEEN_BATCHES'])
            logger.info("MailChimp Batch: {} Finished".format(mailchimp_batch['id']))
            total_batch_num += 1
    except Exception as ex:
        logger.error(str(ex))
        if config['DEBUG']:
            logger.exception(ex)
    job.stop()
    logger.info("Job ended at: {}".format(job.ended))

def is_mailchimp_batch_finished(config, logger, mailchimp_batch):
    """ Uses MailChimp's APIs to check if the batch has Finished.
    https://developer.mailchimp.com/documentation/mailchimp/reference/batches/#read-get_batches_batch_id
    """
    endpoint = mailchimp_endpoint(config, "/batches/{}".format(mailchimp_batch.get('id')))
    result = requests.get(endpoint, auth=("janrain-mailchimp", config['MC_API_KEY']))
    result_json = result.json()
    logger.info("MailChimp Batch: {id}, Status: {status}, Total Operations: {total_operations}, Finished Operations: {finished_operations}, Errored Operations: {errored_operations}".format_map(result_json))
    return result.json()['status'] == 'finished'

def capture_batch_generator(config, logger, job):
    """ Downloads records from Capture and yields them in batches. """
    batch_size = config['JANRAIN_BATCH_SIZE']

    lastUpdated = datetime.utcfromtimestamp(0)
    if not config['JANRAIN_FULL_EXPORT'] and job.lastUpdated:
        lastUpdated = job.lastUpdated

    if not config['JANRAIN_FULL_EXPORT'] and (datetime.now()-lastUpdated).days > config['JANRAIN_MAX_LASTUPDATED']:
        exit(logger, "LastUpdated too many days ago {} > {}".format((datetime.now()-lastUpdated).days, config['JANRAIN_MAX_LASTUPDATED']))

    kwargs = {
        'batch_size': batch_size,
        'attributes': ['email', 'uuid', 'lastUpdated', config['JANRAIN_OPT_IN_ATTRIBUTE']] + list(config["FIELD_MAPPING"]),
        'filtering': "lastUpdated > '{}'".format(toRecordDateTime(lastUpdated))
    }

    logger.info("Export Started")
    batch = []
    total_record_num = 0
    capture_app = janrain_datalib.get_app(config['JANRAIN_URI'], config['JANRAIN_CLIENT_ID'], config['JANRAIN_CLIENT_SECRET'])
    for record_num, record in enumerate(capture_app.get_schema(config['JANRAIN_SCHEMA_NAME']).records.iterator(**kwargs), start=1):
        logger.debug("fetched record: %d, uuid: %s", record_num, record.get('uuid', "unknown"))
        batch.append(record)
        total_record_num +=1
        if len(batch) == config['JANRAIN_BATCH_SIZE']:
            yield batch
            job.lastUpdated = fromRecordDateTime(batch[-1]['lastUpdated'])
            batch = []
    if len(batch):
        yield batch
        job.lastUpdated = fromRecordDateTime(batch[-1]['lastUpdated'])

    logger.info("Export Finished, Total records fetched: %d", total_record_num)

def mailchimp_build_batch_operation(config, record):
    """ Builds the MailChimp batch operation.
    https://developer.mailchimp.com/documentation/mailchimp/reference/batches/#read-get_batches_batch_id
    """
    email_md5 = hashlib.md5(record['email'].encode()).hexdigest()
    janrain_status = bool(record.get(config['JANRAIN_OPT_IN_ATTRIBUTE'], False))
    status = 'subscribed' if janrain_status else 'unsubscribed'
    return {
        "method": "PUT",
        "path": "lists/{list_id}/members/{email_md5}".format(list_id=config['MC_LIST_ID'], email_md5=email_md5),
        "body": json.dumps({
            "email_address": record['email'],
            "status": status,
            "status_if_new": status,
            "merge_fields": {
                mc_field_label: record.get(janrain_attribute)
                for (janrain_attribute, mc_field_label)
                in config["FIELD_MAPPING"].items()
            }
        })
    }

def mailchimp_build_batch(config, records):
    """ Builds the entire MailChimp batch.
    https://developer.mailchimp.com/documentation/mailchimp/reference/batches/#read-get_batches_batch_id
    """
    return {
       "operations": [
           mailchimp_build_batch_operation(config, record)
           for record in records
           if record.get('email')
        ],
    }

def send_batch_to_mailchimp(config, logger, records):
    """ Make the post call to mailchimp with the batch.
    mailchimp endpoint: https://<dc>.api.mailchimp.com/3.0/batches
    https://developer.mailchimp.com/documentation/mailchimp/reference/batches/#read-get_batches_batch_id
    """
    batch = mailchimp_build_batch(config, records)
    if len(records) > config['MC_MAX_RECORDS_IN_BATCH']:
        exit(logger, "Too many records in batch to send to MailChimp: {} > {}".format(len(records), config['MC_MAX_RECORDS_IN_BATCH']))
    if sys.getsizeof(batch) > config['MC_MAX_BYTES_IN_BATCH']:
        exit(logger, "Too many bytes in batch to send to MailChimp: {} > {}".format(sys.getsizeof(batch), config['MC_MAX_BYTES_IN_BATCH']))
    endpoint = mailchimp_endpoint(config, "/batches")
    result = requests.post(endpoint, auth=("janrain-mailchimp", config['MC_API_KEY']), json=batch)
    result_json = result.json()
    logger.info("MailChimp Batch: {id}, Status: {status}, Total Operations: {total_operations}, Finished Operations: {finished_operations}, Errored Operations: {errored_operations}".format_map(result_json))
    return result_json

def mailchimp_endpoint(config, path=None):
    """ Builds the MailChimp endpoint
    http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/ 
    """
    data_center= config['MC_API_KEY'].split('-')[-1]
    base_endpoint = config["MC_URI_TEMPLATE"].format(data_center=data_center)
    if path is None:
        return base_endpoint
    else:
        return urljoin(base_endpoint, path.lstrip('/'))

def exit(logger, message):
    logger.error(message)
    raise SystemExit(message)
