"""Measure functions."""

from __future__ import annotations

from typing import Optional, Union

from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._measures.boolean_measure import BooleanMeasure
from .._measures.calculated_measure import CalculatedMeasure, Operator
from .._measures.filtered_measure import LevelValueFilteredMeasure, WhereMeasure
from .._measures.rank_measure import RankMeasure
from .._multi_condition import MultiCondition
from ..hierarchy import Hierarchy
from ..measure import Measure, MeasureLike, _convert_to_measure


def max(*measures: MeasureLike) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the maximum of the passed arguments."""
    if len(measures) < 2:
        raise ValueError(
            "This function is not made to compute the maximum of a single measure."
            " To find the maximum value of this measure on the levels it is expressed,"
            " use atoti.agg.max() instead."
        )
    return CalculatedMeasure(
        Operator("max", [_convert_to_measure(measure) for measure in measures])
    )


def min(*measures: MeasureLike) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the minimum of the passed arguments."""
    if len(measures) < 2:
        raise ValueError(
            "You can not calculate the min of a single measure using this function. "
            "If you want to find the minimum value of this measure on the levels it is defined on, "
            "please use atoti.agg.min"
        )
    return CalculatedMeasure(
        Operator("min", [_convert_to_measure(measure) for measure in measures])
    )


def abs(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the absolute value of the passed measure."""
    return CalculatedMeasure(Operator("abs", [measure]))


def exp(measure: Measure) -> Measure:
    """Return a measure equal to the exponential value of the passed measure."""
    return CalculatedMeasure(Operator("exp", [measure]))


def log(measure: Measure) -> Measure:
    """Return a measure equal to the natural logarithm (base *e*) of the passed measure."""
    return CalculatedMeasure(Operator("log", [measure]))


def log10(measure: Measure) -> Measure:
    """Return a measure equal to the base 10 logarithm of the passed measure."""
    return CalculatedMeasure(Operator("log10", [measure]))


def floor(measure: Measure) -> Measure:
    """Return a measure equal to the largest integer <= to the passed measure."""
    return CalculatedMeasure(Operator("floor", [measure]))


def ceil(measure: Measure) -> Measure:
    """Return a measure equal to the smallest integer that is >= to the passed measure."""
    return CalculatedMeasure(Operator("ceil", [measure]))


def round(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the closest integer to the passed measure."""
    return CalculatedMeasure(Operator("round", [measure]))


def sin(measure: Measure) -> Measure:
    """Return a measure equal to the sine of the passed measure in radians."""
    return CalculatedMeasure(Operator("sin", [measure]))


def cos(measure: Measure) -> Measure:
    """Return a measure equal to the cosine of the passed measure in radians."""
    return CalculatedMeasure(Operator("cos", [measure]))


def tan(measure: Measure) -> Measure:
    """Return a measure equal to the tangent of the passed measure in radians."""
    return CalculatedMeasure(Operator("tan", [measure]))


def sqrt(measure: Measure) -> Measure:
    """Return a measure equal to the square root of the passed measure."""
    return measure ** 0.5


def filter(  # pylint: disable=redefined-builtin
    measure: MeasureLike,
    condition: Union[
        LevelCondition, MultiCondition, LevelIsInCondition, HierarchyIsInCondition
    ],
) -> Measure:
    """Return a filtered measure.

    The new measure is equal to the passed one where the condition is ``True``
    and to ``None`` elsewhere.

    Different types of conditions are supported:

    * Levels compared to levels::

        lvl["source"] == lvl["destination"]

    * Levels compared to literals::

        lvl["city"] == "Paris"

    * A conjunction of conditions using the ``&`` operator::

        (lvl["source"] == lvl["destination"]) & (lvl["city"] == "Paris")

    Args:
        measure: The measure to filter.
        condition: The condition to evaluate.

    """
    measure = _convert_to_measure(measure)
    if isinstance(condition, BooleanMeasure):
        raise ValueError("Use atoti.where() for conditions with measures.")

    if isinstance(condition, LevelCondition):
        return LevelValueFilteredMeasure(measure, _level_conditions=[condition])

    if isinstance(condition, LevelIsInCondition):
        return LevelValueFilteredMeasure(measure, _level_isin_conditions=[condition])

    if isinstance(condition, HierarchyIsInCondition):
        return LevelValueFilteredMeasure(
            measure, _hierarchy_isin_conditions=[condition]
        )

    # We only allow the use of level conditions
    if condition._measure_conditions:  # pylint: disable=protected-access
        raise ValueError("Use atoti.where() for conditions with measures.")

    # pylint: disable=protected-access
    return LevelValueFilteredMeasure(
        measure,
        condition._level_conditions if condition._level_conditions else None,
        condition._level_isin_conditions if condition._level_isin_conditions else None,
        condition._hierarchy_isin_condition
        if condition._hierarchy_isin_condition
        else None,
    )


def where(
    condition: Union[
        BooleanMeasure,
        LevelCondition,
        MultiCondition,
        HierarchyIsInCondition,
        LevelIsInCondition,
    ],
    true_measure: MeasureLike,
    # Not keyword-only to be symmetrical with true_measure and because
    # there probably will not be more optional parameters.
    false_measure: Optional[MeasureLike] = None,
) -> Measure:
    """Return a conditional measure.

    This function is like an *if-then-else* statement:

    * Where the condition is ``True``, the new measure will be equal to ``true_measure``.
    * Where the condition is ``False``, the new measure will be equal to ``false_measure``.

    Different types of conditions are supported:

    * Measures compared to anything measure-like::

        m["Test"] == 20

    * Levels compared to levels::

        lvl["source"] == lvl["destination"]

    * Levels compared to literals::

        lvl["city"] == "Paris"

    * A conjunction of conditions using the ``&`` operator::

        (m["Test"] == 20) & (lvl["city"] == "Paris")

    Args:
        condition: The condition to evaluate.
        true_measure: The measure to propagate where the condition is ``True``.
        false_measure: The measure to propagate where the condition is ``False``.

    """
    # Collect the measure conditions.
    measure_conditions = []

    if isinstance(condition, BooleanMeasure):
        measure_conditions.append(condition)

    elif isinstance(
        condition, (LevelCondition, HierarchyIsInCondition, LevelIsInCondition)
    ):
        measure_conditions.append(condition._to_measure())

    elif isinstance(condition, MultiCondition):
        # condition._... is empty nothing happen
        measure_conditions.extend(
            [
                level_condition._to_measure()
                for level_condition in condition._level_conditions  # pylint: disable=protected-access
            ]
            + [
                hierarchy_isin_condition._to_measure()
                for hierarchy_isin_condition in condition._hierarchy_isin_condition  # pylint: disable=protected-access
            ]
            + [
                level_isin_condition._to_measure()
                for level_isin_condition in condition._level_isin_conditions  # pylint: disable=protected-access
            ]
            + list(condition._measure_conditions)  # pylint: disable=protected-access
        )

    else:
        raise ValueError(
            "Incorrect condition type."
            f" Expected {Union[BooleanMeasure, LevelCondition, MultiCondition]}"
            f" but got {type(condition)}."
        )

    return WhereMeasure(
        _convert_to_measure(true_measure),
        _convert_to_measure(false_measure) if false_measure is not None else None,
        measure_conditions,
    )


def conjunction(*measures: BooleanMeasure) -> BooleanMeasure:
    """Return a measure equal to the logical conjunction of the passed measures."""
    return BooleanMeasure("and", measures)


def rank(
    measure: Measure,
    hierarchy: Hierarchy,
    ascending: bool = True,
    apply_filters: bool = True,
):
    """Return a measure equal to the rank of a hierarchy's members according to a reference measure.

    Members with equal values are further ranked using the level comparator.

    Example::

        m2 = atoti.rank(m1, hierarchy["date"])

    +------+-------+-----+----+----+------------------------------------------------------+
    | Year | Month | Day | m1 | m2 |                        Comments                      |
    +======+=======+=====+====+====+======================================================+
    | 2000 |       |     | 90 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |   01  |     | 25 |  2 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  01 | 15 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  02 | 10 |  2 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |   02  |     | 50 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  01 | 30 |  1 | same value as 2000/02/05 but this member comes first |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  03 | 20 |  3 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  05 | 30 |  2 |  same value as 2000/02/01 but this member comes last |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |   04  |     | 15 |  3 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  05 |  5 |  2 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+
    |      |       |  05 | 10 |  1 |                                                      |
    +------+-------+-----+----+----+------------------------------------------------------+

    Args:
        measure: The measure on which the ranking is done.
        hierarchy: The hierarchy containing the members to rank.
        ascending: When set to ``False``, the 1st place goes to the member with greatest value.
        apply_filters: When ``True``, query filters will be applied before ranking members. When
        ``False``, query filters will be applied after the ranking, resulting in "holes" in the
        ranks.
    """
    return RankMeasure(measure, hierarchy, ascending, apply_filters)
