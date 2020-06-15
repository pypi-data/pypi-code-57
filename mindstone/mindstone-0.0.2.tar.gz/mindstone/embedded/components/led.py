""" LED component module.

"""

from mindstone.embedded.channels.output import OutputChannelABC
from mindstone.embedded.components.component import ComponentABC
from mindstone.embedded.components.mutable import MutableComponentABC
from mindstone.embedded.components.observable import ObservableComponentABC


class LEDComponent(ComponentABC, ObservableComponentABC, MutableComponentABC):
    """ switch/button component class.

    """

    def __init__(self, trigger: int):
        super().__init__()
        self.is_on = False
        self.new_channel("output", trigger, "output")

    def observe(self) -> dict:
        return {
            "is_on": self.is_on
        }

    def update(self, is_on: bool = None):
        if is_on and is_on != self.is_on:
            self.is_on = is_on
            if is_on:
                self.turn_on()
            else:
                self.turn_off()

    def turn_on(self):
        output_channel = self.channels["output"]

        if not isinstance(output_channel, OutputChannelABC):
            raise TypeError("Channel is not an output channel.")

        output_channel.high()

    def turn_off(self):
        output_channel = self.channels["output"]

        if not isinstance(output_channel, OutputChannelABC):
            raise TypeError("Channel is not an output channel.")

        output_channel.low()
