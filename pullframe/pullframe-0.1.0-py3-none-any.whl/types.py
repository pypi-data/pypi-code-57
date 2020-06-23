from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel  # type: ignore


class CacheFormat(str, Enum):
    PYTABLES = "PyTables"


class Node(BaseModel):
    host: str
    directory: str


class Demand(BaseModel):
    cache_format: CacheFormat
    name: str
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class Request(BaseModel):
    source: Node
    directory: str
    demand: Demand


class Resource(BaseModel):
    nodes: List[Node]
    version: int
    last_idx: datetime
