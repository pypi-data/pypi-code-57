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

from cognite.geospatial.internal.models import RasterGeometrySpatialDTO


class RasterGeometrySpatialObject(RasterGeometrySpatialDTO):
    """Raster spatial geometry.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {"type": "str", "row_min": "int", "row_max": "int", "column_min": "int", "column_max": "int"}

    attribute_map = {
        "type": "type",
        "row_min": "rowMin",
        "row_max": "rowMax",
        "column_min": "columnMin",
        "column_max": "columnMax",
    }

    def __init__(
        self, row_min=None, row_max=None, column_min=None, column_max=None, local_vars_configuration=None
    ):  # noqa: E501
        """RasterGeometrySpatialObject - a model defined in OpenAPI"""  # noqa: E501
        super(RasterGeometrySpatialObject, self).__init__(
            row_min, row_max, column_min, column_max, local_vars_configuration
        )
        self._type = "raster"

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

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RasterGeometrySpatialObject):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RasterGeometrySpatialObject):
            return True

        return self.to_dict() != other.to_dict()
