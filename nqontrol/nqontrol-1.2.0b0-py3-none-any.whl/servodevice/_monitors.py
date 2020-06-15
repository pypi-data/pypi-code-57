# pylint: disable=protected-access,redefined-outer-name

from nqontrol.general import settings


def disableMonitor(self, monitor_channel):
    """
    Disable the selected monitor channel.

    Parameters
    ----------
    monitor_channel: :obj:`int`
        Channel to disable the output.
    """
    if not monitor_channel in range(1, settings.NUMBER_OF_MONITORS + 1):
        raise IndexError(
            f"Use a channel from 1 to {settings.NUMBER_OF_MONITORS}, not {monitor_channel}!"
        )
    self.monitors[monitor_channel - 1] = None
    self.adw.SetData_Long([0], settings.DATA_MONITORS, monitor_channel, 1)


def enableMonitor(self, monitor_channel, servo, card):
    """
    Enable the monitor output on the hardware channel `monitor_channel` for a given Servo.

    Parameters
    ----------
    monitor_channel: :obj:`int`
        Select the channel on the ADwin D/A card (1 to {0}).
    servo: :obj:`int`
        The index of the Servo which will be assigned to the monitor channel.
    card: :obj:`str`
        Choose one of the possible cards a servo has control over: 'input', 'aux', 'output' or 'ttl'.
    """.format(
        settings.NUMBER_OF_MONITORS
    )
    if not monitor_channel in range(1, settings.NUMBER_OF_MONITORS + 1):
        raise IndexError(
            f"Use a channel from 1 to {settings.NUMBER_OF_MONITORS}, not {monitor_channel}!"
        )
    if servo is None:
        raise ValueError(f"Please provide a servo index, was None.")
    if not servo in range(1, settings.NUMBER_OF_SERVOS + 1):
        raise IndexError(
            f"Make sure to assign a servo index that does exist, from 1 to {settings.NUMBER_OF_SERVOS} -- was {servo}"
        )

    if card == "input":
        monitor = servo
    elif card == "aux":
        monitor = servo + 8
    elif card == "output":
        monitor = servo + 20
    elif card == "ttl":
        monitor = 30
    else:
        raise ValueError(
            "You should choose one of the possible cards for the monitor output."
        )

    self.monitors[monitor_channel - 1] = dict({"servo": servo, "card": card})
    self.adw.SetData_Long([monitor], settings.DATA_MONITORS, monitor_channel, 1)


@property  # type: ignore[misc]
def monitors(self):
    """
    Return the list of parameters monitor configurations of the device.

    :getter: List of monitor parameters. Each entry is a list containing servo index and card String.
    :setter: Set the list of parameters for ADwin monitor channels.
    :type: :obj:`list`
    """
    return self._monitors


@monitors.setter
def monitors(self, monitors):
    self._monitors = monitors
