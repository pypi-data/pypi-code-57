"""
Draft Sport Python
Fantasy Position Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from draft_sport.universe.position.category import PositionCategory
from typing import TypeVar, Type, Any, List

T = TypeVar('T', bound='Position')


class Position(Decodable):

    def __init__(
        self,
        indexid: int,
        name: str,
        categories: List[PositionCategory]
    ) -> None:

        self._indexid = indexid
        self._name = name
        self._categories = categories

        return

    name = Immutable(lambda s: s._name)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            indexid=data['indexid'],
            name=data['name'],
            categories=PositionCategory.optionally_decode_many(
                data['categories'],
                default_to_empty_list=True
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        if self._indexid == other._indexid:
            return True
        return False

    def __ne__(self, other) -> bool:
        return not other == self
