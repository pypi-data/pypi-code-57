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


class ValidationResults(object):
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
        'diagnostics': 'ValidationDiagnostics',
        'revision': 'RevisionDescriptor',
        'rules': 'list[ValidationRule]'
    }

    attribute_map = {
        'diagnostics': 'diagnostics',
        'revision': 'revision',
        'rules': 'rules'
    }

    def __init__(self, diagnostics=None, revision=None, rules=None):  # noqa: E501
        """ValidationResults - a model defined in OpenAPI"""  # noqa: E501

        self._diagnostics = None
        self._revision = None
        self._rules = None
        self.discriminator = None

        self.diagnostics = diagnostics
        self.revision = revision
        self.rules = rules

    @property
    def diagnostics(self):
        """Gets the diagnostics of this ValidationResults.  # noqa: E501


        :return: The diagnostics of this ValidationResults.  # noqa: E501
        :rtype: ValidationDiagnostics
        """
        return self._diagnostics

    @diagnostics.setter
    def diagnostics(self, diagnostics):
        """Sets the diagnostics of this ValidationResults.


        :param diagnostics: The diagnostics of this ValidationResults.  # noqa: E501
        :type: ValidationDiagnostics
        """
        if diagnostics is None:
            raise ValueError("Invalid value for `diagnostics`, must not be `None`")  # noqa: E501

        self._diagnostics = diagnostics

    @property
    def revision(self):
        """Gets the revision of this ValidationResults.  # noqa: E501


        :return: The revision of this ValidationResults.  # noqa: E501
        :rtype: RevisionDescriptor
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this ValidationResults.


        :param revision: The revision of this ValidationResults.  # noqa: E501
        :type: RevisionDescriptor
        """
        if revision is None:
            raise ValueError("Invalid value for `revision`, must not be `None`")  # noqa: E501

        self._revision = revision

    @property
    def rules(self):
        """Gets the rules of this ValidationResults.  # noqa: E501


        :return: The rules of this ValidationResults.  # noqa: E501
        :rtype: list[ValidationRule]
        """
        return self._rules

    @rules.setter
    def rules(self, rules):
        """Sets the rules of this ValidationResults.


        :param rules: The rules of this ValidationResults.  # noqa: E501
        :type: list[ValidationRule]
        """
        if rules is None:
            raise ValueError("Invalid value for `rules`, must not be `None`")  # noqa: E501

        self._rules = rules

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
        if not isinstance(other, ValidationResults):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
