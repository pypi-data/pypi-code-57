"""
Draft Sport Python
Communication Module
author: hugh@blinkybeach.com
"""
from nozomi import Decodable, Immutable
from typing import TypeVar, Type, Any

T = TypeVar('T', bound='CommunicationMethod')


class CommunicationMethod(Decodable):

    def __init__(
        self,
        public_id: str,
        mode: int,
        body: str,
        confirmed: bool
    ) -> None:

        self._public_id = public_id
        self._mode = mode
        self._body = body
        self._confirmed = confirmed

        return

    body = Immutable(lambda s: s._body)
    public_id = Immutable(lambda s: s._public_id)
    confirmed = Immutable(lambda s: s._confirmed)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            mode=data['mode'],
            body=data['body'],
            confirmed=data['confirmed']
        )
