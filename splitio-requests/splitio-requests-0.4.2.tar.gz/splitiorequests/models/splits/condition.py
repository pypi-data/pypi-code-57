from dataclasses import dataclass
from typing import List
from splitiorequests.models.splits.matcher import Matcher


@dataclass
class Condition:
    combiner: str
    matchers: List[Matcher]
