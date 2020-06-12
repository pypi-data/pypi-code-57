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

from pulpcore.client.pulp_ansible.configuration import Configuration


class CollectionVersionRead(object):
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
        'version': 'str',
        'certification': 'str',
        'href': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'artifact': 'str',
        'collection': 'CollectionRef',
        'download_url': 'str',
        'name': 'str',
        'namespace': 'CollectionNamespace',
        'metadata': 'CollectionMetadata'
    }

    attribute_map = {
        'version': 'version',
        'certification': 'certification',
        'href': 'href',
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'artifact': 'artifact',
        'collection': 'collection',
        'download_url': 'download_url',
        'name': 'name',
        'namespace': 'namespace',
        'metadata': 'metadata'
    }

    def __init__(self, version=None, certification=None, href=None, created_at=None, updated_at=None, artifact=None, collection=None, download_url=None, name=None, namespace=None, metadata=None, local_vars_configuration=None):  # noqa: E501
        """CollectionVersionRead - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._version = None
        self._certification = None
        self._href = None
        self._created_at = None
        self._updated_at = None
        self._artifact = None
        self._collection = None
        self._download_url = None
        self._name = None
        self._namespace = None
        self._metadata = None
        self.discriminator = None

        if version is not None:
            self.version = version
        if certification is not None:
            self.certification = certification
        if href is not None:
            self.href = href
        self.created_at = created_at
        self.updated_at = updated_at
        if artifact is not None:
            self.artifact = artifact
        if collection is not None:
            self.collection = collection
        if download_url is not None:
            self.download_url = download_url
        if name is not None:
            self.name = name
        if namespace is not None:
            self.namespace = namespace
        if metadata is not None:
            self.metadata = metadata

    @property
    def version(self):
        """Gets the version of this CollectionVersionRead.  # noqa: E501


        :return: The version of this CollectionVersionRead.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this CollectionVersionRead.


        :param version: The version of this CollectionVersionRead.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                version is not None and len(version) < 1):
            raise ValueError("Invalid value for `version`, length must be greater than or equal to `1`")  # noqa: E501

        self._version = version

    @property
    def certification(self):
        """Gets the certification of this CollectionVersionRead.  # noqa: E501


        :return: The certification of this CollectionVersionRead.  # noqa: E501
        :rtype: str
        """
        return self._certification

    @certification.setter
    def certification(self, certification):
        """Sets the certification of this CollectionVersionRead.


        :param certification: The certification of this CollectionVersionRead.  # noqa: E501
        :type: str
        """
        allowed_values = ["certified", "not_certified", "needs_review"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and certification not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `certification` ({0}), must be one of {1}"  # noqa: E501
                .format(certification, allowed_values)
            )

        self._certification = certification

    @property
    def href(self):
        """Gets the href of this CollectionVersionRead.  # noqa: E501


        :return: The href of this CollectionVersionRead.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this CollectionVersionRead.


        :param href: The href of this CollectionVersionRead.  # noqa: E501
        :type: str
        """

        self._href = href

    @property
    def created_at(self):
        """Gets the created_at of this CollectionVersionRead.  # noqa: E501


        :return: The created_at of this CollectionVersionRead.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this CollectionVersionRead.


        :param created_at: The created_at of this CollectionVersionRead.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this CollectionVersionRead.  # noqa: E501


        :return: The updated_at of this CollectionVersionRead.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this CollectionVersionRead.


        :param updated_at: The updated_at of this CollectionVersionRead.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and updated_at is None:  # noqa: E501
            raise ValueError("Invalid value for `updated_at`, must not be `None`")  # noqa: E501

        self._updated_at = updated_at

    @property
    def artifact(self):
        """Gets the artifact of this CollectionVersionRead.  # noqa: E501


        :return: The artifact of this CollectionVersionRead.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this CollectionVersionRead.


        :param artifact: The artifact of this CollectionVersionRead.  # noqa: E501
        :type: str
        """

        self._artifact = artifact

    @property
    def collection(self):
        """Gets the collection of this CollectionVersionRead.  # noqa: E501


        :return: The collection of this CollectionVersionRead.  # noqa: E501
        :rtype: CollectionRef
        """
        return self._collection

    @collection.setter
    def collection(self, collection):
        """Sets the collection of this CollectionVersionRead.


        :param collection: The collection of this CollectionVersionRead.  # noqa: E501
        :type: CollectionRef
        """

        self._collection = collection

    @property
    def download_url(self):
        """Gets the download_url of this CollectionVersionRead.  # noqa: E501


        :return: The download_url of this CollectionVersionRead.  # noqa: E501
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """Sets the download_url of this CollectionVersionRead.


        :param download_url: The download_url of this CollectionVersionRead.  # noqa: E501
        :type: str
        """

        self._download_url = download_url

    @property
    def name(self):
        """Gets the name of this CollectionVersionRead.  # noqa: E501


        :return: The name of this CollectionVersionRead.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CollectionVersionRead.


        :param name: The name of this CollectionVersionRead.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def namespace(self):
        """Gets the namespace of this CollectionVersionRead.  # noqa: E501


        :return: The namespace of this CollectionVersionRead.  # noqa: E501
        :rtype: CollectionNamespace
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this CollectionVersionRead.


        :param namespace: The namespace of this CollectionVersionRead.  # noqa: E501
        :type: CollectionNamespace
        """

        self._namespace = namespace

    @property
    def metadata(self):
        """Gets the metadata of this CollectionVersionRead.  # noqa: E501


        :return: The metadata of this CollectionVersionRead.  # noqa: E501
        :rtype: CollectionMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this CollectionVersionRead.


        :param metadata: The metadata of this CollectionVersionRead.  # noqa: E501
        :type: CollectionMetadata
        """

        self._metadata = metadata

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
        if not isinstance(other, CollectionVersionRead):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CollectionVersionRead):
            return True

        return self.to_dict() != other.to_dict()
