"""Query hierarchy."""

from dataclasses import dataclass
from typing import Any, Tuple

from .._docs_utils import HIERARCHY_ISIN_DOC, doc
from .._hierarchy_isin_conditions import (
    HierarchyIsInCondition,
    create_condition_from_member_paths,
)
from .._mappings import ImmutableMapping
from .._repr_utils import convert_repr_json_to_html, repr_json_hierarchy
from .level import QueryLevel


@dataclass(frozen=True)
class QueryHierarchy:
    """Hierarchy for query cube."""

    name: str
    dimension: str
    levels: ImmutableMapping[str, QueryLevel]
    slicing: bool

    @doc(HIERARCHY_ISIN_DOC)
    def isin(self, *member_paths: Tuple[Any, ...]) -> HierarchyIsInCondition:
        return create_condition_from_member_paths(self, *member_paths)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_hierarchy(self)
