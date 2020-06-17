"""Measures calculating members for which extrema are reached."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..level import Level
from ..measure import Measure
from .utils import get_measure_name

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


@dataclass(eq=False)
class MaxMemberMeasure(Measure):
    """Member of the level for which the maximum of the underlying measure is reached."""

    _underlying: Measure
    _level: Level

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_measure = get_measure_name(java_api, self._underlying, cube)
        distilled_name = java_api.max_member(
            cube, measure_name, underlying_measure, self._level
        )
        return distilled_name


@dataclass(eq=False)
class MinMemberMeasure(Measure):
    """Member of the level for which the minimum of the underlying measure is reached."""

    _underlying: Measure
    _level: Level

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_measure = get_measure_name(java_api, self._underlying, cube)
        distilled_name = java_api.min_member(
            cube, measure_name, underlying_measure, self._level
        )
        return distilled_name
