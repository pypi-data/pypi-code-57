import logging
from dataclasses import dataclass
from datetime import datetime
from socket import gethostname
from typing import Optional

import pandas as pd  # type: ignore
import requests

from pullframe.api import Coordinator, Persist
from pullframe.exceptions import AllSyncFailed, NoResourceAvailable
from pullframe.types import Demand, Node, Request


@dataclass
class _PullFrame:
    persist: Persist
    coordinator: Coordinator
    client: requests.Session
    sync_timeo: float

    def __post_init__(self):
        self.node = Node(
            directory=str(self.persist.directory), host=gethostname(),
        )

    def load(
        self,
        name: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> pd.DataFrame:
        demand = self._demand(name, start, end)
        self._sync(demand)
        return self.persist.load(name, start, end)

    def save(self, name: str, df: pd.DataFrame) -> None:
        version = self._version(name, df.index[0])
        self.persist.set_version(name, version)
        self.persist.save(name, df)

    def _demand(self, name, start, end):
        if not self.persist.exists(name):
            return Demand(cache_format=self.persist.format(), name=name)

        last_index = self.persist.last_index(name)

        return Demand(
            cache_format=self.persist.format(),
            name=name,
            start=last_index,
            end=end,
        )

    def _sync(self, demand: Demand) -> None:
        local_version = self.persist.version(demand.name)
        if local_version is None:
            local_version = 0

        resource = self.coordinator.available(
            demand.name, demand.end, local_version
        )

        if resource is None:
            raise NoResourceAvailable(demand)

        def version_outdated():
            return resource.version > local_version

        start, end = None, None

        if self.persist.exists(demand.name) and not version_outdated():
            start = demand.start
            end = demand.end

        for node in resource.nodes:
            request = Request(
                source=self.node,
                directory=str(node.directory),
                demand=Demand(
                    cache_format=self.persist.format(),
                    name=demand.name,
                    start=start,
                    end=end,
                ),
            )

            try:
                response = self.client.post(
                    "http://{node.host}", data=request.json()
                )
            except Exception as e:
                logging.warning(f"request failed {e}", exc_info=True)
                continue

            if response.status_code != 200:
                continue

            path = self.persist.dump_path(request)
            with open(path, "wb") as f:
                f.write(response.content)
            self.persist.update(request.demand.name, path)
            self.persist.set_version(request.demand.name, resource.version)
            return

            logging.warning(f"Download failed: {response}")

        raise AllSyncFailed(resource.nodes, demand)

    def _version(self, name: str, first_idx: datetime) -> int:
        if self.persist.exists(name):
            cur_version = self.persist.version(name)

            if cur_version is None:
                return 0

            if first_idx < self.persist.last_index(name):
                return cur_version + 1
            else:
                return cur_version
        else:
            remote_version = self.coordinator.version(name)

            if remote_version is None:
                return 0
            else:
                return remote_version + 1
