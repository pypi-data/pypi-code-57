__all__ = ["GpioDigitalOutput"]

import asyncio
from typing import Dict, Any, List

import gpiozero  # type: ignore

from yaqd_core import DiscreteHardware

from .__version__ import __branch__


class GpioDigitalOutput(DiscreteHardware):
    _kind = "gpio-digital-output"
    _version = "0.2.0" + f"+{__branch__}" if __branch__ else ""
    traits: List[str] = []
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.index = config["index"]
        self.controller = gpiozero.DigitalOutputDevice(pin=self.index)
        self._position_identifiers = {"low": 0, "high": 1}

    def _connection_lost(self, peername):
        super()._connection_lost(peername)
        if len(self._clients) == 0:
            self.controller.value = 0

    def _set_position(self, value):
        self.controller.value = value

    async def update_state(self):
        while True:
            self._position = self.controller.value
            if self._position:
                self._position_identifier = "high"
            else:
                self._position_identifier = "low"
            self._busy = False
            await self._busy_sig.wait()
