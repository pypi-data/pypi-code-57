from typing import Any

from dbdaora.service import Service

from ..keys import FallbackKey
from .repositories import HashData


class HashService(Service[Any, HashData, FallbackKey]):
    ...
