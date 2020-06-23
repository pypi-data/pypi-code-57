import json
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Optional, Set

from kazoo.client import KazooClient  # type: ignore

from pullframe.api import Coordinator
from pullframe.types import Node, Resource


class _ZookeeperCoordinator(Coordinator):
    def __init__(self, zk: KazooClient):
        self.zk = zk

    def available(
        self, name: str, last_idx: Optional[datetime], version: int
    ) -> Optional[Resource]:
        current = self._cur_resource(name)

        if current is None:
            return None

        if version > current.version:
            return None

        if last_idx is not None and last_idx > current.last_idx:
            return None

        return current

    def notify(
        self, name: str, node: Node, version: int, last_idx: datetime
    ) -> None:
        def resource_having_only_current_node():
            return Resource(nodes=[node], version=version, last_idx=last_idx)

        def create_resource_having_only_current_node():
            resource = resource_having_only_current_node()
            self.zk.create(store, resource.json().encode(), makepath=True)

        def version_or_last_idx_updated():
            return version > current.version or last_idx > current.last_idx

        def set_resource_having_only_current_node():
            resource = resource_having_only_current_node()
            self.zk.set(store, resource.json().encode())

        def version_or_last_idx_outdated():
            return version < current.version or last_idx < current.last_idx

        def set_resource_including_current_node():
            new = Resource(
                nodes=current.nodes + [node],
                version=version,
                last_idx=last_idx,
            )
            self.zk.set(store, new.json().encode())

        store = self._store(name)
        current = self._cur_resource(name)

        if current is None:
            return create_resource_having_only_current_node()

        if version_or_last_idx_updated():
            return set_resource_having_only_current_node()

        if version_or_last_idx_outdated():
            return

        set_resource_including_current_node()

    def version(self, name: str) -> Optional[int]:
        current = self._cur_resource(name)

        if current is None:
            return None

        return current.version

    @staticmethod
    def _store(name: str) -> str:
        return f"/pullframe/{name}"

    def _cur_resource(self, name) -> Optional[Resource]:
        store = self._store(name)

        if not self.zk.exists(store):
            return None

        data, _ = self.zk.get(store)
        data = json.loads(data.decode())
        return Resource(**data)


@contextmanager
def zookeeper_coordinator(
    hosts: Set[str] = {"localhost:2181"}, timeout=300.0
) -> Any:
    client = KazooClient(hosts=",".join(hosts), timeout=timeout)
    client.start(timeout=timeout)
    yield _ZookeeperCoordinator(client)
    client.stop()
    client.close()
