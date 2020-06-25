"""
Draft Sport API
Secret Reset Request Module
author: hugh@blinkybeach.com
"""
from nozomi import Immutable, Decodable, NozomiTime, Configuration
from typing import Optional, Type, TypeVar, Any
from nozomi import URLParameter, URLParameters, HTTPMethod, ApiRequest

T = TypeVar('T', bound='SecretResetRequest')


class SecretResetRequest(Decodable):

    _PATH = '/human/secret-reset-request'

    def __init__(
        self,
        created: NozomiTime
    ) -> None:

        self._created = created

        return

    created = Immutable(lambda s: s._created)

    @classmethod
    def decode(cls: Type[T], data: Any) -> None:
        return cls(
            created=NozomiTime.decode(data['created'])
        )

    @classmethod
    def create(
        cls: Type[T],
        email_address: str,
        configuration: Configuration
    ) -> T:

        target = URLParameter('email', email_address)
        parameters = URLParameters([target])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.POST,
            configuration=configuration,
            url_parameters=parameters
        )

        return cls.decode(request.response_data)

    @classmethod
    def retrieve(
        cls: Type[T],
        reset_key: str,
        configuration: Configuration
    ) -> Optional[T]:

        target = URLParameter('reset-key', reset_key)
        parameters = URLParameters([target])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            configuration=configuration,
            url_parameters=parameters
        )

        return cls.optionally_decode(request.response_data)
