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


class PersistIndexData(object):
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
        'compartment_uri': 'str',
        'write_handle': 'str',
        'index_data': 'IndexUpdateData',
        'all_updates_from_primary_model': 'bool'
    }

    attribute_map = {
        'compartment_uri': 'compartmentURI',
        'write_handle': 'writeHandle',
        'index_data': 'indexData',
        'all_updates_from_primary_model': 'allUpdatesFromPrimaryModel'
    }

    def __init__(self, compartment_uri=None, write_handle=None, index_data=None, all_updates_from_primary_model=None):  # noqa: E501
        """PersistIndexData - a model defined in OpenAPI"""  # noqa: E501

        self._compartment_uri = None
        self._write_handle = None
        self._index_data = None
        self._all_updates_from_primary_model = None
        self.discriminator = None

        self.compartment_uri = compartment_uri
        self.write_handle = write_handle
        self.index_data = index_data
        if all_updates_from_primary_model is not None:
            self.all_updates_from_primary_model = all_updates_from_primary_model

    @property
    def compartment_uri(self):
        """Gets the compartment_uri of this PersistIndexData.  # noqa: E501


        :return: The compartment_uri of this PersistIndexData.  # noqa: E501
        :rtype: str
        """
        return self._compartment_uri

    @compartment_uri.setter
    def compartment_uri(self, compartment_uri):
        """Sets the compartment_uri of this PersistIndexData.


        :param compartment_uri: The compartment_uri of this PersistIndexData.  # noqa: E501
        :type: str
        """
        if compartment_uri is None:
            raise ValueError("Invalid value for `compartment_uri`, must not be `None`")  # noqa: E501

        self._compartment_uri = compartment_uri

    @property
    def write_handle(self):
        """Gets the write_handle of this PersistIndexData.  # noqa: E501


        :return: The write_handle of this PersistIndexData.  # noqa: E501
        :rtype: str
        """
        return self._write_handle

    @write_handle.setter
    def write_handle(self, write_handle):
        """Sets the write_handle of this PersistIndexData.


        :param write_handle: The write_handle of this PersistIndexData.  # noqa: E501
        :type: str
        """
        if write_handle is None:
            raise ValueError("Invalid value for `write_handle`, must not be `None`")  # noqa: E501

        self._write_handle = write_handle

    @property
    def index_data(self):
        """Gets the index_data of this PersistIndexData.  # noqa: E501


        :return: The index_data of this PersistIndexData.  # noqa: E501
        :rtype: IndexUpdateData
        """
        return self._index_data

    @index_data.setter
    def index_data(self, index_data):
        """Sets the index_data of this PersistIndexData.


        :param index_data: The index_data of this PersistIndexData.  # noqa: E501
        :type: IndexUpdateData
        """
        if index_data is None:
            raise ValueError("Invalid value for `index_data`, must not be `None`")  # noqa: E501

        self._index_data = index_data

    @property
    def all_updates_from_primary_model(self):
        """Gets the all_updates_from_primary_model of this PersistIndexData.  # noqa: E501


        :return: The all_updates_from_primary_model of this PersistIndexData.  # noqa: E501
        :rtype: bool
        """
        return self._all_updates_from_primary_model

    @all_updates_from_primary_model.setter
    def all_updates_from_primary_model(self, all_updates_from_primary_model):
        """Sets the all_updates_from_primary_model of this PersistIndexData.


        :param all_updates_from_primary_model: The all_updates_from_primary_model of this PersistIndexData.  # noqa: E501
        :type: bool
        """

        self._all_updates_from_primary_model = all_updates_from_primary_model

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
        if not isinstance(other, PersistIndexData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
