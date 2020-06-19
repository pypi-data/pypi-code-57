from abc import ABC, abstractmethod
from functools import partialmethod
from typing import (
    Callable,
    Optional
)

from .common import (
    stringify,
    check_vector,

    Vector,
    Symbol,
    Payload
)


class Provider(ABC):
    """
    """

    __str__ = partialmethod(stringify, 'provider')

    @staticmethod
    def check(provider) -> None:
        if not isinstance(provider, Provider):
            raise ValueError(
                f'provider must be an instance of Provider, but got `{provider}`'  # noqa: E501
            )

        check_vector(provider.vector, provider)

    @property
    @abstractmethod
    def vector(self) -> Vector:  # pragma: no cover
        """A provider should only have one vector
        which means a provider should only handle a single type of message
        """

        return

    @abstractmethod
    async def init(
        self,
        symbol: Symbol
    ) -> Optional[Payload]:  # pragma: no cover
        """Initialize the data for symbol `symbol` from the very beginning
        """

        return

    @abstractmethod
    def remove(
        self,
        symbol: Symbol
    ) -> None:  # pragma: no cover
        """Discard the symbol, and do not receive further updates
        """

        return

    @abstractmethod
    def when_update(
        dispatch: Callable[[Symbol, Payload], None]
    ) -> None:  # pragma: no cover
        """Sets the receiver to receive update messages
        """

        return
