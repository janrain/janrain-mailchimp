import unittest
from unittest.mock import MagicMock
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