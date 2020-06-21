from abc import ABC, abstractmethod
from functools import partialmethod
from typing import (
    Optional,
    Tuple
)

from .common import (
    stringify,
    check_vector,

    Vector,
    Symbol,
    Payload
)


class Reducer(ABC):
    """
    """

    __str__ = partialmethod(stringify, 'reducer')

    @staticmethod
    def check(reducer) -> None:
        if not isinstance(reducer, Reducer):
            raise ValueError(
                f'reducer must be an instance of Reducer, but got `{reducer}`'  # noqa: E501
            )

        check_vector(reducer.vector, reducer)

    def __init__(self) -> None:
        self._not_updated = {}

    @property
    @abstractmethod
    def vector(self) -> Vector:  # pragma: no cover
        """The vector of a reducer could be a more generic vector which is much
        shorter.

        Reducer::vector always does semi matching
        """
        ...

    def reduce(
        self,
        init: bool,
        vector: Vector,
        symbol: Symbol,
        previous: Payload,
        payload: Payload
    ) -> Tuple[bool, Optional[Payload]]:
        """Applies the update payload

        Args:
            previous (Payload):
            payload (Payload):
            symbol (str):
            vector (tuple):
            init (bool): If `True`, payload
            will be treated as the initial value

        Returns:
            Tuple[bool, Optional[Payload]]:
            - the first item in the tuple indicates whether the data changes.
            - If no changes, the second item will be `None`
        """

        full_vector = (symbol, vector)

        not_updated = self._not_updated.get(full_vector, None)

        if init:
            # Usually, the truth value of a StockDataFrame is ambiguous
            if not_updated is not None:
                del self._not_updated[full_vector]
                return True, self.merge(
                    payload,
                    not_updated
                )

            return True, self.merge(None, payload)

        if previous is None:
            # If not initialized
            self._not_updated[full_vector] = self.merge(
                not_updated,
                payload
            ) if not_updated is not None else payload

            return False, None

        return True, self.merge(previous, payload)

    @abstractmethod
    def merge(
        self,
        target: Optional[Payload],
        payload: Payload
    ) -> Payload:  # pragma: no cover
        ...
