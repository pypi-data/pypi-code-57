"""
Draft Sport Python Library
Denomination Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from typing import Type, TypeVar, Any

T = TypeVar('T', bound='Denomination')


class Denomination(Decodable):

    def __init__(
        self,
        name: str,
        iso_4217: str,
        symbol: str
    ) -> None:

        self._name = name
        self._iso_4217 = iso_4217
        self._symbol = symbol

        return

    name: str = Immutable(lambda s: s._name)
    iso_4217: str = Immutable(lambda s: s._iso_4217)
    symbol: str = Immutable(lambda s: s._symbol)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            name=data['name'],
            iso_4217=data['iso_4217'],
            symbol=data['symbol']
        )
