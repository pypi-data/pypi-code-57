""" mutable components abstract base class module.

"""

from abc import ABC, abstractmethod


class MutableComponentABC(ABC):

    @abstractmethod
    def update(self, *args, **kwargs):
        pass
