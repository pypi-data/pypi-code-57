from typing import List

import requests

from datatosk import types
from datatosk.errors import HttpRequestFailedError
from datatosk.sources.source import Source, SourceParam, SourceRead


# pylint: disable = abstract-method
class RequestsRead(SourceRead):
    """Interface element for retrieving data through get requests.

    Attributes:
        url: End-point URL configuration.
    """

    def __init__(self, url: str) -> None:
        self.url = url

    def __call__(self, path: str = "", **kwargs: types.KwargsType,) -> types.JSONType:
        """Default RequestsSource().read() implementation."""
        return self.to_dict(path=path, **kwargs)

    def to_dict(self, path: str = "", **kwargs: types.KwargsType,) -> types.JSONType:
        response = requests.get(self.url + path, **kwargs)

        if not response.ok:
            raise HttpRequestFailedError(
                f"Server responded with status code {response.status_code}"
            )

        json_response: types.JSONType = response.json()
        return json_response


class RequestsSource(Source):
    """Requests interface, it enables retrieving data through get request.

    Attributes:
        source_name: source identifier.
            Envioronment variables that should be defined:
            - `HTTP_PROTOCOL_[SOURCE_NAME]`
            - `HTTP_HOST_[SOURCE_NAME]`
            - `HTTP_PORT_[SOURCE_NAME]`
        url: End-point URL configuration.

    Examples:
        >>> import datatosk
        >>> source = datatosk.requests(source_name="chuck_norris_facts")
        >>> source.read(path="jokes/random/")
    """

    def __init__(self, source_name: str) -> None:
        super().__init__(source_name)

        self.url = (
            f"{self.init_params['HTTP_PROTOCOL']}://"
            f"{self.init_params['HTTP_HOST']}:"
            f"{self.init_params['HTTP_PORT']}/"
        )

    @property
    def params(self) -> List[SourceParam]:
        return [
            SourceParam(env_name="HTTP_PROTOCOL", is_required=False, default="http"),
            SourceParam(env_name="HTTP_HOST", is_required=False, default="localhost"),
            SourceParam(env_name="HTTP_PORT", is_required=False, default="80"),
        ]

    @property
    def read(self) -> RequestsRead:
        """Interface element for retrieving data from get requests.

        Returns:
            Method-like class which can be used to retrieve data in various types.
        """
        return RequestsRead(self.url)

    def write(self) -> None:
        """Not implemented yet"""
        raise NotImplementedError
