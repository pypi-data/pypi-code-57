# Copyright 2020 Cognite AS
"""Cognite Geospatial API store and query spatial data.

 Spatial objects represent a revision of an object present in a geographic position at a point
 in time (or for all time if no time is specified). The object has a position according to a
 specific coordinate reference system and can be a point, linestring, polygon, or surface
 defined by a position in 3-dimensional space. Within the defined area, the object can have
 attributes or values associated with more specific points or areas.

"""

import pprint
import re  # noqa: F401

import six

from cognite.geospatial.internal.models import PrimitiveGeometrySpatialDTO


class PrimitiveGeometrySpatialObject(PrimitiveGeometrySpatialDTO):
    """Primitive spatial geometry.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {"type": "str", "wkt": "str"}

    attribute_map = {"type": "type", "wkt": "wkt"}

    def __init__(self, type, wkt=None, local_vars_configuration=None):  # noqa: E501
        """PrimitiveGeometrySpatialObject - a model defined in OpenAPI"""  # noqa: E501
        super(PrimitiveGeometrySpatialObject, self).__init__(wkt, local_vars_configuration)
        self._type = type

    @property
    def type(self):
        """Gets the type of this GeometrySpatialDTO.  # noqa: E501


        :return: The type of this GeometrySpatialDTO.  # noqa: E501
        :rtype: str
        """
        return self._type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], "to_dict") else item,
                        value.items(),
                    )
                )
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
        if not isinstance(other, PrimitiveGeometrySpatialDTO):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PrimitiveGeometrySpatialDTO):
            return True

        return self.to_dict() != other.to_dict()
