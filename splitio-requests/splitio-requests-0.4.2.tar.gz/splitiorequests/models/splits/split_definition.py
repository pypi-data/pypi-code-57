from dataclasses import dataclass
from typing import Optional, List
from splitiorequests.models.splits.treatment import Treatment
from splitiorequests.models.splits.default_rule import DefaultRule
from splitiorequests.models.splits.environment import Environment
from splitiorequests.models.splits.traffic_type import TrafficType
from splitiorequests.models.splits.rule import Rule


@dataclass
class SplitDefinition:
    treatments: List[Treatment]
    defaultTreatment: str
    defaultRule: List[DefaultRule]
    name: Optional[str] = None
    environment: Optional[Environment] = None
    trafficType: Optional[TrafficType] = None
    killed: Optional[bool] = None
    baselineTreatment: Optional[str] = None
    trafficAllocation: Optional[int] = None
    rules: Optional[List[Rule]] = None
    creationTime: Optional[int] = None
    lastUpdateTime: Optional[int] = None
    comment: Optional[str] = None
