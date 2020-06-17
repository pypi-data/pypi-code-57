#  (C) Copyright 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
The SupMCU interface is the responsibility of the :class:`~pumpkin_supmcu.SupMCUMaster` class. This provides the
interface to request telemetry and write commands that are registered with the :class:`~pumpkin_supmcu.SupMCUMaster`.
Note that the telemetry definitions need to be discovered via the :func:`~pumpkin_supmcu.request_telemetry_definition`
for single telemetry items or :func:`~pumpkin_supmcu.request_module_definition` for whole modules.
"""
import time
from typing import Optional, Iterable, Union, Dict

from .parsing import parse_telemetry
from .types import SupMCUModuleDefinition, SupMCUTelemetry, TelemetryType
from ..i2c import I2CMaster


class SupMCUMaster:
    """
    An interface into communicating to SupMCU modules via I2CMaster object.

    :ivar i2c_master: The underling I2CMaster device used to communicate with the I2C bus.
    """

    def __init__(self,
                 i2c_master: I2CMaster,
                 supmcu_modules: Optional[Iterable[SupMCUModuleDefinition]] = None,
                 request_delay: float = 0.1):
        """
        Initializes the SupMCUMaster device for communicating with the SupMCU modules over I2C.

        :param i2c_master: The I2CMaster device to use for communicating with the I2C Bus.
        :param supmcu_modules: The list of SupMCU modules on the bus. Can be set via `supmcu_modules` property.
        """
        self.i2c_master = i2c_master
        self._request_delay = request_delay
        if supmcu_modules is None:
            supmcu_modules = []

        # Convert supmcu_modules into a mapping of address to SupMCUModuleDefinition
        self._supmcu_modules: Dict[int, SupMCUModuleDefinition] = {}
        self.supmcu_modules = supmcu_modules

    @property
    def supmcu_modules(self) -> Iterable[SupMCUModuleDefinition]:
        """Returns the list of SupMCUModuleDefinitions known by the SupMCUMaster."""
        return self._supmcu_modules.values()

    @supmcu_modules.setter
    def supmcu_modules(self, supmcu_modules: Iterable[SupMCUModuleDefinition]):
        """
        Sets the SupMCUModuleDefinitions for the SupMCUMaster used by the `request_telemetry` method to parse
        the SupMCU telemetry.

        :param supmcu_modules: The new iterable of SupMCUModuleDefinitions. Replaces the previously set modules.
        """
        self._supmcu_modules = {mod.address: mod for mod in supmcu_modules}
        self._supmcu_name_address = {mod.name: mod.address for mod in supmcu_modules}
        self._supmcu_cmd_name_address = {mod.cmd_name: mod.address for mod in supmcu_modules}

        # Make sure that we don't have duplicate addresses/command names/names
        assert len(supmcu_modules) == len(self._supmcu_modules) == len(
            self._supmcu_name_address) == len(self._supmcu_cmd_name_address)

    @property
    def request_delay(self) -> float:
        """
        The amount of delay in seconds that is made between a telemetry write and read request.

        :return: The amount in fractional seconds between the TEL? write and read I2C transactions.
        """
        return self._request_delay

    @request_delay.setter
    def request_delay(self, value: float):
        """
        Set the amount of delay in seconds that is made between a telemetry write and read request.

        :param value: The amount of delay in fractional seconds.
        """
        if value <= 0:
            raise ValueError(f"value cannot be less than or equal to 0: {value}")

        self._request_delay = value

    def _resolve_module_address(self, name: str) -> int:
        """Internal method for figuring out the I2C address from a given command_name or module name."""
        # Check for command name first then for the module name
        try:
            return self._supmcu_cmd_name_address[name]
        except KeyError:
            # Unable to find by command name
            pass

        try:
            return self._supmcu_name_address[name]
        except KeyError:
            raise ValueError(f"No such module by name or command name `{name}` in supmcu_modules.")

    def send_command(self, module: Union[int, str], cmd: str):
        """
        Sends the SCPI command `cmd` to the `module` given. The module must be in the list of the registered modules
        `supmcu_modules`.

        :param module: The I2C, cmd_name or name of the module to send the command to.
        :param cmd: The command to send to the module.
        """
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        if isinstance(module, str):
            module = self._resolve_module_address(module)

        if module not in self._supmcu_modules:
            raise ValueError(f"No such module with I2C address `{hex(module)}` in supmcu_modules.")

        # Write the command out to the module.
        self.i2c_master.write(module, cmd.encode('ascii'))

    def request_telemetry(self, module: Union[int, str], tel_type: TelemetryType, idx: int) -> SupMCUTelemetry:
        """
        Requests the telemetry of `tel_type` at index `idx` from the `module`. `module` can be a I2C address, command
        name or the name of a module contained in `supmcu_modules`.

        This will write the I2C request to the I2C Master, then wait `self.request_delay` seconds before reading
        the telemetry back from the I2C Master.

        :param module: The I2C address/command_name or name of the module to request telemetry from.
        :param tel_type: The type of telemetry being requested.
        :param idx: The telemetry index being requested.
        :return: The backing SupMCUTelemetry object from the telemetry request.
        """
        if isinstance(module, str):
            module = self._resolve_module_address(module)
        try:
            module_def = self._supmcu_modules[module]
        except KeyError:
            raise ValueError(f"No such module with I2C address `{hex(module)}` in supmcu_modules.")

        if tel_type == TelemetryType.SupMCU:
            module_tel_defs = module_def.supmcu_telemetry
            cmd_str = "SUP"
        else:
            module_tel_defs = module_def.module_telemetry
            cmd_str = module_def.cmd_name

        try:
            tel_def = module_tel_defs[idx]
        except IndexError:
            raise ValueError(f"No definition found for corresponding `{cmd_str}:TEL? {idx}` command.")

        # Send the telemetry request, and parse the response.
        cmd_str = f"{cmd_str}:TEL? {tel_def.idx}\n"
        self.i2c_master.write(module_def.address, cmd_str.encode('ascii'))
        time.sleep(self.request_delay)
        b = self.i2c_master.read(module_def.address, tel_def.telemetry_length)
        return parse_telemetry(b, tel_def)
