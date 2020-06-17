"""
This module deals with the configuration file in YAML format
"""
import copy
import os
import re

import yaml
from collections import abc
from typing import Any, Iterable, Mapping, Union


class DataObject:
    def __repr__(self):
        return str({k: v for k, v in vars(self).items()})

    def __getitem__(self, item):
        """
        Overload on [] operator
        Args:
            item (str): parameter name
        Returns:
            object: whatever the parameter is holding
        Raises:
            AttributeError: if the item does not exist
        """
        if hasattr(self, item):
            return getattr(self, item)
        raise AttributeError("No attribute named {} found".format(item))


def data_to_object(data: Union[Mapping[str, Any], Iterable]) -> object:
    """
    Gets a generic list/dict type and transtaforms into a object
    Returns:
        object: the converted object
    """
    if isinstance(data, abc.Mapping):
        r = DataObject()
        for k, v in data.items():
            if type(v) is dict or type(v) is list:
                setattr(r, k, data_to_object(v))
            else:
                setattr(r, k, v)
        return r
    elif isinstance(data, abc.Iterable):
        return [data_to_object(e) for e in data]
    else:
        return data


class Config(object):
    """
    Class to deal with config files. You can access the parameters using the method get or with brackets
    """
    def __init__(self, filepath="config.yaml"):
        self.filepath = filepath
        if os.path.exists(filepath):
            with open(filepath, "r") as stream:
                self.__merge_object(data_to_object(yaml.safe_load(stream)))
        else:
            raise IOError("Config file not found on path " + filepath)

    def get(self, param_name):
        """
        Gets the parameter on config. Returns none if not found
        Args:
            param_name (str): Desired parameter
        Returns:
            object: Value if found
        Raises:
            AttributeError: if parameter not found
        """
        if hasattr(self, param_name):
            return getattr(self, param_name)
        raise AttributeError("Parameter {} does not exist".format(param_name))

    def set(self, param_name, param_value):
        """
        Sets a value for the configuration. Creates it if does not exist
        Args:
            param_name (str): Parameter name
            param_value (object): Parameter value
        """
        setattr(self, param_name, param_value)

    def save(self, filepath=None):
        """
        Saves the current configuration values to the file
        """
        if not filepath:
            filepath = self.filepath
        with open(filepath, "w") as stream:
            dic = copy.deepcopy(self.__dict__)
            del dic["filepath"]
            yaml_str = "\n".join([re.sub(r" ?!!python/.*$", "", l) for l in yaml.dump(dic).splitlines()])
            stream.write(yaml_str)

    def __getitem__(self, item):
        """
        Overload on [] operator
        Args:
            item (str): parameter name
        Returns:
            object: whatever the parameter is holding
        Raises:
            AttributeError: If item does not exist
        """
        if hasattr(self, item):
            return getattr(self, item)
        raise AttributeError("Parameter {} does not exist".format(item))

    def __setitem__(self, key, value):
        """
        Overloads the []  operator for set operation
        Args:
            key (str): param name
            value (object): param value
        """
        setattr(self, key, value)

    def __merge_object(self, obj):
        """
        Used to copy properties from one object to another if there isn't a naming conflict;
        Args:
            obj (object): object to be merged
        """
        for item in obj.__dict__:
            # Check to make sure it can't be called... ie a method.
            # Also make sure the self doesn't have a property of the same name.
            if not callable(obj.__dict__[item]) and not hasattr(self, item):
                setattr(self, item, getattr(obj, item))
