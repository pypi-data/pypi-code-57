""" raspberry pi platform module.

"""

from mindstone.embedded.channels.raspberry import RPiOutputChannel, RPiInputChannel, RPiPWMChannel, gpio
from mindstone.embedded.platforms.platform import PlatformABC


class RPiPlatform(PlatformABC):
    """ Raspberry Pi platform interface class.

    """
    input_channel_object = RPiInputChannel
    output_channel_object = RPiOutputChannel
    pwm_channel_object = RPiPWMChannel

    def setup(self, mode: str = "board", warnings=False):
        if mode == "board":
            gpio.setmode(gpio.BOARD)
        elif mode == "bcm":
            gpio.setmode(gpio.BCM)
        else:
            ValueError("provided board mode is invalid. try 'board' or 'bcm'")
