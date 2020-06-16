from typing import Iterator
from .integer_array import IntegerArray
from .write import (
    write_u8, write_s8, write_u16, write_s16, write_s32, write_integer_array
)


class SignedIntegerArray(IntegerArray):
    def _perform_write(
        self,
        identifier: int,
        trimmed_length: int
    ) -> Iterator[int]:
        minimum = min(self._values)
        maximum = max(self._values)

        if minimum >= -128 and maximum <= 127:
            return write_integer_array(
                identifier, 0x01, trimmed_length, self._values, write_s8
            )
        elif minimum >= 0 and maximum <= 255:
            return write_integer_array(
                identifier, 0x00, trimmed_length, self._values, write_u8
            )
        elif minimum >= -32768 and maximum <= 32767:
            return write_integer_array(
                identifier, 0x03, trimmed_length, self._values, write_s16
            )
        elif minimum >= 0 and maximum <= 65535:
            return write_integer_array(
                identifier, 0x02, trimmed_length, self._values, write_u16
            )
        else:
            return write_integer_array(
                identifier, 0x05, trimmed_length, self._values, write_s32
            )
