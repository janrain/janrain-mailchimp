# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest.mock import patch
from janrain_mailchimp_connect.config import get_config, ENV_VARS

class getConfigTests(TestCase):

    @patch('os.getenv')
    def test_boolean_false(self, getenv_mock):
        ENV_VARS['BOOL'] = True
        getenv_mock.return_value = 'FALSE'
        config = get_config()
        self.assertIs(config['BOOL'], False)

    @patch('os.getenv')
    def test_boolean_true(self, getenv_mock):
        ENV_VARS['BOOL'] = True
        getenv_mock.return_value = 'T'
        config = get_config()
        self.assertIs(config['BOOL'], True)

    @patch('os.getenv')
    def test_invalid_boolean(self, getenv_mock):
        ENV_VARS['BOOL'] = True
        getenv_mock.return_value = 'X'
        config = get_config()
        self.assertIs(config['BOOL'], True)

    @patch('os.getenv')
    def test_valid_int(self, getenv_mock):
        ENV_VARS['INT'] = 0
        getenv_mock.return_value = '1'
        config = get_config()
        self.assertIs(config['INT'], 1)

    @patch('os.getenv')
    def test_invalid_int(self, getenv_mock):
        ENV_VARS['INT'] = 0
        getenv_mock.return_value = 'a'
        config = get_config()
        self.assertIs(config['INT'], 0)

    @patch('os.getenv')
    def test_invalid_int(self, getenv_mock):
        ENV_VARS['INT'] = 0
        getenv_mock.return_value = 'a'
        config = get_config()
        self.assertEqual(config['INT'], 0)

    @patch('os.getenv')
    def test_valid_dict(self, getenv_mock):
        ENV_VARS['DICT'] = {}
        getenv_mock.return_value = '{"a":1}'
        config = get_config()
        self.assertEqual(config['DICT'], {"a":1})

    @patch('os.getenv')
    def test_invalid_dict(self, getenv_mock):
        ENV_VARS['DICT'] = {}
        getenv_mock.return_value = 'a'
        config = get_config()
        self.assertEqual(config['DICT'], {})
