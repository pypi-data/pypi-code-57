# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_deb.configuration import Configuration


class DebInstallerFileIndexRead(object):
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
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'artifacts': 'dict(str, str)',
        'release': 'str',
        'component': 'str',
        'architecture': 'str',
        'relative_path': 'str'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'artifacts': 'artifacts',
        'release': 'release',
        'component': 'component',
        'architecture': 'architecture',
        'relative_path': 'relative_path'
    }

    def __init__(self, pulp_href=None, pulp_created=None, artifacts=None, release=None, component=None, architecture=None, relative_path=None, local_vars_configuration=None):  # noqa: E501
        """DebInstallerFileIndexRead - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._artifacts = None
        self._release = None
        self._component = None
        self._architecture = None
        self._relative_path = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.artifacts = artifacts
        self.release = release
        self.component = component
        self.architecture = architecture
        if relative_path is not None:
            self.relative_path = relative_path

    @property
    def pulp_href(self):
        """Gets the pulp_href of this DebInstallerFileIndexRead.  # noqa: E501


        :return: The pulp_href of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this DebInstallerFileIndexRead.


        :param pulp_href: The pulp_href of this DebInstallerFileIndexRead.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this DebInstallerFileIndexRead.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this DebInstallerFileIndexRead.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this DebInstallerFileIndexRead.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def artifacts(self):
        """Gets the artifacts of this DebInstallerFileIndexRead.  # noqa: E501

        A dict mapping relative paths inside the Content to the correspondingArtifact URLs. E.g.: {'relative/path': '/artifacts/1/'  # noqa: E501

        :return: The artifacts of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts):
        """Sets the artifacts of this DebInstallerFileIndexRead.

        A dict mapping relative paths inside the Content to the correspondingArtifact URLs. E.g.: {'relative/path': '/artifacts/1/'  # noqa: E501

        :param artifacts: The artifacts of this DebInstallerFileIndexRead.  # noqa: E501
        :type: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and artifacts is None:  # noqa: E501
            raise ValueError("Invalid value for `artifacts`, must not be `None`")  # noqa: E501

        self._artifacts = artifacts

    @property
    def release(self):
        """Gets the release of this DebInstallerFileIndexRead.  # noqa: E501

        Release this index file belongs to.  # noqa: E501

        :return: The release of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: str
        """
        return self._release

    @release.setter
    def release(self, release):
        """Sets the release of this DebInstallerFileIndexRead.

        Release this index file belongs to.  # noqa: E501

        :param release: The release of this DebInstallerFileIndexRead.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and release is None:  # noqa: E501
            raise ValueError("Invalid value for `release`, must not be `None`")  # noqa: E501

        self._release = release

    @property
    def component(self):
        """Gets the component of this DebInstallerFileIndexRead.  # noqa: E501

        Component of the component - architecture combination.  # noqa: E501

        :return: The component of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: str
        """
        return self._component

    @component.setter
    def component(self, component):
        """Sets the component of this DebInstallerFileIndexRead.

        Component of the component - architecture combination.  # noqa: E501

        :param component: The component of this DebInstallerFileIndexRead.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and component is None:  # noqa: E501
            raise ValueError("Invalid value for `component`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                component is not None and len(component) < 1):
            raise ValueError("Invalid value for `component`, length must be greater than or equal to `1`")  # noqa: E501

        self._component = component

    @property
    def architecture(self):
        """Gets the architecture of this DebInstallerFileIndexRead.  # noqa: E501

        Architecture of the component - architecture combination.  # noqa: E501

        :return: The architecture of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: str
        """
        return self._architecture

    @architecture.setter
    def architecture(self, architecture):
        """Sets the architecture of this DebInstallerFileIndexRead.

        Architecture of the component - architecture combination.  # noqa: E501

        :param architecture: The architecture of this DebInstallerFileIndexRead.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and architecture is None:  # noqa: E501
            raise ValueError("Invalid value for `architecture`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                architecture is not None and len(architecture) < 1):
            raise ValueError("Invalid value for `architecture`, length must be greater than or equal to `1`")  # noqa: E501

        self._architecture = architecture

    @property
    def relative_path(self):
        """Gets the relative_path of this DebInstallerFileIndexRead.  # noqa: E501

        Path of directory containing MD5SUMS and SHA256SUMS relative to url.  # noqa: E501

        :return: The relative_path of this DebInstallerFileIndexRead.  # noqa: E501
        :rtype: str
        """
        return self._relative_path

    @relative_path.setter
    def relative_path(self, relative_path):
        """Sets the relative_path of this DebInstallerFileIndexRead.

        Path of directory containing MD5SUMS and SHA256SUMS relative to url.  # noqa: E501

        :param relative_path: The relative_path of this DebInstallerFileIndexRead.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                relative_path is not None and len(relative_path) < 1):
            raise ValueError("Invalid value for `relative_path`, length must be greater than or equal to `1`")  # noqa: E501

        self._relative_path = relative_path

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
        if not isinstance(other, DebInstallerFileIndexRead):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DebInstallerFileIndexRead):
            return True

        return self.to_dict() != other.to_dict()
