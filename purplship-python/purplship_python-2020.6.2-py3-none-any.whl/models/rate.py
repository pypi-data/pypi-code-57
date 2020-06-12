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


class Rate(object):
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
        'carrier_name': 'str',
        'carrier_id': 'str',
        'currency': 'str',
        'service': 'str',
        'discount': 'float',
        'base_charge': 'float',
        'total_charge': 'float',
        'duties_and_taxes': 'float',
        'estimated_delivery': 'str',
        'extra_charges': 'list[Charge]'
    }

    attribute_map = {
        'id': 'id',
        'carrier_name': 'carrierName',
        'carrier_id': 'carrierId',
        'currency': 'currency',
        'service': 'service',
        'discount': 'discount',
        'base_charge': 'baseCharge',
        'total_charge': 'totalCharge',
        'duties_and_taxes': 'dutiesAndTaxes',
        'estimated_delivery': 'estimatedDelivery',
        'extra_charges': 'extraCharges'
    }

    def __init__(self, id=None, carrier_name=None, carrier_id=None, currency=None, service=None, discount=None, base_charge=None, total_charge=None, duties_and_taxes=None, estimated_delivery=None, extra_charges=None):  # noqa: E501
        """Rate - a model defined in PurplShip"""  # noqa: E501

        self._id = None
        self._carrier_name = None
        self._carrier_id = None
        self._currency = None
        self._service = None
        self._discount = None
        self._base_charge = None
        self._total_charge = None
        self._duties_and_taxes = None
        self._estimated_delivery = None
        self._extra_charges = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.carrier_name = carrier_name
        self.carrier_id = carrier_id
        self.currency = currency
        if service is not None:
            self.service = service
        if discount is not None:
            self.discount = discount
        if base_charge is not None:
            self.base_charge = base_charge
        if total_charge is not None:
            self.total_charge = total_charge
        if duties_and_taxes is not None:
            self.duties_and_taxes = duties_and_taxes
        if estimated_delivery is not None:
            self.estimated_delivery = estimated_delivery
        if extra_charges is not None:
            self.extra_charges = extra_charges

    @property
    def id(self):
        """Gets the id of this Rate.  # noqa: E501

        A unique rate identifier  # noqa: E501

        :return: The id of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Rate.

        A unique rate identifier  # noqa: E501

        :param id: The id of this Rate.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def carrier_name(self):
        """Gets the carrier_name of this Rate.  # noqa: E501

        The rate's carrier  # noqa: E501

        :return: The carrier_name of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._carrier_name

    @carrier_name.setter
    def carrier_name(self, carrier_name):
        """Sets the carrier_name of this Rate.

        The rate's carrier  # noqa: E501

        :param carrier_name: The carrier_name of this Rate.  # noqa: E501
        :type: str
        """
        if carrier_name is None:
            raise ValueError("Invalid value for `carrier_name`, must not be `None`")  # noqa: E501
        if carrier_name is not None and len(carrier_name) < 1:
            raise ValueError("Invalid value for `carrier_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._carrier_name = carrier_name

    @property
    def carrier_id(self):
        """Gets the carrier_id of this Rate.  # noqa: E501

        The targeted carrier's name (unique identifier)  # noqa: E501

        :return: The carrier_id of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._carrier_id

    @carrier_id.setter
    def carrier_id(self, carrier_id):
        """Sets the carrier_id of this Rate.

        The targeted carrier's name (unique identifier)  # noqa: E501

        :param carrier_id: The carrier_id of this Rate.  # noqa: E501
        :type: str
        """
        if carrier_id is None:
            raise ValueError("Invalid value for `carrier_id`, must not be `None`")  # noqa: E501
        if carrier_id is not None and len(carrier_id) < 1:
            raise ValueError("Invalid value for `carrier_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._carrier_id = carrier_id

    @property
    def currency(self):
        """Gets the currency of this Rate.  # noqa: E501

        The rate monetary values currency code  # noqa: E501

        :return: The currency of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Rate.

        The rate monetary values currency code  # noqa: E501

        :param currency: The currency of this Rate.  # noqa: E501
        :type: str
        """
        if currency is None:
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501
        if currency is not None and len(currency) < 1:
            raise ValueError("Invalid value for `currency`, length must be greater than or equal to `1`")  # noqa: E501

        self._currency = currency

    @property
    def service(self):
        """Gets the service of this Rate.  # noqa: E501

        The carrier's rate (quote) service  # noqa: E501

        :return: The service of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this Rate.

        The carrier's rate (quote) service  # noqa: E501

        :param service: The service of this Rate.  # noqa: E501
        :type: str
        """
        if service is not None and len(service) < 1:
            raise ValueError("Invalid value for `service`, length must be greater than or equal to `1`")  # noqa: E501

        self._service = service

    @property
    def discount(self):
        """Gets the discount of this Rate.  # noqa: E501

        The monetary amount of the discount on the rate  # noqa: E501

        :return: The discount of this Rate.  # noqa: E501
        :rtype: float
        """
        return self._discount

    @discount.setter
    def discount(self, discount):
        """Sets the discount of this Rate.

        The monetary amount of the discount on the rate  # noqa: E501

        :param discount: The discount of this Rate.  # noqa: E501
        :type: float
        """

        self._discount = discount

    @property
    def base_charge(self):
        """Gets the base_charge of this Rate.  # noqa: E501

         The rate's monetary amount of the base charge.<br/> This is the net amount of the rate before additional charges   # noqa: E501

        :return: The base_charge of this Rate.  # noqa: E501
        :rtype: float
        """
        return self._base_charge

    @base_charge.setter
    def base_charge(self, base_charge):
        """Sets the base_charge of this Rate.

         The rate's monetary amount of the base charge.<br/> This is the net amount of the rate before additional charges   # noqa: E501

        :param base_charge: The base_charge of this Rate.  # noqa: E501
        :type: float
        """

        self._base_charge = base_charge

    @property
    def total_charge(self):
        """Gets the total_charge of this Rate.  # noqa: E501

         The rate's monetary amount of the total charge.<br/> This is the gross amount of the rate after adding the additional charges   # noqa: E501

        :return: The total_charge of this Rate.  # noqa: E501
        :rtype: float
        """
        return self._total_charge

    @total_charge.setter
    def total_charge(self, total_charge):
        """Sets the total_charge of this Rate.

         The rate's monetary amount of the total charge.<br/> This is the gross amount of the rate after adding the additional charges   # noqa: E501

        :param total_charge: The total_charge of this Rate.  # noqa: E501
        :type: float
        """

        self._total_charge = total_charge

    @property
    def duties_and_taxes(self):
        """Gets the duties_and_taxes of this Rate.  # noqa: E501

        The monetary amount of the duties and taxes if applied  # noqa: E501

        :return: The duties_and_taxes of this Rate.  # noqa: E501
        :rtype: float
        """
        return self._duties_and_taxes

    @duties_and_taxes.setter
    def duties_and_taxes(self, duties_and_taxes):
        """Sets the duties_and_taxes of this Rate.

        The monetary amount of the duties and taxes if applied  # noqa: E501

        :param duties_and_taxes: The duties_and_taxes of this Rate.  # noqa: E501
        :type: float
        """

        self._duties_and_taxes = duties_and_taxes

    @property
    def estimated_delivery(self):
        """Gets the estimated_delivery of this Rate.  # noqa: E501

        The estimated delivery date  # noqa: E501

        :return: The estimated_delivery of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._estimated_delivery

    @estimated_delivery.setter
    def estimated_delivery(self, estimated_delivery):
        """Sets the estimated_delivery of this Rate.

        The estimated delivery date  # noqa: E501

        :param estimated_delivery: The estimated_delivery of this Rate.  # noqa: E501
        :type: str
        """
        if estimated_delivery is not None and len(estimated_delivery) < 1:
            raise ValueError("Invalid value for `estimated_delivery`, length must be greater than or equal to `1`")  # noqa: E501

        self._estimated_delivery = estimated_delivery

    @property
    def extra_charges(self):
        """Gets the extra_charges of this Rate.  # noqa: E501

        list of the rate's additional charges  # noqa: E501

        :return: The extra_charges of this Rate.  # noqa: E501
        :rtype: list[Charge]
        """
        return self._extra_charges

    @extra_charges.setter
    def extra_charges(self, extra_charges):
        """Sets the extra_charges of this Rate.

        list of the rate's additional charges  # noqa: E501

        :param extra_charges: The extra_charges of this Rate.  # noqa: E501
        :type: list[Charge]
        """

        self._extra_charges = extra_charges

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
        if issubclass(Rate, dict):
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
        if not isinstance(other, Rate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
