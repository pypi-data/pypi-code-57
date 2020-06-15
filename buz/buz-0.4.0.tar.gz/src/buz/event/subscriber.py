from abc import ABC, abstractmethod
from typing import Type

from buz.event import Event


class Subscriber(ABC):
    @classmethod
    @abstractmethod
    def subscribed_to(cls) -> Type[Event]:
        pass

    @classmethod
    @abstractmethod
    def fqn(cls) -> str:
        pass

    @abstractmethod
    def consume(self, event: Event) -> None:
        pass
