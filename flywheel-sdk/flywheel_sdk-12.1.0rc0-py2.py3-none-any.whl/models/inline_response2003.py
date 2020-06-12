# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 12.1.0-rc.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class InlineResponse2003(object):

    swagger_types = {
        'id': 'str',
        'role_ids': 'list[str]',
        'access': 'str'
    }

    attribute_map = {
        'id': '_id',
        'role_ids': 'role_ids',
        'access': 'access'
    }

    rattribute_map = {
        '_id': 'id',
        'role_ids': 'role_ids',
        'access': 'access'
    }

    def __init__(self, id=None, role_ids=None, access=None):  # noqa: E501
        """InlineResponse2003 - a model defined in Swagger"""
        super(InlineResponse2003, self).__init__()

        self._id = None
        self._role_ids = None
        self._access = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if role_ids is not None:
            self.role_ids = role_ids
        if access is not None:
            self.access = access

    @property
    def id(self):
        """Gets the id of this InlineResponse2003.

        Database ID of a user

        :return: The id of this InlineResponse2003.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse2003.

        Database ID of a user

        :param id: The id of this InlineResponse2003.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def role_ids(self):
        """Gets the role_ids of this InlineResponse2003.


        :return: The role_ids of this InlineResponse2003.
        :rtype: list[str]
        """
        return self._role_ids

    @role_ids.setter
    def role_ids(self, role_ids):
        """Sets the role_ids of this InlineResponse2003.


        :param role_ids: The role_ids of this InlineResponse2003.  # noqa: E501
        :type: list[str]
        """

        self._role_ids = role_ids

    @property
    def access(self):
        """Gets the access of this InlineResponse2003.


        :return: The access of this InlineResponse2003.
        :rtype: str
        """
        return self._access

    @access.setter
    def access(self, access):
        """Sets the access of this InlineResponse2003.


        :param access: The access of this InlineResponse2003.  # noqa: E501
        :type: str
        """

        self._access = access


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InlineResponse2003):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result
