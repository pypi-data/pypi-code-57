from __future__ import annotations
import time
import typing
import asyncio
from dataclasses import dataclass, field

from pyaware.commands import ValidateIn, ValidateRange, ValidationError, InvalidCommandData, TopicTask
from pyaware import from_coroutine

if typing.TYPE_CHECKING:
    from pyaware.protocol.imac2.modules import ImacModule


@dataclass
class WriteParam:
    parameter: str
    add: int = 0
    override: typing.Union[int, None] = None
    key: str = ""

    def __repr__(self):
        return "Writing parameter"

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        new_data = self._do(cmd)
        await imac_module.write_parameters({self.parameter: new_data})
        cmd["parameters_written"][self.parameter] = new_data

    def _sync_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        new_data = self._do(cmd)
        imac_module.write_parameters({self.parameter: new_data})
        cmd["parameters_written"][self.parameter] = new_data

    def _do(self, cmd):
        if self.key:
            val = cmd["data"][self.key]
        else:
            val = list(cmd["data"].values())
            if len(val) > 1:
                raise InvalidCommandData("Need to specify key if multiple data keys are given")
            val = val[0]
        if self.override is not None:
            val = self.override
        else:
            val = val + self.add
        return val

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        if imac_module._async:
            return self._async_do(cmd, imac_module, **kwargs)
        else:
            return self._sync_do(cmd, imac_module, **kwargs)


@dataclass
class ReadParam:
    parameter: str
    exact: bool = False

    def __repr__(self):
        return "Reading parameter"

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        if imac_module._async:
            return self._async_do(cmd, imac_module, **kwargs)
        else:
            return self._sync_do(cmd, imac_module, **kwargs)

    def _sync_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        cmd["parameters_read"].update(imac_module.read_parameters({self.parameter}, exact=self.exact))

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        params = await imac_module.read_parameters({self.parameter}, exact=self.exact)
        cmd["parameters_read"].update(params)


class ValidateParams:
    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        invalid = {k for k in cmd["data"]["parameters"] if k not in imac_module.block_specs}
        if invalid:
            raise InvalidCommandData(f"Parameters do not exist in imac module {','.join(invalid)}")

    def __repr__(self):
        return "Validating Parameters"


class ReadParams:
    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        if imac_module._async:
            return self._async_do(cmd, imac_module, **kwargs)
        else:
            return self._sync_do(cmd, imac_module, **kwargs)

    def _sync_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        cmd["parameters_read"].update(imac_module.read_parameters(set(cmd["data"]["parameters"])))

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        params = await imac_module.read_parameters(set(cmd["data"]["parameters"]))
        cmd["parameters_read"].update(params)

    def __repr__(self):
        return "Reading Parameters"


@dataclass
class WriteParams:
    parameters: set = field(default_factory=set)

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        if imac_module._async:
            return self._async_do(cmd, imac_module, **kwargs)
        else:
            return self._sync_do(cmd, imac_module, **kwargs)

    def _sync_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        invalid_params = set(cmd["data"]).difference(self.parameters)
        if invalid_params:
            raise InvalidCommandData(f"Command parameters provided are not valid: {invalid_params}")
        imac_module.write_parameters(cmd["data"])
        cmd["parameters_written"].update(cmd["data"])

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        invalid_params = set(cmd["data"]).difference(self.parameters)
        if invalid_params:
            raise InvalidCommandData(f"Command parameters provided are not valid: {invalid_params}")
        await imac_module.write_parameters(cmd["data"])
        cmd["parameters_written"].update(cmd["data"])

    def __repr__(self):
        return "Writing Parameters"


class WriteAndValidateParams:
    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        """
        Reads a parameter from an imac module
        :param cmd:
        :param imac_module:
        :param kwargs:
        :return:
        """
        if imac_module._async:
            return self._async_do(cmd, imac_module, **kwargs)
        else:
            return self._sync_do(cmd, imac_module, **kwargs)

    def _sync_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        imac_module.write_parameters(cmd["data"])
        cmd["parameters_written"].update(cmd["data"])

    async def _async_do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        await imac_module.write_parameters(cmd["data"])
        read_data = await imac_module.read_parameters(set(cmd["data"]))
        mismatched = [(param, value) for param, value in cmd["data"].items() if value != read_data[param]]
        if mismatched:
            msg = "\n".join(
                f"Parameter '{param}' read back as {read_data[param]}, expected {value}" for param, value in mismatched)
            raise ValidationError(msg)

    def __repr__(self):
        return "Writing and Validating Parameters"


@dataclass
class ValidateParam:
    parameter: str

    def __repr__(self):
        return "Validating parameter"

    def do(self, cmd: dict, **kwargs):
        read_value = cmd["parameters_read"][self.parameter]
        written_value = cmd["parameters_written"][self.parameter]
        if read_value != written_value:
            raise ValidationError(f"Parameter '{self.parameter}' read back as {read_value}, expected {written_value}")


@dataclass
class UpdateMeta:
    parameter: str

    def __repr__(self):
        return "Updating metadata"

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        imac_module.current_state[self.parameter] = cmd["parameters_read"][self.parameter]


@dataclass
class UpdateSpecs:
    def __repr__(self):
        return "Updating module specifications"

    def do(self, cmd: dict, imac_module: ImacModule, **kwargs):
        imac_module.update_specs()


@dataclass
class WaitL1Block:
    def __repr__(self):
        return "Waiting"

    def do(self, cmd: dict, **kwargs):
        pass


@dataclass
class Wait:
    seconds: typing.Union[float, int]

    def __repr__(self):
        return "Waiting"

    def _sync_do(self):
        time.sleep(self.seconds)

    def do(self, cmd: dict, **kwargs):
        if from_coroutine():
            return self._async_do()
        else:
            return self._sync_do()

    async def _async_do(self):
        await asyncio.sleep(self.seconds)


@dataclass
class RespondParam:
    parameter: str
    read_key: str = ""

    def __repr__(self):
        return "Building Response"

    def do(self, cmd: dict, **kwargs):
        key = self.read_key or self.parameter
        cmd["return_values"][self.parameter] = cmd["parameters_read"][key]


@dataclass
class RespondParamsAll:
    def __repr__(self):
        return "Building Response"

    def do(self, cmd: dict, **kwargs):
        cmd["return_values"] = cmd["parameters_read"]


@dataclass
class WaitParam:
    parameter: str
    result: int
    mask: int = 0xffff
    timeout: typing.Union[int, None] = None
    error: typing.Union[int, None] = None

    def __repr__(self):
        return "Waiting for result"

    def do(self, cmd: dict, **kwargs):
        pass


def write_and_validate(parameter: str):
    return [WriteParam(parameter), ReadParam(parameter), ValidateParam(parameter)]


gasguard_2 = {
    "action-catalytic-latch-reset": [
        WriteParam("command-register-code", override=0x1e),
        WriteParam("command-register-result", override=1 << 7),
        WaitParam("command-register-result", 0),
    ],
    "action-remote-telemetry-test": [
        WriteParam("command-register-code", override=0x2d),
        WriteParam("command-register-result", override=1 << 7),
        WaitParam("command-register-result", 0),
    ],
    "get-linearity-test-time": [
        ReadParam("linearity-test-time"),
        RespondParam("linearity-test-time"),
    ],
    "get-parameters": [
        ValidateParams(),
        ReadParams(),
        RespondParamsAll()
    ],
    "get-rtc-time": [
        ReadParam("rtc-time"),
        RespondParam("rtc-time"),
    ],
    "get-t90-test-time": [
        ReadParam("t90-test-time"),
        RespondParam("t90-test-time"),
    ],
    "get-serial-detector": [
        ReadParam("detector-serial-number", exact=False),
        RespondParam("detector-serial-number")
    ],
    "get-telemetry-test-time": [
        ReadParam("telemetry-test-time"),
        RespondParam("telemetry-test-time")
    ],
    "set-aim-compatibility-mode": [
        ValidateIn(range(2)),
        *write_and_validate("aim-compatibility-mode"),
        UpdateMeta("aim-compatibility-mode"),
        # TODO Should require update to specs for the AIM vs GG2 mode for power
        UpdateSpecs(),
    ],
    "set-exception-trigger": [
        ValidateIn(range(20001)),
        *write_and_validate("exception-trigger"),
    ],
    # TODO investigate
    "set-imac-address-rtgm": [
        ValidateIn(range(1, 41)),
        WriteParam("address-power", override=0),
        WriteParam("address-analog", add=40),
        WriteParam("address-flags"),
        ReadParam("address-flags"),
        ReadParam("address-analog"),
        ReadParam("address-power"),
        UpdateMeta("address-flags"),
        UpdateMeta("address-analog"),
        UpdateMeta("address-power"),
        UpdateSpecs(),
        ValidateParam("address-flags"),
        ValidateParam("address-analog"),
        ValidateParam("address-power"),
    ],
    "set-gas-point-1": [
        ValidateIn(range(20001)),
        *write_and_validate("set-point-1"),
    ],
    "set-gas-point-2": [
        ValidateIn(range(20001)),
        *write_and_validate("set-point-2"),
    ],
    "set-gas-point-3": [
        ValidateIn(range(20001)),
        *write_and_validate("set-point-3"),
    ],
    "set-gas-points": [
        ValidateIn(range(20001), key="set-point-1"),
        ValidateIn(range(20001), key="set-point-2"),
        ValidateIn(range(20001), key="set-point-3"),
        WriteParams(parameters={"set-point-1", "set-point-2", "set-point-3"}),
        ReadParam("set-point-1"),
        ValidateParam("set-point-1"),
        ValidateParam("set-point-2"),
        ValidateParam("set-point-3"),
    ],
    "set-healthy-state": [
        ValidateIn(range(5)),
        *write_and_validate("healthy-config"),
    ],
    "set-hysteresis": [
        ValidateIn(range(16)),
        *write_and_validate("hysteresis-config"),
    ],
    "set-imac-address-analog": [
        ValidateIn(range(256)),
        *write_and_validate("address-analog"),
        UpdateMeta("address-analog"),
        UpdateSpecs()
    ],
    "set-imac-address-flags": [
        ValidateIn(range(256)),
        *write_and_validate("address-flags"),
        UpdateMeta("address-flags"),
        UpdateSpecs()
    ],
    "set-imac-address-power": [
        ValidateIn(range(256)),
        *write_and_validate("address-power"),
        UpdateMeta("address-power"),
        UpdateSpecs()
    ],
    "set-imac-address-bypass": [
        ValidateIn(list(range(81, 121)) + [0]),
        *write_and_validate("address-bypass"),
        UpdateSpecs()
    ],
    "set-imac-address-rtc": [
        ValidateIn([x for x in range(256) if x % 4 != 3]),
        *write_and_validate("address-rtc"),
    ],
    "set-power-point-alarm": [
        ValidateRange(0, 24),
        *write_and_validate("power-point-alarm"),
    ],
    "set-power-point-trip": [
        ValidateRange(0, 24),
        *write_and_validate("power-point-trip"),
    ],
    "set-power-points": [
        ValidateRange(8, 24, key="power-point-trip"),
        ValidateRange(10, 24, key="power-point-alarm"),
        WriteParams(parameters={"power-point-trip", "power-point-alarm"}),
        ReadParam("power-point-trip"),
        ValidateParam("power-point-trip"),
        ValidateParam("power-point-alarm"),
    ],
    "set-warmup-config": [
        ValidateIn(range(2)),
        *write_and_validate("warmup-config")
    ],
    "remote-bypass": [
        ValidateIn(range(1, 41), key="address"),
        ValidateIn(range(2), key="value"),
        TopicTask(topic="remote_bypass_gg2", key_map={"logical_address": "address", "value": "value"}),
    ]
}
