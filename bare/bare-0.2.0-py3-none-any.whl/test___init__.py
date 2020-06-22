from unittest import TestCase

from bare import _pack_varint


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
