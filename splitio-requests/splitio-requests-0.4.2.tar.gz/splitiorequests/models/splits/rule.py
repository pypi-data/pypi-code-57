from dataclasses import dataclass
from typing import List
from splitiorequests.models.splits import condition, bucket


@dataclass
class Rule:
    buckets: List[bucket.Bucket]
    condition: condition.Condition
