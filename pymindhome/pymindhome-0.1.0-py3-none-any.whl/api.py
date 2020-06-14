"""Define a base module to interact with the API."""
import logging
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import RequestError, raise_on_response_payload
from .events import Events

_LOGGER: logging.Logger = logging.getLogger(__name__)

API_BASE_URL: str = "https://33ecrc50n7.execute-api.us-east-1.amazonaws.com/hassdev"

DEFAULT_TIMEOUT: int = 10


class MindHomeAPI:  # pylint: disable=too-few-public-methods
    """Define an API object."""

    def __init__(
        self, api_key: str, *, session: Optional[ClientSession] = None
    ) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._session: Optional[ClientSession] = session

        self.events: Events = Events(self._request)

    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an API request."""
        kwargs.setdefault("headers", {})
        kwargs["headers"]["x-api-key"] = self._api_key

        use_running_session = self._session and not self._session.closed

        session: ClientSession
        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, f"{API_BASE_URL}/{endpoint}", **kwargs
            ) as resp:
                resp.raise_for_status()
                payload = await resp.json()
        except ClientError as err:
            raise RequestError(f"Error requesting data from /{endpoint}: {err}")
        finally:
            if not use_running_session:
                await session.close()

        raise_on_response_payload(payload)

        return payload
