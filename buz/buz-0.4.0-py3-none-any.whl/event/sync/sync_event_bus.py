from typing import Collection

from buz.event import Event, EventBus
from buz.event.sync import Locator


class SyncEventBus(EventBus):
    def __init__(self, locator: Locator):
        self.locator = locator

    def publish(self, event: Event) -> None:
        subscribers = self.locator.get(event)
        for subscriber in subscribers:
            subscriber.consume(event)

    def bulk_publish(self, events: Collection[Event]) -> None:
        for event in events:
            self.publish(event)
