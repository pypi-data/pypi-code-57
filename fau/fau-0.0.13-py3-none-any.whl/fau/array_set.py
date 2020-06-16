from collections import OrderedDict
from typing import Iterator
from .fixed_length_array import FixedLengthArray
from .u8 import U8
from .s8 import S8
from .u16 import U16
from .s16 import S16
from .u32 import U32
from .s32 import S32
from .f32 import F32
from .write import write_u8


class ArraySet:
    def __init__(self) -> None:
        self._arrays: OrderedDict[int, FixedLengthArray] = OrderedDict()

    def _add_array(self, identifier: int, array: FixedLengthArray) -> None:
        if identifier < 0:
            raise OverflowError
        elif identifier > 4294967295:
            raise OverflowError
        elif identifier in self._arrays:
            raise AttributeError
        else:
            self._arrays[identifier] = array

    def u8(self, identifier: int, length: int) -> U8:
        u8 = U8(length)
        self._add_array(identifier, u8)
        return u8

    def s8(self, identifier: int, length: int) -> S8:
        s8 = S8(length)
        self._add_array(identifier, s8)
        return s8

    def u16(self, identifier: int, length: int) -> U16:
        u16 = U16(length)
        self._add_array(identifier, u16)
        return u16

    def s16(self, identifier: int, length: int) -> S16:
        s16 = S16(length)
        self._add_array(identifier, s16)
        return s16

    def u32(self, identifier: int, length: int) -> U32:
        u32 = U32(length)
        self._add_array(identifier, u32)
        return u32

    def s32(self, identifier: int, length: int) -> S32:
        s32 = S32(length)
        self._add_array(identifier, s32)
        return s32

    def f32(self, identifier: int, length: int) -> F32:
        f32 = F32(length)
        self._add_array(identifier, f32)
        return f32

    def write(self) -> Iterator[int]:
        for identifier, array in self._arrays.items():
            for byte in array._write(identifier):
                yield byte

        for byte in write_u8(0xFF):
            yield byte
