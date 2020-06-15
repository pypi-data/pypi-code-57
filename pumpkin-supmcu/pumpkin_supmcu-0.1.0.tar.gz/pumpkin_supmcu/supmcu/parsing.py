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
The telemetry parsing system for the :mod:`pumpkin_supmcu` package uses a set of :class:`~pumpkin_supmcu.DataItemParser`
to parse the various different data formats returned from the SupMCU modules.
These are used by the :func:`pumpkin_supmcu.parse_telemetry` method in conjunction with the
:class:`pumpkin_supmcu.SupMCUTelemetryDefinition` in order to parse any set of telemetry from the SupMCU modules.
"""
import struct
import sys
from abc import abstractmethod
from typing import Tuple, Callable, List, Dict, Union, Any

from .types import TelemetryDataItem, SupMCUHDR, SupMCUTelemetry, SupMCUTelemetryDefinition, DataType, \
    sizeof_supmcu_type, typeof_supmcu_fmt_char

if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    from typing import Protocol
else:
    from typing_extensions import Protocol


def parse_header(b: bytes) -> Tuple[SupMCUHDR, bytes]:
    """
    Parses the SupMCU Telemetry header from the bytes and returns the SupMCUHDR object and the left-over
    bytes.

    :param b: The bytes to parse the SupMCU header from.
    :return: A tuple of the SupMCUHDR object and the left-over bytes.
    """
    header_bytes_len = 5
    header_fmt = "<?I"
    parse_bytes = b[:header_bytes_len]
    left_over = b[header_bytes_len:]
    try:
        return SupMCUHDR(*struct.unpack(header_fmt, parse_bytes)), left_over
    except struct.error:
        raise ValueError(f'`b` does not contain enough bytes: expected len(b) >= 5 got {len(b)}')


class DataItemParser(Protocol):
    """Parses a series of bytes for a given SupMCU `fmt_specifier` returning the corresponding python type."""
    fmt_specifier: List[str]
    fmt_type: DataType

    @abstractmethod
    def parse(self, b: bytes) -> Tuple[TelemetryDataItem, bytes]:
        """
        Parses the byte array for a DataItem and returns the left-over bytes after parsing the data item.

        :param b: The input bytes to parse the data item from
        :return: A tuple of the data item parsed and remaining bytes
        """


class _FixedSizeParser(DataItemParser):
    """Parses a fixed-size data item in a bytes array."""

    def __init__(self,
                 supmcu_fmt_specifier: List[str],
                 struct_fmt_specifier: str,
                 data_type: DataType,
                 size: int,
                 str_parse: Callable[[Any], str]):
        self.fmt_type = data_type
        self.fmt_specifier = supmcu_fmt_specifier
        self.struct_fmt_specifier = struct_fmt_specifier
        self.size = size
        self.str_parse = str_parse

    def parse(self, b: bytes) -> Tuple[TelemetryDataItem, bytes]:
        """
        Parses a fixed number of bytes as a telemetry item.
        :param b: The bytes to parse the data from.
        :return: The DataItem parsed, and the left-over bytes
        """
        left = b[self.size:]
        parse_bytes = b[:self.size]

        value, = struct.unpack(self.struct_fmt_specifier, parse_bytes)
        return TelemetryDataItem(self.fmt_type, value, self.str_parse(value)), left


class _StringParser(DataItemParser):
    """Parses null-terminated strings from the byte array"""

    def __init__(self):
        self.fmt_type = DataType.Str
        self.fmt_specifier = ['S']

    def parse(self, b: bytes) -> Tuple[TelemetryDataItem, bytes]:
        """
        Parses a null-terminated string from the bytes, clamping any single byte value to 127 in the
        bytes for the null-terminated string.

        :param b: The bytes to parse the null-terminated string from.
        :return: The DataItem representing the null-terminated string and the bytes left over.
        :raises ValueError: If the bytes don't contain a null-terminated string.
        """
        try:
            null_term_pos = b.index(0)
        except ValueError:
            raise ValueError("`b` does not contain a null-terminated string")
        parse_bytes = b[:null_term_pos]
        left = b[null_term_pos + 1:]  # Everything AFTER the null terminator

        # Change any byte with a value over 127 to 127
        parse_bytes = bytes([b if b < 128 else 127 for b in parse_bytes])
        return TelemetryDataItem(self.fmt_type, str(parse_bytes, 'ascii'), str(parse_bytes, 'ascii')), left


_parsers = [
    _FixedSizeParser(['c'], '<c', DataType.Char, 1, str),
    _FixedSizeParser(['u'], '<B', DataType.U8, 1, str),
    _FixedSizeParser(['t'], '<b', DataType.I8, 1, str),
    _FixedSizeParser(['s'], '<H', DataType.U16, 2, str),
    _FixedSizeParser(['n'], '<h', DataType.I16, 2, str),
    _FixedSizeParser(['i'], '<I', DataType.U32, 4, str),
    _FixedSizeParser(['d'], '<i', DataType.I32, 4, str),
    _FixedSizeParser(['l'], '<Q', DataType.U64, 8, str),
    _FixedSizeParser(['k'], '<q', DataType.I64, 8, str),
    _FixedSizeParser(['f'], '<f', DataType.Float, 4, str),
    _FixedSizeParser(['F'], '<d', DataType.Double, 8, str),
    _FixedSizeParser(['x', 'X'], '<B', DataType.Hex8, 1, lambda v: '0x{:02X}'.format(v)),
    _FixedSizeParser(['z', 'Z'], '<H', DataType.Hex16, 2, lambda v: '0x{:04X}'.format(v)),
    _StringParser()
]
_parsers = [[(fmt_char, p) for fmt_char in p.fmt_specifier] for p in _parsers]
Parsers: Dict[str, DataItemParser] = dict(parser_item for l in _parsers for parser_item in l)
"""Contains a mapping of SupMCU format character to appropriate parser for the format specifier"""


def _format_to_length(fmt_str: str) -> int:
    """
    Returns the amount of bytes the SupMCU formatting string `fmt_str` would use. Raises ValueError if
    the `fmt_str` includes a String, as those are not statically sized.

    :param fmt_str: The format string to calculate the size for.
    :return: The size in bytes.
    :raises ValueError: If the fmt_str includes a String.
    """
    tel_length = 0
    for c in fmt_str:
        try:
            size = sizeof_supmcu_type(typeof_supmcu_fmt_char(c))
        except KeyError:
            continue
        if size is None:
            raise ValueError(f'`{fmt_str}` contains dynamically sized items.')
        tel_length += size

    return tel_length


_SIZEOF_FOOTER = 8  # There is a footer on telemetry items...


def parse_telemetry(b: bytes, supmcu_telemetry_def: Union[str, SupMCUTelemetryDefinition]) -> SupMCUTelemetry:
    """
    Parses the bytes `b` as SupMCU telemetry using the given `supmcu_telemetry_def` format string or definition.

    :param b: The telemetry bytes to parse.
    :param supmcu_telemetry_def: The SupMCU format string or definition to use.
    :return: A SupMCU parsed telemetry item.
    """
    if isinstance(supmcu_telemetry_def, SupMCUTelemetryDefinition):
        assert_str = f'Incorrect format string `{supmcu_telemetry_def.format}` for `{supmcu_telemetry_def.name}`.'
        supmcu_fmt = supmcu_telemetry_def.format
    else:
        supmcu_fmt = supmcu_telemetry_def
        assert_str = f'Incorrect format string `{supmcu_fmt}`.'

    # Parse the SupMCU header
    header, b = parse_header(b)

    try:
        length = _format_to_length(supmcu_fmt)
    except ValueError:
        # We're unable to parse the supmcu_fmt string because of dynamically sized telemetry item.
        length = None

    if length is not None and length != (len(b) - _SIZEOF_FOOTER):
        hdr_size = 5
        raise ValueError(
            f'{assert_str} Expected `{length + _SIZEOF_FOOTER + hdr_size}` bytes, got `{len(b) + hdr_size}` bytes.')

    # Parse out each character of the format string one by one
    items = []
    for c in supmcu_fmt:
        try:
            item, b = Parsers[c].parse(b)
            items.append(item)
        except KeyError:
            # We don't care if a formatter wasn't found for the format specifier, as there can be non-format characters
            # in the format string (e.g. SUP:TEL? 14,FORMAT returns `s,s` where the `,` is not a format specifier).
            pass

    return SupMCUTelemetry(header, items)
