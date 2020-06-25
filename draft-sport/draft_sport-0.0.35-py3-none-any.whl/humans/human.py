"""
Draft Sport Python
Human Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Configuration, RequestCredentials
from nozomi import Decodable
from typing import Optional, Type, TypeVar, Any
from nozomi import URLParameter, URLParameters, HTTPMethod, ApiRequest
from draft_sport.communication.method import CommunicationMethod

T = TypeVar('T', bound='Human')


class Human(Decodable):

    _PATH = '/human'

    def __init__(
        self,
        public_id: str,
        email: CommunicationMethod
    ) -> None:

        self._email = email
        self._public_id = public_id

        return

    display_name: str = Immutable(lambda s: s._email.body.split('@')[0])
    public_id: str = Immutable(lambda s: s._public_id)
    email: CommunicationMethod = Immutable(lambda s: s._email)

    @classmethod
    def retrieve(
        cls: Type[T],
        public_id: str,
        credentials: RequestCredentials,
        configuration: Configuration
    ) -> Optional[T]:
        """
        Optionally return a Human with the given public ID, if it exists
        """

        assert isinstance(public_id, str)

        target = URLParameter('public_id', public_id)
        parameters = URLParameters([target])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            configuration=configuration,
            data=None,
            url_parameters=parameters,
            credentials=credentials
        )

        return cls.optionally_decode(request.response_data)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            email=CommunicationMethod.decode(data['email'])
        )
