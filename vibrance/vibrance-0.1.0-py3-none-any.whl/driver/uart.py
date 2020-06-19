import serial
import serial.tools.list_ports
import atexit

from . import driver


def list_ports():
    """List the names of all serial ports present on this device."""
    return [port.device for port in serial.tools.list_ports.comports()]


class SerialDriver(driver.Driver):
    """Driver that reads bytes from a serial port.

    Generates events based on individual bytes received.
    """
    def __init__(self, name="", portname=""):
        super().__init__(name)
        self.portname = portname

    def _open(self):
        self.port = serial.Serial(self.portname)
        atexit.register(self.close)

    def _close(self):
        self.port.close()

    def _read(self):
        events = []
        while self.port.in_waiting > 0:
            byte = self.port.read().decode("utf-8")

            events.append({"driver": "uart",
                           "type": "byte",
                           "byte": byte})

            events.append({"driver": "uart",
                           "type": byte,
                           "byte": byte})

        return tuple(events)

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "Serial Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "Serial Disabled"

        return status
