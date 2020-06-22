import os
import unittest
from datetime import date, datetime

from tests.mocks.config_mock import ConfigMock, SpecialConfigMock


class TestConfig(unittest.TestCase):

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def setUp(self):
        os.environ.clear()
        os.environ.update({
            'STRING_CONF': 'TESTING',
            'INT_CONF': '5',
            'FLOAT_CONF': '3.14',
            'BOOL_CONF': 'True',
            'DEFAULT_CONF': 'ANYTHING',
            'DATE': '2020-06-22',
            'DATETIME': '2020-06-22 10:10:10'
        })

    def test_simple_default_values(self):
        d = datetime.now()
        test_case = ConfigMock(auto_load=False)
        self.assertIsInstance(test_case, ConfigMock)
        self.assertEqual(test_case.STRING_CONF, '')
        self.assertEqual(test_case.INT_CONF, 0)
        self.assertEqual(test_case.FLOAT_CONF, 0.0)
        self.assertEqual(test_case.BOOL_CONF, False)
        self.assertEqual(test_case.DEFAULT_CONF, None)
        self.assertEqual(test_case.DATE, date.today())
        self.assertEqual(test_case.DATETIME.strftime(self.DATE_FORMAT),
                         d.strftime(self.DATE_FORMAT))

    def test_init(self):
        test_case = ConfigMock()
        self.assertIsInstance(test_case, ConfigMock)

        self.assertIsInstance(test_case.to_dict(), dict)
        self.assertIsInstance(test_case.description_dict(), dict)
        self.assertEqual(test_case.STRING_CONF, 'TESTING')
        self.assertEqual(test_case.INT_CONF, 5)
        self.assertEqual(test_case.FLOAT_CONF, 3.14)
        self.assertEqual(test_case.BOOL_CONF, True)
        self.assertEqual(test_case.DEFAULT_CONF, 'ANYTHING')
        self.assertEqual(test_case.DATE, date(2020, 6, 22))
        self.assertEqual(test_case.DATETIME, datetime(2020, 6, 22, 10, 10, 10))

    def test_special_default_vallues(self):
        test_case = SpecialConfigMock(auto_load=False)
        self.assertIsInstance(test_case, SpecialConfigMock)
        self.assertEqual(test_case.STRING_CONF, 'DEFAULT_STRING')
        self.assertEqual(test_case.INT_CONF, 100)
        self.assertEqual(test_case.FLOAT_CONF, 0.5)
        self.assertEqual(test_case.BOOL_CONF, False)
        self.assertEqual(test_case.DEFAULT_CONF, None)
        self.assertEqual(test_case.DATE, date.today())
        self.assertEqual(test_case.DATETIME.strftime(self.DATE_FORMAT),
                         datetime.now().strftime(self.DATE_FORMAT))

    def test_special(self):
        test_case = SpecialConfigMock(auto_load=True)
        self.assertIsInstance(test_case, SpecialConfigMock)
        self.assertEqual(test_case.STRING_CONF, 'TESTING')
        self.assertEqual(test_case.INT_CONF, 5)
        self.assertEqual(test_case.FLOAT_CONF, 3.14)
        self.assertEqual(test_case.BOOL_CONF, True)
        self.assertEqual(test_case.DEFAULT_CONF, 'ANYTHING')
        self.assertEqual(test_case.DATE, date(2020, 6, 22))
        self.assertEqual(test_case.DATETIME, datetime(2020, 6, 22, 10, 10, 10))
