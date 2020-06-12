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


class MDObjectIDList(object):
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
        'md_object_ids': 'list[str]',
        'include_only_latest_revisions_of_branches': 'bool'
    }

    attribute_map = {
        'md_object_ids': 'mdObjectIds',
        'include_only_latest_revisions_of_branches': 'includeOnlyLatestRevisionsOfBranches'
    }

    def __init__(self, md_object_ids=None, include_only_latest_revisions_of_branches=False):  # noqa: E501
        """MDObjectIDList - a model defined in OpenAPI"""  # noqa: E501

        self._md_object_ids = None
        self._include_only_latest_revisions_of_branches = None
        self.discriminator = None

        self.md_object_ids = md_object_ids
        if include_only_latest_revisions_of_branches is not None:
            self.include_only_latest_revisions_of_branches = include_only_latest_revisions_of_branches

    @property
    def md_object_ids(self):
        """Gets the md_object_ids of this MDObjectIDList.  # noqa: E501

        MDObject ID list of model elements   # noqa: E501

        :return: The md_object_ids of this MDObjectIDList.  # noqa: E501
        :rtype: list[str]
        """
        return self._md_object_ids

    @md_object_ids.setter
    def md_object_ids(self, md_object_ids):
        """Sets the md_object_ids of this MDObjectIDList.

        MDObject ID list of model elements   # noqa: E501

        :param md_object_ids: The md_object_ids of this MDObjectIDList.  # noqa: E501
        :type: list[str]
        """
        if md_object_ids is None:
            raise ValueError("Invalid value for `md_object_ids`, must not be `None`")  # noqa: E501

        self._md_object_ids = md_object_ids

    @property
    def include_only_latest_revisions_of_branches(self):
        """Gets the include_only_latest_revisions_of_branches of this MDObjectIDList.  # noqa: E501

        If true, the results will only include dependencies from latest revisions of each branch   # noqa: E501

        :return: The include_only_latest_revisions_of_branches of this MDObjectIDList.  # noqa: E501
        :rtype: bool
        """
        return self._include_only_latest_revisions_of_branches

    @include_only_latest_revisions_of_branches.setter
    def include_only_latest_revisions_of_branches(self, include_only_latest_revisions_of_branches):
        """Sets the include_only_latest_revisions_of_branches of this MDObjectIDList.

        If true, the results will only include dependencies from latest revisions of each branch   # noqa: E501

        :param include_only_latest_revisions_of_branches: The include_only_latest_revisions_of_branches of this MDObjectIDList.  # noqa: E501
        :type: bool
        """

        self._include_only_latest_revisions_of_branches = include_only_latest_revisions_of_branches

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
        if not isinstance(other, MDObjectIDList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
