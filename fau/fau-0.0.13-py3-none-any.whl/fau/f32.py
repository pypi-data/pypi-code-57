from array import array
from typing import Iterator
from .fixed_length_array import FixedLengthArray
from .write import write_u8, write_u32, write_f32


class F32(FixedLengthArray):
    def __init__(self, length: int) -> None:
        if length < 0:
            raise OverflowError
        else:
            # This logic can't be shared with IntegerArray via a common base
            # class as MyPy assumes it returns an array[int].
            self._values = array('f', [0] * length)

    def __getitem__(self, index: int) -> float:
        if index < 0:
            raise IndexError
        elif index >= len(self._values):
            raise IndexError
        else:
            return self._values[index]

    def __setitem__(self, index: int, value: float) -> None:
        if index < 0:
            raise IndexError
        elif index >= len(self._values):
            raise IndexError
        else:
            self._values[index] = value

    def __len__(self) -> int:
        return len(self._values)

    def _write(self, identifier: int) -> Iterator[int]:
        trimmed_length = len(self._values)

        while True:
            if self._values[trimmed_length - 1] != 0:
                break

            trimmed_length = trimmed_length - 1

            if trimmed_length == 0:
                return

        for byte in write_u8(0x06):
            yield byte

        for byte in write_u32(identifier):
            yield byte

        for byte in write_u32(trimmed_length):
            yield byte

        for value in self._values[:trimmed_length]:
            for byte in write_f32(value):
                yield byte
