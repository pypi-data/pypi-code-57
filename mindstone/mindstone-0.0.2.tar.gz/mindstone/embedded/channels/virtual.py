""" virtual channels module.

"""

from mindstone.embedded.channels.input import InputChannelABC
from mindstone.embedded.channels.output import OutputChannelABC
from mindstone.embedded.channels.pwm import PWMChannelABC


class VirtualInputChannel(InputChannelABC):
    """ virtual input channel class.
    """

    LOW = 0
    HIGH = 1
    PULL_UP = 1
    PULL_DOWN = 0
    RISING = 1
    FALLING = 0
    BOTH = 2

    def value(self) -> bool:
        pass

    def wait_for_edge(self, edge_type, *args, **kwargs):
        pass

    def event(self, edge_type, *args, **kwargs):
        pass

    def remove_event(self):
        pass

    def event_callback(self, callback, *args, **kwargs):
        pass

    def event_detected(self) -> bool:
        pass

    def setup(self):
        if self._pull is None:
            print("NEW INPUT CHANNEL ({})".format(self.id))
        else:
            print("NEW INPUT CHANNEL ({}, {})".format(self.id, self._pull))

    def clean(self):
        print("CLEANED INPUT CHANNEL ({})".format(self.id))


class VirtualOutputChannel(OutputChannelABC):
    """ virtual output channel class.
    """

    LOW = 0
    HIGH = 1

    def high(self):
        self._state = 1
        print("OUTPUT CHANNEL SET ({}, {})".format(self.id, self.HIGH))

    def low(self):
        self._state = 0
        print("OUTPUT CHANNEL SET ({}, {})".format(self.id, self.LOW))

    def setup(self):
        print("NEW OUTPUT CHANNEL ({}, {})".format(self.id, self._state))

    def clean(self):
        print("CLEANED OUTPUT CHANNEL ({}, {})".format(self.id, self._state))


class VirtualPWMChannel(PWMChannelABC):
    """ virtual pulse width modulation channel class.
    """

    def start(self, duty_cycle: float):
        self.duty_cycle = duty_cycle
        print("START PWM CHANNEL ({}, {})".format(self.id, self.duty_cycle))

    def stop(self):
        print("STOP PWM CHANNEL ({}, {})".format(self.id, self.duty_cycle))

    def change_frequency(self, frequency: float):
        self.frequency = frequency
        print("CHANGED PWM CHANNEL FREQUENCY ({}, {})".format(self.id, frequency))

    def change_duty_cycle(self, duty_cycle: float):
        self.duty_cycle = duty_cycle
        print("CHANGED PWM CHANNEL DUTY CYCLE ({}, {})".format(self.id, duty_cycle))

    def setup(self):
        print("NEW PWM CHANNEL ({}, {})".format(self.id, self.frequency))

    def clean(self):
        print("CLEANED PWM CHANNEL ({})".format(self.id))
