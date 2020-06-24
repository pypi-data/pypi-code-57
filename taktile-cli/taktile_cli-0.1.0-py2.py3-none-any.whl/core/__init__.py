from enum import Enum
from typing import Set, List, Iterable


class ExtendedEnum(Enum):
    @classmethod
    def set(cls) -> Set:
        return set(map(lambda c: c.value, cls))

    @classmethod
    def list(cls) -> List:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def names(cls: Iterable) -> List:
        return list(map(lambda c: c.name, cls))
