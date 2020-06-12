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

from flywheel.models.report_access_log_origin import ReportAccessLogOrigin  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class AuthLoginStatus(object):

    swagger_types = {
        'origin': 'ReportAccessLogOrigin',
        'user_is_admin': 'bool',
        'is_device': 'bool',
        'roles': 'list[str]'
    }

    attribute_map = {
        'origin': 'origin',
        'user_is_admin': 'user_is_admin',
        'is_device': 'is_device',
        'roles': 'roles'
    }

    rattribute_map = {
        'origin': 'origin',
        'user_is_admin': 'user_is_admin',
        'is_device': 'is_device',
        'roles': 'roles'
    }

    def __init__(self, origin=None, user_is_admin=None, is_device=None, roles=None):  # noqa: E501
        """AuthLoginStatus - a model defined in Swagger"""
        super(AuthLoginStatus, self).__init__()

        self._origin = None
        self._user_is_admin = None
        self._is_device = None
        self._roles = None
        self.discriminator = None
        self.alt_discriminator = None

        self.origin = origin
        self.user_is_admin = user_is_admin
        self.is_device = is_device
        if roles is not None:
            self.roles = roles

    @property
    def origin(self):
        """Gets the origin of this AuthLoginStatus.


        :return: The origin of this AuthLoginStatus.
        :rtype: ReportAccessLogOrigin
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this AuthLoginStatus.


        :param origin: The origin of this AuthLoginStatus.  # noqa: E501
        :type: ReportAccessLogOrigin
        """

        self._origin = origin

    @property
    def user_is_admin(self):
        """Gets the user_is_admin of this AuthLoginStatus.

        Whether or not the user has admin privileges

        :return: The user_is_admin of this AuthLoginStatus.
        :rtype: bool
        """
        return self._user_is_admin

    @user_is_admin.setter
    def user_is_admin(self, user_is_admin):
        """Sets the user_is_admin of this AuthLoginStatus.

        Whether or not the user has admin privileges

        :param user_is_admin: The user_is_admin of this AuthLoginStatus.  # noqa: E501
        :type: bool
        """

        self._user_is_admin = user_is_admin

    @property
    def is_device(self):
        """Gets the is_device of this AuthLoginStatus.

        Whether or not the credentials identified a device

        :return: The is_device of this AuthLoginStatus.
        :rtype: bool
        """
        return self._is_device

    @is_device.setter
    def is_device(self, is_device):
        """Sets the is_device of this AuthLoginStatus.

        Whether or not the credentials identified a device

        :param is_device: The is_device of this AuthLoginStatus.  # noqa: E501
        :type: bool
        """

        self._is_device = is_device

    @property
    def roles(self):
        """Gets the roles of this AuthLoginStatus.


        :return: The roles of this AuthLoginStatus.
        :rtype: list[str]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this AuthLoginStatus.


        :param roles: The roles of this AuthLoginStatus.  # noqa: E501
        :type: list[str]
        """

        self._roles = roles


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
        if not isinstance(other, AuthLoginStatus):
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
