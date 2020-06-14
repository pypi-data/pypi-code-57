"""
Draft Sport Python
Composition Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Decodable
from typing import TypeVar, Type, Any, List
from draft_sport.leagues.position_requirement import PositionRequirement
from draft_sport.leagues.category_requirement import CategoryRequirement

T = TypeVar('T', bound='Composition')


class Composition(Decodable):

    def __init__(
        self,
        position_requirements: List[PositionRequirement],
        category_requirements: List[CategoryRequirement]
    ) -> None:

        self._position_requirements = position_requirements
        self._category_requirements = category_requirements

        return

    position_requirements = Immutable(
        lambda s: s._position_requirements
    )
    category_requirements = Immutable(
        lambda s: s._category_requirements
    )
    unique_positions: List[str] = Immutable(
        lambda s: list(set(r.position for r in s._position_requirements))
    )

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            position_requirements=PositionRequirement.decode_many(
                data['position_requirements']
            ),
            category_requirements=CategoryRequirement.decode_many(
                data['category_requirements']
            )
        )
