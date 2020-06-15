""" switch component module.

"""

from mindstone.embedded.channels.input import InputChannelABC
from mindstone.embedded.components.component import ComponentABC
from mindstone.embedded.components.observable import ObservableComponentABC


class SwitchComponent(ComponentABC, ObservableComponentABC):
    """ switch/button component class.

    """

    def __init__(self, input_pin: int):
        super().__init__()

        self.new_channel("input", input_pin, "input")

    def observe(self) -> dict:
        input_channel = self.channels["input"]

        if not isinstance(input_channel, InputChannelABC):
            raise TypeError("Channel is not an input channel.")

        return {
            "is_on": input_channel.value()
        }
