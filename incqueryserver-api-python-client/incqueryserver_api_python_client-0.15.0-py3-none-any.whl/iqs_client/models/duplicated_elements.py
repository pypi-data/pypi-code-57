# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: 0.15.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class DuplicatedElements(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'duplicated': 'object'
    }

    attribute_map = {
        'duplicated': 'duplicated'
    }

    def __init__(self, duplicated=None):  # noqa: E501
        """DuplicatedElements - a model defined in OpenAPI"""  # noqa: E501

        self._duplicated = None
        self.discriminator = None

        if duplicated is not None:
            self.duplicated = duplicated

    @property
    def duplicated(self):
        """Gets the duplicated of this DuplicatedElements.  # noqa: E501


        :return: The duplicated of this DuplicatedElements.  # noqa: E501
        :rtype: object
        """
        return self._duplicated

    @duplicated.setter
    def duplicated(self, duplicated):
        """Sets the duplicated of this DuplicatedElements.


        :param duplicated: The duplicated of this DuplicatedElements.  # noqa: E501
        :type: object
        """

        self._duplicated = duplicated

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        if not isinstance(other, DuplicatedElements):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
