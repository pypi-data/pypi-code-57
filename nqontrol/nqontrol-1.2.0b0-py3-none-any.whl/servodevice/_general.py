# pylint: disable=protected-access,redefined-outer-name,cyclic-import

import logging as log
import sys
from pathlib import Path

from ADwin import ADwinError
from openqlab.analysis.servo_design import ServoDesign

from nqontrol.general import settings

_DONT_SERIALIZE = ["adw", "_servos", "deviceNumber"]
"""Path of the compiled binary. It comes usually with the source code, but can be exchanged."""
_DEFAULT_PROCESS = "nqontrol.TC1"
_JSONPICKLE = ["_servoDesign"]


def __repr__(self):
    return f"ServoDevice {self.deviceNumber}"


@property  # type: ignore
def servoDesign(self) -> ServoDesign:
    """
    Return the dummy ServoDesign object associated with the device.

    :getter: The ServoDesign object.
    :type: :obj:`openqlab.analysis.servo_design.ServoDesign`
    """
    return self._servoDesign


@property  # type: ignore
def workload(self):
    """
    Get the current workload of the ADwin device.

    :getter: CPU load (0 to 100).
    :type:  :obj:`int`
    """
    return int(self.adw.Workload())


@property  # type: ignore
def timestamp(self):
    """
    Get the current time stamp of the ADwin device.

    It is a counter that ist started on booting and counts the runtime in seconds.
    It is mainly a debugging feature to see that the device is running.

    :getter: Runtime in seconds.
    :type:  :obj:`int`
    """
    return int(self.adw.Get_Par(settings.PAR_TIMER))


def _bootAdwin(self, process=_DEFAULT_PROCESS, reboot=False):
    """Boot ADwin if necessary."""
    # Firmware that is needed to boot an ADwin with T12 CPU
    firmware = "ADwin12.btl"
    # Making the boot platform independent
    if sys.platform == "win32":
        btl = self.adw.ADwindir + firmware
    else:
        btl = self.adw.ADwindir + "/share/btl/" + firmware

    if reboot:
        self.adw.Boot(btl)
    else:
        # Hack to check if the ADwin is booted.
        # It throws a timeout error with the number 2 if it has not.
        try:
            self.adw.Workload()
        except ADwinError as e:
            if e.errorNumber == 2:
                # Boot the device
                self.adw.Boot(btl)

    try:
        if self.adw.Process_Status(1) == 0:
            # change to script directory to load the default binary
            sd_dir = Path(__file__).parent
            process_path = sd_dir / process
            # Start the control process
            self.adw.Load_Process(str(process_path))
            self.adw.Start_Process(1)
    except ADwinError as e:
        log.error(
            "There is something strange with the ADwin connection. Rebooting the device should help."
        )
        raise e


def _lockControlRegister(self):
    return self.adw.Get_Par(settings.PAR_LCR)


def _greaterControlRegister(self):
    return self.adw.Get_Par(settings.PAR_GCR)


def reboot(self):
    """Make a reboot of the ADwin device."""
    self._bootAdwin(reboot=True)
    self._sendAllToAdwin()
    for s in self._servos:
        if s is not None:
            s._sendLockControl()
            s._initLockValues()
            s._sendAllToAdwin()
