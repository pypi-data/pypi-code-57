# pylint: disable=protected-access

from nqontrol import Servo
from nqontrol.general import settings


def servo(self, channel):
    """
    Get the servo of the selected physical channel to control it directly.

    Parameters
    ----------
    channel: :obj:`int`
        Physical channel from 1 to {}.

    Returns
    -------
    :obj:`Servo`
        Servo object.
    """.format(
        settings.NUMBER_OF_SERVOS
    )
    if not channel in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise IndexError(
            f"Choose a servo from 1 to {settings.NUMBER_OF_SERVOS}, {channel} is not valid."
        )
    return self._servos[channel - 1]


def servo_iterator(self):
    for s in self._servos:
        yield s


def list_servos(self):
    print(self._list_servos_str())


def _list_servos_str(self):
    str_ = f"ServoDevice {self.deviceNumber}\n"
    for s in self.servo_iterator():
        str_ += f"  Servo {s.channel}: {s.name}\n"
    return str_


def addServo(self, channel, applySettings=None, name=None):
    """
    Add a new servo to be able to control it.

    Parameters
    ----------
    channel: :obj:`int`
        Physical channel from 1 to {}.
    applySettings: :obj:`str` or :obj:`dict`
        You can directly apply settings from a json file or a dict.
    """.format(
        settings.NUMBER_OF_SERVOS
    )
    if not channel in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise IndexError(
            "Choose a channel from 1 to {}!".format(settings.NUMBER_OF_SERVOS)
        )
    if self._servos[channel - 1] is None:
        self._servos[channel - 1] = Servo(
            channel, self.adw, applySettings=applySettings, name=name
        )
    else:
        raise IndexError("A servo on this channel does already exist!")


def removeServo(self, channel):
    """
    Remove a servo from the device object and stop controlling it.

    Parameters
    ----------
    channel: :obj:`int`
        Number of the physical channel to remove from 1 to {}.
    """.format(
        settings.NUMBER_OF_SERVOS
    )
    self._servos[channel - 1] = None
