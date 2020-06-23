from dataclasses import dataclass
from typing import List

from pullframe.types import Demand, Node


@dataclass
class AllSyncFailed(Exception):
    nodes: List[Node]
    demand: Demand

    def __str__(self):
        return f"All sync failed, node: {self.nodes}, req: {self.demand}"


@dataclass
class NoResourceAvailable(Exception):
    demand: Demand

    def __str__(self):
        return "No host available for the demand: {self.demand}"
