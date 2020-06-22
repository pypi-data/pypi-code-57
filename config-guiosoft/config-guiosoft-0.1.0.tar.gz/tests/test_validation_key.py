import unittest
from gs_config.validation_key import ValidationKey, ValidationKeyException


class TestValidationKey(unittest.TestCase):

    def test_none(self):
        test_case = ValidationKey()
        self.assertTrue(test_case.is_valid(None))

    def test_callable(self):
        test_case = ValidationKey(lambda v: bool(v))
        self.assertTrue(test_case.is_valid('A'))
        self.assertFalse(test_case.is_valid(0))

    def test_invalid_callable(self):
        with self.assertRaises(ValidationKeyException):
            ValidationKey(lambda: True)

    def test_enumerable(self):
        test_case = ValidationKey([1, 2, 3])
        self.assertTrue(test_case.is_valid(1))
        self.assertFalse(test_case.is_valid(5))

        test_case = ValidationKey({'a': 1, 'b': 2, 'c': 3})
        self.assertTrue(test_case.is_valid('b'))
        self.assertFalse(test_case.is_valid('d'))

        test_case = ValidationKey({'a', 'b', 'c'})
        self.assertTrue(test_case.is_valid('b'))
        self.assertFalse(test_case.is_valid('d'))

        test_case = ValidationKey(range(4))
        self.assertTrue(test_case.is_valid(1))
        self.assertFalse(test_case.is_valid(5))

    def test_invalid_validation(self):
        with self.assertRaises(ValidationKeyException):
            ValidationKey('a')
