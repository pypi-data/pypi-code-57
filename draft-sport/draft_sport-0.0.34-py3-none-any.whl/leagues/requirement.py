"""
Draft Sport
Requirement Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Decodable
from typing import Type, TypeVar, Any

T = TypeVar('T', bound='Requirement')


class Requirement(Decodable):

    def __init__(
        self,
        count: int,
        position_name: str
    ) -> None:

        self._count = count
        self._position_name = position_name

        return

    count: int = Immutable(lambda s: s._count)
    position_name: str = Immutable(lambda s: s._position_name)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            count=data['count'],
            position_name=data['position_name']
        )
