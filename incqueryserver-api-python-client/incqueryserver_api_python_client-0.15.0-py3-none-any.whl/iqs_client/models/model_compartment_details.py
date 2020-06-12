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


class ModelCompartmentDetails(object):
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
        'repository_path': 'str',
        'author': 'str',
        'details': 'object'
    }

    attribute_map = {
        'repository_path': 'repositoryPath',
        'author': 'author',
        'details': 'details'
    }

    def __init__(self, repository_path=None, author=None, details=None):  # noqa: E501
        """ModelCompartmentDetails - a model defined in OpenAPI"""  # noqa: E501

        self._repository_path = None
        self._author = None
        self._details = None
        self.discriminator = None

        self.repository_path = repository_path
        self.author = author
        if details is not None:
            self.details = details

    @property
    def repository_path(self):
        """Gets the repository_path of this ModelCompartmentDetails.  # noqa: E501


        :return: The repository_path of this ModelCompartmentDetails.  # noqa: E501
        :rtype: str
        """
        return self._repository_path

    @repository_path.setter
    def repository_path(self, repository_path):
        """Sets the repository_path of this ModelCompartmentDetails.


        :param repository_path: The repository_path of this ModelCompartmentDetails.  # noqa: E501
        :type: str
        """
        if repository_path is None:
            raise ValueError("Invalid value for `repository_path`, must not be `None`")  # noqa: E501

        self._repository_path = repository_path

    @property
    def author(self):
        """Gets the author of this ModelCompartmentDetails.  # noqa: E501


        :return: The author of this ModelCompartmentDetails.  # noqa: E501
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """Sets the author of this ModelCompartmentDetails.


        :param author: The author of this ModelCompartmentDetails.  # noqa: E501
        :type: str
        """
        if author is None:
            raise ValueError("Invalid value for `author`, must not be `None`")  # noqa: E501

        self._author = author

    @property
    def details(self):
        """Gets the details of this ModelCompartmentDetails.  # noqa: E501


        :return: The details of this ModelCompartmentDetails.  # noqa: E501
        :rtype: object
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this ModelCompartmentDetails.


        :param details: The details of this ModelCompartmentDetails.  # noqa: E501
        :type: object
        """

        self._details = details

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
        if not isinstance(other, ModelCompartmentDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
