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


class IndexModelCompartmentDeltaRequest(object):
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
        'required_model_compartment': 'ModelCompartment',
        'base_model_compartment': 'ModelCompartment'
    }

    attribute_map = {
        'required_model_compartment': 'requiredModelCompartment',
        'base_model_compartment': 'baseModelCompartment'
    }

    def __init__(self, required_model_compartment=None, base_model_compartment=None):  # noqa: E501
        """IndexModelCompartmentDeltaRequest - a model defined in OpenAPI"""  # noqa: E501

        self._required_model_compartment = None
        self._base_model_compartment = None
        self.discriminator = None

        self.required_model_compartment = required_model_compartment
        self.base_model_compartment = base_model_compartment

    @property
    def required_model_compartment(self):
        """Gets the required_model_compartment of this IndexModelCompartmentDeltaRequest.  # noqa: E501


        :return: The required_model_compartment of this IndexModelCompartmentDeltaRequest.  # noqa: E501
        :rtype: ModelCompartment
        """
        return self._required_model_compartment

    @required_model_compartment.setter
    def required_model_compartment(self, required_model_compartment):
        """Sets the required_model_compartment of this IndexModelCompartmentDeltaRequest.


        :param required_model_compartment: The required_model_compartment of this IndexModelCompartmentDeltaRequest.  # noqa: E501
        :type: ModelCompartment
        """
        if required_model_compartment is None:
            raise ValueError("Invalid value for `required_model_compartment`, must not be `None`")  # noqa: E501

        self._required_model_compartment = required_model_compartment

    @property
    def base_model_compartment(self):
        """Gets the base_model_compartment of this IndexModelCompartmentDeltaRequest.  # noqa: E501


        :return: The base_model_compartment of this IndexModelCompartmentDeltaRequest.  # noqa: E501
        :rtype: ModelCompartment
        """
        return self._base_model_compartment

    @base_model_compartment.setter
    def base_model_compartment(self, base_model_compartment):
        """Sets the base_model_compartment of this IndexModelCompartmentDeltaRequest.


        :param base_model_compartment: The base_model_compartment of this IndexModelCompartmentDeltaRequest.  # noqa: E501
        :type: ModelCompartment
        """
        if base_model_compartment is None:
            raise ValueError("Invalid value for `base_model_compartment`, must not be `None`")  # noqa: E501

        self._base_model_compartment = base_model_compartment

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
        if not isinstance(other, IndexModelCompartmentDeltaRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
