import os

from .data_types import (CONFIG_TYPES, CONFIG_TYPES_STR, DataTypeException,
                         convert)
from .default_value import DefaultValue
from .validation_key import ValidationKey


class ConfigType:

    __slots__ = ['_env_name', '_type', '_default', '_value', '_validation']

    def __init__(self, env_name: str, type=str,
                 default=None, validation: callable = None):
        """
        Config Type

        :param env_name: Environment var name
        :param type: type for parsing
        :param default: default value
        :param validation: validation method or enumerable
        """
        if not isinstance(env_name, str) or not env_name:
            raise ConfigTypeException(
                "Invalid env_name. Must be an non-empty string")
        self._env_name = env_name
        if type not in CONFIG_TYPES.keys():
            raise ConfigTypeException(
                "Invalid type {0} for env_name {1}. Expected: {2}".format(
                    type,
                    env_name,
                    list(CONFIG_TYPES.keys())
                ))

        self._type = type
        self._default = DefaultValue(default)
        if self._default.value is not None and \
                not isinstance(self._default.value, type):
            raise ConfigTypeException(
                'Invalid default type {0} for env_name {1}. Expected = {2}'
                .format(
                    self._default.value,
                    env_name,
                    self._type))

        self._validation = ValidationKey(validation)
        if not self._validation.is_valid(self._default.value):
            raise ConfigTypeException(
                'Default value can´t be validated: {0}'.format(default))
        self._default = default

        self._value = default

    @classmethod
    def from_attribute(cls, env_name: str, attribute):
        if isinstance(attribute, cls):
            return attribute

        if isinstance(attribute, str) or attribute is None:
            return cls(env_name, str, attribute)

        return cls(env_name, type(attribute), attribute)

    @property
    def value(self):
        return self._value

    def is_valid(self, value) -> bool:
        return self._validation.is_valid(value)

    @property
    def default_value(self):
        return self._default

    def load(self):
        value = os.getenv(self._env_name, self._default)
        try:
            value = convert(value, self._type, self._default, self._env_name)
            if not self._validation.is_valid(value):
                raise DataTypeException()
        except DataTypeException:
            value = self._default

        return value

    def __str__(self):
        return "({0}) : {1}".format(
            CONFIG_TYPES_STR.get(self._type, 'str'),
            "VALIDATION"
        )


class ConfigTypeException(Exception):
    pass
