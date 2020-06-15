from collections import defaultdict
from typing import List, DefaultDict, Type

from pypendency.builder import Container

from buz.event import Subscriber, Event
from buz.event.pypendency import (
    SubscriberAlreadyRegisteredException,
    SubscriberNotRegisteredException,
    SubscriberNotFoundException,
)
from buz.event.sync.locator import Locator


class ContainerLocator(Locator):
    CHECK_MODE_REGISTER_TIME = "register"
    CHECK_MODE_GET_TIME = "get"

    def __init__(self, container: Container, check_mode: str = CHECK_MODE_REGISTER_TIME) -> None:
        self.__container = container
        self.__check_mode = check_mode
        self.__mapping: DefaultDict[Type[Event], List[str]] = defaultdict(lambda: [])
        self.__subscriber_ids: List[str] = []
        self.__subscribers_resolved = False

    def register(self, subscriber_id: str) -> None:
        self.__guard_subscriber_already_registered(subscriber_id)
        if self.__check_mode == self.CHECK_MODE_REGISTER_TIME:
            self.__guard_subscriber_not_found(subscriber_id)
        self.__subscriber_ids.append(subscriber_id)
        self.__subscribers_resolved = False

    def __guard_subscriber_already_registered(self, subscriber_id: str) -> None:
        if subscriber_id in self.__subscriber_ids:
            raise SubscriberAlreadyRegisteredException(subscriber_id)

    def __guard_subscriber_not_found(self, subscriber_id: str) -> None:
        if not self.__container.has(subscriber_id):
            raise SubscriberNotFoundException(subscriber_id)

    def unregister(self, subscriber_id: str) -> None:
        self.__guard_subscriber_not_registered(subscriber_id)
        self.__subscriber_ids.remove(subscriber_id)
        self.__subscribers_resolved = False

    def __guard_subscriber_not_registered(self, subscriber_id: str) -> None:
        if subscriber_id not in self.__subscriber_ids:
            raise SubscriberNotRegisteredException(subscriber_id)

    def get(self, event: Event) -> List[Subscriber]:
        if not self.__subscribers_resolved:
            self.__resolve_subscribers()
        subscriber_ids = self.__mapping.get(event.__class__, [])
        return [self.__container.get(subscriber_id) for subscriber_id in subscriber_ids]

    def __resolve_subscribers(self) -> None:
        self.__mapping = defaultdict(lambda: [])
        for subscriber_id in self.__subscriber_ids:
            if self.__check_mode == self.CHECK_MODE_GET_TIME:
                self.__guard_subscriber_not_found(subscriber_id)
            subscriber = self.__container.get(subscriber_id)
            event_class = subscriber.subscribed_to()
            self.__mapping[event_class].append(subscriber_id)
        self.__subscribers_resolved = True
