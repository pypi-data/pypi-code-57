__all__ = ["GpioDigitalSensor"]

import asyncio
from typing import Dict, Any, List

import gpiozero  # type: ignore

from yaqd_core import Sensor

from .__version__ import __branch__


class GpioDigitalSensor(Sensor):
    _kind = "gpio-digital-sensor"
    _version = "0.1.0" + f"+{__branch__}" if __branch__ else ""
    traits: List[str] = []
    defaults: Dict[str, Any] = {}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.channel_names = config["channels"].keys()
        self.channel_units = {k: None for k in self.channel_names}
        self.controllers = []
        for name in self.channel_names:
            pin = config["channels"][name]["pin"]
            pull_up = config["channels"][name].get("pull_up", False)
            dev = gpiozero.InputDevice(pin=pin, pull_up=pull_up)
            self.controllers.append(dev)

    async def _measure(self):
        out = dict()
        for name, controller in zip(self.channel_names, self.controllers):
            out[name] = controller.value
        return out
