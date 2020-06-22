import unittest
from datetime import date, datetime

from gs_config.data_types import convert


class TestDataTypes(unittest.TestCase):

    def test_str(self):
        value = convert(None, str, '', 'Test STR')
        self.assertIsInstance(value, str)

    def test_int(self):
        value = convert('1', int, 1, 'Test INT')
        self.assertIsInstance(value, int)

    def test_float(self):
        value = convert('1', float, 1.0, 'Test FLOAT')
        self.assertIsInstance(value, float)

    def test_bool(self):
        value = convert('1', bool, True, 'Test BOOL')
        self.assertEqual(value, True)

    def test_datetime(self):
        value = convert('2020-06-22 10:10:10', datetime,
                        datetime.now(), 'Test DATETIME')
        self.assertEqual(value, datetime(2020, 6, 22, 10, 10, 10))

    def test_date(self):
        value = convert('2020-06-22', date, date.today(), 'Test DATE')
        self.assertEqual(value, date(2020, 6, 22))

    def test_invalid_default(self):
        value = convert('', str, 0, 'Test INVALID STR')
        self.assertEqual(value, '')

    def test_invalid_data_type(self):
        value = convert('test', None, 0, 'Test INVALID NONE')
        self.assertEqual(value, 0)
