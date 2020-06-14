"""
Draft Sport Python Library
Price Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from typing import Type, TypeVar, Any
from decimal import Decimal
from draft_sport.store.denomination import Denomination

T = TypeVar('T', bound='Price')


class Price(Decodable):

    def __init__(
        self,
        magnitude: Decimal,
        denomination: Denomination
    ) -> None:

        self._magnitude = magnitude
        self._denomination = denomination

        return

    magnitude = Immutable(lambda s: s._magnitude)
    denomination = Immutable(lambda s: s._denomination)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            magnitude=Decimal(data['magnitude']),
            denomination=Denomination.decode(data['denomination'])
        )
