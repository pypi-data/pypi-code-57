from typing import List, Optional, TypeVar

T = TypeVar("T")


def first(source: List[T]) -> Optional[T]:
    if source is None or len(source) > 0:
        return source[0]
    return None
