"""Cellset conversion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .._serialization_utils import FromDict

LevelName = str
MeasureName = str

CubeName = str
DimensionName = str
HierarchyName = str

MemberIdentifier = str


@dataclass(frozen=True)
class DiscoveryLevel(FromDict):
    """DiscoveryLevel class."""

    name: str
    type: str

    @classmethod
    def _from_dict(cls, data: dict):
        return DiscoveryLevel(data["name"], data["type"])


@dataclass(frozen=True)
class DiscoveryHierarchy(FromDict):
    """DiscoveryHierarchy class."""

    levels: List[DiscoveryLevel]
    name: HierarchyName
    slicing: bool

    @classmethod
    def _from_dict(cls, data: dict):
        return DiscoveryHierarchy(
            [DiscoveryLevel._from_dict(level) for level in data["levels"]],
            data["name"],
            data["slicing"],
        )


@dataclass(frozen=True)
class DiscoveryDimension(FromDict):
    """DiscoveryDimension class."""

    hierarchies: List[DiscoveryHierarchy]
    name: DimensionName

    @classmethod
    def _from_dict(cls, data: dict):
        return DiscoveryDimension(
            [
                DiscoveryHierarchy._from_dict(hierarchy)
                for hierarchy in data["hierarchies"]
            ],
            data["name"],
        )


@dataclass(frozen=True)
class DiscoveryMeasure(FromDict):
    """DiscoveryMeasure class."""

    name: DimensionName
    visible: bool
    folder: Optional[str]
    formatter: Optional[str]

    @classmethod
    def _from_dict(cls, data: dict):
        return DiscoveryMeasure(
            data["name"], data["visible"], data.get("folder"), data.get("formatString"),
        )


@dataclass(frozen=True)
class DiscoveryCube(FromDict):
    """DiscoveryCube class."""

    dimensions: List[DiscoveryDimension]
    measures: List[DiscoveryMeasure]
    name: CubeName

    @classmethod
    def _from_dict(cls, data: dict):
        return DiscoveryCube(
            [
                DiscoveryDimension._from_dict(dimension)
                for dimension in data["dimensions"]
            ],
            [DiscoveryMeasure._from_dict(measure) for measure in data["measures"]]
            if "measures" in data
            else [],
            data["name"],
        )


@dataclass(frozen=True)
class DiscoveryCatalog(FromDict):
    """DiscoveryCatalog class."""

    cubes: List[DiscoveryCube]

    @classmethod
    def _from_dict(cls, data: dict):
        return DiscoveryCatalog(
            [DiscoveryCube._from_dict(cube) for cube in data["cubes"]]
        )


@dataclass(frozen=True)
class Discovery(FromDict):
    """Discovery class."""

    catalogs: List[DiscoveryCatalog]

    @classmethod
    def _from_dict(cls, data: dict):
        return Discovery(
            [DiscoveryCatalog._from_dict(catalog) for catalog in data["catalogs"]]
        )


DiscoveryHierarchyDict = Dict[HierarchyName, DiscoveryHierarchy]
DiscoveryDimensionDict = Dict[DimensionName, DiscoveryHierarchyDict]


def _dictionarize_dimension_hierarchies(
    dimension: DiscoveryDimension,
) -> DiscoveryHierarchyDict:
    """Make access to hierarchy by name more efficient."""
    return {hierarchy.name: hierarchy for hierarchy in dimension.hierarchies}


def dictionarize_cube_dimensions(cube: DiscoveryCube) -> DiscoveryDimensionDict:
    """Make access to dimension by name more efficient."""
    return {
        dimension.name: _dictionarize_dimension_hierarchies(dimension)
        for dimension in cube.dimensions
    }
