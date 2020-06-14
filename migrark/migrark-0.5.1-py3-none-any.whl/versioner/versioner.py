from abc import ABC, abstractmethod


class Versioner(ABC):

    @property
    @abstractmethod
    def version(self) -> str:
        """Retrieve method to be implemented"""

    @version.setter
    def version(self, value: str) -> None:
        """Set method to be implemented"""
