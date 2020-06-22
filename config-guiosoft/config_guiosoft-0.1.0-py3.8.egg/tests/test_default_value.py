import unittest

from gs_config.default_value import DefaultValue, DefaultValueException


class TestDefaultValue(unittest.TestCase):

    def test_default_value(self):
        test_case = DefaultValue('abcd')
        self.assertEqual(test_case.value, 'abcd')

    def test_callable_default_value(self):
        test_case = DefaultValue(lambda: 'default_value')
        self.assertEqual(test_case.value, 'default_value')

    def test_invalid_callable(self):
        with self.assertRaises(DefaultValueException):
            DefaultValue(lambda x: x*1)
