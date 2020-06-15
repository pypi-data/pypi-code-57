"""
Utilities for handling geometry operations.
"""

from typing import List, Generator
import math

import mercantile
import geojson
import shapely
import shapely.geometry
from shapely.geometry import box
from area import area

from .stac import STACQuery, BoundingBox

from .logging import get_logger

logger = get_logger(__name__)


def filter_tiles_intersect_with_geometry(
    tiles: List[mercantile.Tile], geometry: geojson.geometry.Geometry
) -> Generator[mercantile.Tile, None, None]:
    """
    Given a list of WMTS tiles, this function filters out all tiles which
    don't intersect with the supplied geojson geometry.

    Arguments:
        tiles: List of tiles to filter from.
        geometry: Geometry to use for filtering.

    Returns:
        Tile generator with only tiles that intersect geometry.
    """
    geometry = shapely.geometry.shape(geometry)
    for tile in tiles:
        tile_bbox = shapely.geometry.box(*mercantile.bounds(tile)._asdict().values())
        if geometry.intersects(tile_bbox) and not geometry.touches(tile_bbox):
            yield tile


def intersect_geojson_polygons(
    geom1: geojson.geometry.Geometry, geom2: geojson.geometry.Geometry
) -> geojson.geometry.Geometry:
    """
    Convenience method for intersecting two geojson polygons.

    Arguments:
        geom1: A geometry.
        geom2: A different geometry to intersect with.

    Returns:
        Geometry of the intersection.
    """
    geometry1 = shapely.geometry.shape(geom1)
    geometry2 = shapely.geometry.shape(geom2)
    intersection = geometry1.intersection(geometry2)

    return shapely.geometry.mapping(intersection)


def get_query_bbox(query: STACQuery) -> BoundingBox:
    """
    From a STACQuery object return the bounding box of the query.

    Arguments:
        query: A STACQuery object.

    Returns:
        A bounding box object of the query.

    Important:
        If the geometry type is Point or a very small area, a very small buffer
        will be computed and the bounding box of the buffered geometry returned.
    """

    bbox: BoundingBox = query.bounds()

    poly = box(*bbox)
    if poly.area == 0.0:
        # If the geometry in the query was just a point (rather than a box),
        # then make a very small polygon around it so we can derive a
        # bounding box for the OABM API.
        bbox = poly.buffer(0.0001).bounds

    return bbox


def aoi_size_check(
    query: STACQuery, min_sqkm: float = None, max_sqkm: float = None
) -> bool:
    """
    Checks if the query geometry is within set AOI size bounds.

    Arguments:
        query: A STACQuery object.
        min_sqkm: The minimum size in square kilometers.
        max_sqkm: The maximum size in square kilometers.

    Returns:
        Is the query within AOI size bounds.
    """
    valid = True
    area_sqkm = area(query.geometry()) / (10 ** 6)

    if min_sqkm is not None:
        if area_sqkm < min_sqkm:
            valid = False

    if max_sqkm is not None:
        if area_sqkm > max_sqkm:
            valid = False

    return valid


# pylint: disable=chained-comparison
def get_utm_zone_epsg(lon: float, lat: float) -> int:
    """
    Calculates the suitable UTM crs epsg code for an input geometry point.

    Adapted from https://stackoverflow.com/a/55781862/6400555.

    Arguments:
        lon : Longitude of point in degrees (WGS84)
        lat : Latitude of point in degrees (WGS84)

    Returns:
        EPSG code of suitable UTM zone for given (lon, lat). i.e. 32658
    """
    zone_number = int((math.floor((lon + 180) / 6) % 60) + 1)

    # Special zones for Norway
    if lat >= 56.0 and lat < 64.0 and lon >= 3.0 and lon < 12.0:
        zone_number = 32
    # Special zones for Svalbard
    elif lat >= 72.0 and lat < 84.0:
        if lon >= 0.0 and lon < 9.0:
            zone_number = 31
        elif lon >= 9.0 and lon < 21.0:
            zone_number = 33
        elif lon >= 21.0 and lon < 33.0:
            zone_number = 35
        elif lon >= 33.0 and lon < 42.0:
            zone_number = 37

    if lat > 0:
        utm_code = zone_number + 32600
    else:
        utm_code = zone_number + 32700

    return utm_code
