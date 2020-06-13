# -*- coding:utf-8 -*-
from dataclasses import dataclass
from math import cos, radians, sqrt

from typing import Collection

# https://en.wikipedia.org/wiki/Earth_radius
EARTH_RADIUS = 6_378_100  # meters, approximate


__all__ = ['Coordinates', 'Rectangle']


@dataclass(frozen=True)
class Coordinates:
    """Value Object representing a point on the surface of the Earth."""
    lat: float
    lng: float

    def distance_to(self, other: 'Coordinates') -> float:
        """Very rough approximation of distance between two sets of coordinates.

        The distance is given in meters and is to be used only for comparison with
        other distances calculated by this method.

        The point is that moving in the longitude direction gets cheaper the
        further away you are from the equator.
        """
        dx = radians(other.lng - self.lng) * cos(radians(self.lat))
        dy = radians(other.lat - self.lat)
        return EARTH_RADIUS * sqrt(dx*dx + dy*dy)

    def __post_init__(self):
        if not -90 <= self.lat <= 90:
            raise ValueError("Latitude value out of bounds!")
        if not -180 <= self.lng <= 180:
            raise ValueError("Longitude value out of bounds!")


@dataclass(frozen=True)
class Rectangle:
    """Value Object representing a spherical rectangle on the surface of the Earth.

    The rectangle is always aligned with the latitude/longitude axes and is closed
    (meaning that its borders are considered to be "in" it), therefore, it can be
    easily defined by two of its "corners".
    """
    sw: Coordinates  # Southwestern "corner"
    ne: Coordinates  # Northeastern "corner"

    @staticmethod
    def enclosing(points: Collection[Coordinates]) -> 'Rectangle':
        """Build the smallest possible rectangle containing all given points."""
        north = east = float('-inf')
        south = west = float('inf')
        for x in points:
            north = max(north, x.lat)
            east = max(east, x.lng)
            south = min(south, x.lat)
            west = min(west, x.lng)
        return Rectangle(Coordinates(south, west), Coordinates(north, east))

    def area(self) -> float:
        """Approximate the area of this Rectangle.

        Uses the area of a Cartesian trapezoid for the approximation.
        """
        base1 = radians(self.ne.lng - self.sw.lng) * cos(radians(self.ne.lat)) * EARTH_RADIUS
        base2 = radians(self.ne.lng - self.sw.lng) * cos(radians(self.sw.lat)) * EARTH_RADIUS
        height = radians(self.ne.lat - self.sw.lat) * EARTH_RADIUS
        return (base1 + base2) * height / 2

    def contains(self, point: Coordinates) -> bool:
        """Check if this Rectangle contains the given Coordinates.

        Coordinates at the borders are considered "contained".
        """
        return (self.sw.lat <= point.lat <= self.ne.lat
                and self.sw.lng <= point.lng <= self.ne.lng)

    def distance_to_point(self, point: Coordinates) -> float:
        """Calculate the minimum distance from this Rectangle to the given Coordinates."""
        nearest = self._point_nearest_to(point)
        return point.distance_to(nearest)

    def _point_nearest_to(self, point: Coordinates) -> Coordinates:
        """Calculate the point inside the Rectangle nearest to the given Coordinates."""
        lat = (self.ne.lat if point.lat > self.ne.lat
               else self.sw.lat if point.lat < self.sw.lat
               else point.lat)
        lng = (self.ne.lng if point.lng > self.ne.lng
               else self.sw.lng if point.lng < self.sw.lng
               else point.lng)
        return Coordinates(lat, lng)
