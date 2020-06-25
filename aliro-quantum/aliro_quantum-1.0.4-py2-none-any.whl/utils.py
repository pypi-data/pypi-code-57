from dataclasses import dataclass
import json
from typing import Any, Callable

from aliro_quantum import ApiClient
import sseclient


@dataclass
class FakeResponse:
    data: Any


class StreamingApiClient:
    def __init__(self,
                 api_client: ApiClient):
        self._api_client = api_client

    def stream_response(self,
                        response_function: Callable,
                        response_class: type,
                        **kwargs):
        # Wait for results
        response = response_function(_preload_content=False,
                                     **kwargs)

        client = sseclient.SSEClient(response)
        for event in client.events():
            response_data = json.loads(event.data)['data']
            yield self._api_client.deserialize(
                FakeResponse(data=response_data),
                response_class)
