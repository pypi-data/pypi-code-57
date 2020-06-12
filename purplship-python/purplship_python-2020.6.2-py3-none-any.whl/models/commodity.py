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


class Commodity(object):
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
        'id': 'str',
        'weight': 'float',
        'width': 'float',
        'height': 'float',
        'length': 'float',
        'description': 'str',
        'quantity': 'int',
        'sku': 'str',
        'value_amount': 'float',
        'value_currency': 'str',
        'origin_country': 'str'
    }

    attribute_map = {
        'id': 'id',
        'weight': 'weight',
        'width': 'width',
        'height': 'height',
        'length': 'length',
        'description': 'description',
        'quantity': 'quantity',
        'sku': 'sku',
        'value_amount': 'valueAmount',
        'value_currency': 'valueCurrency',
        'origin_country': 'originCountry'
    }

    def __init__(self, id=None, weight=None, width=None, height=None, length=None, description=None, quantity=None, sku=None, value_amount=None, value_currency=None, origin_country=None):  # noqa: E501
        """Commodity - a model defined in PurplShip"""  # noqa: E501

        self._id = None
        self._weight = None
        self._width = None
        self._height = None
        self._length = None
        self._description = None
        self._quantity = None
        self._sku = None
        self._value_amount = None
        self._value_currency = None
        self._origin_country = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if weight is not None:
            self.weight = weight
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if length is not None:
            self.length = length
        if description is not None:
            self.description = description
        if quantity is not None:
            self.quantity = quantity
        if sku is not None:
            self.sku = sku
        if value_amount is not None:
            self.value_amount = value_amount
        if value_currency is not None:
            self.value_currency = value_currency
        if origin_country is not None:
            self.origin_country = origin_country

    @property
    def id(self):
        """Gets the id of this Commodity.  # noqa: E501

        A unique commodity's identifier  # noqa: E501

        :return: The id of this Commodity.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Commodity.

        A unique commodity's identifier  # noqa: E501

        :param id: The id of this Commodity.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def weight(self):
        """Gets the weight of this Commodity.  # noqa: E501

        The commodity's weight  # noqa: E501

        :return: The weight of this Commodity.  # noqa: E501
        :rtype: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this Commodity.

        The commodity's weight  # noqa: E501

        :param weight: The weight of this Commodity.  # noqa: E501
        :type: float
        """

        self._weight = weight

    @property
    def width(self):
        """Gets the width of this Commodity.  # noqa: E501

        The commodity's width  # noqa: E501

        :return: The width of this Commodity.  # noqa: E501
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this Commodity.

        The commodity's width  # noqa: E501

        :param width: The width of this Commodity.  # noqa: E501
        :type: float
        """

        self._width = width

    @property
    def height(self):
        """Gets the height of this Commodity.  # noqa: E501

        The commodity's height  # noqa: E501

        :return: The height of this Commodity.  # noqa: E501
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Commodity.

        The commodity's height  # noqa: E501

        :param height: The height of this Commodity.  # noqa: E501
        :type: float
        """

        self._height = height

    @property
    def length(self):
        """Gets the length of this Commodity.  # noqa: E501

        The commodity's lenght  # noqa: E501

        :return: The length of this Commodity.  # noqa: E501
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Commodity.

        The commodity's lenght  # noqa: E501

        :param length: The length of this Commodity.  # noqa: E501
        :type: float
        """

        self._length = length

    @property
    def description(self):
        """Gets the description of this Commodity.  # noqa: E501

        A description of the commodity  # noqa: E501

        :return: The description of this Commodity.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Commodity.

        A description of the commodity  # noqa: E501

        :param description: The description of this Commodity.  # noqa: E501
        :type: str
        """
        if description is not None and len(description) < 1:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

    @property
    def quantity(self):
        """Gets the quantity of this Commodity.  # noqa: E501

        The commodity's quantity (number or item)  # noqa: E501

        :return: The quantity of this Commodity.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this Commodity.

        The commodity's quantity (number or item)  # noqa: E501

        :param quantity: The quantity of this Commodity.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def sku(self):
        """Gets the sku of this Commodity.  # noqa: E501

        The commodity's sku number  # noqa: E501

        :return: The sku of this Commodity.  # noqa: E501
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """Sets the sku of this Commodity.

        The commodity's sku number  # noqa: E501

        :param sku: The sku of this Commodity.  # noqa: E501
        :type: str
        """
        if sku is not None and len(sku) < 1:
            raise ValueError("Invalid value for `sku`, length must be greater than or equal to `1`")  # noqa: E501

        self._sku = sku

    @property
    def value_amount(self):
        """Gets the value_amount of this Commodity.  # noqa: E501

        The monetary value of the commodity  # noqa: E501

        :return: The value_amount of this Commodity.  # noqa: E501
        :rtype: float
        """
        return self._value_amount

    @value_amount.setter
    def value_amount(self, value_amount):
        """Sets the value_amount of this Commodity.

        The monetary value of the commodity  # noqa: E501

        :param value_amount: The value_amount of this Commodity.  # noqa: E501
        :type: float
        """

        self._value_amount = value_amount

    @property
    def value_currency(self):
        """Gets the value_currency of this Commodity.  # noqa: E501

        The currency of the commodity value amount  # noqa: E501

        :return: The value_currency of this Commodity.  # noqa: E501
        :rtype: str
        """
        return self._value_currency

    @value_currency.setter
    def value_currency(self, value_currency):
        """Sets the value_currency of this Commodity.

        The currency of the commodity value amount  # noqa: E501

        :param value_currency: The value_currency of this Commodity.  # noqa: E501
        :type: str
        """
        if value_currency is not None and len(value_currency) < 1:
            raise ValueError("Invalid value for `value_currency`, length must be greater than or equal to `1`")  # noqa: E501

        self._value_currency = value_currency

    @property
    def origin_country(self):
        """Gets the origin_country of this Commodity.  # noqa: E501

        The origin or manufacture country  # noqa: E501

        :return: The origin_country of this Commodity.  # noqa: E501
        :rtype: str
        """
        return self._origin_country

    @origin_country.setter
    def origin_country(self, origin_country):
        """Sets the origin_country of this Commodity.

        The origin or manufacture country  # noqa: E501

        :param origin_country: The origin_country of this Commodity.  # noqa: E501
        :type: str
        """
        if origin_country is not None and len(origin_country) < 1:
            raise ValueError("Invalid value for `origin_country`, length must be greater than or equal to `1`")  # noqa: E501

        self._origin_country = origin_country

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
        if issubclass(Commodity, dict):
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
        if not isinstance(other, Commodity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
