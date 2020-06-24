from __future__ import annotations

import datetime
import struct
import typing
from collections import namedtuple
from dataclasses import dataclass, field
from math import log10, floor
import ruamel.yaml


def round_sig(x, sig=2):
    if x == 0:
        return x
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


class Endian:
    big = ">"
    little = "<"


c_decode = namedtuple('c_decode', ["format", "size"])
data_types = {
    "char": c_decode("c", 1),
    "schar": c_decode("b", 1),
    "uchar": c_decode("B", 1),
    "bool": c_decode("?", 1),
    "short": c_decode("h", 2),
    "ushort": c_decode("H", 2),
    "int": c_decode("i", 4),
    "uint": c_decode("I", 4),
    "long": c_decode("l", 4),
    "ulong": c_decode("L", 4),
    "longlong": c_decode("q", 8),
    "ulonglong": c_decode("Q", 8),
    "float": c_decode("f", 4),
    "double": c_decode("d", 8),
    "char[]": c_decode("s", None)
}


class AddressMap:
    def __init__(self, buffer: dict = None):
        if buffer is None:
            self._buf = {}
        else:
            self._buf = buffer

    def __getitem__(self, addr):
        """
        :param addr: Address int or slice of addresses to return
        :return:
        """
        if isinstance(addr, int):
            if addr < 0:
                raise TypeError('Address should be >= 0.')
            return self._buf[addr]
        elif isinstance(addr, slice):
            return [self._buf.get(i) for i in range(*slice_list(addr))]
        else:
            raise TypeError("Address has unsupported type")

    def __setitem__(self, key, value):
        """
        :param key: Int of the address
        :param value: Set the value of the item if the value is not None
        :return:
        """
        if isinstance(key, slice):
            for index, addr in enumerate(range(*slice_list(key))):
                if value[index] is not None:
                    self._buf[addr] = value[index]
        else:
            if value is not None:
                self._buf[key] = value

    def __delitem__(self, key):
        try:
            del self._buf[key]
        except KeyError:
            pass

    def __delslice__(self, i, j):
        for x in range(i, j):
            try:
                del self._buf[x]
            except KeyError:
                pass

    def __bool__(self):
        return bool(self._buf)

    def merge(self, addr: AddressMap):
        """
        Merges another address map into this existing address map
        :param addr:
        :return:
        """
        overlap = set(self._buf.keys()).intersection(set(addr._buf.keys()))
        if overlap:
            raise ValueError("Cannot join AddressMap with overlapping addresses: {}".format(overlap))

        self._buf.update(addr._buf)

    def save_block(self, start_addr, values):
        for index, itm in enumerate(values):
            self._buf[start_addr + index] = itm

    def __repr__(self):
        return f"AddressMap: {self._buf}"

    def copy(self):
        return self.__class__(self._buf)


class AddressMapUint16(AddressMap):
    def __setitem__(self, key, value):
        """
        :param key: Int of the address
        :param value: Set the value of the item if the value is not None
        :return:
        """
        if isinstance(key, slice):
            if any(x for x in slice_list(key) if x is not None and not (0 <= x < 1 << 16) and not isinstance(x, int)):
                raise OverflowError("Values provided are not UINT16 compatible")
        else:
            if value is not None and not (0 <= value < 1 << 16) and not isinstance(value, int):
                raise OverflowError("Value provided is not UINT16 compatible")
        super().__setitem__(key, value)


def slice_list(slic):
    return [x for x in [slic.start, slic.stop, slic.step] if x is not None]


@dataclass
class Param:
    address: int
    idx: str
    scale: float = 1
    block: typing.Any = None
    significant_figures: typing.Optional[int] = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        result = addr_map[self.address] * self.scale
        if self.significant_figures:
            result = round_sig(result, self.significant_figures)
        return {self.idx: result}

    def encode(self, data, addr_map: AddressMapUint16):
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map

        value = round(value / self.scale)
        if value > 0xffff:
            raise OverflowError(f"Target value {data[self.idx]} when scaled 0x{value:02X} "
                                f"is bigger than a 16 bit number")
        addr_map[self.address] = value
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamBoolArray:
    address: [int]
    idx: str
    length: int
    block: typing.Any = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or any(
                [True for addr in self.address if addr_map[addr] is None]):
            return {}
        bin_number = ""
        for addr in self.address:
            bin_number += f"{addr_map[addr]:0>16b}"[::-1]
        bin_number = bin_number[:self.length]
        bin_arr = [int(x) for x in bin_number]
        return {self.idx: bin_arr}

    def encode(self, data, addr_map: AddressMapUint16):
        try:
            addr_map[self.address] = data[self.idx]
        except KeyError:
            pass
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamText:
    address: int
    idx: str
    length: int
    block: typing.Any = None
    padding: bytes = b'\x00'
    null_byte: bool = True
    swap_bytes: bool = False
    swap_words: bool = False
    strip_leading: str = ""
    strip_lagging: str = ""

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        dec_str = bytearray()
        for x in addr_map[self.address: self.address + self.length]:
            if self.swap_bytes:
                dec_str.append((x & 0xff00) >> 8)
                dec_str.append(x & 0xff)
            else:
                dec_str.append(x & 0xff)
                dec_str.append((x & 0xff00) >> 8)
        dec_str = dec_str.strip(self.padding)
        dec_str = dec_str.strip(b"\x00").decode('utf-8', 'ignore')
        if self.strip_leading:
            dec_str = dec_str.lstrip(self.strip_leading)
        if self.strip_lagging:
            dec_str = dec_str.rstrip(self.strip_lagging)
        return {self.idx: dec_str}

    def encode(self, data, addr_map: AddressMapUint16):
        if len(data[self.idx]) > self.length * 2:
            raise ValueError(f"Invalid string length to pack into {self.idx} starting @ address: {self.address}")
        addr_map[self.address: self.address + self.length * 2] = [self.padding] * self.length * 2
        for index, byt in data[self.idx].encode('utf-8'):
            addr_map[self.address + index // 2] += byt << (8 * index % 2)
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamDict:
    key: str
    idx: str
    table: dict = field(default_factory=dict)

    def decode(self, json_obj: dict):
        return {self.idx: self.table.get(json_obj[self.key], json_obj[self.key])}


@dataclass
class ParamBits:
    address: int
    bitmask: dict
    block: typing.Any = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        parameter_value = addr_map[self.address]
        return {idx: bool(parameter_value & (1 << bit)) for idx, bit in self.bitmask.items()}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        for idx, bit_shift in self.bitmask.items():
            try:
                data_bit = data[idx]
            except KeyError:
                # Data not relevant
                continue
            if data_bit:
                addr_map[self.address] |= (1 << bit_shift)
            else:
                addr_map[self.address] &= ~ (1 << bit_shift)
        return addr_map

    def keys(self):
        return set(self.bitmask)


@dataclass
class ParamMask:
    address: int
    idx: str
    mask: int = 0xffff
    rshift: int = 0
    block: typing.Any = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        return {self.idx: ((addr_map[self.address] & self.mask) >> self.rshift)}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = data[self.idx]
        except KeyError:
            return addr_map
        if value << self.rshift > self.mask:
            raise OverflowError(
                f"Target value 0x{value:02X} when shifted 0x{value << self.rshift:02X} "
                f"is bigger than the target mask 0x{self.mask:02X}")
        addr_map[self.address] &= ~ self.mask
        addr_map[self.address] |= (value << self.rshift)
        return addr_map

    def keys(self):
        return {self.idx}


class ParamMaskBool(ParamMask):

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        decoded[self.idx] = bool(decoded[self.idx])
        return decoded


@dataclass
class ParamMaskScale:
    address: int
    idx: str
    mask: int = 0xffff
    rshift: int = 0
    block: typing.Any = None
    scale: float = 1.0
    significant_figures: typing.Optional[int] = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        if block != self.block or addr_map[self.address] is None:
            return {}
        result = ((addr_map[self.address] & self.mask) >> self.rshift) * self.scale
        if self.significant_figures:
            result = round_sig(result, self.significant_figures)
        return {self.idx: result}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = round(data[self.idx] / self.scale)
        except KeyError:
            return addr_map
        if value << self.rshift > self.mask:
            raise OverflowError(
                f"Target value {value} when shifted 0x{value << self.rshift:02X} "
                f"is bigger than the target mask 0x{self.mask:02X}")
        addr_map[self.address] &= ~ self.mask
        addr_map[self.address] |= (value << self.rshift)
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamLookup:
    address: int
    idx: str
    table: dict
    table_reversed: dict
    mask: int = 0xffff
    rshift: int = 0
    block: typing.Any = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        try:
            assert block == self.block
            return {self.idx: self.table[(addr_map[self.address] & self.mask) >> self.rshift]}
        except (AssertionError, KeyError, TypeError):
            return {}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        try:
            value = self.table_reversed[data[self.idx]]
        except KeyError:
            return addr_map
        addr_map[self.address] &= ~ self.mask
        addr_map[self.address] |= (value << self.rshift)
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamCType:
    address: int
    idx: str
    data_type: str = "ushort"
    byte_order: str = ">"
    word_order: str = ">"
    block: typing.Any = None

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        param_type = data_types[self.data_type]
        data = addr_map[self.address: self.address + ((param_type.size + 1) // 2)]
        if any((x is None for x in data)) or block != self.block:
            return {}
        if self.word_order != ">":
            data = data[::-1]
        data_bytes = struct.pack(self.byte_order + "H" * len(data), *data)
        if self.byte_order == ">":
            data_bytes = data_bytes[len(data_bytes) - param_type.size:]
        else:
            data_bytes = data_bytes[:param_type.size]
        param = struct.unpack(f"{self.byte_order}{param_type.format}", data_bytes)[0]
        return {self.idx: param}

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        # TODO Implement
        # addr_map[self.address: self.address + len(data)] = data
        return addr_map

    def keys(self):
        return {self.idx}


@dataclass
class ParamCTypeScale(ParamCType):
    scale: float = 1.0

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        decoded[self.idx] = decoded[self.idx] * self.scale
        return decoded

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        return super().encode(int(data / self.scale), addr_map)

    def keys(self):
        return {self.idx}


@dataclass
class ParamCTypeScaleModulus(ParamCType):
    modulus: int = 65535
    scale: float = 1.0
    invert_on_overflow: bool = False

    def decode(self, addr_map: AddressMapUint16, block=None) -> dict:
        decoded = super().decode(addr_map, block)
        val = decoded[self.idx] % self.modulus
        if val != decoded[self.idx] and self.invert_on_overflow:
            val = -val
        decoded[self.idx] = val * self.scale
        return decoded

    def encode(self, data, addr_map: AddressMapUint16) -> AddressMapUint16:
        return super().encode(int(data / self.scale) % self.modulus, addr_map)

    def keys(self):
        return {self.idx}


@dataclass
class ParamTimestampAmp(ParamCType):
    """
    Timestamp for Ampcontrol products where the epoch is 2000-01-01 instead of 1970-01-01 as is in UNIX
    """
    data_type: str = "uint"

    def decode(self, *args, **kwargs):
        resp = super().decode(*args, **kwargs)
        if not resp:
            return {}
        stamp = datetime.datetime.utcfromtimestamp(resp[self.idx])
        stamp = stamp.replace(year=stamp.year + 30)
        resp[self.idx] = stamp
        return resp


def build_from_device_config(path):
    with open(path) as f:
        parsed = ruamel.yaml.safe_load(f)
    return parse_data_types(parsed["parameters"])


def parse_data_types(parameters):
    params = {}
    for idx, param in parameters.items():
        try:
            form = param["form"]
            cls = globals()[form.pop("type")]
        except KeyError:
            continue
        inst = cls(**form)
        params[idx] = inst
    return params
