"""Aggregation measure over a scope."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..hierarchy import Hierarchy
from ..measure import Measure

if TYPE_CHECKING:
    from ..cube import Cube
    from ..level import Level
    from .._java_api import JavaApi


@dataclass(eq=False)
class SiblingsAggregationMeasure(Measure):
    """Aggregation measure over a scope."""

    _underlying_measure: Measure
    _agg_fun: str
    _hierarchy: Hierarchy
    _exclude_self: bool = False

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measure
        underlying_name = self._underlying_measure._distil(java_api, cube, None)
        distilled_name = java_api.agg_siblings(
            cube,
            measure_name,
            underlying_name,
            self._hierarchy,
            self._agg_fun,
            self._exclude_self,
        )
        return distilled_name


@dataclass(eq=False)
class WindowAggregationMeasure(Measure):
    """Aggregation measure over a scope."""

    _underlying_measure: Measure
    _agg_fun: str
    _level: Level
    _partitioning: Optional[Level]
    _window: Optional[range]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measure
        underlying_name = self._underlying_measure._distil(java_api, cube, None)
        distilled_name = java_api.window_aggregation_measure(
            cube,
            measure_name,
            underlying_name,
            self._level._java_description,  # pylint: disable=protected-access
            self._partitioning,
            self._window,
            self._agg_fun,
        )
        return distilled_name
