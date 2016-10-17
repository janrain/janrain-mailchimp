import datetime
import flask
import hashlib
import janrain_datalib
import json
import logging
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


# def init_sync(config,logger):
#     ### need to update this list
#     """initialize all needed services and store references in dict with the
#         the following values:
#
#         capture_app
#         capture_schema
#         janrain_ccid_name
#         janrain_attribute_map
#         custom_field_map
#         janrain_attributes
#         queue
#         sdb
#         sdb_domain_name
#         sdb_item_name
#         mc_list_ids
#         mc_client
#         last_run_time
#     """
#     sync_info = {}
#
#     #1. validate config
#     #      If we have a list, we need to add email if it doesnt exist
#     #       if mapping, verify that there is an email mapping
#
#
#     #2. quary capture for records
#
#     #3. send to mailchimp
#
#     # if not init_janrain(sync_info, config, logger):
#     #     return None
#     #
#     # if not init_mc(sync_info, config, logger):
#     #     return None
#     #
#     # """check for info from last run. if there is a run in progress still aborting
#     # if there is no info to be found set the lock and set last_run_time to now - 15minutes
#     # """
#     # job_table = sync_info['job_table']
#     # response = job_table.get_item(Key={'job_id':'sync_job'})
#     # try:
#     #     job = response['Item']
#     #     if job['running']:
#     #         logger.warning("aborting: sync is already in process")
#     #         return None
#     #     last_run = job['run_start']
#     #     job_table.update_item(Key={'job_id':'sync_job'},
#     #                         UpdateExpression='SET running = :val1, run_start = :val2',
#     #                         ExpressionAttributeValues=
#     #                             {':val1': True, ':val2': datetime.datetime.utcnow().__str__()})
#     # except KeyError:
#     #     job_table.put_item(Item={'job_id':'sync_job','running':True,
#     #                                             'run_start': datetime.datetime.utcnow().__str__()})
#     #     last_run = (datetime.datetime.utcnow() - datetime.timedelta(hours=get_int(config['APP_DEFAULT_UPDATE_DELTA_HOURS']))).__str__()
#     #     pass
#     # sync_info['job_table'] = job_table
#     # sync_info['last_run'] = last_run
#     # return sync_info
#
# def init_mc(sync_info,config,logger):
#     logger.debug ("intializing mailchimp connect")
#
#     list_ids = [x.strip() for x in config['MC_LIST_IDS'].split(',')]
#     mc_api_key = config['MC_API_KEY']
#
#     #cc_client = ConstantContactClient(cc_api_key,cc_access_token)
#     passed = False
#     if not list_ids[0]:
#         message = "aborting: MC_LIST_IDS is not configured"
#     elif not mc_api_key:
#         message = "aborting: MC_API_KEY is not configured"
#     #elif not mc_client.health_check(list_ids[0],logger):
#     #    message = "Can not connect to Constant Contact"
#     else:
#         passed = True
#     if not passed:
#         return log_and_return_warning(message,logger)
#     sync_info['mc_list_ids'] = list_ids
#     #sync_info['mc_client'] = mc_client
#
#     logger.debug("constant contact complete")
#     return True
#
# def init_janrain(sync_info, config, logger):
#     logger.debug("intializing janrain")
#
#     """check that janrain info is configured and create janrain objects for sync"""
#     janrain_uri = config['JANRAIN_URI']
#     janrain_client_id = config['JANRAIN_CLIENT_ID']
#     janrain_client_secret = config['JANRAIN_CLIENT_SECRET']
#     passed = False
#
#     if not janrain_uri:
#         message = "aborting: JANRAIN_URI is not configured"
#     elif not janrain_client_id:
#         message = "aborting: JANRAIN_CLIENT_ID is not configured"
#     elif not janrain_client_secret:
#         message = "aborting: JANRAIN_CLIENT_SECRET is not configured"
#     else:
#         passed = True
#     if not passed:
#         return log_and_return_warning(message, logger)
#
#     capture_app = janrain_datalib.get_app(janrain_uri, janrain_client_id, janrain_client_secret)
#     # sync_info['capture_app'] = capture_app
#     # # should I check for existence (default is user)?
#     #
#     # #### need to set the properties for how many users to get at a time
#     # sync_info['capture_schema'] = capture_app.get_schema('user')
#     #
#     #
#     # #### need to setup the mappings
#     # #### 'MC_FIELDS_TO_EXPORT' in config should tell us which fields need to be mapped
#     # #### may have some fields that are always mapped such as email
#     # """we will always sync email so create dictionary if not configured
#     #     all attributes are optional but we will fail if the mapping is configured poorly
#     # """
#     # janrain_attribute_map = eval_mapping(config['JANRAIN_MC_ATTRIBUTE_MAPPING'],
#     #                                      'JANRAIN_MC_ATTRIBUTE_MAPPING', logger)
#     # janrain_attribute_map.pop('email', None)
#     # janrain_attribute_map['email'] = 'email_addresses'
#     # sync_info['janrain_attribute_map'] = janrain_attribute_map
#     #
#     # """grab list of attributes from map for janrain filtering"""
#     # janrain_attributes = []
#     # janrain_attributes += list(janrain_attribute_map.keys())
#     #
#     # ### need to update thse fields for the current app. They are referring to the constant contact
#     # """custom fields are optional but we will fail if the mapping is configured poorly"""
#     # custom_field_map = eval_mapping(config['JANRAIN_MC_CUSTOM_FIELD_MAPPING'],
#     #                                 'JANRAIN_MC_CUSTOM_FIELD_MAPPING', logger)
#     # if custom_field_map:
#     #     janrain_attributes += list(custom_field_map.keys())
#     # sync_info['custom_field_map'] = custom_field_map
#     #
#     # """uuid must be added to list of attributes"""
#     # try:
#     #     janrain_attributes.remove('uuid')
#     # except ValueError:
#     #     pass
#     # janrain_attributes.append('uuid')
#     #
#     # sync_info['janrain_attributes'] = janrain_attributes
#     #
#     # logger.debug("janrain complete")
#     return True



############ Shouldnt need, should be able to just filter out what we need
def json_converter (json_data, config):
    ### possibly need this method to load the users into sqs instead
    """
    This method will get the user data out of the json

    :param json_data: where we will extract the data from
    :param config: we need the config to know which fields to extract
    :return: a list of users along with their related fields
    """
    fields = config['MC_FIELDS_TO_EXPORT']
    raw_data = json.loads(json_data)
    user_list = []

    for user in raw_data['results']:
        ### also need to verify that we check 'list_optin_status'
        to_add = {'email':user['email']}
        # add each additional requested field to the user
        for field in fields:
            to_add[field] = user[field]
        user_list.append(to_add)
    return user_list
############

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
        "body": {
            "email_address": record['email'],
            "status_if_new": "subscribed",
        }

    }

def mailchimp_build_batch(config, records):
    return {
       "operations": [mailchimp_build_batch_operation(config, record) for record in records],
    }



def build_batch( config, logger, records):
    """
    Method to create the json to send to mailchimp

    MailChimp handles batch operations but using json. For example:
    // POST https://.api.mailchimp.com/3.0/batches
    // replace  with your datacenter
    {
      "operations": [
        {
          "method": "PUT",
          "path": "lists/abc123/members/a707d04bf913e1660427c9c8f970518b",
          "body": "{\"email_address\":\"oates@hallandoates.com\", \"status_if_new\":\"subscribed\"}"
        },
        {
          "method": "PUT",
          "path": "lists/abc123/members/817f1571000f0b843c2b8a6982813db2",
          "body": "{\"email_address\":\"hall@hallandoates.com\", \"status_if_new\":\"subscribed\"}"
        },...
      ]
    }
    where abc123 = list ID
    and the string after memeber/ = the MD5 hash of the members email address

    info at: https://devs.mailchimp.com/blog/batch-operations-and-put-in-api-v3-0/

    :param sync_info:
    :param config:
    :param logger:
    :param records: the list of records to convert
    :return: json formated code for the mailchimp put
    """
    output = '{ "operatons": ['
    for record in records:
        hash_name = hashlib.md5(record['email'])



def send_to_mailchimp(config, logger, records):
    """make the post call to mailchimp with the batch, mailchimp will return a batch id which we can use to check
    the status

    mailchimp endpoint: https://<dc>.api.mailchimp.com/3.0/batches

    """
    #conver the records into operations
    batch = mailchimp_build_batch(config, records)
    #make the endpoint
    endpoint = mailchimp_endpoint(config, "/batches")
    print(endpoint)

def mailchimp_endpoint(config, path=None):
    data_center= config['MC_API_KEY'].split('-')[-1]
    base_endpoint = config["MC_URI_TEMPLATE"].format(data_center=data_center)
    if path is None:
        return base_endpoint
    else:
        return urljoin(base_endpoint, path)


def batch_call_status():
    """
    when making a batch call to mailchimp it will return a batch ID. We can use that ID to check the status of our batch request
    https://<dc>.api.mailchimp.com/3.0/batches/<batch_id>
    <dc> is the datacenter
    <batch_id> is the returned id from our original batch call

    info at: http://developer.mailchimp.com/documentation/mailchimp/guides/how-to-use-batch-operations/
    :return:
    """


def fromRecordDateTime(record_field):
    return datetime.strptime(record_field.replace(' +0000', ''), '%Y-%m-%d %H:%M:%S.%f')

def toRecordDateTime(datetime_object):
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S.%f")



def get_int(number):
    try:
        return int(number)
    except ValueError:
        return number