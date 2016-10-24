import unittest
import json
from collections import namedtuple
from unittest.mock import (
    MagicMock,
    patch,
    sentinel,
    Mock,
    call,
    ANY,
)
from janrain_mailchimp_connect.actions.sync import *
from janrain_mailchimp_connect.actions.sync import _sync

class test_sync(unittest.TestCase):

    @patch('janrain_mailchimp_connect.actions.sync.logging', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.flask')
    def test(self, flask, logging):
        app = Mock()
        flask.current_app = app
        app.config = {
            'LOGGER_NAME': sentinel.logger_name,
        }
        job = Mock()
        app.JobModel.get.return_value = job
        app.executor = Mock()

        self.assertEqual(sync(), "OK")
        logging.getLogger.assert_called_once_with(sentinel.logger_name)
        app.JobModel.get.assert_called_once_with(app.config)
        app.executor.submit.assert_called_once_with(_sync, app.config, logging.getLogger(), job)

class test__sync(unittest.TestCase):

    @patch('janrain_mailchimp_connect.actions.sync.time.sleep', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.send_batch_to_mailchimp', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.is_mailchimp_batch_finished', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.capture_batch_generator', autospec=True, spec_set=True)
    def test(self, capture_batch_generator, is_mailchimp_batch_finished, send_batch_to_mailchimp, sleep):
        job = Mock()
        logger = Mock()
        config = MagicMock()
        capture_batch_generator.return_value = [
            sentinel.capture_batch_1, sentinel.capture_batch_2,
        ]
        is_mailchimp_batch_finished.side_effect = [
            False, True, True,
        ]

        self.assertIsNone(_sync(config, logger, job))
        job.start.assert_called_once_with()
        is_mailchimp_batch_finished.assert_has_calls([
            call(config, logger, send_batch_to_mailchimp(config, logger, sentinel.capture_batch_1)),
            call(config, logger, send_batch_to_mailchimp(config, logger, sentinel.capture_batch_1)),
            call(config, logger, send_batch_to_mailchimp(config, logger, sentinel.capture_batch_2)),
        ])
        sleep.assert_has_calls([
            call(config['MC_TIME_BETWEEN_BATCHES']),
        ])
        job.stop.assert_called_once_with()

class test_capture_batch_generator(unittest.TestCase):

    def setUp(self):
        self.fromRecorpdDateTime = patch('janrain_mailchimp_connect.actions.sync.fromRecordDateTime', autospec=True, spec_set=True).start()
        self.toRecordDateTime = patch('janrain_mailchimp_connect.actions.sync.toRecordDateTime', autospec=True, spec_set=True).start()
        self.janrain_datalib = patch('janrain_mailchimp_connect.actions.sync.janrain_datalib', autospec=True, spec_set=True).start()
        self.exit = patch('janrain_mailchimp_connect.actions.sync.exit', autospec=True, spec_set=True).start()
        self.exit.side_effect = SystemExit
        self.logger = Mock()
        self.job = Mock()
        self.datalib_schema = Mock()
        self.datalib_app = Mock()
        self.datalib_app.get_schema.return_value = self.datalib_schema
        self.janrain_datalib.get_app.return_value = self.datalib_app

    def tearDown(self):
        patch.stopall()

    def test_0_record(self):
        config = {
            'JANRAIN_URI': sentinel.janrain_uri,
            'JANRAIN_CLIENT_ID': sentinel.janrain_client_id,
            'JANRAIN_CLIENT_SECRET': sentinel.janrain_client_secret,
            'JANRAIN_BATCH_SIZE': sentinel.janrain_batch_size,
            'JANRAIN_SCHEMA_NAME': sentinel.janrain_schema_name,
            'JANRAIN_OPT_IN_ATTRIBUTE': sentinel.janrain_opt_in_attribute,
            'JANRAIN_FULL_EXPORT': True,
            'FIELD_MAPPING': {},
        }
        self.datalib_schema.records.iterator.return_value = []
        generator = capture_batch_generator(config, self.logger, self.job)
        self.assertListEqual(list(generator), [])
        self.janrain_datalib.get_app.assert_called_once_with(
            sentinel.janrain_uri,
            sentinel.janrain_client_id,
            sentinel.janrain_client_secret)

    def test_1_record(self):
        config = {
            'JANRAIN_URI': sentinel.janrain_uri,
            'JANRAIN_CLIENT_ID': sentinel.janrain_client_id,
            'JANRAIN_CLIENT_SECRET': sentinel.janrain_client_secret,
            'JANRAIN_BATCH_SIZE': sentinel.janrain_batch_size,
            'JANRAIN_SCHEMA_NAME': sentinel.janrain_schema_name,
            'JANRAIN_OPT_IN_ATTRIBUTE': sentinel.janrain_opt_in_attribute,
            'JANRAIN_FULL_EXPORT': True,
            'FIELD_MAPPING': {},
        }
        self.datalib_schema.records.iterator.return_value = [
            { 'uuid': sentinel.uuid_1, 'lastUpdated': sentinel.lastUpdated_1 },
        ]
        generator = capture_batch_generator(config, self.logger, self.job)
        self.assertListEqual(list(generator), [
            [{ 'uuid': sentinel.uuid_1, 'lastUpdated': sentinel.lastUpdated_1 }]
        ])
        self.janrain_datalib.get_app.assert_called_once_with(
            sentinel.janrain_uri,
            sentinel.janrain_client_id,
            sentinel.janrain_client_secret)

    def test_2_record(self):
        config = {
            'JANRAIN_URI': sentinel.janrain_uri,
            'JANRAIN_CLIENT_ID': sentinel.janrain_client_id,
            'JANRAIN_CLIENT_SECRET': sentinel.janrain_client_secret,
            'JANRAIN_BATCH_SIZE': 1,
            'JANRAIN_SCHEMA_NAME': sentinel.janrain_schema_name,
            'JANRAIN_OPT_IN_ATTRIBUTE': sentinel.janrain_opt_in_attribute,
            'JANRAIN_FULL_EXPORT': True,
            'FIELD_MAPPING': {},
        }
        self.datalib_schema.records.iterator.return_value = [
            { 'uuid': sentinel.uuid_1, 'lastUpdated': sentinel.lastUpdated_1 },
            { 'uuid': sentinel.uuid_2, 'lastUpdated': sentinel.lastUpdated_2 },
        ]
        generator = capture_batch_generator(config, self.logger, self.job)
        self.assertListEqual(list(generator), [
            [{ 'uuid': sentinel.uuid_1, 'lastUpdated': sentinel.lastUpdated_1 }],
            [{ 'uuid': sentinel.uuid_2, 'lastUpdated': sentinel.lastUpdated_2 }]
        ])
        self.janrain_datalib.get_app.assert_called_once_with(
            sentinel.janrain_uri,
            sentinel.janrain_client_id,
            sentinel.janrain_client_secret)

class test_isMailChimpBatchFinished(unittest.TestCase):
    def setUp(self):
        self.requests = patch("janrain_mailchimp_connect.actions.sync.requests", autospec=True).start()
        self.mailchimp_endpoint = patch("janrain_mailchimp_connect.actions.sync.mailchimp_endpoint", autospec=True).start()
        self.logger = Mock()

    def tearDown(self):
        patch.stopall()

    def test_happy_path(self):
        self.mailchimp_endpoint.return_value = sentinel.endpoint
        result = Mock()
        result.json.return_value = {
            'id': sentinel.id,
            'status': 'finished',
            'total_operations': sentinel.total_operations,
            'finished_operations': sentinel.finished_operations,
            'errored_operations': sentinel.errored_operations,
        }
        self.requests.get.return_value = result
        config = MagicMock()
        batch = MagicMock()

        actual = is_mailchimp_batch_finished(config, self.logger, batch)

        self.assertTrue(actual)
        self.mailchimp_endpoint.assert_called_once_with(config, "/batches/{}".format(batch.get()))
        batch.get.assert_has_calls([call('id')])


class test_mailchimp_build_batch_operation(unittest.TestCase):

    @patch('janrain_mailchimp_connect.actions.sync.hashlib.md5', autospec=True, spec_set=True)
    @patch('janrain_mailchimp_connect.actions.sync.json.dumps', autospec=True, spec_set=True)
    def test_no_merge_fields(self, json_dumps, md5):
        config = {
            'MC_LIST_ID': sentinel.mc_list_id,
            'JANRAIN_OPT_IN_ATTRIBUTE': sentinel.janrain_opt_in_attribute,
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
            'JANRAIN_OPT_IN_ATTRIBUTE': sentinel.janrain_opt_in_attribute,
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

    @patch('janrain_mailchimp_connect.actions.sync.mailchimp_build_batch_operation', autospec=True, spec_set=True)
    def test_email_is_none(self, mailchimp_build_batch_operation):
        records = [
            {'email': None},
        ]
        expected = {
            "operations": [
            ]
        }
        actual = mailchimp_build_batch(sentinel.config, records)
        self.assertEqual(actual, expected)

class test_mailchimp_endpoint(unittest.TestCase):

    def test_happy_path_is_none(self):
        config = {
            'MC_API_KEY': '',
            'MC_URI_TEMPLATE': '{data_center}'
        }
        expected = ''
        actual = mailchimp_endpoint(config, None)
        self.assertEqual(actual, expected)

    @patch("janrain_mailchimp_connect.actions.sync.urljoin")
    def test_happy_path_is_not_none(self, urljoin):
        path = "abc"
        config = {
            'MC_API_KEY': '',
            'MC_URI_TEMPLATE': '{data_center}'
        }
        expected = urljoin('', path)
        actual = mailchimp_endpoint(config, path)
        self.assertEqual(actual, expected)

    @patch("janrain_mailchimp_connect.actions.sync.urljoin")
    def test_happy_path_with_slashes(self, urljoin):
        path = "//abc"
        config = {
            'MC_API_KEY': '',
            'MC_URI_TEMPLATE': '{data_center}'
        }
        expected = urljoin('', path.lstrip('/'))
        actual = mailchimp_endpoint(config, path)
        self.assertEqual(actual, expected)

    def test_error_invalid_template(self):
        config = {
            'MC_API_KEY': '',
            'MC_URI_TEMPLATE': ''
        }
        expected = ''
        actual = mailchimp_endpoint(config, None)
        self.assertEqual(actual, expected)

class test_send_batch_to_mailchimp(unittest.TestCase):

    def setUp(self):
        self.mailchimp_build_batch = patch('janrain_mailchimp_connect.actions.sync.mailchimp_build_batch', autospec=True, spec_set=True).start()
        self.mailchimp_endpoint = patch('janrain_mailchimp_connect.actions.sync.mailchimp_endpoint', autospec=True, spec_set=True).start()
        self.requests = patch('janrain_mailchimp_connect.actions.sync.requests', autospec=True, spec_set=True).start()
        self.exit = patch('janrain_mailchimp_connect.actions.sync.exit', autospec=True, spec_set=True).start()
        self.exit.side_effect = SystemExit
        self.logger = Mock()

    def tearDown(self):
        patch.stopall()

    def test_None_records(self):
        config = {
            'MC_MAX_RECORDS_IN_BATCH': 1000,
            'MC_MAX_BYTES_IN_BATCH': 1000,
            'MC_API_KEY': sentinel.mc_api_key,
        }
        records = None
        with self.assertRaises(TypeError):
            send_batch_to_mailchimp(config, self.logger, records)

    def test_no_records(self):
        config = {
            'MC_MAX_RECORDS_IN_BATCH': 1000,
            'MC_MAX_BYTES_IN_BATCH': 1000,
            'MC_API_KEY': sentinel.mc_api_key,
        }
        records = []
        self.assertEqual(
            send_batch_to_mailchimp(config, self.logger, records),
            self.requests.post(self.mailchimp_endpoint(config, "batches")).json()
        )

    def test_number_of_records_assert(self):
        config = {
            'MC_MAX_RECORDS_IN_BATCH': 0,
            'MC_MAX_BYTES_IN_BATCH': 1000,
            'MC_API_KEY': sentinel.mc_api_key,
        }
        records = [{}]
        self.mailchimp_build_batch.return_value = [sentinel.record_1]
        with self.assertRaises(SystemExit):
            send_batch_to_mailchimp(config, self.logger, records)

    def test_number_of_bytes_assert(self):
        config = {
            'MC_MAX_RECORDS_IN_BATCH': 1000,
            'MC_MAX_BYTES_IN_BATCH': 0,
            'MC_API_KEY': sentinel.mc_api_key,
        }
        records = [{}]
        self.mailchimp_build_batch.return_value = [sentinel.record_1]
        with self.assertRaises(SystemExit):
            send_batch_to_mailchimp(config, self.logger, records)

class test_exit(unittest.TestCase):

    def test(self):
        logger = Mock()
        with self.assertRaises(SystemExit):
            exit(logger, sentinel.message)
        logger.error.assert_called_with(sentinel.message)
