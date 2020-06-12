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
These data types are used throughout the :mod:`pumpkin_supmcu.supmcu` to type and structure the module definitions.
"""
from enum import Enum
from typing import NamedTuple, Dict, Any, List


class DataType(Enum):
    """
    Different possible data types that can be returned from SupMCU Telemetry
    """
    Str = 1
    """A null-terminated string"""
    Char = 2
    """A single `char` character"""
    U8 = 3
    """A `uint8_t` item."""
    I8 = 4
    """A `int8_t` item."""
    U16 = 5
    """A `uint16_t` item."""
    I16 = 6
    """A `int16_t` item."""
    U32 = 7
    """A `uint32_t` item."""
    I32 = 8
    """A `int32_t` item."""
    U64 = 9
    """A `uint64_t` item."""
    I64 = 10
    """A `int64_t` item."""
    Float = 11
    """A `float` item."""
    Double = 12
    """A `double` item."""
    Hex8 = 13
    """A `uint8_t` item, displayed as a hexadecimal value."""
    Hex16 = 14
    """A `uint16_t` item, displayed as a hexadecimal value."""


class TelemetryType(Enum):
    """Represents a module request for the SUP:TEL? items or MOD:TEL? items."""
    SupMCU = 0
    """SupMCU telemetry item (e.g. SUP:TEL? #)"""
    Module = 1
    """Module telemetry items (e.g. BM:TEL? #)"""


_data_type_sizes = {
    DataType.Str: None,
    DataType.Char: 1,
    DataType.U8: 1,
    DataType.I8: 1,
    DataType.U16: 2,
    DataType.I16: 2,
    DataType.U32: 4,
    DataType.I32: 4,
    DataType.U64: 8,
    DataType.I64: 8,
    DataType.Float: 4,
    DataType.Double: 8,
    DataType.Hex8: 1,
    DataType.Hex16: 2
}

_supmcu_fmt_data_type = {
    'S': DataType.Str,
    'c': DataType.Char,  # char
    'u': DataType.U8,  # uint8_t
    't': DataType.I8,  # int8_t
    's': DataType.U16,  # uint16_t
    'n': DataType.I16,  # int16_t
    'i': DataType.U32,  # uint32_t
    'd': DataType.I32,  # int32_t
    'l': DataType.U64,  # uint64_t
    'k': DataType.I64,  # int64_t
    'f': DataType.Float,  # float
    'F': DataType.Double,  # double
    'x': DataType.Hex8,  # uint8_t (hex)
    'X': DataType.Hex8,  # uint8_t (hex)
    'z': DataType.Hex16,  # uint16_t (hex)
    'Z': DataType.Hex16  # uint16_t (hex)
}

_data_type_supmcu_fmt = {
    DataType.Str: 'S',
    DataType.Char: 'c',  # char
    DataType.U8: 'u',  # uint8_t
    DataType.I8: 't',  # int8_t
    DataType.U16: 's',  # uint16_t
    DataType.I16: 'n',  # int16_t
    DataType.U32: 'i',  # uint32_t
    DataType.I32: 'd',  # int32_t
    DataType.U64: 'l',  # uint64_t
    DataType.I64: 'k',  # int64_t
    DataType.Float: 'f',  # float
    DataType.Double: 'F',  # double
    DataType.Hex8: 'x',  # uint8_t (hex)
    DataType.Hex16: 'z',  # uint16_t (hex)
}


SupMCUTelemetryDefinition = NamedTuple("SupMCUTelemetryDefinition", [("name", str),
                                                                     ("telemetry_length", int),
                                                                     ("idx", int),
                                                                     ("format", str)])
"""A SupMCU Telemetry definition consists of the name, length and format of the returned data."""
SupMCUModuleDefinition = NamedTuple("SupMCUModuleDefinition", [("name", str),
                                                               ("cmd_name", str),
                                                               ("address", int),
                                                               ("supmcu_telemetry",
                                                                Dict[int, SupMCUTelemetryDefinition]),
                                                               ("module_telemetry",
                                                                Dict[int, SupMCUTelemetryDefinition])])
"""A SupMCU Module definition consists of the name, address, cmd_name, SupMCU Telemetry and module telemetry."""
TelemetryDataItem = NamedTuple('TelemetryDataItem', [('data_type', DataType), ('value', Any), ('string_value', str)])
"""A single data item from a telemetry request."""
SupMCUHDR = NamedTuple('SupMCUHDR', [('ready', bool), ('timestamp', int)])
"""The SupMCU Telemetry header with timestamp and is_ready information."""
SupMCUTelemetry = NamedTuple("SupMCUTelemetry", [('header', SupMCUHDR), ('items', List[TelemetryDataItem])])
"""A SupMCU Telemetry request response. Consists of zero or more TelemetryDataItems."""


def sizeof_supmcu_type(t: DataType) -> int:
    """
    Returns the size in bytes of a SupMCU Data type.
    Note the Str type returns 0 as it's size is unknown until parsed.

    :param t: The DataType t.
    :return: The size of the type in bytes, unless Str, then its zero.
    """
    return _data_type_sizes[t]


def typeof_supmcu_fmt_char(fmt_char: str) -> DataType:
    """
    Returns the underlying SupMCU Data type for a given `fmt_char`.

    :param fmt_char: The format character.
    :return: The DataType for the format character.
    :raises KeyError: If no corresponding DataType is found for the format character.
    """
    return _supmcu_fmt_data_type[fmt_char]


def datatype_to_supmcu_fmt_char(data_type: DataType) -> str:
    """
    Converts `data_type` to the corresponding SupMCU format character.

    :param data_type: The DataType to get the corresponding format character for.
    :return: The format character as used in SUP/MOD:TEL? #,FORMAT commands.
    :raises KeyError: If no corresponding SupMCU format character is found for the `data_type`.
    """
    return _data_type_supmcu_fmt[data_type]
