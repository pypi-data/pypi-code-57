from abc import ABC, abstractmethod
from typing import Any


class Encoding(ABC):
    """Encoding abstract class."""

    @abstractmethod
    def encode(self, payload: Any) -> bytes:
        """
        Encode abstract method.

        Parameters
        ----------
        payload: Any

        Returns
        -------
        payload : bytes
        """
        pass

    @abstractmethod
    def decode(self, payload: bytes) -> Any:
        """
        Decode abstract method.

        Parameters
        ----------
        payload: bytes

        Returns
        -------
        payload : Any
        """
        pass


class DecodeError(Exception):
    """Decode error exception."""

    pass
