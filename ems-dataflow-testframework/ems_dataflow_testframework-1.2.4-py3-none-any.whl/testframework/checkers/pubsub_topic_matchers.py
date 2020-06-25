from abc import ABC, abstractmethod


class AbstractPubsubMessageMatcher(ABC):

    @abstractmethod
    def matches(self, message: dict) -> bool:
        pass
