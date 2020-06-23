from unittest import TestCase

from bare import _pack_varint, _unpack_varint


class Test(TestCase):
    def test__pack_varint(self):
        self.assertEqual(_pack_varint(0), b'\0', 'uint zero')
        self.assertEqual(_pack_varint(0x7F), b'\x7f', 'uint 0x7f')
        self.assertEqual(_pack_varint(0x1337), b'\xb7\x26', 'uint 0x1337')

        self.assertEqual(_pack_varint(42, signed=True), b'\x54', 'int 42')
        self.assertEqual(_pack_varint(0, signed=True), b'\0', 'int 0')
        self.assertEqual(_pack_varint(1, signed=True), b'\x02', 'int 1')
        self.assertEqual(_pack_varint(-1, signed=True), b'\x01', 'int -1')
        self.assertEqual(_pack_varint(-1337, signed=True), b'\xf1\x14', 'int -1337')

    def test__unpack_varint(self):
        self.assertEqual(_unpack_varint(b'\0', 0)[0], 0, 'uint zero')
        self.assertEqual(_unpack_varint(b'\x7f', 0)[0], 0x7f, 'uint 0x7f')
        self.assertEqual(_unpack_varint(b'\xb7\x26', 0)[0], 0x1337, 'uint 0x1337')

        self.assertEqual(_unpack_varint(b'\x54', 0, signed=True)[0], 42, 'int 42')
        self.assertEqual(_unpack_varint(b'\0', 0, signed=True)[0], 0, 'int 0')
        self.assertEqual(_unpack_varint(b'\x02', 0, signed=True)[0], 1, 'int 1')
        self.assertEqual(_unpack_varint(b'\x01', 0, signed=True)[0], -1, 'int -1')
        self.assertEqual(_unpack_varint(b'\xf1\x14', 0, signed=True)[0], -1337, 'int -1')
