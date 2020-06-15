from dataclasses import dataclass
from typing import List, Optional
from splitiorequests.models.splits.traffic_type import TrafficType
from splitiorequests.models.splits.tag import Tag


@dataclass
class Split:
    name: str
    description: Optional[str] = None
    trafficType: Optional[TrafficType] = None
    creationTime: Optional[int] = None
    tags: Optional[List[Tag]] = None
