from typing import Collection

from buz.event import Subscriber, Event


class Locator:
    def get(self, event: Event) -> Collection[Subscriber]:
        pass
