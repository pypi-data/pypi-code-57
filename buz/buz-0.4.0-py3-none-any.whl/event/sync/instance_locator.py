from collections import defaultdict
from typing import List, DefaultDict, Type

from buz.event import Subscriber, Event
from buz.event.sync import (
    SubscriberAlreadyRegisteredException,
    SubscriberNotRegisteredException,
)
from buz.event.sync import Locator


class InstanceLocator(Locator):
    def __init__(self) -> None:
        self.__mapping: DefaultDict[Type[Event], List[Subscriber]] = defaultdict(lambda: [])

    def register(self, subscriber: Subscriber) -> None:
        event_class = subscriber.subscribed_to()
        self.__guard_subscriber_already_registered(event_class, subscriber)
        self.__mapping[event_class].append(subscriber)

    def __guard_subscriber_already_registered(self, event_class: Type[Event], subscriber: Subscriber) -> None:
        if subscriber in self.__mapping[event_class]:
            raise SubscriberAlreadyRegisteredException(subscriber)

    def unregister(self, subscriber: Subscriber) -> None:
        event_class = subscriber.subscribed_to()
        self.__guard_subscriber_not_registered(event_class, subscriber)
        self.__mapping[event_class].remove(subscriber)

    def __guard_subscriber_not_registered(self, event_class: Type[Event], subscriber: Subscriber) -> None:
        if subscriber not in self.__mapping[event_class]:
            raise SubscriberNotRegisteredException(subscriber)

    def get(self, event: Event) -> List[Subscriber]:
        return self.__mapping.get(event.__class__, [])
