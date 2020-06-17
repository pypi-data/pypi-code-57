"""Query measure."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QueryMeasure:
    """Query measure."""

    name: str
    visible: bool
    folder: Optional[str]
    formatter: Optional[str]
