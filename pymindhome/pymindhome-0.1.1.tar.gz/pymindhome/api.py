"""Define a base module to interact with the API."""
import logging
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import InvalidAPIKeyError, RequestError
from .events import Events

_LOGGER: logging.Logger = logging.getLogger(__name__)

API_BASE_URL: str = "https://33ecrc50n7.execute-api.us-east-1.amazonaws.com/hassdev"

DEFAULT_TIMEOUT: int = 10


class MindHomeAPI:  # pylint: disable=too-few-public-methods
    """Define an API object."""

    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        """Initialize."""
        self._api_key: Optional[str] = None
        self._session: Optional[ClientSession] = session

        self.events: Events = Events(self._request)

    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an API request."""
        kwargs.setdefault("headers", {})
        if self._api_key:
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
            raise RequestError(
                f"Error requesting data from /{endpoint}: {err}"
            ) from None
        finally:
            if not use_running_session:
                await session.close()

        return payload

    async def validate(self, api_key: str) -> None:
        """Validate an API key."""
        try:
            await self._request(
                "get", "device/api_keys/verify", headers={"x-api-key": api_key}
            )
        except RequestError:
            raise InvalidAPIKeyError("Invalid API key")

        self._api_key = api_key


async def get_api(
    api_key: str, *, session: Optional[ClientSession] = None
) -> MindHomeAPI:
    """Instantiate a valid API object."""
    api = MindHomeAPI(session=session)
    await api.validate(api_key)
    return api
