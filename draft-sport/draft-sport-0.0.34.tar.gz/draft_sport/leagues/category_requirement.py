"""
Draft Sport
Position Requirement Module
author: hugh@blinkybeach.com
"""
from draft_sport.universe.position.category import PositionCategory
from nozomi import Immutable, Decodable
from typing import Type, TypeVar, Any

T = TypeVar('T', bound='PositionRequirement')


class CategoryRequirement(Decodable):

    def __init__(
        self,
        count: int,
        category: PositionCategory
    ) -> None:

        self._count = count
        self._category = category

        return

    count: int = Immutable(lambda s: s._count)
    category: PositionCategory = Immutable(lambda s: s._category)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            count=data['count'],
            category=PositionCategory.decode(data['category'])
        )
