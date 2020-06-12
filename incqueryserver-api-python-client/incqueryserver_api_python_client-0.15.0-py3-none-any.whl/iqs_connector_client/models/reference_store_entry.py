# coding: utf-8

"""
    IncQuery Server Connector API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: 0.15.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ReferenceStoreEntry(object):
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
        'reference': 'EReferenceDescriptor',
        'tuples': 'list[ReferenceSlot]'
    }

    attribute_map = {
        'reference': 'reference',
        'tuples': 'tuples'
    }

    def __init__(self, reference=None, tuples=None):  # noqa: E501
        """ReferenceStoreEntry - a model defined in OpenAPI"""  # noqa: E501

        self._reference = None
        self._tuples = None
        self.discriminator = None

        self.reference = reference
        self.tuples = tuples

    @property
    def reference(self):
        """Gets the reference of this ReferenceStoreEntry.  # noqa: E501


        :return: The reference of this ReferenceStoreEntry.  # noqa: E501
        :rtype: EReferenceDescriptor
        """
        return self._reference

    @reference.setter
    def reference(self, reference):
        """Sets the reference of this ReferenceStoreEntry.


        :param reference: The reference of this ReferenceStoreEntry.  # noqa: E501
        :type: EReferenceDescriptor
        """
        if reference is None:
            raise ValueError("Invalid value for `reference`, must not be `None`")  # noqa: E501

        self._reference = reference

    @property
    def tuples(self):
        """Gets the tuples of this ReferenceStoreEntry.  # noqa: E501


        :return: The tuples of this ReferenceStoreEntry.  # noqa: E501
        :rtype: list[ReferenceSlot]
        """
        return self._tuples

    @tuples.setter
    def tuples(self, tuples):
        """Sets the tuples of this ReferenceStoreEntry.


        :param tuples: The tuples of this ReferenceStoreEntry.  # noqa: E501
        :type: list[ReferenceSlot]
        """
        if tuples is None:
            raise ValueError("Invalid value for `tuples`, must not be `None`")  # noqa: E501

        self._tuples = tuples

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
        if not isinstance(other, ReferenceStoreEntry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
