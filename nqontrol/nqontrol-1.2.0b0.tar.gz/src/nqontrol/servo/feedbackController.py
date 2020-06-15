import logging as log
from threading import Thread
from time import sleep

from websocket import create_connection

from nqontrol.general import settings
from nqontrol.general.helpers import convertFloat2Volt


class FeedbackController(Thread):  # pylint: disable=too-many-instance-attributes
    """The FeedbackController is used for a temperature correction
    to avoid using a high voltage amplifier.

    It is used with an internal temperature control system and can
    possibly be adapted to another system.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self, servo, dT, mtd, voltage_limit, server, port, update_interval=1
    ):
        mtd = tuple(mtd)
        if not isinstance(mtd, tuple) and len(mtd) == 2:
            raise ValueError(
                "The parameter mtd must be a tuple with port and mtd number."
            )

        Thread.__init__(self)
        self._server = server
        self._port = port
        self._servo = servo
        self._dT = dT
        self._mtd = mtd
        self._voltage_limit = voltage_limit
        self._update_interval = update_interval
        self.enabled = True
        self.last_answer = ""

        self._servo._tempFeedbackSettings.update(
            {
                "dT": dT,
                "mtd": mtd,
                "voltage_limit": voltage_limit,
                "update_interval": update_interval,
            }
        )

    @property
    def dT(self):
        return self._dT

    @dT.setter
    def dT(self, value):
        self._dT = value
        self._servo._tempFeedbackSettings[  # pylint: disable=protected-access
            "dT"
        ] = value

    @property
    def mtd(self):
        return self._mtd

    @mtd.setter
    def mtd(self, value):
        value = tuple(value)
        self._mtd = value
        self._servo._tempFeedbackSettings[  # pylint: disable=protected-access
            "mtd"
        ] = value

    @property
    def voltage_limit(self):
        return self._voltage_limit

    @voltage_limit.setter
    def voltage_limit(self, value):
        self._voltage_limit = value
        self._servo._tempFeedbackSettings[  # pylint: disable=protected-access
            "voltage_limit"
        ] = value

    @property
    def update_interval(self):
        return self._update_interval

    @update_interval.setter
    def update_interval(self, value):
        self._update_interval = value
        self._servo._tempFeedbackSettings[  # pylint: disable=protected-access
            "update_interval"
        ] = value

    def _send(self, feedback):
        socket = create_connection(f"ws://{self._server}:{self._port}")
        socket.send(f"mtd:{self.mtd[0]},{self.mtd[1]}:{feedback}")
        answer = socket.recv()
        self.last_answer = answer
        socket.close()
        return answer

    def _calculateFeedback(self, voltage):
        return self.dT * voltage / 10

    def _checkConditions(self):
        return not self._servo.lockSearch

    def _last_output(self):
        out = self._servo._adw.GetData_Long(  # pylint: disable=protected-access
            settings.DATA_LAST_OUTPUT,
            self._servo._channel,  # pylint: disable=protected-access
            1,
        )[0]
        return convertFloat2Volt(out)

    def run(self):
        while self.enabled:
            if self._checkConditions():
                output = self._last_output()
                if abs(output) >= self.voltage_limit:
                    feedback = self._calculateFeedback(output)
                    answer = self._send(feedback)
                    if "OK." in answer:
                        log.info(answer)
                    else:
                        log.warning(answer)
            sleep(self.update_interval)
