# coding: utf-8

"""
    PurplShip Multi-carrier API

    PurplShip is a Multi-carrier Shipping API that simplifies the integration of logistic carrier services  # noqa: E501

    OpenAPI spec version: v1
    Contact: hello@purplship.com
    Generated by: https://github.com/purplship-api/purplship-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class TrackingResponse(object):
    """NOTE: This class is auto generated by the purplship code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      purplship_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    purplship_types = {
        'messages': 'list[Message]',
        'tracking_details': 'TrackingDetails'
    }

    attribute_map = {
        'messages': 'messages',
        'tracking_details': 'trackingDetails'
    }

    def __init__(self, messages=None, tracking_details=None):  # noqa: E501
        """TrackingResponse - a model defined in PurplShip"""  # noqa: E501

        self._messages = None
        self._tracking_details = None
        self.discriminator = None

        if messages is not None:
            self.messages = messages
        if tracking_details is not None:
            self.tracking_details = tracking_details

    @property
    def messages(self):
        """Gets the messages of this TrackingResponse.  # noqa: E501

        The list of note or warning messages  # noqa: E501

        :return: The messages of this TrackingResponse.  # noqa: E501
        :rtype: list[Message]
        """
        return self._messages

    @messages.setter
    def messages(self, messages):
        """Sets the messages of this TrackingResponse.

        The list of note or warning messages  # noqa: E501

        :param messages: The messages of this TrackingResponse.  # noqa: E501
        :type: list[Message]
        """

        self._messages = messages

    @property
    def tracking_details(self):
        """Gets the tracking_details of this TrackingResponse.  # noqa: E501


        :return: The tracking_details of this TrackingResponse.  # noqa: E501
        :rtype: TrackingDetails
        """
        return self._tracking_details

    @tracking_details.setter
    def tracking_details(self, tracking_details):
        """Sets the tracking_details of this TrackingResponse.


        :param tracking_details: The tracking_details of this TrackingResponse.  # noqa: E501
        :type: TrackingDetails
        """

        self._tracking_details = tracking_details

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.purplship_types):
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
        if issubclass(TrackingResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TrackingResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
