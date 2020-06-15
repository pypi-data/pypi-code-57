""" virtual platform module.

"""

from mindstone.embedded.channels.virtual import VirtualPWMChannel, VirtualOutputChannel, VirtualInputChannel
from mindstone.embedded.platforms.platform import PlatformABC


class VirtualPlatform(PlatformABC):
    """ virtual platform interface class.

    """
    input_channel_object = VirtualInputChannel
    output_channel_object = VirtualOutputChannel
    pwm_channel_object = VirtualPWMChannel

    def setup(self, *args, **kwargs):
        pass
