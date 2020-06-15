""" output channel module.

"""

from abc import ABC, abstractmethod

from mindstone.embedded.channels.channel import ChannelABC


class OutputChannelABC(ChannelABC, ABC):
    """ output channel abstract base class.

    """

    LOW = None
    HIGH = None

    def __init__(self, channel_id: int, initial=None):
        super().__init__(channel_id)
        self._state = self.LOW if initial is None else initial

    @property
    def state(self) -> int:
        return self._state

    @abstractmethod
    def high(self):
        pass

    @abstractmethod
    def low(self):
        pass
