""" platform module.

"""

from abc import ABC, abstractmethod

from mindstone.embedded.channels.channel import ChannelABC

_current_platform = None


class PlatformABC(ABC):
    """ platform abstract base class.

    """

    input_channel_object = None
    output_channel_object = None
    pwm_channel_object = None

    def __init__(self, *args, **kwargs):
        global _current_platform
        if _current_platform is not None:
            raise Exception("More than one platform can't be set.")

        self.channels = dict()
        self.setup(*args, **kwargs)

        # assign to global current platform
        _current_platform = self

    @abstractmethod
    def setup(self, *args, **kwargs):
        pass

    def trigger_channel(self, channel_id: int, method: str, **kwargs):
        getattr(self.channels[channel_id], method)(**kwargs)

    def new_channel(self, channel_id: int, channel_type: str, **kwargs) -> ChannelABC:
        if channel_type == "input":
            channel_object = self.input_channel_object
        elif channel_type == "output":
            channel_object = self.output_channel_object
        elif channel_type == "pwm":
            channel_object = self.pwm_channel_object
        else:
            raise ValueError("invalid channel type provide.")
        self.channels[channel_id] = channel_object(channel_id, **kwargs)
        return self.channels[channel_id]

    def cleanup(self):
        for channel in self.channels.values():
            channel.clean()


def get_current_platform() -> PlatformABC:
    if not isinstance(_current_platform, PlatformABC):
        raise NotImplementedError("Platform has not been set.")
    return _current_platform
