"""
Draft Sport Python Library
Product Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from typing import TypeVar, Type, Any, List

T = TypeVar('T', bound='Product')


class Product(Decodable):

    def __init__(
        self,
        public_id: str,
        name: str,
        features: List[str]
    ) -> None:

        self._public_id = public_id
        self._name = name
        self._features = features

        return

    features = Immutable(lambda s: s._features)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            name=data['name'],
            features=data['features']
        )
