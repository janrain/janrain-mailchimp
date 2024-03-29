import logging
from janrain_mailchimp_connect import models
from unittest import TestCase
from unittest.mock import patch, sentinel, Mock, MagicMock, call, ANY
from janrain_mailchimp_connect.__init__ import create_app, logging_init

class init_test(TestCase):

    def setUp(self):
        self.Flask = patch("janrain_mailchimp_connect.__init__.flask.Flask", autospec=True).start()
        self.sync = patch("janrain_mailchimp_connect.__init__.sync", autospec=True).start()
        self.app = MagicMock()
        self.Flask.return_value = self.app
        self.JobModel = MagicMock(spec=models.JobModel)

    def tearDown(self):
        patch.stopall()

    def test_create_app(self):
        # setup
        # call
        result = create_app(sentinel.config, self.JobModel, sentinel.executor)
        # test
        self.assertEqual(result, self.app)
        self.app.config.update.assert_called_with(sentinel.config)
        self.app.add_url_rule.assert_has_calls([
            call('/', 'root', ANY),
            call('/sync', 'sync', self.sync, methods=['POST'])
        ])

    def test_create_app_2(self):
        # setip
        self.app.config.__getitem__.return_value = True
        self.JobModel.exists.return_value = False
        # call
        result = create_app(sentinel.config, self.JobModel, sentinel.executor)
        # test
        print(self.JobModel.create_table)
        self.JobModel.create_table.assert_called_once_with(
            read_capacity_units=1,
            write_capacity_units=1,
        )

class logging_init_test(TestCase):

    def setUp(self):

        self.app = Mock()
        self.app.config = {
            'APP_LOG_FILE': 'test_app_log_file.log',
            'APP_LOG_NUM_BACKUPS': 'test_app_log_backups',
            'APP_LOG_FILESIZE': 1000,
            'LOGGER_NAME': 'test_logger_name',
        }

    def test_production(self):

        self.app.debug = False
        logger = logging_init(self.app)
        self.assertEqual(logger.handlers[1].level, logging.INFO)

    def test_debug(self):

        self.app.debug = True
        logger = logging_init(self.app)
        self.assertEqual(logger.handlers[0].level, logging.DEBUG)
