from abc import ABC
from typing import Type, get_type_hints

from buz.event import Event, Subscriber


class BaseSubscriber(Subscriber, ABC):
    @classmethod
    def subscribed_to(cls) -> Type[Event]:
        consume_types = get_type_hints(cls.consume)

        if "event" not in consume_types:
            raise TypeError("event parameter not found in consume method")

        if not issubclass(consume_types["event"], Event):
            raise TypeError("event parameter is not an buz.event.Event subclass")

        return consume_types["event"]

    @classmethod
    def fqn(cls) -> str:
        return f"{cls.__module__}.{cls.__name__}"
