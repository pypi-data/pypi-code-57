from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Result:
    composers: List[str] = field(default_factory=list)
    lyricists: List[str] = field(default_factory=list)
    lyric: Optional[str] = None
