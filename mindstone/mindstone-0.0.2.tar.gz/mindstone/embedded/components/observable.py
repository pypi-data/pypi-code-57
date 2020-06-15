""" observer component abstract base class module.

"""

from abc import ABC, abstractmethod


class ObservableComponentABC(ABC):

    @abstractmethod
    def observe(self) -> dict:
        pass
