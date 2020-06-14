from typing import List
from .collector import Collector
from ..models import Migration


class MemoryCollector(Collector):
    def __init__(self, migrations: List[Migration]) -> None:
        self.migrations = migrations

    def retrieve(self) -> List[Migration]:
        return self.migrations
