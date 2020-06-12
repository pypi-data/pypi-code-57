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

from flywheel.models.job_ask_return import JobAskReturn  # noqa: F401,E501
from flywheel.models.job_config_inputs import JobConfigInputs  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class JobAsk(object):

    swagger_types = {
        'whitelist': 'JobConfigInputs',
        'blacklist': 'JobConfigInputs',
        'capabilities': 'list[str]',
        '_return': 'JobAskReturn'
    }

    attribute_map = {
        'whitelist': 'whitelist',
        'blacklist': 'blacklist',
        'capabilities': 'capabilities',
        '_return': 'return'
    }

    rattribute_map = {
        'whitelist': 'whitelist',
        'blacklist': 'blacklist',
        'capabilities': 'capabilities',
        'return': '_return'
    }

    def __init__(self, whitelist=None, blacklist=None, capabilities=None, _return=None):  # noqa: E501
        """JobAsk - a model defined in Swagger"""
        super(JobAsk, self).__init__()

        self._whitelist = None
        self._blacklist = None
        self._capabilities = None
        self.__return = None
        self.discriminator = None
        self.alt_discriminator = None

        self.whitelist = whitelist
        self.blacklist = blacklist
        self.capabilities = capabilities
        self._return = _return

    @property
    def whitelist(self):
        """Gets the whitelist of this JobAsk.

        Properties that must match against jobs

        :return: The whitelist of this JobAsk.
        :rtype: JobConfigInputs
        """
        return self._whitelist

    @whitelist.setter
    def whitelist(self, whitelist):
        """Sets the whitelist of this JobAsk.

        Properties that must match against jobs

        :param whitelist: The whitelist of this JobAsk.  # noqa: E501
        :type: JobConfigInputs
        """

        self._whitelist = whitelist

    @property
    def blacklist(self):
        """Gets the blacklist of this JobAsk.

        Properties that must NOT match against jobs

        :return: The blacklist of this JobAsk.
        :rtype: JobConfigInputs
        """
        return self._blacklist

    @blacklist.setter
    def blacklist(self, blacklist):
        """Sets the blacklist of this JobAsk.

        Properties that must NOT match against jobs

        :param blacklist: The blacklist of this JobAsk.  # noqa: E501
        :type: JobConfigInputs
        """

        self._blacklist = blacklist

    @property
    def capabilities(self):
        """Gets the capabilities of this JobAsk.

        A set of capabilities that must be a superset of matched jobs

        :return: The capabilities of this JobAsk.
        :rtype: list[str]
        """
        return self._capabilities

    @capabilities.setter
    def capabilities(self, capabilities):
        """Sets the capabilities of this JobAsk.

        A set of capabilities that must be a superset of matched jobs

        :param capabilities: The capabilities of this JobAsk.  # noqa: E501
        :type: list[str]
        """

        self._capabilities = capabilities

    @property
    def _return(self):
        """Gets the _return of this JobAsk.

        Which sorts of return values to receive from ask

        :return: The _return of this JobAsk.
        :rtype: JobAskReturn
        """
        return self.__return

    @_return.setter
    def _return(self, _return):
        """Sets the _return of this JobAsk.

        Which sorts of return values to receive from ask

        :param _return: The _return of this JobAsk.  # noqa: E501
        :type: JobAskReturn
        """

        self.__return = _return


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
        if not isinstance(other, JobAsk):
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
