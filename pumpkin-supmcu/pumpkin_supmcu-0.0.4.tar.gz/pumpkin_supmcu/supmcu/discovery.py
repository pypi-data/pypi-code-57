# coding: utf-8
# ##############################################################################
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
The discovery modules allow for automated discovery of all SupMCU and module telemetry definitions for a given I2C
address. The list of telemetry items can be serialized after the fact and loaded again at a later time to avoid the
lengthy discovery process.
"""
import time
from typing import Union, Optional

from .i2c import SupMCUMaster
from .parsing import parse_telemetry
from .types import SupMCUTelemetryDefinition, SupMCUModuleDefinition
from ..i2c import I2CMaster

SIZEOF_HEADER_FOOTER = 13
SUPMCU_LENGTH_DEFINITION = SupMCUTelemetryDefinition("Length", 2 + SIZEOF_HEADER_FOOTER, 0, "s")
SUPMCU_NAME_DEFINITION = SupMCUTelemetryDefinition("Name", 33 + SIZEOF_HEADER_FOOTER, 0, "S")
SUPMCU_FORMAT_DEFINITION = SupMCUTelemetryDefinition("Format", 25 + SIZEOF_HEADER_FOOTER, 0, "S")
SUPMCU_TELEMETRY_AMOUNT_DEFINITION = SupMCUTelemetryDefinition("Amount", 4 + SIZEOF_HEADER_FOOTER, 14, "s,s")
SUPMCU_TELEMETRY_AMOUNT_STR = "SUP:TEL? 14\n"
_DEFAULT_RESPONSE_DELAY = 0.1  # 100 ms between I2C Write and Read


def _write_read_supcmu_i2c(i2c_master: I2CMaster,
                           address: int,
                           cmd: str,
                           read_length: int,
                           response_delay: float) -> bytes:
    """
    Writes to the I2C bus `cmd` to I2C Address `address`, then sleeps `response_delay` seconds, and finally reads
    `read_length` bytes from the I2C Address. Meant for internal usage in the request_telemetry_definition function.

    :param i2c_master: The I2CMaster object to use for the telemetry request.
    :param address: The I2C address to send the command to.
    :param cmd: The command to send to the I2C device.
    :param read_length: The amount of bytes to read back from the I2C device.
    :param response_delay: The amount of time in seconds to wait between the I2C write and read.
    :return: The response in bytes.
    """
    i2c_master.write(address, cmd.encode('ascii'))
    time.sleep(response_delay)
    return i2c_master.read(address, read_length)


def request_telemetry_definition(i2c_master: Union[I2CMaster, SupMCUMaster],
                                 address: int,
                                 module_cmd_name: str,
                                 idx: int,
                                 response_delay: Optional[float] = None) -> SupMCUTelemetryDefinition:
    """
    Requests the formatting, name and length information from the device at I2C address `address`, using the module
    short name `module_cmd_name` (e.g. BM for Battery Module), concatenating that with `idx` in a telemetry request
    s.t. cmd_to_send is `<module_cmd_name>:TEL? <idx>,NAME/FORMAT/LENGTH`

    :param i2c_master: The I2CMaster device to use.
    :param address: The address of the device to request information from.
    :param module_cmd_name: The module name used in the context of SCPI commands (e.g. DCPS for Desktop CubeSat Power
                            Supply).
    :param idx: The telemetry index to grab the information for.
    :param response_delay: The amount of time in seconds to wait between I2C Write and read. Can be None, or set
                            from SupMCUMaster passed in as `i2c_master`.
    :return: The SupMCUTelemetryDefinition that represents the Telemetry data.
    """
    if isinstance(i2c_master, SupMCUMaster):
        if response_delay is None:
            response_delay = i2c_master.request_delay
        i2c_master = i2c_master.i2c_master
    if response_delay is None:
        # None was set by the SupMCU master or the passed in variable.
        response_delay = _DEFAULT_RESPONSE_DELAY

    # Find out format, name and length information
    format_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},FORMAT\n',
                                          SUPMCU_FORMAT_DEFINITION.telemetry_length, response_delay)
    name_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},NAME\n',
                                        SUPMCU_NAME_DEFINITION.telemetry_length, response_delay)
    length_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},LENGTH\n',
                                          SUPMCU_LENGTH_DEFINITION.telemetry_length, response_delay)

    # Parse the response bytes as telemetry items, then check to see if any are not ready yet
    format_response = parse_telemetry(format_bytes, SUPMCU_FORMAT_DEFINITION)
    name_response = parse_telemetry(name_bytes, SUPMCU_NAME_DEFINITION)
    length_response = parse_telemetry(length_bytes, SUPMCU_LENGTH_DEFINITION)

    # Raise exception if any of the responses are flagged as not ready.
    if not format_response.header.ready:
        raise RuntimeError(
            f'`{module_cmd_name}:TEL? {idx},FORMAT` returned a non-ready response. Try increasing `response_delay`.')
    if not name_response.header.ready:
        raise RuntimeError(
            f'`{module_cmd_name}:TEL? {idx},NAME` returned a non-ready response. Try increasing `response_delay`.')
    if not length_response.header.ready:
        raise RuntimeError(
            f'`{module_cmd_name}:TEL? {idx},LENGTH` returned a non-ready response. try increasing `response_delay`.')

    # Create the telemetry definition
    return SupMCUTelemetryDefinition(name_response.items[0].value,
                                     length_response.items[0].value,
                                     idx,
                                     format_response.items[0].value)


def request_module_definition(i2c_master: Union[I2CMaster, SupMCUMaster],
                              address: int,
                              module_cmd_name: str,
                              module_name: Optional[str] = None,
                              response_delay: Optional[float] = None) -> SupMCUModuleDefinition:
    """
    Requests all of the telemetry definitions from the module at I2C Address `address`, using `module_cmd_name` when
    requesting module telemetry definitions.

    :param i2c_master: The I2C master to write/read the requests from.
    :param address: The address of the module on the I2C bus.
    :param module_cmd_name: The short name of the module as used in telemetry requests (e.g. BM for Battery Module).
    :param module_name: Optional name to give module, if None, then is set to `module_cmd_name`
    :param response_delay: The delay in seconds to wait between I2C read and I2C write.
    :return: The module definition for the device at I2C Address `address`
    """
    if isinstance(i2c_master, SupMCUMaster):
        if response_delay is None:
            response_delay = i2c_master.request_delay
        i2c_master = i2c_master.i2c_master
    if response_delay is None:
        # None was set by the SupMCU master or the passed in variable.
        response_delay = _DEFAULT_RESPONSE_DELAY
    if module_name is None:
        module_name = module_cmd_name

    # Grab the amount of telemetry items on the module, then start requesting ALL telemetry definitions.
    amount_resp = _write_read_supcmu_i2c(i2c_master,
                                         address,
                                         SUPMCU_TELEMETRY_AMOUNT_STR,
                                         SUPMCU_TELEMETRY_AMOUNT_DEFINITION.telemetry_length,
                                         response_delay)
    amount_telemetry = parse_telemetry(amount_resp, SUPMCU_TELEMETRY_AMOUNT_DEFINITION)
    supmcu_amount, module_amount = amount_telemetry.items[0].value, amount_telemetry.items[1].value

    supmcu_defs = {}
    for idx in range(supmcu_amount):
        supmcu_defs[idx] = request_telemetry_definition(i2c_master, address, 'SUP', idx, response_delay)
    module_defs = {}
    for idx in range(module_amount):
        module_defs[idx] = request_telemetry_definition(i2c_master, address, module_cmd_name, idx, response_delay)
    return SupMCUModuleDefinition(module_name, module_cmd_name, address, supmcu_defs, module_defs)
