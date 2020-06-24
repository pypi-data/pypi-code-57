from __future__ import annotations
import struct


class VarInt:
    """
    Variable length integer as specified in the mumble documentation.
    https://mumble-protocol.readthedocs.io/en/latest/voice_data.html#variable-length-integer-encoding
    """

    def __init__(self, integer):
        """"""
        self.integer = integer

    @classmethod
    def from_int(cls, integer: int) -> VarInt:
        """"""
        return cls(integer)

    @classmethod
    def from_bytes(cls, bytes_in: bytes) -> VarInt:
        """"""
        length = len(bytes_in)
        if length == 0:
            raise ValueError("Zero length VarInt")
        byte0, = struct.unpack("!B", bytes_in[0:1])
        # 111110__ + varint: Negative recursive varint
        # Throw __ away and append varint of positive integer
        if byte0 & 0b11111100 == 0b11111000:
            result = cls.from_bytes(bytes_in[1:])
            result.integer = -result.integer
            return result
        if length == 1:
            # 0xxxxxxx: 7-bit positive number
            # 01111111 -> 127
            if byte0 & 0b10000000 == 0b00000000:
                return cls(byte0)
            # 111111xx: Byte-inverted negative two bit number (~xx)
            # values between and including -1 and -4
            if byte0 & 0b11111100 == 0b11111100:
                return cls(~(byte0 & 0b00000011))
        elif length == 2:
            # 10xxxxxx + 1 byte: 14-bit positive number
            # 00111111 11111111 -> 16383
            if byte0 & 0b11000000 == 0b10000000:
                first, = struct.unpack("!H", bytes_in)
                return cls(first & 0b0011111111111111)
        elif length == 3:
            # 110xxxxx + 2 bytes: 21-bit positive number
            # 00011111 11111111 11111111 -> 2097151
            if byte0 & 0b11100000 == 0b11000000:
                first, second = struct.unpack("!BH", bytes_in)
                return cls(((first & 0b00011111) << 16) + second)
        elif length == 4:
            # 1110xxxx + 3 bytes: 28-bit positive number
            # 00001111 11111111 11111111 11111111 -> 268435455
            if byte0 & 0b11110000 == 0b11100000:
                first, = struct.unpack("!L", bytes_in)
                return cls(first & 0b00001111111111111111111111111111)
        elif length == 5:
            # 111100__ + int (32-bit): 32-bit positive number
            # 00000000 11111111 11111111 11111111 11111111 -> 4294967295
            if byte0 & 0b11111100 == 0b11110000:
                first, second = struct.unpack("!BL", bytes_in)
                return cls(second)
        elif length == 9:
            # 111101__ + long (64-bit): 64-bit number
            if byte0 & 0b11111100 == 0b11110100:
                first, second = struct.unpack("!BQ", bytes_in)
                return cls(second)
        return cls(0)

    def to_int(self) -> int:
        """"""
        return self.integer

    @property
    def int(self) -> int:
        """"""
        return self.to_int()

    def to_bytes(self) -> bytes:
        """"""
        return self.__to_bytes(self.integer)

    @property
    def bytes(self) -> bytes:
        """"""
        return self.to_bytes()

    def __to_bytes(self, integer) -> bytes:
        """"""
        # 111111xx: Byte-inverted negative two bit number (~xx)
        # values between and including -1 and -4
        # where xx ->
        #   00: -1
        #   01: -2
        #   10: -3
        #   11: -4
        if -5 < integer < 0:
            return struct.pack("!B", (0b11111100 | ~integer))
        # 111110__ + varint: Negative recursive varint
        # Ignore __ and append varint of positive integer
        if integer < 0:
            return struct.pack("!B", 0b11111000) + self.__to_bytes(-integer)
        # 0xxxxxxx: 7-bit positive number
        # 01111111 -> 127
        if integer < 128:
            return struct.pack("!B", integer)
        # 10xxxxxx + 1 byte: 14-bit positive number
        # 00111111 11111111 -> 16383
        if integer < 16384:
            return struct.pack("!H", 0b1000000000000000 | integer)
        # 110xxxxx + 2 bytes: 21-bit positive number
        # 00011111 11111111 11111111 -> 2097151
        if integer < 2097152:
            return struct.pack("!BH", 0b11000000 | (integer >> 16), integer & 0b1111111111111111)
        # 1110xxxx + 3 bytes: 28-bit positive number
        # 00001111 11111111 11111111 11111111 -> 268435455
        if integer < 268435456:
            return struct.pack("!L", 0b11100000000000000000000000000000 | integer)
        # 111100__ + int (32-bit): 32-bit positive number
        # 00000000 11111111 11111111 11111111 11111111 -> 4294967295
        if integer < 4294967296:
            return struct.pack("!BL", 0b11110000, integer)
        # 111101__ + long (64-bit): 64-bit number
        return struct.pack("!BQ", 0b11110100, integer)

    def __add__(self, other: [VarInt, int, bytes]) -> VarInt:
        """"""
        if isinstance(other, VarInt):
            return VarInt.from_int(self.int + other.int)
        elif isinstance(other, int):
            return VarInt.from_int(self.int + other)
        elif isinstance(other, bytes):
            return self + VarInt.from_bytes(other)
        raise TypeError(f"Unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")

    def __mul__(self, other: [VarInt, int, bytes]) -> VarInt:
        """"""
        if isinstance(other, VarInt):
            return VarInt.from_int(self.int * other.int)
        elif isinstance(other, int):
            return VarInt.from_int(self.int * other)
        elif isinstance(other, bytes):
            return self * VarInt.from_bytes(other)
        raise TypeError(f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")

    def __repr__(self) -> repr:
        """"""
        return f"{self.integer} -> {self.to_bytes()}"
