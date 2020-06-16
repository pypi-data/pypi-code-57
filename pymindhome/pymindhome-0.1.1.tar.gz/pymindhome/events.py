"""Define a module related to /events routes."""
from typing import Callable, Coroutine


class Events:  # pylint: disable=too-few-public-methods
    """Define a manager object for /events routes."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request: Callable[..., Coroutine] = request

    async def post(self, event: dict) -> dict:
        """Post an event dictionary."""
        return await self._request("post", "events", json={"envelope": event})
