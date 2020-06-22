import os
import re

from yaml import load, Loader

_instance = None


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class RuntimeConfiguration(Singleton):
    """
    Runtime configuration helper
    """
    KEY_SEPARATOR_LIST = ['\.', '\:', '\/']

    def __init__(self, config_path=None):
        self._key_separator_pattern = r'|'.join(self.KEY_SEPARATOR_LIST)
        if not hasattr(self, '_configuration'):
            self._configuration = self._read_configuration(config_path)

    @property
    def configuration(self):
        """
        Configuration property
        :return: 
        :rtype: dict
        """
        return self._configuration

    def _read_configuration(self, config_path):
        """Read configuration from file if exists or use default"""
        if config_path and os.path.isfile(config_path) and os.access(config_path, os.R_OK):
            with open(config_path, 'r') as config:
                return load(config, Loader=Loader)

    def read_key(self, complex_key, default_value=None):
        """
        Value for complex key like CLI.PORTS
        :param complex_key:
        :param default_value: Default value
        :return:
        """
        value = self.configuration
        for key in re.split(self._key_separator_pattern, complex_key):
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default_value

        return value if value is not None else default_value
