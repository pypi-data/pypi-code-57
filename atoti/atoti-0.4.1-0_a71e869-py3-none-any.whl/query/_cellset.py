"""Cellset conversion."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Union

import pandas as pd

from .._serialization_utils import FromDict
from ._discovery import Discovery, dictionarize_cube_dimensions

LevelName = str
MeasureName = str

CubeName = str
DimensionName = str
HierarchyName = str

MeasureValue = Union[float, int, str, None]
MemberIdentifier = str
DataFrameCell = Union[MemberIdentifier, MeasureValue]
DataFrameRow = List[DataFrameCell]
DataFrameData = List[DataFrameRow]
LevelCoordinates = Tuple[HierarchyName, LevelName]
# Any correspond to pd.TimeStamp
# otherwise raise AttributeError: module 'pandas' has no attribute 'TimeStamp'
IndexDataType = Union[str, float, int, Any]

SUPPORTED_DATE_FORMATS = [
    "LocalDate[yyyy-MM-dd]",
    "localDate[yyyy/MM/dd]",
    "localDate[MM-dd-yyyy]",
    "localDate[MM/dd/yyyy]",
    "localDate[dd-MM-yyyy]",
    "localDate[dd/MM/yyyy]",
    "localDate[d-MMM-yyyy]",
    "zonedDateTime[EEE MMM dd HH:mm:ss zzz yyyy]",
]

LOCAL_DATE_REGEX = re.compile(r"[lL]ocalDate\[(.*)\]")

DATE_FORMAT_MAPPING = {
    "yyyy": "%Y",
    "MM": "%m",
    "MMM": "%m",
    "dd": "%d",
    r"^d": "%d",
    "HH": "%H",
    "mm": "%M",
    "ss": "%S",
}


@dataclass(frozen=True)
class CellsetHierarchy(FromDict):
    """Cellset Hierarchy class."""

    dimension: DimensionName
    hierarchy: HierarchyName

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        return CellsetHierarchy(data["dimension"], data["hierarchy"])


@dataclass(frozen=True)
class CellsetMember(FromDict):
    """Cellset Member class."""

    name_path: List[MemberIdentifier]

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        return CellsetMember(data["namePath"])


@dataclass(frozen=True)
class CellsetAxis(FromDict):
    """Cellset Axis class."""

    id: int
    hierarchies: List[CellsetHierarchy]
    positions: List[List[CellsetMember]]

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        return CellsetAxis(
            data["id"],
            [
                CellsetHierarchy._from_dict(hierarchy)
                for hierarchy in data["hierarchies"]
            ],
            [
                [CellsetMember._from_dict(member) for member in position]
                for position in data["positions"]
            ],
        )


@dataclass(frozen=True)
class CellsetCell(FromDict):
    """Cellset Cell class."""

    ordinal: int
    value: MeasureValue

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        return CellsetCell(data["ordinal"], data["value"])


@dataclass(frozen=True)
class CellsetDefaultMember(FromDict):
    """Cellset Default member class."""

    dimension: DimensionName
    hierarchy: HierarchyName
    path: List[MemberIdentifier]

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        return CellsetDefaultMember(data["dimension"], data["hierarchy"], data["path"])


@dataclass(frozen=True)
class Cellset(FromDict):
    """Cellset class."""

    axes: List[CellsetAxis]
    cells: List[CellsetCell]
    cube: CubeName
    default_members: List[CellsetDefaultMember]

    @classmethod
    def _from_dict(cls, data: dict):  # noqa
        return Cellset(
            [CellsetAxis._from_dict(axis) for axis in data["axes"]],
            [CellsetCell._from_dict(cell) for cell in data["cells"]],
            data["cube"],
            [
                CellsetDefaultMember._from_dict(default_member)
                for default_member in data["defaultMembers"]
            ],
        )


def _extract_axes(
    axes: List[CellsetAxis],
) -> Tuple[Optional[CellsetAxis], Optional[CellsetAxis]]:
    non_slicing_axes = [axis for axis in axes if axis.id != -1]
    if len(non_slicing_axes) > 2:
        raise ValueError("Cellset cannot have more than two non-slicing axes")
    columns_axis = None
    rows_axis = None
    for axis in non_slicing_axes:
        if axis.id == 0:
            columns_axis = axis
        else:
            rows_axis = axis
    return (columns_axis, rows_axis)


def _extract_measure_names(
    default_members: List[CellsetDefaultMember], columns_axis: Any, rows_axis: Any
) -> List[str]:
    if not columns_axis:
        if not rows_axis:
            # When there are no axes at all, we get only one cell:
            # the aggregated value of the default measure at the top.
            return [
                next(
                    member.path[0]
                    for member in default_members
                    if member.dimension == "Measures"
                )
            ]
        return []
    if len(columns_axis.hierarchies) > 0 and columns_axis.hierarchies != [
        CellsetHierarchy("Measures", "Measures")
    ]:
        raise ValueError(
            "Cellset must have nothing else but measures on the COLUMNS axis"
        )
    return [position[0].name_path[0] for position in columns_axis.positions]


def _extract_level_count_per_hierarchy(rows_axis: CellsetAxis) -> List[int]:
    level_count_per_hierarchy = []
    for (position_index, position) in enumerate(rows_axis.positions):
        for (hierachy_index, member) in enumerate(position):
            identifier_count = len(member.name_path)
            if position_index == 0:
                level_count_per_hierarchy.insert(hierachy_index, identifier_count)
            elif identifier_count != level_count_per_hierarchy[hierachy_index]:
                raise ValueError("Cellset cannot have grand or sub totals")
    return level_count_per_hierarchy


def _extract_level_coords(
    cube_name: CubeName, rows_axis: Optional[CellsetAxis], discovery: Discovery
) -> List[LevelCoordinates]:
    if not rows_axis:
        return []
    dimensions = dictionarize_cube_dimensions(
        next(
            cube
            for catalog in discovery.catalogs
            for cube in catalog.cubes
            if cube.name == cube_name
        )
    )
    level_count_per_hierarchy = _extract_level_count_per_hierarchy(rows_axis)
    return [
        (hierarchy.hierarchy, level.name)
        for (hierarchy_index, hierarchy) in enumerate(rows_axis.hierarchies)
        for (level_index, level) in enumerate(
            dimensions[hierarchy.dimension][hierarchy.hierarchy].levels
        )
        if level_index < level_count_per_hierarchy[hierarchy_index]
        and level.type != "ALL"
    ]


def _extract_dataframe_data(
    cells: List[CellsetCell],
    measure_names: List[MeasureName],
    rows_axis: Optional[CellsetAxis],
) -> DataFrameData:
    data: DataFrameData = (
        [[None] * len(measure_names) for position in rows_axis.positions]
        if rows_axis
        else [[None] * len(measure_names)]
    )
    if measure_names:
        measure_count = len(measure_names)
        for cell in cells:
            (row_index, column_offset) = divmod(cell.ordinal, measure_count)
            data[row_index][column_offset] = cell.value
    return data


def _format_zoned_date_time(value: str) -> str:
    splitted_value = value.split(" ")
    hour = splitted_value[3].split(":")
    return (
        f"{splitted_value[-1]}"
        f"-{splitted_value[1]}"
        f"-{splitted_value[2]} {hour[0]}"
        f":{hour[1]}"
        f":{hour[2]}"
    )


def _format_to_pandas_type(value_type: str, values: List[Any]) -> List[IndexDataType]:
    """Format values to a specific pandas data type.

    Formated value can be a date, int, float or object.

    Args:
        value_type: String representing ActivePivot type.
        value: value to format.

    Returns:
        Value with the wanted type.

    """
    if value_type in SUPPORTED_DATE_FORMATS:
        try:
            if value_type.lower().startswith("localdate["):
                clean_type = LOCAL_DATE_REGEX.match(value_type).groups()[0]  # type: ignore
                for regex, value in DATE_FORMAT_MAPPING.items():
                    clean_type = re.sub(regex, value, clean_type)
                return [datetime.strptime(value, clean_type) for value in values]
            if value_type.startswith("zonedDateTime["):
                return [
                    datetime.strptime(
                        _format_zoned_date_time(value), "%Y-%b-%d %H:%M:%S"
                    )
                    for value in values
                ]
        except ValueError as err:
            logging.getLogger("atoti.query").warning(
                "Failed to convert type %s to a pandas date, using string instead. %s",
                value_type,
                err,
            )
    if value_type in ["int", "float"]:
        return pd.to_numeric(values)
    return values


def _extract_multi_index_data(
    rows_axis: CellsetAxis, level_data_types: List[str],
) -> List[List[IndexDataType]]:
    """Convert an MDX cellsetAxis to a list of list of Index data.

    Each level correspond to an index column.
    Generate a list of list containing index data column to be
    able to use pd.MultiIndex.from_arrays.

    Args:
        rows_axis: CellsetAxis
        level_data_types: list of level data types

    Returns:
        List of list, each sublist correspond to an index column containing formated index data.
        example: [
            [Continent1, Continent1, Continent2],
            [Continent1.city1, Continent1.city, Continent2.city1]
        ]

    """
    index_data: List[List[str]] = [[] for k in level_data_types]
    for position in rows_axis.positions:
        index_data = _add_row_to_index_data(index_data, position)
    return [
        _format_to_pandas_type(level_data_type, index_data[index])
        for index, level_data_type in enumerate(level_data_types)
    ]


def _add_row_to_index_data(
    df_index_columns: List[List[str]], position: List[CellsetMember]
) -> List[List[str]]:
    """Add a value to each sub array of index data.

    It is equivalent to add a row in the index

    Args:
        df_index_columns: dataframe index data array
        position: list of cellset members
                    Position is a list of CellsetMember from the higher level to the deeper one.
                    For instance [Continent, Country, City, ...]
                    position = [CellsetMember(name_path=['AllMember', 'Level']), ...]

    Returns:
        List of list, each sublist correspond to an index column

    """
    # List of values for a row sorted by columns order of the index [value_col_1, value_col_2, ...]
    row_values = []
    for cellset_member in position:
        name_path = cellset_member.name_path
        if name_path[0] == "AllMember":
            name_path.pop(0)
        row_values += name_path
    # Fill df_index_columns column after column
    for i, column in enumerate(df_index_columns):
        column.append(row_values[i])
    return df_index_columns


def _create_dataframe_multi_index(
    level_coords: List[Tuple[MemberIdentifier, MemberIdentifier]],
    level_data_types: List[str],
    rows_axis: Optional[CellsetAxis],
) -> Optional[pd.Index]:
    """Convert an MDX cellsetAxis to a pandas DataFrameIndex.

    Use level description type to convert index in the good pandas format.
    Index data is an array of arrays containing index values.

    Args:
        level_coords: level coordinates ((hierarchy, level)) of the indexes
        rows_axis: optional cellset_axis
                [
                    id = int,
                    Hierarchies = [
                        CellsetHierarchy(dimension='Hierarchies', hierarchy='Name'),
                        ...],
                    positions =  [...],
                ]
        level_data_types: list of types matching the list of level names

    Returns:
        a pandas MultiIndex

    """
    number_of_levels = len(level_coords)
    index_data = [[] for k in range(number_of_levels)]
    if rows_axis:
        index_data = _extract_multi_index_data(rows_axis, level_data_types)
    return pd.MultiIndex.from_arrays(
        index_data, names=[level_coord[1] for level_coord in level_coords]
    )


def _extract_dataframe_index(
    level_coords: List[LevelCoordinates],
    level_data_types: List[str],
    rows_axis: Optional[CellsetAxis],
) -> Optional[pd.Index]:
    """Convert an MDX cellsetAxis to a pandas DataFrameIndex.

    Args:
        level_coords: list of coordinates of the indexes
        rows_axis: optional cellset_axis
        level_data_types: list of types matching the list of level names

    Returns:
        a pandas Index or MultiIndex

    """
    number_of_levels = len(level_coords)
    if number_of_levels > 1:
        return _create_dataframe_multi_index(level_coords, level_data_types, rows_axis)
    if number_of_levels == 1:
        index_data: List[str] = (
            [
                identifier
                for position in rows_axis.positions
                for member in position
                for identifier in member.name_path
                if identifier != "AllMember"
            ]
            if rows_axis
            else []
        )
        return pd.Index(
            _format_to_pandas_type(level_data_types[0], index_data),
            name=level_coords[0][1],
        )
    return None


def cellset_to_pandas(
    cellset: Cellset,
    discovery: Discovery,
    get_level_data_types: Optional[
        Callable[[str, List[LevelCoordinates]], List[str]]
    ] = None,
) -> pd.DataFrame:
    """Convert an MDX cellset to a pandas DataFrame.

    Requirements to guarantee that the DataFrame is well shaped:
      - no more than two axes
      - no grand or sub totals
      - nothing else but measures on the COLUMNS axis

    Args:
        cellset: the MDX cellset
        discovery: the discovery of the corresponding server
        get_level_data_types: return the list of types matching the list of level names

    Returns:
        the resulting DataFrame

    """
    (columns_axis, rows_axis) = _extract_axes(cellset.axes)
    measure_names = _extract_measure_names(
        cellset.default_members, columns_axis, rows_axis
    )
    if not cellset.cells or (not columns_axis and not rows_axis):
        data = [cellset.cells[0].value] if cellset.cells else []
        return pd.DataFrame(data, columns=measure_names)
    level_coords = _extract_level_coords(cellset.cube, rows_axis, discovery)
    level_data_types = (
        get_level_data_types(cellset.cube, level_coords)
        if get_level_data_types
        else ["object"] * len(level_coords)
    )
    index = _extract_dataframe_index(level_coords, level_data_types, rows_axis)
    data = _extract_dataframe_data(cellset.cells, measure_names, rows_axis)
    return pd.DataFrame(data, columns=measure_names, index=index)
