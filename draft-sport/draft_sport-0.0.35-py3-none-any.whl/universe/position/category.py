"""
Draft Sport Python
Position Category Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from typing import TypeVar, Type, Any

T = TypeVar('T', bound='PositionCategory')


class PositionCategory(Decodable):

    def __init__(
        self,
        indexid: int,
        name: str
    ) -> None:

        self._indexid = indexid
        self._name = name

        return

    name = Immutable(lambda s: s._name)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            indexid=data['indexid'],
            name=data['name']
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, PositionCategory):
            return False
        if self._indexid == other._indexid:
            return True
        return False

    def __ne__(self, other) -> bool:
        return not other == self
