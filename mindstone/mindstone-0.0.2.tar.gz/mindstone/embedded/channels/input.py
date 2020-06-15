""" input channel module.

"""

from abc import ABC, abstractmethod

from mindstone.embedded.channels.channel import ChannelABC


class InputChannelABC(ChannelABC, ABC):
    """ input channel abstract base class.

    """

    LOW = None
    HIGH = None
    PULL_UP = None
    PULL_DOWN = None
    RISING = None
    FALLING = None
    BOTH = None

    def __init__(self, channel_id: int, pull=None):
        self._pull = pull
        super().__init__(channel_id)

    @abstractmethod
    def value(self) -> bool:
        """input value."""
        pass

    @abstractmethod
    def wait_for_edge(self, edge_type, timeout: int = None):
        """blocks the execution of the program until an edge is detected"""
        pass

    @abstractmethod
    def event(self, edge_type, callback=None, bounce_time: int = None):
        pass

    @abstractmethod
    def remove_event(self):
        pass

    @abstractmethod
    def event_callback(self, callback, bounce_time: int = None):
        pass

    @abstractmethod
    def event_detected(self) -> bool:
        pass
