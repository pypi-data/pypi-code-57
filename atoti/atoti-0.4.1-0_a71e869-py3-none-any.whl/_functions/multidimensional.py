"""Multidimensional operations using parents, siblings, children, etc."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping, Optional, Union, cast

from typing_extensions import Literal

from atoti.vendor.atotipy4j.protocol import JAVA_MAX_INT

from .._measures.utils import get_measure_name
from .._py4j_utils import as_java_object
from .._type_utils import check_literal
from ..hierarchy import Hierarchy
from ..level import Level
from ..measure import Measure, MeasureLike

if TYPE_CHECKING:
    from ..cube import Cube
    from .._java_api import JavaApi


@dataclass(eq=False)
class ParentValue(Measure):
    """The value of the measure for the parent."""

    _underlying_measure: Union[Measure, str]
    _hierarchy: Hierarchy
    _total_value: Optional[MeasureLike]
    _apply_filters: bool
    _degree: int

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_name = (
            self._underlying_measure
            if isinstance(self._underlying_measure, str)
            else get_measure_name(java_api, self._underlying_measure, cube)
        )
        total_measure_name = (
            self._total_value._distil(java_api, cube, None)
            if isinstance(self._total_value, Measure)
            else None
        )
        total_literal = self._total_value if total_measure_name is None else None

        distilled_name = java_api.parent_value(
            cube,
            measure_name,
            underlying_name,
            self._hierarchy,
            total_measure_name,
            total_literal,
            self._apply_filters,
            self._degree,
        )
        return distilled_name


def parent_value(
    measure: Union[Measure, str],
    on: Hierarchy,
    *,
    apply_filters: bool = False,
    degree: int = 1,
    total_value: Optional[MeasureLike] = None,
) -> Measure:
    """Return a measure equal to the passed measure at the parent member on the given hierarchy.

    Example:
        Measure definitions::

            m1 = parent_value(Quantity.SUM, Date)
            m2 = parent_value(Quantity.SUM, Date, degree=3)
            m3 = parent_value(Quantity.SUM, Date, degree=3, total_value=Quantity.SUM))
            m4 = parent_value(Quantity.SUM, Date, degree=3, total_value=Other.SUM))

        Considering a non slicing hierarchy ``Date`` with three levels ``Years``, ``Month`` and ``Day``:

        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        | Year       | Month | Day | Quantity.SUM | Other.SUM | m1    | m2    | m3    | m4    |
        +============+=======+=====+==============+===========+=======+=======+=======+=======+
        | 2019       |       |     | 75           | 1000      | 110   | null  | 110   | 1500  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  7    |     | 35           | 750       | 75    | null  | 110   | 1500  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 15           | 245       | 35    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 20           | 505       | 35    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  6    |     | 40           | 250       | 75    | null  | 110   | 1500  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 25           | 115       | 40    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 15           | 135       | 40    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        | 2018       |       |     | 35           | 500       | 110   | null  | 110   | 1500  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  7    |     | 15           | 200       | 35    | null  | 110   | 1500  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 5            | 55        | 15    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 10           | 145       | 15    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  6    |     | 20           | 300       | 35    | null  | 110   | 1500  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 15           | 145       | 20    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 5            | 155       | 20    | 110   | 110   | 110   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+

        Considering a slicing hierarchy ``Date`` with three levels ``Years``, ``Month`` and ``Day``:

        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        | Year       | Month | Day | Quantity.SUM | Other.SUM | m1    | m2    | m3    | m4    |
        +============+=======+=====+==============+===========+=======+=======+=======+=======+
        | 2019       |       |     | 75           | 1000      | 75    | null  | 75    | 1000  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  7    |     | 35           | 750       | 75    | null  | 75    | 1000  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 15           | 245       | 35    | 75    | 75    | 75    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 20           | 505       | 35    | 75    | 75    | 75    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  6    |     | 40           | 250       | 75    | null  | 75    | 1000  |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 25           | 115       | 40    | 75    | 75    | 75    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 15           | 135       | 40    | 75    | 75    | 75    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        | 2018       |       |     | 35           | 500       | 35    | null  | 35    | 500   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  7    |     | 15           | 200       | 35    | null  | 35    | 500   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 5            | 55        | 15    | 35    | 35    | 35    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 10           | 145       | 15    | 35    | 35    | 35    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |  6    |     | 20           | 300       | 35    | null  | 35    | 500   |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 1   | 15           | 145       | 20    | 35    | 35    | 35    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+
        |            |       | 2   | 5            | 155       | 20    | 35    | 35    | 35    |
        +------------+-------+-----+--------------+-----------+-------+-------+-------+-------+

    Args:
        measure: The measure to take the parent value of.
        on: The hierarchy to drill up to take the parent value.
        apply_filters: Whether to apply the query filters when computing the
            value at the parent member.
        degree: The number of levels to go up to take the value on. A value
            of ``1`` as parent_degree will do a one step drill up in the hierarchy.
        total_value: The value to take when the drill up went above the top level of the hierarchy.

    """
    return ParentValue(measure, on, total_value, apply_filters, degree,)


def total(measure: Measure, on: Hierarchy,) -> Measure:
    """Return a measure equal to the measure on the top level member on each hierarchy member.

    It ignores the filters on this hierarchy.

    If the hierarchy is not slicing, total is equal to the value for all the members.
    If the hierarchy is slicing, total is equal to the value on the first level.

    Example:
        Considering a hierarchy ``Date`` with three levels ``Year, Month and Day``. In the first
        case ``Date`` is not slicing. In the second case Date is slicing.

        +------------+-------+-----+-------+----------------------------+------------------------+
        | Year       | Month | Day | Price |  total(Price) NON SLICING  |  total(Price) SLICING  |
        +============+=======+=====+=======+============================+========================+
        | 2019       |       |     | 75.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |  7    |     | 35.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 1   | 15.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 2   | 20.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |  6    |     | 40.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 1   | 25.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 2   | 15.0  | 110.0                      |  75.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        | 2018       |       |     | 35.0  | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |  7    |     | 15.0  | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 1   | 5.0   | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 2   | 10.0  | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |  6    |     | 20.0  | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 1   | 15.0  | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+
        |            |       | 2   | 5.0   | 110.0                      |  35.0                  |
        +------------+-------+-----+-------+----------------------------+------------------------+

    Args:
        measure: The measure to take the total of.
        on: The hierarchy on which to find the top-level member.

    """
    return ParentValue(measure, on, measure, False, JAVA_MAX_INT)


@dataclass(eq=False)
class Shift(Measure):
    """Shift the value."""

    _underlying_measure: Measure
    _hierarchy: Hierarchy
    _offset: int

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_name = get_measure_name(java_api, self._underlying_measure, cube)
        distilled_name = java_api.shift(
            cube, measure_name, underlying_name, self._hierarchy, self._offset
        )
        return distilled_name


def shift(measure: Measure, on: Level, *, offset: int = 1) -> Measure:
    """Return a measure equal to the passed measure shifted to another member.

    Args:
        measure: The measure to shift.
        on: The level to shift on.
        offset: The amount of members to shift by.

    """
    hier = cast(Hierarchy, on._hierarchy)  # pylint: disable=protected-access
    return Shift(measure, hier, offset)


@dataclass(eq=False)
class DateShift(Measure):
    """Shift the value."""

    _underlying_measure: Measure
    _hierarchy_name: str
    _shift: str
    _method: str

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_name = get_measure_name(java_api, self._underlying_measure, cube)
        levels = cube.hierarchies[self._hierarchy_name].levels
        level = list(levels.values())[-1]
        distilled_name = java_api.date_shift(
            cube, measure_name, underlying_name, level, self._shift, self._method
        )
        return distilled_name


_DateShiftMethod = Literal[  # pylint: disable=invalid-name
    "exact", "previous", "following", "interpolate"
]


def date_shift(  # pylint: disable=invalid-name
    measure: Measure, on: Hierarchy, offset: str, *, method: _DateShiftMethod = "exact",
) -> Measure:
    # pylint: disable=line-too-long
    """Return a measure equal to the passed mesure shifted to another date.

    Args:
        measure: The measure to shift.
        on: The hierarchy to shift on.
        offset: The offset of the form ``xxDxxWxxMxxQxxY`` to shift by.
            Only the ``D``, ``W``, ``M``, ``Q``, and ``Y`` offset aliases are supported.
            Offset aliases have the `same meaning as Pandas' <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`_.
        method: Determine the value to use when there is no member at the shifted date:

            * ``exact``: ``None``.
            * ``previous``: Value at the previous existing date.
            * ``following``: Value at the following existing date.
            * ``interpolate``: Linear interpolation of the values at the previous and following existing dates:

                Example::

                    m2 = atoti.date_shift("m1", on=h["date"], offset="1M", method="interpolate")

                +------------+----+-------+----------------------------------------------------------------------------+
                |    date    | m1 |   m2  |                         explanation                                        |
                +============+====+=======+============================================================================+
                | 2000-01-05 | 15 | 10.79 | linear interpolation of 2000-02-03's 10 and 2000-03-03's 21 for 2000-02-05 |
                +------------+----+-------+----------------------------------------------------------------------------+
                | 2000-02-03 | 10 |    21 | exact match at 2000-03-03: no need to interpolate                          |
                +------------+----+-------+----------------------------------------------------------------------------+
                | 2000-03-03 | 21 |  9.73 | linear interpolation of 2000-03-03's 21 and 2000-04-05's 9 for 2000-04-03  |
                +------------+----+-------+----------------------------------------------------------------------------+
                | 2000-04-05 |  9 |     ∅ | no record after 2000-04-05: cannot interpolate                             |
                +------------+----+-------+----------------------------------------------------------------------------+

    """
    # pylint: enable=line-too-long
    check_literal("method", method, _DateShiftMethod)
    return DateShift(measure, on.name, offset, method)


@dataclass(eq=False)
class AtMeasure(Measure):
    """Measure at a given position."""

    _underlying_measure: Measure
    _coordinates: Mapping[Level, Any]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        conditions = {
            level: as_java_object(java_api.gateway, value)
            for level, value in self._coordinates.items()
        }
        underlying_name = get_measure_name(java_api, self._underlying_measure, cube)
        distilled_name = java_api.at_level(
            cube, measure_name, underlying_name, conditions
        )
        return distilled_name


def at(measure: Measure, coordinates: Mapping[Level, Any]):
    """Return a measure equal to the passed measure at some other coordinates of the cube.

    Args:
        measure: The measure to take at other coordinates.
        coordinates: A ``{level_to shift_on: value_to_shift_to}`` mapping.
            Values can either be:

            * A literal matching an existing member of the key level::

                # Return the value of Quantity for France on each member of the Country level.
                atoti.at(m["Quantity"], {lvl["Country"]: "France"})

            * Another level whose current member the key level will be shifted to::

                # Return the value of Quantity for the current member
                # of the Target Country and Target City levels.
                atoti.at(m["Quantity"], {
                    lvl["Country"]: lvl["Target Country"],
                    lvl["City"]: lvl["Target City"],
                })

              If this other level is not expressed, the shifting will not be done.

    """
    return AtMeasure(measure, coordinates)
