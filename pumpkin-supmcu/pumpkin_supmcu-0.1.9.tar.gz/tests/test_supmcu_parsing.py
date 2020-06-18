# coding: utf-8
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
"""Tests the :func:`pumpkin_supmcu.parse_telemetry` and :func:`pumpkin_supmcu.parse_header` functions."""
import struct
from itertools import combinations

from pumpkin_supmcu import parse_header, parse_telemetry, SupMCUHDR, Parsers, DataType, TelemetryDataItem, \
    sizeof_supmcu_type, SupMCUTelemetry, SupMCUTelemetryDefinition, datatype_to_supmcu_fmt_char

# Testing the parse_header function.
NOT_ENOUGH_BYTES_HEADER = bytes([1, 2, 3, 4])  # Not enough bytes
VALID_HEADER = SupMCUHDR(ready=True, timestamp=1234)
VALID_HEADER_BYTES = struct.pack("<?I", VALID_HEADER.ready, VALID_HEADER.timestamp)


def test_bad_header_parse():
    """Tests :func:`~pumpkin_supmcu.parse_header` to validate raising ValueError on not enough header bytes."""
    try:
        parse_header(NOT_ENOUGH_BYTES_HEADER)
        assert False and "`test_bad_header_parse()` failed. No ValueError thrown."
    except ValueError as e:
        assert str(e) == '`b` does not contain enough bytes: expected len(b) >= 5 got 4'


def test_header_parse():
    """Tests :func:`~pumpkin_supmcu.parse_header` to validate parsing a correctly defined SupMCUHDR."""
    hdr, _ = parse_header(VALID_HEADER_BYTES)
    assert hdr == VALID_HEADER


# Testing the parse_telemetry function.
VALID_FOOTER = bytes([i for i in range(1, 9)])
DATA_TYPE_TO_VALUE = {
    DataType.Hex16: 0xafaf,
    DataType.Hex8: 0xaf,
    DataType.Double: 1.25,
    DataType.Float: 1.25,
    DataType.U8: 127,
    DataType.U16: 1234,
    DataType.U32: 123456,
    DataType.U64: 68719476735,
    DataType.I8: -127,
    DataType.I16: -1234,
    DataType.I32: -123456,
    DataType.I64: -68719476735,
    DataType.Char: bytes('a', 'ascii'),
    DataType.Str: bytes('This is a string with a null terminator added.', 'ascii') + bytes([0])
}


def _gen_parse_fixed_tel_data(test_comb):
    """Internal method used to generate the test cases for parse_telemetry."""
    cur_len = len(VALID_HEADER_BYTES) + 8  # +8 for sizeof telemetry footer
    byte_value = bytearray(VALID_HEADER_BYTES)
    fmt = ""
    expected_response_items = []
    for data_type, fmt_char, value in test_comb:
        # grab the struct fmt char from the parsers
        try:
            struct_fmt = Parsers[fmt_char].struct_fmt_specifier
            str_fmt = Parsers[fmt_char].str_parse
            byte_value += struct.pack(f"{struct_fmt}", value)
        except AttributeError:
            # Dealing with the string parser here
            struct_fmt = f'<{len(value)}s'
            str_fmt = str
            byte_value += struct.pack(f"{struct_fmt}", value)
            value = str(value[:-1], 'ascii')
        expected_response_items.append(TelemetryDataItem(data_type, value, str_fmt(value)))
        item_len = sizeof_supmcu_type(data_type)
        if item_len is None:
            cur_len += len(value)
        else:
            cur_len += sizeof_supmcu_type(data_type)
        fmt += f'{fmt_char},'

    fmt = fmt[:-1]
    # add some footer at the end, its ignored for now, but will cause errors if not there
    byte_value += VALID_FOOTER
    return SupMCUTelemetry(VALID_HEADER, expected_response_items), SupMCUTelemetryDefinition(fmt, cur_len, 0,
                                                                                             fmt), byte_value


# Generate all possible combinations of 1,2,3,4 the test cases for fixed items
parse_telemetry_test_cases = [_gen_parse_fixed_tel_data([(t, datatype_to_supmcu_fmt_char(t), v)]) for t, v in
                              DATA_TYPE_TO_VALUE.items()]
for i in range(2, 5):
    for comb in combinations(DATA_TYPE_TO_VALUE.items(), i):
        parse_telemetry_test_cases.append(
            _gen_parse_fixed_tel_data([(t, datatype_to_supmcu_fmt_char(t), v) for t, v in comb]))


def test_parse_telemetry():
    """Tests :func:`~pumpkin_supmcu.parse_telemetry` function with multiple different variations of tests"""
    for expected, tel_def, bytes_value in parse_telemetry_test_cases:
        parsed = parse_telemetry(bytes_value, tel_def)
        assert parsed == expected


# Create failure test cases, add header and footer to each
BAD_TELEMETRY_TEST_CASES = [
    (bytes("Python doesn't add a null-terminator when encoding strings as bytes", 'ascii'),
     datatype_to_supmcu_fmt_char(DataType.Str), '`b` does not contain a null-terminated string'),
    # bad fixed size item
    (struct.pack("<I", 1234)[:-1], datatype_to_supmcu_fmt_char(DataType.U32),
     f'Incorrect format string `{datatype_to_supmcu_fmt_char(DataType.U32)}`. Expected `17` bytes, got `16` bytes.'),
]
BAD_TELEMETRY_TEST_CASES = [(VALID_HEADER_BYTES + b + VALID_FOOTER, fmt, err) for b, fmt, err in
                            BAD_TELEMETRY_TEST_CASES]


def test_parse_telemetry_fail():
    """
    Tests :func:`~pumpkin_supmcu.parse_telemetry` function to make sure a :class:`ValueError` is thrown when fed with
    non-valid telemetry bytes.
    """
    for test, fmt, err in BAD_TELEMETRY_TEST_CASES:
        try:
            parse_telemetry(test, fmt)
            assert 0 and 'No error for {test}:{fmt}'
        except ValueError as e:
            assert str(e) == err
