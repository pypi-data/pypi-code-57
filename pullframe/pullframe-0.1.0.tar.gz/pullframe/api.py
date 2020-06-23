from abc import ABC, abstractclassmethod, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd  # type: ignore

from pullframe.types import CacheFormat, Demand, Node, Request, Resource


class Persist(ABC):
    directory: Path

    def __init__(self, directory: Path):
        self.directory = directory
        (directory / "dump").mkdir(exist_ok=True, parents=True)

    @abstractclassmethod
    def on(cls, directory: Path) -> "Persist":
        """ polinomial initialize method """

    @abstractmethod
    def load(
        self,
        name: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        include_start: bool = True,
    ) -> pd.DataFrame:
        """ read cache and return dataframe """

    @abstractmethod
    def save(self, name: str, df: pd.DataFrame) -> None:
        """ save dataframe to cache """

    @abstractmethod
    def exists(self, name: str) -> bool:
        """ check whether the cache exists on a local node """

    @abstractmethod
    def last_index(self, name: str) -> datetime:
        """ return cache's last index """

    @abstractmethod
    def update(self, name: str, path: Path) -> None:
        """ append/overwrite cache from dumped updates """

    @abstractclassmethod
    def format(cls) -> CacheFormat:
        """ return cache format """

    @staticmethod
    @abstractmethod
    def suffix() -> str:
        """ file suffix, e.g, '.csv' """

    def version(self, name: str) -> Optional[int]:
        if not self.version_path(name).exists():
            return None

        with open(self.version_path(name), "r") as f:
            return int(f.read())

    def set_version(self, name: str, version: int) -> None:
        with open(self.version_path(name), "w") as f:
            f.write(str(version))

    def supply(self, demand: Demand, include_start: bool) -> pd.DataFrame:
        return self.load(demand.name, demand.start, demand.end, include_start)

    def version_path(self, name: str) -> Path:
        return self.directory / f"{name}.version"

    def path(self, name: str) -> Path:
        return self.directory / f"{name}.{self.suffix()}"

    def dump_path(self, request: Request):
        return (
            self.directory
            / "dump"
            / ".".join(
                [
                    request.demand.name,
                    _fmt(request.demand.start),
                    _fmt(request.demand.end),
                    self.suffix(),
                ]
            )
        )


def _fmt(dt):
    if dt is None:
        return "all"
    else:
        return dt.strftime("%Y%m%d%H%M%S")


class Coordinator(ABC):
    @abstractmethod
    def available(
        self, name: str, last_idx: Optional[datetime], version: int
    ) -> Optional[Resource]:
        return None

    @abstractmethod
    def notify(
        self, name: str, node: Node, version: int, last_idx: datetime
    ) -> None:
        """ notify node's cache is updated to be another available node """

    @abstractmethod
    def version(self, name: str) -> Optional[int]:
        """ return the latest version of the cache """
