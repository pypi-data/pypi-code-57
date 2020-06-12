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


class CompartmentOperationState(object):
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
        'message': 'object',
        'operation_state': 'str',
        'estimated_time_remaining': 'int',
        'total_units_of_work': 'int',
        'completed_units_of_work': 'int'
    }

    attribute_map = {
        'message': 'message',
        'operation_state': 'operationState',
        'estimated_time_remaining': 'estimatedTimeRemaining',
        'total_units_of_work': 'totalUnitsOfWork',
        'completed_units_of_work': 'completedUnitsOfWork'
    }

    def __init__(self, message=None, operation_state=None, estimated_time_remaining=None, total_units_of_work=None, completed_units_of_work=None):  # noqa: E501
        """CompartmentOperationState - a model defined in OpenAPI"""  # noqa: E501

        self._message = None
        self._operation_state = None
        self._estimated_time_remaining = None
        self._total_units_of_work = None
        self._completed_units_of_work = None
        self.discriminator = None

        self.message = message
        self.operation_state = operation_state
        self.estimated_time_remaining = estimated_time_remaining
        self.total_units_of_work = total_units_of_work
        self.completed_units_of_work = completed_units_of_work

    @property
    def message(self):
        """Gets the message of this CompartmentOperationState.  # noqa: E501


        :return: The message of this CompartmentOperationState.  # noqa: E501
        :rtype: object
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this CompartmentOperationState.


        :param message: The message of this CompartmentOperationState.  # noqa: E501
        :type: object
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def operation_state(self):
        """Gets the operation_state of this CompartmentOperationState.  # noqa: E501


        :return: The operation_state of this CompartmentOperationState.  # noqa: E501
        :rtype: str
        """
        return self._operation_state

    @operation_state.setter
    def operation_state(self, operation_state):
        """Sets the operation_state of this CompartmentOperationState.


        :param operation_state: The operation_state of this CompartmentOperationState.  # noqa: E501
        :type: str
        """
        if operation_state is None:
            raise ValueError("Invalid value for `operation_state`, must not be `None`")  # noqa: E501
        allowed_values = ["TERMINATED", "STARTING", "IN_PROGRESS", "COMPLETED", "ERROR"]  # noqa: E501
        if operation_state not in allowed_values:
            raise ValueError(
                "Invalid value for `operation_state` ({0}), must be one of {1}"  # noqa: E501
                .format(operation_state, allowed_values)
            )

        self._operation_state = operation_state

    @property
    def estimated_time_remaining(self):
        """Gets the estimated_time_remaining of this CompartmentOperationState.  # noqa: E501


        :return: The estimated_time_remaining of this CompartmentOperationState.  # noqa: E501
        :rtype: int
        """
        return self._estimated_time_remaining

    @estimated_time_remaining.setter
    def estimated_time_remaining(self, estimated_time_remaining):
        """Sets the estimated_time_remaining of this CompartmentOperationState.


        :param estimated_time_remaining: The estimated_time_remaining of this CompartmentOperationState.  # noqa: E501
        :type: int
        """
        if estimated_time_remaining is None:
            raise ValueError("Invalid value for `estimated_time_remaining`, must not be `None`")  # noqa: E501

        self._estimated_time_remaining = estimated_time_remaining

    @property
    def total_units_of_work(self):
        """Gets the total_units_of_work of this CompartmentOperationState.  # noqa: E501


        :return: The total_units_of_work of this CompartmentOperationState.  # noqa: E501
        :rtype: int
        """
        return self._total_units_of_work

    @total_units_of_work.setter
    def total_units_of_work(self, total_units_of_work):
        """Sets the total_units_of_work of this CompartmentOperationState.


        :param total_units_of_work: The total_units_of_work of this CompartmentOperationState.  # noqa: E501
        :type: int
        """
        if total_units_of_work is None:
            raise ValueError("Invalid value for `total_units_of_work`, must not be `None`")  # noqa: E501

        self._total_units_of_work = total_units_of_work

    @property
    def completed_units_of_work(self):
        """Gets the completed_units_of_work of this CompartmentOperationState.  # noqa: E501


        :return: The completed_units_of_work of this CompartmentOperationState.  # noqa: E501
        :rtype: int
        """
        return self._completed_units_of_work

    @completed_units_of_work.setter
    def completed_units_of_work(self, completed_units_of_work):
        """Sets the completed_units_of_work of this CompartmentOperationState.


        :param completed_units_of_work: The completed_units_of_work of this CompartmentOperationState.  # noqa: E501
        :type: int
        """
        if completed_units_of_work is None:
            raise ValueError("Invalid value for `completed_units_of_work`, must not be `None`")  # noqa: E501

        self._completed_units_of_work = completed_units_of_work

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
        if not isinstance(other, CompartmentOperationState):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
