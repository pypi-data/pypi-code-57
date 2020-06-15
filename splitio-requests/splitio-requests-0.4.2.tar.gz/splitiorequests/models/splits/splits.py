from dataclasses import dataclass
from typing import List
from splitiorequests.models.splits.split import Split


@dataclass
class Splits:
    objects: List[Split]
    offset: int
    limit: int
    totalCount: int
