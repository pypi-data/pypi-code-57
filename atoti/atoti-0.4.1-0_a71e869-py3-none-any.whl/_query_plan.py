"""Query plan objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import yaml


@dataclass(frozen=True)
class RetrievalData:
    """Retrieval data."""

    id: int
    retrieval_type: str
    location: str
    measures: List[str]
    start_times: List[int]
    elapsed_times: List[int]
    retrieval_filter: str
    partitioning: str
    measures_provider: str

    def _repr_json_(self) -> Tuple[dict, Dict[str, Any]]:
        """JSON representation."""
        if self.retrieval_type == "NoOpPrimitiveAggregatesRetrieval":
            return (
                dict(),
                {"expanded": False, "root": self.title},
            )

        data = dict()
        data["Location"] = self.location
        data["Measures"] = "[" + ", ".join(self.measures) + "]"
        data["Partitioning"] = self.partitioning
        data["Measures provider"] = self.measures_provider
        data["Start time   (in ms)"] = (
            "[" + ", ".join([str(t) for t in self.start_times]) + "]"
        )
        data["Elapsed time (in ms)"] = (
            "[" + ", ".join([str(t) for t in self.elapsed_times]) + "]"
        )
        return (data, {"expanded": False, "root": self.title})

    @property
    def title(self):
        """Title of this retrieval."""
        return f"Retrieval #{self.id}: {self.retrieval_type}"


class QueryPlan:
    """Query plan."""

    def __init__(
        self,
        infos: Dict[str, Any],
        retrievals: List[RetrievalData],
        dependencies: Dict[int, List[int]],
    ):
        """Init."""
        self.retrievals = {retr.id: retr for retr in retrievals}
        self.infos = infos
        self.dependencies = dependencies

    def _enrich_repr_json(self, retr_id: int) -> Dict[str, Any]:
        """Add the dependencies to the JSON of the retrieval."""
        retr = self.retrievals[retr_id]
        json = retr._repr_json_()
        if retr_id not in self.dependencies:
            return json[0]  # leaf
        dependencies = {
            self.retrievals[id].title: self._enrich_repr_json(id)
            for id in self.dependencies[retr_id]
        }
        return {**json[0], "Dependencies": dependencies}

    def _repr_json_(self) -> Tuple[dict, Dict[str, Any]]:
        """JSON representation."""
        retrievals = {
            retr.title: self._enrich_repr_json(id)
            for id, retr in self.retrievals.items()
            if id in self.dependencies[-1]
        }
        data = {
            "Info": self.infos,
            "Retrievals": retrievals,
        }
        return data, {"expanded": True, "root": f"QueryPlan"}


@dataclass(frozen=True)
class QueryAnalysis:
    """Query Analysis."""

    query_plans: List[QueryPlan]

    def _repr_json_(self) -> Tuple[dict, Dict[str, Any]]:
        data = {
            f"Query plan #{idx}": plan._repr_json_()[0]
            for idx, plan in enumerate(self.query_plans)
        }
        return data, {"expanded": True, "root": f"Query analysis"}

    def __str__(self) -> str:
        """Return string representation of the JSON."""
        return yaml.dump(self._repr_json_()[0], sort_keys=False)
