from abc import ABC, abstractmethod
from typing import Union, Tuple

__all__ = [
    "BaseDataConnection"
]


class BaseDataConnection(ABC):
    """
    Base class for  DataConnection.
    """

    @abstractmethod
    def _to_dict(self) -> dict:
        """Convert DataConnection object to dictionary representation."""
        pass

    @classmethod
    @abstractmethod
    def _from_dict(cls, _dict: dict) -> 'BaseDataConnection':
        """Create a DataConnection object from dictionary."""
        pass

    @abstractmethod
    def read(self, with_holdout_split: bool = False) -> Union['DataFrame', Tuple['DataFrame', 'DataFrame']]:
        """Download dataset stored in remote data storage."""
        pass

    @abstractmethod
    def write(self, data: Union[str, 'DataFrame'], remote_name: str) -> None:
        """Upload file to a remote data storage."""
        pass
