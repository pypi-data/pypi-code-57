"""
Draft Sport Python
Fantasy Competition Module
author: hugh@blinkybeach.com
"""
from typing import TypeVar, Type, Any
from nozomi import Decodable

T = TypeVar('T', bound='Competition')


class Competition(Decodable):

    def __init__(
        self,
        public_id: str,
        name: str
    ) -> None:

        self._public_id = public_id
        self._name = name

        return

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            name=data['name']
        )
