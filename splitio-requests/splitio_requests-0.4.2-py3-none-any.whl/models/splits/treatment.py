from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Treatment:
    name: str
    description: Optional[str] = None
    configurations: Optional[str] = None
    keys: Optional[List[str]] = None
    segments: Optional[List[str]] = None
