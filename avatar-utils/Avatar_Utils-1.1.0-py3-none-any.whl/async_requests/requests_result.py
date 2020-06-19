from dataclasses import dataclass, field
from typing import List, Dict, Optional

from avatar_utils.async_requests.response_data import ResponseData


@dataclass
class RequestsResult:

    responses: List[Optional[ResponseData]]
    elapsed: float

    average: float = field(default=None, init=False)
    min: float = field(default=None, init=False)
    max: float = field(default=None, init=False)
    status_codes: Dict[int, int] = field(default=None, init=False)
    failed: int = field(default=None, init=False)

    def __post_init__(self):
        self.average = self.elapsed / len(self.responses) if self.responses else None
        self.status_codes = dict()
        self.failed = 0
        elapsed_times = {r.elapsed for r in self.responses if r.elapsed is not None}

        if elapsed_times:
            self.min = min(elapsed_times)
            self.max = max(elapsed_times)

        for response in self.responses:
            if response.exception:
                self.failed += 1
                continue

            status_stat = self.status_codes.get(response.response.status)
            self.status_codes[response.response.status] = status_stat + 1 if status_stat else 1
