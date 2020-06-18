from abc import ABC

__all__ = [
    "BaseLocation"
]


class BaseLocation(ABC):
    """
    Base class for storage Location.
    """

    def to_dict(self) -> dict:
        """Return a json dictionary representing this model."""
        return vars(self)
