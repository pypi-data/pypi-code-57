from typing import Iterator
from .integer_array import IntegerArray
from .write import write_u8, write_u16, write_u32, write_integer_array


class UnsignedIntegerArray(IntegerArray):
    def _perform_write(
        self,
        identifier: int,
        trimmed_length: int
    ) -> Iterator[int]:
        maximum = max(self._values)

        if maximum <= 255:
            return write_integer_array(
                identifier, 0x00, trimmed_length, self._values, write_u8
            )
        elif maximum <= 65535:
            return write_integer_array(
                identifier, 0x02, trimmed_length, self._values, write_u16
            )
        else:
            return write_integer_array(
                identifier, 0x04, trimmed_length, self._values, write_u32
            )
