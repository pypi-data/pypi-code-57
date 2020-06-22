import os
import unittest

from gs_config.config_type import ConfigType, ConfigTypeException


class TestConfigType(unittest.TestCase):

    def setUp(self):
        os.environ.clear()

    def test_empty_env(self):
        with self.assertRaises(ConfigTypeException):
            ConfigType('')

    def test_invalid_type(self):
        with self.assertRaises(ConfigTypeException):
            ConfigType('STRING_ENV', tuple)

    def test_config_type(self):
        test_case = ConfigType('STRING_ENV', default='TEST')
        self.assertEqual(test_case.value, 'TEST')

    def test_invalid_default_value(self):
        with self.assertRaises(ConfigTypeException):
            ConfigType("STRING_ENV", str, 0)

        with self.assertRaises(ConfigTypeException):
            ConfigType("STRING_ENV", str, "abcd", lambda x: len(x) == 0)

    def test_value(self):
        os.environ.update({"STRING_ENV": "TEST"})
        test_case = ConfigType("STRING_ENV", str, "test", lambda x: bool(x))
        self.assertTrue(test_case.is_valid('abcd'))
        self.assertEqual(test_case.default_value, 'test')
        self.assertIsInstance(str(test_case), str)
