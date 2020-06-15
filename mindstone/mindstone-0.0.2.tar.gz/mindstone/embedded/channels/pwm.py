""" pulse width modulation (pwm) channel module.

"""

from abc import ABC, abstractmethod

from mindstone.embedded.channels.channel import ChannelABC


class PWMChannelABC(ChannelABC, ABC):
    """ pulse width modulation (pwm) channel abstract base class.

    """

    LOW = None
    HIGH = None

    def __init__(self, channel_id: int, frequency: float):
        self.frequency = frequency
        self.duty_cycle = None
        # the attributes above may be used to set up this channel
        # this means that the super class should be initialized after
        # they are defined.
        super().__init__(channel_id)

    @abstractmethod
    def start(self, duty_cycle: float):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def change_frequency(self, frequency: float):
        pass

    @abstractmethod
    def change_duty_cycle(self, duty_cycle: float):
        pass
