from array import array
from typing import List, Iterator, Callable


def integer_requires_byte_swap(
    type_code: str,
    value: int,
    bytes: List[int]
) -> bool:
    temp = list(array(type_code, [value]).tobytes())

    if bytes == temp:
        return False  # pragma: no cover
    elif list(reversed(bytes)) == temp:  # pragma: no cover
        return True  # pragma: no cover
    else:  # pragma: no cover
        raise NotImplementedError(type_code, temp)  # pragma: no cover


u8_requires_byte_swap = integer_requires_byte_swap(
    'B', 0x12, [0x12]
)
s8_requires_byte_swap = integer_requires_byte_swap(
    'b', 0x12, [0x12]
)
u16_requires_byte_swap = integer_requires_byte_swap(
    'H', 0x1234, [0x34, 0x12]
)
s16_requires_byte_swap = integer_requires_byte_swap(
    'h', 0x1234, [0x34, 0x12]
)
u32_requires_byte_swap = integer_requires_byte_swap(
    'I', 0x12345678, [0x78, 0x56, 0x34, 0x12]
)
s32_requires_byte_swap = integer_requires_byte_swap(
    'i', 0x12345678, [0x78, 0x56, 0x34, 0x12]
)

f32_temp = list(array('f', [-14.37]).tobytes())
if [0x85, 0xEB, 0x65, 0xC1] == f32_temp:
    f32_requires_byte_swap = False  # pragma: no cover
elif [0xC1, 0x65, 0xEB, 0x85] == f32_temp:  # pragma: no cover
    f32_requires_byte_swap = True  # pragma: no cover
else:  # pragma: no cover
    raise NotImplementedError('f', f32_temp)  # pragma: no cover


def write_integer(
    type_code: str,
    requires_byte_swap: bool,
    value: int
) -> Iterator[int]:
    temp = array(type_code, [value])

    if requires_byte_swap:
        temp.byteswap()  # pragma: no cover

    for byte in temp.tobytes():
        yield byte


def write_u8(value: int) -> Iterator[int]:
    return write_integer('B', u8_requires_byte_swap, value)


def write_s8(value: int) -> Iterator[int]:
    return write_integer('b', s8_requires_byte_swap, value)


def write_u16(value: int) -> Iterator[int]:
    return write_integer('H', u16_requires_byte_swap, value)


def write_s16(value: int) -> Iterator[int]:
    return write_integer('h', s16_requires_byte_swap, value)


def write_u32(value: int) -> Iterator[int]:
    return write_integer('I', u32_requires_byte_swap, value)


def write_s32(value: int) -> Iterator[int]:
    return write_integer('i', s32_requires_byte_swap, value)


def write_f32(value: float) -> Iterator[int]:
    temp = array('f', [value])

    if f32_requires_byte_swap:
        temp.byteswap()  # pragma: no cover

    for byte in temp.tobytes():
        yield byte


def write_integer_array(
    identifier: int,
    primitive: int,
    trimmed_length: int,
    values: array,
    write_value: Callable[[int], Iterator[int]]
) -> Iterator[int]:
    for byte in write_u8(primitive):
        yield byte

    for byte in write_u32(identifier):
        yield byte

    for byte in write_u32(trimmed_length):
        yield byte

    for value in values[:trimmed_length]:
        for byte in write_value(value):
            yield byte
