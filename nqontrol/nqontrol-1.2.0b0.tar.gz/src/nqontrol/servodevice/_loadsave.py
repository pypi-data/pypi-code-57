"""Loading and saving part of ServoDevice."""
# pylint: disable=protected-access

import json
import logging as log
import os
from datetime import datetime
from shutil import copyfile

import jsonpickle

from nqontrol.general import settings


def _backupSettingsFile(cls, filename):
    if os.path.isfile(filename):
        timestamp = datetime.now().strftime(settings.BACKUP_SUBSTRING)
        filename_base, extension = os.path.splitext(filename)
        backup = "{}.{}{}".format(filename_base, timestamp, extension)

        if os.path.isfile(backup):
            log.error("The filename of the backup does already exist.")
            raise IOError(
                f"The backup filename {backup} does already exist. Not overwriting the old backup..."
            )

        try:
            copyfile(filename, backup)
            log.warning("Created backup file at {}.".format(backup))
        except (IOError, OSError) as e:
            log.error(e)
            raise e


def _writeSettingsToFile(self, filename, data):
    if settings.CREATE_SETTINGS_BACKUP:
        self._backupSettingsFile(filename)
    with open(filename, "w+") as file:
        json.dump(data, file, indent=2)


def saveDeviceToJson(self, filename=settings.SETTINGS_FILE):
    """
    Save the settings of this device and all servos to a json file.

    Parameters
    ----------
    filename: :obj:`str`
        Filename of the output file.
        It will be overwritten without asking.
    """
    data = {
        self.__class__.__name__: {
            "deviceNumber": self.deviceNumber,
            "_monitors": self.monitors,
            "_servoDesign": jsonpickle.encode(self.servoDesign),
            "_servos": {},
        }
    }
    for s in self._servos:
        if s is not None:
            servoName = (
                s.__class__.__name__
                + "_"
                + str(s._channel)  # pylint: disable=protected-access
            )
            data[self.__class__.__name__]["_servos"][servoName] = s.getSettingsDict()

    self._writeSettingsToFile(filename, data)


def loadServoFromJson(self, channel, applySettings):
    """
    Load settings directly to a new or existing :obj:`Servo`.

    All existing settings on this channel will be overwritten.

    Parameters
    ----------
    channel: :obj:`int`
        Physical channel from 1 to {}.
    applySettings: :obj:`str` or :obj:`dict`
        Settings to apply to the selected :obj:`Servo`.
    """.format(
        settings.NUMBER_OF_SERVOS
    )
    self.servo(channel).loadSettings(applySettings)


def loadDeviceFromJson(self, filename=settings.SETTINGS_FILE):
    """
    Load a device with all servos from json file.

    Read the `deviceNumber` only if it is called from the constructor,
    because it can not be changed for an existing :obj:`ServoDevice`.

    Parameters
    ----------
    filename: :obj:`str`
        Filename with a saved :obj:`ServoDevice` state.
    """
    # load them from json
    with open(filename, "r") as file:
        data = json.load(file)
    if not data.get(self.__class__.__name__):
        raise Exception("Wrong file format.")

    # loading servo settings
    servos = data[self.__class__.__name__]["_servos"]
    for s in servos:
        channel = servos[s]["_channel"]
        if channel <= settings.NUMBER_OF_SERVOS:
            self.loadServoFromJson(channel, servos[s])

    # loading monitor settings
    monitors = data[self.__class__.__name__]["_monitors"]
    for m, mon in enumerate(monitors):
        if mon is not None and m in range(0, settings.NUMBER_OF_MONITORS):
            self._monitors[m] = mon

    # Loading device parameters
    self._applySettingsDict(data)
    self._sendAllToAdwin()


def _sendAllToAdwin(self):
    """Write all settings to ADwin."""
    # Enabling all monitors contained in the save
    for i, monitor in enumerate(self.monitors):
        if monitor is not None:
            self.enableMonitor(i + 1, monitor["servo"], monitor["card"])


def _applySettingsDict(self, data):
    data = data[self.__class__.__name__]
    DONT_SERIALIZE = self._DONT_SERIALIZE + ["_monitors"]
    for d in self.__dict__:
        value = data.get(d.__str__())
        if (d.__str__() not in DONT_SERIALIZE) and (value is not None):
            if d.__str__() in self._JSONPICKLE:
                value = jsonpickle.decode(value)
            self.__dict__[d.__str__()] = value
