""" channel module.

"""

from abc import ABC, abstractmethod


class ChannelABC(ABC):
    """ channel abstract base class.

    """

    def __init__(self, channel_id: int, **parameters):
        self.id = channel_id
        self.setup(**parameters)

    @abstractmethod
    def setup(self, **parameters):
        pass

    @abstractmethod
    def clean(self):
        pass
