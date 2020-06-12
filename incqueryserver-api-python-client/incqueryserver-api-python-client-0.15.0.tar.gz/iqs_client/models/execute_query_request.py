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


class ExecuteQueryRequest(object):
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
        'revision_descriptor': 'RevisionDescriptor',
        'query_fqn': 'str',
        'parameter_binding': 'list[Argument]',
        'use_osmc_links_for_elements': 'bool',
        'query_mode': 'str'
    }

    attribute_map = {
        'revision_descriptor': 'revisionDescriptor',
        'query_fqn': 'queryFQN',
        'parameter_binding': 'parameterBinding',
        'use_osmc_links_for_elements': 'useOSMCLinksForElements',
        'query_mode': 'queryMode'
    }

    def __init__(self, revision_descriptor=None, query_fqn=None, parameter_binding=None, use_osmc_links_for_elements=None, query_mode=None):  # noqa: E501
        """ExecuteQueryRequest - a model defined in OpenAPI"""  # noqa: E501

        self._revision_descriptor = None
        self._query_fqn = None
        self._parameter_binding = None
        self._use_osmc_links_for_elements = None
        self._query_mode = None
        self.discriminator = None

        self.revision_descriptor = revision_descriptor
        self.query_fqn = query_fqn
        if parameter_binding is not None:
            self.parameter_binding = parameter_binding
        if use_osmc_links_for_elements is not None:
            self.use_osmc_links_for_elements = use_osmc_links_for_elements
        if query_mode is not None:
            self.query_mode = query_mode

    @property
    def revision_descriptor(self):
        """Gets the revision_descriptor of this ExecuteQueryRequest.  # noqa: E501


        :return: The revision_descriptor of this ExecuteQueryRequest.  # noqa: E501
        :rtype: RevisionDescriptor
        """
        return self._revision_descriptor

    @revision_descriptor.setter
    def revision_descriptor(self, revision_descriptor):
        """Sets the revision_descriptor of this ExecuteQueryRequest.


        :param revision_descriptor: The revision_descriptor of this ExecuteQueryRequest.  # noqa: E501
        :type: RevisionDescriptor
        """
        if revision_descriptor is None:
            raise ValueError("Invalid value for `revision_descriptor`, must not be `None`")  # noqa: E501

        self._revision_descriptor = revision_descriptor

    @property
    def query_fqn(self):
        """Gets the query_fqn of this ExecuteQueryRequest.  # noqa: E501


        :return: The query_fqn of this ExecuteQueryRequest.  # noqa: E501
        :rtype: str
        """
        return self._query_fqn

    @query_fqn.setter
    def query_fqn(self, query_fqn):
        """Sets the query_fqn of this ExecuteQueryRequest.


        :param query_fqn: The query_fqn of this ExecuteQueryRequest.  # noqa: E501
        :type: str
        """
        if query_fqn is None:
            raise ValueError("Invalid value for `query_fqn`, must not be `None`")  # noqa: E501

        self._query_fqn = query_fqn

    @property
    def parameter_binding(self):
        """Gets the parameter_binding of this ExecuteQueryRequest.  # noqa: E501


        :return: The parameter_binding of this ExecuteQueryRequest.  # noqa: E501
        :rtype: list[Argument]
        """
        return self._parameter_binding

    @parameter_binding.setter
    def parameter_binding(self, parameter_binding):
        """Sets the parameter_binding of this ExecuteQueryRequest.


        :param parameter_binding: The parameter_binding of this ExecuteQueryRequest.  # noqa: E501
        :type: list[Argument]
        """

        self._parameter_binding = parameter_binding

    @property
    def use_osmc_links_for_elements(self):
        """Gets the use_osmc_links_for_elements of this ExecuteQueryRequest.  # noqa: E501


        :return: The use_osmc_links_for_elements of this ExecuteQueryRequest.  # noqa: E501
        :rtype: bool
        """
        return self._use_osmc_links_for_elements

    @use_osmc_links_for_elements.setter
    def use_osmc_links_for_elements(self, use_osmc_links_for_elements):
        """Sets the use_osmc_links_for_elements of this ExecuteQueryRequest.


        :param use_osmc_links_for_elements: The use_osmc_links_for_elements of this ExecuteQueryRequest.  # noqa: E501
        :type: bool
        """

        self._use_osmc_links_for_elements = use_osmc_links_for_elements

    @property
    def query_mode(self):
        """Gets the query_mode of this ExecuteQueryRequest.  # noqa: E501


        :return: The query_mode of this ExecuteQueryRequest.  # noqa: E501
        :rtype: str
        """
        return self._query_mode

    @query_mode.setter
    def query_mode(self, query_mode):
        """Sets the query_mode of this ExecuteQueryRequest.


        :param query_mode: The query_mode of this ExecuteQueryRequest.  # noqa: E501
        :type: str
        """
        allowed_values = ["searchBased", "standing"]  # noqa: E501
        if query_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `query_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(query_mode, allowed_values)
            )

        self._query_mode = query_mode

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
        if not isinstance(other, ExecuteQueryRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
