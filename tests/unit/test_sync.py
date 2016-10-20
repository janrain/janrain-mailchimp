import unittest
from unittest.mock import (
    MagicMock,
    patch,
    sentinel,
)
from janrain_mailchimp_connect.actions.sync import *

class TestMyMethods(unittest.TestCase) :

    def test_load_records(self):
        #setuo
        logger = MagicMock()
        logger.info = MagicMock()
        sync_info = {'last_run': 'a_time',
                     'janrain_attributes':[],
                     'capture_schema':"put something here",
                     'queue':"put something here",
                     }
        config = {'MC_FIELDS_TO_EXPORT':['familyName', 'givenName'],
                  'JANRAIN_BATCH_SIZE':'100',
                  }
        #call
        result = capture_batch_generator(sync_info, config, logger)
        #test

class test_mailchimp_build_batch_operation(unittest.TestCase):

    @patch('janrain_mailchimp_connect.actions.sync.hashlib.md5', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.json.dumps', autospec=True, spec_set=True)
    def test_no_merge_fields(self, json_dumps, md5):
        config = {
            'MC_LIST_ID': sentinel.mc_list_id,
            'FIELD_MAPPING': {},
        }
        record = {
            'email': 'abc@example.com',
        }
        expected = {
            'method': 'PUT',
            'path': 'lists/{}/members/{}'.format(config['MC_LIST_ID'], md5(record['email']).hexdigest()),
            'body': json_dumps({
                'email_address': record['email'],
                'status_if_new': 'subscribed',
                'merge_fields': {}
            })
        }
        actual = mailchimp_build_batch_operation(config, record)
        self.assertEqual(expected, actual)

    @patch('janrain_mailchimp_connect.actions.sync.hashlib.md5', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.json.dumps', autospec=True, spec_set=True)
    def test_with_merge_fields(self, json_dumps, md5):
        config = {
            'MC_LIST_ID': sentinel.mc_list_id,
            'FIELD_MAPPING': {
                'janrain_a': 'mc_a',
                'janrain_b': 'mc_b',
            },
        }
        record = {
            'email': 'abc@example.com',
            'janrain_a': sentinel.janrain_a,
            'janrain_b': sentinel.janrain_b,
        }
        expected = {
            'method': 'PUT',
            'path': 'lists/{}/members/{}'.format(config['MC_LIST_ID'], md5(record['email']).hexdigest()),
            'body': json_dumps({
                'email_address': record['email'],
                'status_if_new': 'subscribed',
                'merge_fields': {
                    'mc_a': sentinel.janrain_a,
                    'mc_b': sentinel.janrain_b,
                }
            })
        }
        actual = mailchimp_build_batch_operation(config, record)
        self.assertEqual(expected, actual)

class test_mailchimp_build_batch(unittest.TestCase):

    @patch('janrain_mailchimp_connect.actions.sync.mailchimp_build_batch_operation', autospec=True, spec_set=True)
    def test_happy(self, mailchimp_build_batch_operation):
        records = [
            { 'email': sentinel.email_1 },
        ]
        expected = {
            "operations": [
                mailchimp_build_batch_operation(sentinel.config, { 'email': sentinel.email_1 }),
            ]
        }
        actual = mailchimp_build_batch(sentinel.config, records)
        self.assertEqual(actual, expected)

    @patch('janrain_mailchimp_connect.actions.sync.mailchimp_build_batch_operation', autospec=True, spec_set=True)
    def test_no_email(self, mailchimp_build_batch_operation):
        records = [
            {},
        ]
        expected = {
            "operations": [
            ]
        }
        actual = mailchimp_build_batch(sentinel.config, records)
        self.assertEqual(actual, expected)
