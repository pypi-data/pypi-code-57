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

from cognite.geospatial.internal.models import SpatialFilterDTO


class SpatialFilterObject(SpatialFilterDTO):
    openapi_types = {
        "filter_type": "str",
        "geometry": "GeometryDTO",
        "projection": "GeometryProjectionDTO",
        "distance_meter": "float",
    }

    attribute_map = {
        "filter_type": "filterType",
        "geometry": "geometry",
        "distance_meter": "distanceMeter",
        "projection": "projection",
    }

    def __init__(
        self, filter_type=None, geometry=None, distance_meter=None, projection=None, local_vars_configuration=None
    ):  # noqa: E501
        """SpatialFilterObject """  # noqa: E501
        super(SpatialFilterObject, self).__init__(filter_type, geometry, projection, local_vars_configuration)

        self._distance_meter = distance_meter

    @property
    def distance_meter(self):
        """Gets the distance_meter of this WithinDistanceFilterDTO.  # noqa: E501


        :return: The distance_meter of this WithinDistanceFilterDTO.  # noqa: E501
        :rtype: float
        """
        return self._distance_meter

    @distance_meter.setter
    def distance_meter(self, distance_meter):
        """Sets the distance_meter of this WithinDistanceFilterDTO.


        :param distance_meter: The distance_meter of this WithinDistanceFilterDTO.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and distance_meter is None:  # noqa: E501
            raise ValueError("Invalid value for `distance_meter`, must not be `None`")  # noqa: E501

        self._distance_meter = distance_meter

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
