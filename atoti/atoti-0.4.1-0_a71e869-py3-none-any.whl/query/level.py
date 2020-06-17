"""Query level."""

from dataclasses import dataclass
from typing import Any

from .._docs_utils import LEVEL_ISIN_DOC, doc
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from ..measure import Measure


@dataclass(frozen=True)
class QueryLevel:
    """Level for query cube."""

    name: str
    dimension: str
    hierarchy: str

    @doc(LEVEL_ISIN_DOC)
    def isin(self, *members: Any) -> LevelIsInCondition:
        if None in members:
            raise ValueError("None is not supported in isin conditions.")
        return LevelIsInCondition(self, list(members))

    def __eq__(self, other: Any) -> LevelCondition:
        """Return an equality condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "eq")

    def __ne__(self, other: Any):
        """Not supported."""
        # Explicitly implemented so that Python doesn't just silently return False.
        raise NotImplementedError(
            "Query level conditions can only be based on equality (==)."
        )

    @property
    def _java_description(self) -> str:  # noqa: D401
        """Description for java."""
        return f"{self.name}@{self.hierarchy}@{self.dimension}"
