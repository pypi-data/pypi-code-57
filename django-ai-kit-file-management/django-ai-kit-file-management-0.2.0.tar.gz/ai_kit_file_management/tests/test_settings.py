from unittest import TestCase

# from unittest.mock import patch

from ..settings import (
    APISettings,
    UnknownConfigurationError,
    InvalidConfigurationError,
)


class APISettingsTests(TestCase):
    def test_raises_if_unknown_setting(self):
        user_settings = {"NOT_A_KEY_IN_DEFAULT": "value"}
        with self.assertRaises(UnknownConfigurationError):
            APISettings(user_settings)

    def test_raises_if_improper_setting(self):
        user_settings = {"MAX_FILE_SIZE_KB": "100000"}
        with self.assertRaises(InvalidConfigurationError):
            APISettings(user_settings)

    def test_values_are_overridden(self):
        user_settings = {"MAX_FILE_SIZE_KB": 42}
        api_settings = APISettings(user_settings)
        self.assertEqual(
            user_settings["MAX_FILE_SIZE_KB"], api_settings.MAX_FILE_SIZE_KB
        )
