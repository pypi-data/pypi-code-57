"""Store measure."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..store import Column, Store


@dataclass(eq=False)
class StoreMeasure(Measure):
    """Measure based on the column of a store."""

    _column: Column
    _agg_fun: Optional[str]
    _store: Store = field(repr=False)

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        agg_fun = self._agg_fun or "SINGLE_VALUE_NULLABLE"
        levels = (
            []
            if self._agg_fun
            else [cube.levels[column] for column in self._store.keys]
        )
        distilled_name = java_api.aggregated_measure(
            cube, measure_name, self._store.name, self._column.name, agg_fun, levels
        )
        return distilled_name
