from dataclasses import dataclass
from typing import List, Optional
from splitiorequests.models.splits.depends import Depends
from splitiorequests.models.splits.between import Between


@dataclass
class Matcher:
    matcher_type: str
    string: Optional[str] = None
    negate: Optional[bool] = None
    depends: Optional[Depends] = None
    attribute: Optional[str] = None
    strings: Optional[List[str]] = None
    date: Optional[int] = None
    between: Optional[Between] = None
    number: Optional[int] = None
    bool: Optional[bool] = None
