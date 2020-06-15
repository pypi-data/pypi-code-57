""" ultrasonic component module.

"""

import time

from mindstone.embedded.channels.input import InputChannelABC
from mindstone.embedded.channels.output import OutputChannelABC
from mindstone.embedded.components.component import ComponentABC
from mindstone.embedded.components.observable import ObservableComponentABC


class UltrasonicSensorComponent(ComponentABC, ObservableComponentABC):
    """ ultrasonic component class.

    """

    def __init__(self, model: str, trigger: int, echo: int):
        super().__init__(model)

        self.new_channel("trigger", trigger, "output")
        self.new_channel("echo", echo, "input")

    def observe(self) -> dict:
        return {
            "time_change": self.measure_time_change()
        }

    def measure_time_change(self) -> float:
        trigger_channel = self.channels["trigger"]
        echo_channel = self.channels["echo"]

        assert isinstance(trigger_channel, OutputChannelABC)
        assert isinstance(echo_channel, InputChannelABC)

        trigger_channel.low()

        # create a short delay for the sensor to settle
        time.sleep(0.1)

        # send a pulse to the sensor's trigger pin
        trigger_channel.high()
        time.sleep(self.properties["trigger_pw"])
        trigger_channel.low()

        # measure time for echo to return to receiver
        while not echo_channel.value():
            pass
        initial_time = time.time()
        while echo_channel.value():
            pass
        final_time = time.time()

        return final_time - initial_time
