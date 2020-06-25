"""
Draft Sport Python
Fantasy Competition Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.competition.competition import Competition
from nozomi import Decodable, HTTPMethod, URLParameter, URLParameters
from nozomi import Immutable, ApiRequest, RequestCredentials, Configuration
from nozomi import NozomiDate
from typing import TypeVar, Type, Any, Optional, List

T = TypeVar('T', bound='Season')


class Season(Decodable):

    _PATH = '/fantasy/season'
    _LIST_PATH = '/fantasy/season/list'

    def __init__(
        self,
        public_id: str,
        name: str,
        start_date: NozomiDate,
        competition: Competition
    ) -> None:

        self._public_id = public_id
        self._name = name
        self._start_date = start_date
        self._competition = competition

        return

    public_id = Immutable(lambda s: s._public_id)
    name = Immutable(lambda s: s._name)
    start_date = Immutable(lambda s: s._start_date)
    competition = Immutable(lambda s: s._competition)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            public_id=data['public_id'],
            name=data['name'],
            start_date=NozomiDate.decode(data['start_date']),
            competition=Competition.decode(data['competition'])
        )

    @classmethod
    def retrieve(
        cls: Type[T],
        public_id: str,
        configuration: Configuration,
        credentials: Optional[RequestCredentials] = None
    ) -> Optional[T]:

        if not isinstance(public_id, str):
            raise TypeError('public_id must be of type `str`')

        parameters = URLParameters([
            URLParameter('public_id', public_id)
        ])

        request = ApiRequest(
            path=cls._PATH,
            method=HTTPMethod.GET,
            data=None,
            url_parameters=parameters,
            credentials=credentials,
            configuration=configuration
        )

        return cls.optionally_decode(request.response_data)

    @classmethod
    def retrieve_list(
        cls: Type[T],
        configuration: Configuration,
        credentials: Optional[RequestCredentials] = None
    ) -> List[T]:

        request = ApiRequest(
            path=cls._LIST_PATH,
            method=HTTPMethod.GET,
            data=None,
            url_parameters=None,
            credentials=credentials,
            configuration=configuration
        )

        return cls.optionally_decode_many(
            request.response_data,
            default_to_empty_list=True
        )
