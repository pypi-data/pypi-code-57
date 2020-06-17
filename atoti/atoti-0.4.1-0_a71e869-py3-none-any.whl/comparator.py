"""Level comparators."""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass(frozen=True)
class Comparator:
    """Level comparator."""

    _name: str
    _first_members: Optional[List[Any]]


ASC = Comparator("ASC", None)
DESC = Comparator("DESC", None)


def first_members(members: List[Any]) -> Comparator:
    """Create a level comparator with the given first members."""
    return Comparator("FIRST", members)
