""" raspberry pi channels module.

"""

try:
    import RPi.GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because"
          " you need superuser privileges.  You can achieve this"
          " by using 'sudo' to run your script")

from mindstone.embedded.channels.input import InputChannelABC
from mindstone.embedded.channels.output import OutputChannelABC
from mindstone.embedded.channels.pwm import PWMChannelABC

gpio = RPi.GPIO


class RPiInputChannel(InputChannelABC):
    """ raspberry pi input channel class.

    Methods for handling switch debounce:
    Switch debounce occurs when an input registers an event more that once per trigger.
     - add a 0.1uF capacitor across your switch.
     - software debouncing
     - a combination of both


    Resources:
     - https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    """

    LOW = gpio.LOW
    HIGH = gpio.HIGH
    PULL_UP = gpio.PUD_UP
    PULL_DOWN = gpio.PUD_DOWN
    RISING = gpio.RISING
    FALLING = gpio.FALLING
    BOTH = gpio.BOTH

    def value(self) -> bool:
        return gpio.input(self.id) == self.HIGH

    def wait_for_edge(self, edge_type, *args, **kwargs):
        gpio.wait_for_edge(self.id, edge_type, *args, **kwargs)

    def event(self, edge_type, *args, **kwargs):
        gpio.add_event_detect(self.id, edge_type, *args, **kwargs)

    def remove_event(self):
        gpio.remove_event_detect(self.id)

    def event_callback(self, callback, *args, **kwargs):
        gpio.add_event_callback(self.id, callback, *args, **kwargs)

    def event_detected(self) -> bool:
        return gpio.event_detected(self.id)

    def setup(self):
        self.clean()
        if self._pull is None:
            # this means that the value that is read by the input is undefined
            # until it receives a signal
            gpio.setup(self.id, gpio.IN)
        else:
            gpio.setup(self.id, gpio.IN, pull_up_down=self._pull)

    def clean(self):
        gpio.cleanup(self.id)


class RPiOutputChannel(OutputChannelABC):
    """ raspberry pi output channel class.

    Resources:
     - https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/
    """

    LOW = gpio.LOW
    HIGH = gpio.HIGH

    def high(self):
        gpio.state(self.id, self.HIGH)
        self._state = 1

    def low(self):
        gpio.state(self.id, self.LOW)
        self._state = 0

    def setup(self):
        self.clean()
        gpio.setup(self.id, gpio.OUT, initial=self._state)

    def clean(self):
        gpio.cleanup(self.id)


class RPiPWMChannel(PWMChannelABC):
    """ raspberry pi pulse width modulation channel class module.

    Resources:
     - https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
    """

    def start(self, duty_cycle: float):
        self._pwm.start(duty_cycle)
        self.duty_cycle = duty_cycle

    def stop(self):
        self._pwm.stop()

    def change_frequency(self, frequency: float):
        self._pwm.ChangeFrequency(frequency)
        self.frequency = frequency

    def change_duty_cycle(self, duty_cycle: float):
        self._pwm.ChangeDutyCycle(duty_cycle)
        self.duty_cycle = duty_cycle

    def setup(self):
        self.clean()
        gpio.setup(self.id, gpio.OUT)
        self._pwm = gpio.PWM(self.id, self.frequency)

    def clean(self):
        gpio.cleanup(self.id)
