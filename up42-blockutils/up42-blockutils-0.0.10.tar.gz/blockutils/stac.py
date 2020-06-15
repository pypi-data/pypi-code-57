"""
Utilities for handling [SpatioTemporal Asset Catalog (STAC)](https://stacspec.org/) queries.
"""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Union, Tuple, Iterable, cast, Optional, Callable, Any

import shapely.geometry

from geojson.geometry import Geometry
import ciso8601

from .logging import get_logger
from .exceptions import UP42Error, SupportedErrors

logger = get_logger(__name__)

Number = Union[int, Decimal, float]
Coordinates = Iterable[Number]
BoundingBox = Tuple[Number, Number, Number, Number]


class STACQuery:
    """
    Object representing a STAC query as used by data blocks.
    """

    def __repr__(self):
        return (
            f"STACQuery(ids={self.ids}, bbox={self.bbox}, intersects={self.intersects}, "
            f"contains={self.contains}, time={self.time}, time_series={self.time_series}, "
            f"limit={self.limit})"
        )

    def __init__(
        self,
        ids: Optional[list] = None,
        bbox: Optional[BoundingBox] = None,
        intersects: Optional[Geometry] = None,
        contains: Optional[Geometry] = None,
        time: Optional[str] = None,
        limit: Optional[int] = None,
        time_series: Optional[list] = None,
        **kwargs,
    ):  # pylint: disable=too-many-arguments
        """
        Arguments:
            ids: Unique identifiers to search for.
            bbox: A bounding box type geometry.
            intersects: A geometry to use for searching with intersection operator.
            contains: A geometry to use for searching with contains operator.
            time: Time string in RFC3339 (for points in time) or RFC3339/RFC3339
                (for datetime ranges).
            limit: Maximum number of returned elements.
            time_series: List of time strings in RFC3339 (for points in time) or RFC3339/RFC3339
                (for datetime ranges).
            kwargs: Arbitrary query arguments.
        """

        if bbox and intersects or intersects and contains or contains and bbox:
            raise UP42Error(
                SupportedErrors.WRONG_INPUT_ERROR,
                """Only one of the following query parameters is
                allowed at a query at any given time:
                * bbox
                * intersects
                * contains.""",
            )

        self.__dict__.update(
            kwargs
        )  # At the front so we do not accidentally overwrite some members
        self.ids = ids
        self.bbox = bbox
        self.intersects = intersects
        self.contains = contains

        if not STACQuery.validate_datetime_str(time):
            raise UP42Error(
                SupportedErrors.WRONG_INPUT_ERROR,
                """Time string could not be validated.
                It must be one of the following formats:
                <RFC3339> (for points in time)
                <RFC3339>/<RFC3339> (for datetime ranges)""",
            )
        self.time = time

        self.limit = 1 if limit is None else limit
        if limit is not None and limit < 0:
            logger.warning(
                "WARNING: limit parameter cannot be < 0, and has been automatically set to 1"
            )
            self.limit = 1

        if time_series is not None:
            for datestr in time_series:
                if not STACQuery.validate_datetime_str(datestr):
                    raise UP42Error(
                        SupportedErrors.WRONG_INPUT_ERROR,
                        """Time string from time_series could not be validated.
                        It must be one of the following formats:
                        <RFC3339> (for points in time)
                        <RFC3339>/<RFC3339> (for datetime ranges)""",
                    )
        self.time_series = time_series

    def bounds(self) -> BoundingBox:
        """
        Get the bounding box of the query AOI(s) as a BoundingBox object.

        Returns:
            A bounding box object.
        """
        if self.bbox:
            return self.bbox
        elif self.intersects:
            return shapely.geometry.shape(self.intersects).bounds
        elif self.contains:
            return shapely.geometry.shape(self.contains).bounds
        else:
            raise UP42Error(
                SupportedErrors.WRONG_INPUT_ERROR,
                """STACQuery does not contain any of the following query parameters:
                * bbox
                * intersects
                * contains.""",
            )

    def geometry(self) -> Geometry:
        """
        Get the geometry of the query AOI(s) as a GeoJson Polygon object.

        Returns:
            A GeoJson Polygon object
        """
        if self.bbox:
            return json.loads(
                json.dumps(shapely.geometry.mapping(shapely.geometry.box(*self.bbox)))
            )
        elif self.intersects:
            return self.intersects
        elif self.contains:
            return self.contains
        else:
            raise UP42Error(
                SupportedErrors.WRONG_INPUT_ERROR,
                """STACQuery does not contain any of the following query parameters:
                * bbox
                * intersects
                * contains.""",
            )

    def set_param_if_not_exists(self, key: str, value: Any):
        """
        Set a query parameter if it does not exist in the STAC query object.

        Arguments:
            key: An identifier of the parameter
            value: The parameter value to set.
        """
        if not key in self.__dict__:
            self.__dict__[key] = value

    @classmethod
    def from_json(cls, json_data: str) -> STACQuery:
        """
        Get a STACQuery from a json string representation of a query.

        Arguments:
            json_data: String representation of the query.

        Returns:
            A STACQuery object/
        """
        return STACQuery.from_dict(json.loads(json_data))

    @classmethod
    def from_dict(
        cls, dict_data: dict, validator: Callable[[dict], bool] = lambda x: True
    ) -> STACQuery:
        """
        Get a STACQuery from a dict representation of a query.

        Arguments:
            dict_data: Dictionary representation of the query.
            validator: Function used to validate the query.

        Returns:
            A STACQuery object.
        """

        if not validator(dict_data):
            raise UP42Error(
                SupportedErrors.WRONG_INPUT_ERROR,
                """Input Query did not pass validation. Please refer
                to the official block documentation or block specification.""",
            )

        bbox: Optional[BoundingBox] = cast(BoundingBox, dict_data.get("bbox")) if not (
            dict_data.get("bbox") is None
            or dict_data.get("bbox") == ""
            or dict_data.get("bbox") == {}
        ) else None

        intersects: Optional[Geometry] = Geometry(
            **dict_data.get("intersects")
        ) if not (
            dict_data.get("intersects") is None
            or dict_data.get("intersects") == ""
            or dict_data.get("intersects") == {}
        ) else None

        contains: Optional[Geometry] = Geometry(**dict_data.get("contains")) if not (
            dict_data.get("contains") is None
            or dict_data.get("contains") == ""
            or dict_data.get("contains") == {}
        ) else None

        time: Optional[str] = dict_data.get("time") if not dict_data.get(
            "time"
        ) == "" else None
        limit: Optional[int] = dict_data.get("limit") if not dict_data.get(
            "limit"
        ) == "" else None
        ids: Optional[list] = dict_data.get("ids") if not dict_data.get(
            "ids"
        ) == "" else None
        time_series: Optional[list] = dict_data.get("time_series") if not dict_data.get(
            "time_series"
        ) == "" else None

        known_filters = [
            "bbox",
            "intersects",
            "contains",
            "time",
            "limit",
            "geometry",
            "bounds",
            "ids",
            "time_series",
        ]

        truncated_dict_data = {
            key: dict_data[key] for key in dict_data if key not in known_filters
        }

        return STACQuery(
            ids=ids,
            bbox=bbox,
            intersects=intersects,
            contains=contains,
            time=time,
            limit=limit,
            time_series=time_series,
            **truncated_dict_data,
        )

    @staticmethod
    def validate_datetime_str(string: Optional[str]) -> bool:
        """
        Validate a datetime string.

        Arguments:
            string: A datetime string representation.

        Returns:
            If datetime string is valid.
        """
        try:
            if string is None:
                return True
            elif len(str(string).split("/")) == 2:
                ciso8601.parse_datetime(str(string).split("/")[0])
                ciso8601.parse_datetime(str(string).split("/")[1])
            else:
                ciso8601.parse_datetime(str(string))
        except ValueError:
            return False
        return True
