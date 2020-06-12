# ##############################################################################
#  Copyright (c) 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This File may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY  OF DESIGN, MERCHANTABILITY AND                      #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""Tests the functions inside of :mod:`~pumpkin_supmcu.supmcu.discovery` and :mod:`~pumpkin_supmcu.supmcu.i2c`."""
import struct
from itertools import repeat, chain
from pumpkin_supmcu import I2CBusSpeed, DataType, datatype_to_supmcu_fmt_char, sizeof_supmcu_type, \
    SupMCUTelemetryDefinition, SupMCUModuleDefinition, typeof_supmcu_fmt_char, Parsers, TelemetryDataItem, \
    parse_header, SupMCUTelemetry, TelemetryType
from pumpkin_supmcu.supmcu.discovery import *


class MockI2CMaster(I2CMaster):
    def __init__(self, expected_values, responses):
        self.expected_values = expected_values
        self.responses = responses

    @property
    def device_name(self) -> str:
        return "MockI2CMaster"

    @property
    def device_speed(self) -> I2CBusSpeed:
        return I2CBusSpeed.Standard

    @property
    def device_pullups(self) -> bool:
        return True

    def write(self, addr: int, b: bytes):
        # Check against the currently set expected value.
        expected_addr, expected_value = self.expected_values.pop(0)
        if addr != expected_addr:
            raise ValueError(f'`addr` does not match `expected_addr`: {addr} != {expected_addr}')
        if b != expected_value:
            raise ValueError(f'`b` does not match `expected_value`: {b} != {expected_value}')
        pass

    def read(self, addr: int, amount: int) -> bytes:
        expected_addr, expected_amount, response = self.responses.pop(0)
        if addr != expected_addr:
            raise ValueError(f'`addr` does not match `expected_addr`: {addr} != {expected_addr}')
        if amount != expected_amount:
            raise ValueError(f'`amount` does not match `expected_amount`: {amount} != {expected_amount}')
        assert len(response) == amount
        return response


VALID_HEADER = bytes([1, 2, 2, 2, 2])
VALID_HEADER_ITEM, _ = parse_header(VALID_HEADER)
VALID_FOOTER = bytes(repeat(0xff, SIZEOF_HEADER_FOOTER - len(VALID_HEADER)))


def _gen_tel_def_request(addr, cmd_name, idx, data_types):
    """
    Generates the expected_values and responses for a telemetry definition request. Used in the Discovery
    """
    # request_telemetry asks for format, name and length in that order for a given cmd_name and idx
    tel_order = ['FORMAT', 'NAME', 'LENGTH']
    expected_write_values = [f'{cmd_name}:TEL? {idx},{tel_item}\n'.encode('ascii') for tel_item in tel_order]
    expected_values = list(zip(repeat(addr, len(expected_write_values)), expected_write_values))

    fmt = ','.join([datatype_to_supmcu_fmt_char(t) for t in data_types])
    name = f'TEL {idx}'
    length = sum([sizeof_supmcu_type(t) for t in data_types]) + SIZEOF_HEADER_FOOTER
    fmt_resp = VALID_HEADER + bytes(fmt, 'ascii') + bytes(
        repeat(0, SUPMCU_FORMAT_DEFINITION.telemetry_length - len(fmt) - SIZEOF_HEADER_FOOTER)) + VALID_FOOTER
    name_resp = VALID_HEADER + bytes(name, 'ascii') + bytes(
        repeat(0, SUPMCU_NAME_DEFINITION.telemetry_length - len(name) - SIZEOF_HEADER_FOOTER)) + VALID_FOOTER
    length_resp = VALID_HEADER + struct.pack("<H", length) + VALID_FOOTER
    responses = [fmt_resp, name_resp, length_resp]
    return expected_values, [(addr, len(r), r) for r in responses], SupMCUTelemetryDefinition(name, length, idx, fmt)


def _gen_mod_def_request(addr, mod_name, cmd_name, sup_data_types, mod_data_types):
    """
    Generates the module request test data for a given `addr` module command name `cmd_name`. The number of telemetry
    items created depends on the amount of `sup_data_types` and `mod_data_types` members. Uses `mod_name` as
    the module name for the :class:`~pumpkin_supmcu.SupMCUModuleDefinition`.
    """
    # Generate the write request for the amount of telemetry as well as the response.
    expected_values = [(addr, bytes(SUPMCU_TELEMETRY_AMOUNT_STR, 'ascii'))]
    amount_response = VALID_HEADER + struct.pack("<2H", len(sup_data_types), len(mod_data_types)) + VALID_FOOTER
    responses = [(addr, len(amount_response), amount_response)]
    sup_defs = []
    mod_defs = []

    # Now generate responses for the sup types then for the module types as that is the order that the module_discovery
    # will query the SupMCU modules.
    sup_req = [(addr, "SUP", i, dt) for dt, i in zip(sup_data_types, range(len(sup_data_types)))]
    mod_req = [(addr, cmd_name, i, dt) for dt, i in zip(mod_data_types, range(len(mod_data_types)))]
    for req in sup_req:
        val, resp, d = _gen_tel_def_request(*req)
        expected_values.extend(val)
        responses.extend(resp)
        sup_defs.append(d)
    for req in mod_req:
        val, resp, d = _gen_tel_def_request(*req)
        expected_values.extend(val)
        responses.extend(resp)
        mod_defs.append(d)

    # transform into proper types for the SupMCUModuleDefinition
    mod_defs = dict([(i, d) for i, d in zip(range(len(mod_defs)), mod_defs)])
    sup_defs = dict([(i, d) for i, d in zip(range(len(sup_defs)), sup_defs)])
    return expected_values, responses, SupMCUModuleDefinition(mod_name, cmd_name, addr, sup_defs, mod_defs)


TEST_I2C_ADDR = 0xab
TEST_MOD_CMD_NAME = "TST"
TEST_MOD_NAME = "Test"
SUP_TYPE_TEST_DATA = list(repeat([t for t in DataType if t not in [DataType.Str, DataType.Hex16, DataType.Hex8]], 15))
MOD_TYPE_TEST_DATA = list(repeat([t for t in DataType if t not in [DataType.Str, DataType.U8, DataType.U16]], 15))


def test_request_telemetry_definition():
    """
    Tests the :func:`~pumpkin_supmcu.request_telemetry_definition` to make sure requesting telemetry returns the
    correct values
    """
    vals, resps, defs = [], [], []
    # generate data for test
    for mod_types, idx in zip(MOD_TYPE_TEST_DATA, range(len(MOD_TYPE_TEST_DATA))):
        val, resp, d = _gen_tel_def_request(TEST_I2C_ADDR, TEST_MOD_CMD_NAME, idx, mod_types)
        vals.extend(val)
        resps.extend(resp)
        defs.append(d)

    i2c_master = MockI2CMaster(vals, resps)
    for expected, idx in zip(defs, range(len(defs))):
        assert request_telemetry_definition(i2c_master, TEST_I2C_ADDR, TEST_MOD_CMD_NAME, idx, 0) == expected


def test_request_module_definition():
    """
    Tests the :func:`~pumpkin_supmcu.request_module_definition` to make sure requesting a whole module returns the
    correct values
    """
    vals, resps, expected_mod_def = _gen_mod_def_request(TEST_I2C_ADDR, TEST_MOD_NAME, TEST_MOD_CMD_NAME,
                                                         SUP_TYPE_TEST_DATA,
                                                         MOD_TYPE_TEST_DATA)
    i2c_master = MockI2CMaster(vals, resps)
    assert request_module_definition(i2c_master, TEST_I2C_ADDR, TEST_MOD_CMD_NAME, TEST_MOD_NAME, 0) == expected_mod_def


# Testing pumpkin_supmcu.supmcu.i2c module
TEST_DATATYPE_VALUES = {
    DataType.U8: 127,
    DataType.U16: 1234,
    DataType.U32: 123456,
    DataType.U64: 12345678,
    DataType.I8: -127,
    DataType.I16: -1234,
    DataType.I32: -123456,
    DataType.I64: -12345678,
    DataType.Hex8: 127,
    DataType.Hex16: 1234,
    DataType.Float: 1.25,
    DataType.Double: 1.25,
    DataType.Char: bytes('c', 'ascii')
}


def _gen_supmcu_telemetry(supmcu_tel_def, addr):
    """Generates a SupMCUTelemetry from the given `supmcu_tel_def`."""
    # Get data for each valid format character
    data = []
    data_bytes = bytes(VALID_HEADER)
    for c in supmcu_tel_def.format:
        try:
            dt = typeof_supmcu_fmt_char(c)
        except KeyError:
            # Probably a comma in the format string
            continue
        parser = Parsers[c]

        item_data = TEST_DATATYPE_VALUES[dt]
        str_data = parser.str_parse(item_data)
        data.append(TelemetryDataItem(dt, item_data, str_data))
        data_bytes += struct.pack(parser.struct_fmt_specifier, item_data)

    return SupMCUTelemetry(VALID_HEADER_ITEM, data), (addr, supmcu_tel_def.telemetry_length, data_bytes + VALID_FOOTER)


def _gen_supmcu_master_test(addr, mod_name, cmd_name, sup_data_types, mod_data_types):
    """Generates the necessary data in order to test the SupMCUMaster class."""
    # Generate the module definition to be used, and generate sample telemetry items based off of the module definition.
    _, _, module_def = _gen_mod_def_request(addr, mod_name, cmd_name, sup_data_types, mod_data_types)
    expected_inputs = []
    response_bytes = []
    expected_outputs = []

    sorted_mod_tel = map(lambda i: i[1], sorted(module_def.module_telemetry.items(), key=lambda x: x[0]))
    sorted_sup_tel = map(lambda i: i[1], sorted(module_def.supmcu_telemetry.items(), key=lambda x: x[0]))

    # Generate expected inputs and outputs for the SupMCUMaster
    for d, mod in chain(zip(sorted_sup_tel, repeat('SUP', len(module_def.supmcu_telemetry))),
                        zip(sorted_mod_tel, repeat(cmd_name, len(module_def.module_telemetry)))):
        inp = (addr, bytes(f'{mod}:TEL? {d.idx}\n', 'ascii'))
        expected_inputs.append(inp)
        tel, b = _gen_supmcu_telemetry(d, addr)
        response_bytes.append(b)
        expected_outputs.append(tel)
    return expected_inputs, response_bytes, expected_outputs, module_def


def test_supmcu_master():
    inps, resp, outputs, mod_def = _gen_supmcu_master_test(TEST_I2C_ADDR, TEST_MOD_NAME, TEST_MOD_CMD_NAME,
                                                           SUP_TYPE_TEST_DATA, MOD_TYPE_TEST_DATA)
    mock = MockI2CMaster(inps, resp)
    master = SupMCUMaster(mock, [mod_def], 0.0)
    sorted_mod_tel = map(lambda i: i[1], sorted(mod_def.module_telemetry.items(), key=lambda x: x[0]))
    sorted_sup_tel = map(lambda i: i[1], sorted(mod_def.supmcu_telemetry.items(), key=lambda x: x[0]))
    for output, test in zip(outputs,
                            chain(zip(sorted_sup_tel, repeat(TelemetryType.SupMCU, len(mod_def.supmcu_telemetry))),
                                  zip(sorted_mod_tel, repeat(TelemetryType.Module, len(mod_def.module_telemetry))))):
        d, t = test
        item = master.request_telemetry(mod_def.cmd_name, t, d.idx)
        assert item == output
