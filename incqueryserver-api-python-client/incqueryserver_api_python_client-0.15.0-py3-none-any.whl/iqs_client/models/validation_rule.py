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


class ValidationRule(object):
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
        'constraint': 'TypedElementDescriptor',
        'severity': 'str',
        'matching_elements': 'list[ValidationMatchingElement]'
    }

    attribute_map = {
        'constraint': 'constraint',
        'severity': 'severity',
        'matching_elements': 'matchingElements'
    }

    def __init__(self, constraint=None, severity=None, matching_elements=None):  # noqa: E501
        """ValidationRule - a model defined in OpenAPI"""  # noqa: E501

        self._constraint = None
        self._severity = None
        self._matching_elements = None
        self.discriminator = None

        self.constraint = constraint
        self.severity = severity
        self.matching_elements = matching_elements

    @property
    def constraint(self):
        """Gets the constraint of this ValidationRule.  # noqa: E501


        :return: The constraint of this ValidationRule.  # noqa: E501
        :rtype: TypedElementDescriptor
        """
        return self._constraint

    @constraint.setter
    def constraint(self, constraint):
        """Sets the constraint of this ValidationRule.


        :param constraint: The constraint of this ValidationRule.  # noqa: E501
        :type: TypedElementDescriptor
        """
        if constraint is None:
            raise ValueError("Invalid value for `constraint`, must not be `None`")  # noqa: E501

        self._constraint = constraint

    @property
    def severity(self):
        """Gets the severity of this ValidationRule.  # noqa: E501


        :return: The severity of this ValidationRule.  # noqa: E501
        :rtype: str
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this ValidationRule.


        :param severity: The severity of this ValidationRule.  # noqa: E501
        :type: str
        """
        if severity is None:
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501
        allowed_values = ["info", "debug", "warning", "error", "fatal"]  # noqa: E501
        if severity not in allowed_values:
            raise ValueError(
                "Invalid value for `severity` ({0}), must be one of {1}"  # noqa: E501
                .format(severity, allowed_values)
            )

        self._severity = severity

    @property
    def matching_elements(self):
        """Gets the matching_elements of this ValidationRule.  # noqa: E501


        :return: The matching_elements of this ValidationRule.  # noqa: E501
        :rtype: list[ValidationMatchingElement]
        """
        return self._matching_elements

    @matching_elements.setter
    def matching_elements(self, matching_elements):
        """Sets the matching_elements of this ValidationRule.


        :param matching_elements: The matching_elements of this ValidationRule.  # noqa: E501
        :type: list[ValidationMatchingElement]
        """
        if matching_elements is None:
            raise ValueError("Invalid value for `matching_elements`, must not be `None`")  # noqa: E501

        self._matching_elements = matching_elements

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
        if not isinstance(other, ValidationRule):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
