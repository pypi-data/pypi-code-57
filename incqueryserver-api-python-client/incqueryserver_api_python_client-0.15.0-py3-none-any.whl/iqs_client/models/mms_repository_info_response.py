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


class MMSRepositoryInfoResponse(object):
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
        'repository_structure': 'MMSRepositoryStructure',
        'last_updated': 'str'
    }

    attribute_map = {
        'repository_structure': 'repositoryStructure',
        'last_updated': 'lastUpdated'
    }

    def __init__(self, repository_structure=None, last_updated=None):  # noqa: E501
        """MMSRepositoryInfoResponse - a model defined in OpenAPI"""  # noqa: E501

        self._repository_structure = None
        self._last_updated = None
        self.discriminator = None

        self.repository_structure = repository_structure
        self.last_updated = last_updated

    @property
    def repository_structure(self):
        """Gets the repository_structure of this MMSRepositoryInfoResponse.  # noqa: E501


        :return: The repository_structure of this MMSRepositoryInfoResponse.  # noqa: E501
        :rtype: MMSRepositoryStructure
        """
        return self._repository_structure

    @repository_structure.setter
    def repository_structure(self, repository_structure):
        """Sets the repository_structure of this MMSRepositoryInfoResponse.


        :param repository_structure: The repository_structure of this MMSRepositoryInfoResponse.  # noqa: E501
        :type: MMSRepositoryStructure
        """
        if repository_structure is None:
            raise ValueError("Invalid value for `repository_structure`, must not be `None`")  # noqa: E501

        self._repository_structure = repository_structure

    @property
    def last_updated(self):
        """Gets the last_updated of this MMSRepositoryInfoResponse.  # noqa: E501


        :return: The last_updated of this MMSRepositoryInfoResponse.  # noqa: E501
        :rtype: str
        """
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated):
        """Sets the last_updated of this MMSRepositoryInfoResponse.


        :param last_updated: The last_updated of this MMSRepositoryInfoResponse.  # noqa: E501
        :type: str
        """
        if last_updated is None:
            raise ValueError("Invalid value for `last_updated`, must not be `None`")  # noqa: E501

        self._last_updated = last_updated

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
        if not isinstance(other, MMSRepositoryInfoResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
