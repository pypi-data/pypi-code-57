from contextlib import contextmanager
from pathlib import Path
from typing import Set

import requests

from .coordinator.zookeeper import zookeeper_coordinator
from .persist.pytables import PyTables
from .pullframe import _PullFrame

__all__ = ["PullFrame"]


@contextmanager
def pullframe(
    kafka_hosts: Set[str], directory: Path, sync_timeo: float = 60.0
):
    persist = PyTables.on(directory)
    with zookeeper_coordinator(hosts=kafka_hosts) as coordinator:
        yield _PullFrame(persist, coordinator, requests.Session(), sync_timeo)
