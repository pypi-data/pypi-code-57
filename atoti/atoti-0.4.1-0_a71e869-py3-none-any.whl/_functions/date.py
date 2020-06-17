"""Date functions."""

from __future__ import annotations

import datetime
from typing import Union

from typing_extensions import Literal

from .._measures.calculated_measure import CalculatedMeasure, Operator
from .._type_utils import check_literal
from ..measure import Measure, _convert_to_measure

DateOrMeasure = Union[Measure, datetime.date, datetime.datetime]

_Unit = Literal[  # pylint: disable=invalid-name
    "seconds", "minutes", "hours", "days", "weeks", "months", "years"
]


def date_diff(
    from_date: DateOrMeasure, to_date: DateOrMeasure, *, unit: _Unit = "days",
) -> Measure:
    """Return a measure equal to the difference between two dates.

    Args:
        from_date: The first date measure or object.
        to_date: The second date measure or object.
        unit: The difference unit.
            Seconds, minutes and hours are only allowed if the dates contain time information.
    """
    check_literal("unit", unit, _Unit)
    return CalculatedMeasure(
        Operator(
            "datediff",
            [_convert_to_measure(from_date), _convert_to_measure(to_date), unit],
        )
    )
