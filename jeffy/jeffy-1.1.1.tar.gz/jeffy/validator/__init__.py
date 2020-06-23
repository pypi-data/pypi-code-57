from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """Validator abstract class."""

    @abstractmethod
    def validate(self, data: Any) -> None:
        """
        Validate abstract method.

        Parameters
        ----------
        data: Any
        """
        pass


class NoneValidator(Validator):
    """No validation class."""

    def validate(self, data: Any) -> None:
        """
        Validate method.

        Parameters
        ----------
        data: Any
        """
        pass


class ValidationError(Exception):
    """Validation error exception."""

    pass
