import collections
import collections.abc
from typing import Union, TextIO

import yaml


def _update_dict(base_dict, keys_to_update):
    for key, value in keys_to_update.items():
        if isinstance(value, collections.abc.Mapping):
            base_dict[key] = _update_dict(base_dict.get(key, {}), value)
        else:
            base_dict[key] = value
    return base_dict


def _read_config_file(stream: Union[TextIO, dict]):
    if isinstance(stream, dict):
        return stream

    try:
        content = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        raise ValueError('Problem reading the yaml file. Error: \n' + str(e)) from None

    return content


def read_config(default: Union[TextIO, dict], custom: Union[TextIO, dict, None] = None) -> dict:
    """
    Reads the configuration stored in a default yaml file, overriding the fields with the ones defined in another
    custom file. The objects passed can be any object accepted by yaml.safe_load or a dict.

    Args:
        default: stream or dict with the the default configuration.
        custom: stream or dict used to override configurations from default

    Returns:
        config_dict: dict with the combined information from default_file and custom_file
    """

    config_dict = _read_config_file(default)

    if custom is not None:
        custom_config = _read_config_file(custom)
        _update_dict(config_dict, custom_config)

    return config_dict


class Config:
    """ Store configurations.
    The configurations are stored as data members, and can be read/written to yaml files.
    The method parse is particularly handy if you store a file with the default configuration and changes it to a custom
    value depending on another file.
    """
    def __init__(self, **options):
        """
        Build the configuration from the kwargs. Nested configurations are supported, and in case a dict of dict is
        passed, the 'child' configuration objects will also be built.
        Args:
            **options: the configuration options. They will be accessible as data members.
        """
        for key, value in options.items():
            if isinstance(value, dict):
                self.__dict__[key] = Config(**value)
            else:
                self.__dict__[key] = value

    @classmethod
    def parse(cls, default: Union[dict, TextIO], custom: Union[dict, TextIO, None] = None):
        """"Build the configuration from a default, overriding with the options from custom.
        Args:
            default: dict or yaml (file-like) with the default configuration
            custom: dict or yaml (file-like) with the custom configuration
        """
        return cls(**read_config(default, custom))

    def __repr__(self):
        return ''.join([' <' + str(k) + ':' + repr(v) + '>' for (k, v) in self.__dict__.items()])

    def to_dict(self) -> dict:
        """
        Export to a dict. Nested configs are exported as dicts as well.
        Returns:
            dict_config: dict with the configuration
        """
        dict_config = dict()
        for key, value in self.__dict__.items():
            if not isinstance(value, Config):
                dict_config[key] = value
            else:
                dict_config[key] = value.to_dict()

        return dict_config

