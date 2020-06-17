"""LiteralMeasure class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .._py4j_utils import as_java_object
from ..measure import LiteralMeasureValue, Measure

if TYPE_CHECKING:
    from ..cube import Cube
    from .._java_api import JavaApi


@dataclass(eq=False)
class LiteralMeasure(Measure):
    """A measure equal to a literal value."""

    _value: LiteralMeasureValue

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        val = as_java_object(java_api.gateway, self._value)
        distilled_name = java_api.constant_measure(cube, measure_name, val)
        return distilled_name
