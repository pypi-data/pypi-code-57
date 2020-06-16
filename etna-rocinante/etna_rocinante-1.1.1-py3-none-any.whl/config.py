"""
Module providing helpers to load configuration files
"""

import json
from typing import Any, Dict


class ConfigurationLoadError(BaseException):
    """
    Class representing an error related to configuration loading
    """

    def __init__(self, cause):
        self.__cause__ = cause

    def __str__(self):
        return f"cannot load configuration: {self.__cause__}"


def load_config(path: str) -> Dict[str, Any]:
    """
    Load a configuration from a given file

    :param path:            the path to the file to load
    :return:                the loaded configuration, as a dictionary
    """

    try:
        with open(path, 'r') as config_file:
            config = json.load(config_file)
    except (OSError, IOError) as e:
        raise ConfigurationLoadError(e)
    return config
