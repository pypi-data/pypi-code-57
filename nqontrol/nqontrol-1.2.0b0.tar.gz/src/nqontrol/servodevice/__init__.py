"""Main part of ServoDevice."""
# pylint: disable=import-outside-toplevel,too-few-public-methods,cyclic-import
import json
import logging as log
import os
import sys
from pathlib import Path

from ADwin import ADwin, ADwinError
from openqlab.analysis.servo_design import ServoDesign

from nqontrol.general import MockADwin, settings


class ServoDevice:
    """
    A ServoDevice is the whole device, containing 8 (default can be changed) single servos.

    With this object you can control one ADwin device and manage all servos of this device.

    Parameters
    ----------
    deviceNumber: :obj:`int`
        Number of the ADwin device on this system.
        The number can be skipped when loading a ServoDevice from file.

        You have to set it using the tool `adconfig`.
        See [installation](install) for configuration details.
    readFromFile: :obj:`str`
        Select a filename if you want to open a whole ServoDevice with all servos from a saved json file.
    process: :obj:`str`
        If you have a compiled special version of the basic program running on ADwin, you can select a custom binary.
    """

    from ._general import (
        _DONT_SERIALIZE,
        _DEFAULT_PROCESS,
        _JSONPICKLE,
        __repr__,
        servoDesign,
        workload,
        timestamp,
        _bootAdwin,
        _lockControlRegister,
        _greaterControlRegister,
        reboot,
    )

    from ._servo_handling import (
        servo,
        servo_iterator,
        list_servos,
        _list_servos_str,
        addServo,
        removeServo,
    )

    from ._loadsave import (
        _backupSettingsFile,
        _writeSettingsToFile,
        saveDeviceToJson,
        loadServoFromJson,
        loadDeviceFromJson,
        _sendAllToAdwin,
        _applySettingsDict,
    )

    from ._monitors import monitors, disableMonitor, enableMonitor

    # The init method has to be here, otherwise mypy dies.
    def __init__(
        self, deviceNumber=0, readFromFile=None, process=_DEFAULT_PROCESS, reboot=False
    ):
        """Create a new ServoDevice object."""
        if deviceNumber is None and readFromFile is None:
            raise Exception(
                "You have to set a deviceNumber if you do not load a ServoDevice from a file!"
            )
        log.info(f"deviceNumber: {deviceNumber}")

        raiseExceptions = 1
        self._servoDesign: ServoDesign = ServoDesign()  # The dummy servo design object
        self._servos = [None] * settings.NUMBER_OF_SERVOS
        self._monitors = [None] * settings.NUMBER_OF_MONITORS

        if (
            readFromFile is not None
            and os.path.isfile(readFromFile)
            and deviceNumber is None
        ):
            with open(readFromFile, "r") as file:
                data = json.load(file)
            if not data.get(self.__class__.__name__):
                raise Exception("Wrong file format.")
            self.deviceNumber = data[self.__class__.__name__]["deviceNumber"]
        else:
            self.deviceNumber = deviceNumber

        if deviceNumber == 0:
            log.warning("Running with mock device!")
            self.adw = MockADwin(deviceNumber)
        else:
            self.adw = ADwin(deviceNumber, raiseExceptions)

        try:
            self._bootAdwin(process, reboot=reboot)
        except ADwinError as e:
            if e.errorNumber == 2001:
                log.warning("No device connected! Starting with mock device!")
            log.error(e.errorNumber)
            self.adw = MockADwin(deviceNumber)
            self._bootAdwin(process)

        # Adding servos
        for i in range(1, settings.NUMBER_OF_SERVOS + 1):
            self.addServo(channel=i)

        if readFromFile is not None and os.path.isfile(readFromFile):
            log.warning(f"Loaded from: {readFromFile}")
            self.loadDeviceFromJson(readFromFile)
