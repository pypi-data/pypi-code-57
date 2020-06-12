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


class WorkspaceWithDependentElements(object):
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
        'workspace_id': 'str',
        'title': 'str',
        'resources': 'list[ResourceWithDependentElements]'
    }

    attribute_map = {
        'workspace_id': 'workspaceId',
        'title': 'title',
        'resources': 'resources'
    }

    def __init__(self, workspace_id=None, title=None, resources=None):  # noqa: E501
        """WorkspaceWithDependentElements - a model defined in OpenAPI"""  # noqa: E501

        self._workspace_id = None
        self._title = None
        self._resources = None
        self.discriminator = None

        self.workspace_id = workspace_id
        if title is not None:
            self.title = title
        self.resources = resources

    @property
    def workspace_id(self):
        """Gets the workspace_id of this WorkspaceWithDependentElements.  # noqa: E501


        :return: The workspace_id of this WorkspaceWithDependentElements.  # noqa: E501
        :rtype: str
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this WorkspaceWithDependentElements.


        :param workspace_id: The workspace_id of this WorkspaceWithDependentElements.  # noqa: E501
        :type: str
        """
        if workspace_id is None:
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

        self._workspace_id = workspace_id

    @property
    def title(self):
        """Gets the title of this WorkspaceWithDependentElements.  # noqa: E501


        :return: The title of this WorkspaceWithDependentElements.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this WorkspaceWithDependentElements.


        :param title: The title of this WorkspaceWithDependentElements.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def resources(self):
        """Gets the resources of this WorkspaceWithDependentElements.  # noqa: E501


        :return: The resources of this WorkspaceWithDependentElements.  # noqa: E501
        :rtype: list[ResourceWithDependentElements]
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this WorkspaceWithDependentElements.


        :param resources: The resources of this WorkspaceWithDependentElements.  # noqa: E501
        :type: list[ResourceWithDependentElements]
        """
        if resources is None:
            raise ValueError("Invalid value for `resources`, must not be `None`")  # noqa: E501

        self._resources = resources

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
        if not isinstance(other, WorkspaceWithDependentElements):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
