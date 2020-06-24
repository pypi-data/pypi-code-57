#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wspr` package."""
import sys
import unittest

from wspr_varint.varint import VarInt


class VarIntTest(unittest.TestCase):
    """"""

    def setUp(self):
        """Set up test fixtures, if any."""
        integers = [
            -4,
            -3,
            -2,
            -1,
        ]
        self.test_cases_from_int = [
            (integer, VarInt.from_int(integer)) for integer in integers
        ]

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_conversion_from_to(self):
        for integer in range(0, 4294967296 + 1000000, 33333):
            expected = VarInt.from_int(integer)
            calculated = VarInt.from_bytes(expected.to_bytes())
            self.assertEqual(calculated.to_int(), expected.to_int())

    def test_int_to_bytes(self):
        """"""
        # 111111xx: integers between and including -1 to -4
        cases = [
            (-1, 0b11111100),
            (-2, 0b11111101),
            (-3, 0b11111110),
            (-4, 0b11111111),
        ]
        for integer, binary in cases:
            varint = VarInt.from_int(integer)
            self.assertEqual(binary_to_bytes(binary), varint.to_bytes())

        # 111110__ + varint: Negative recursive varint
        # TODO

        # 0xxxxxxx: 7-bit positive number
        for integer in range(0, 128):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b10000000, 0b00000000)
            self.assertEqual(binary_to_bytes(integer), varint.to_bytes())

        # 10xxxxxx + 1 byte: 14-bit positive number
        for integer in range(128, 16384):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b1100000000000000, 0b1000000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b1000000000000000), varint.to_bytes())

        # 110xxxxx + 2 bytes: 21-bit positive number
        for integer in range(16384, 16384 + 5000):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b111000000000000000000000, 0b110000000000000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b110000000000000000000000), varint.to_bytes())
        for integer in range(2097152 - 5000, 2097152):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b1110000000000000, 0b1100000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b110000000000000000000000), varint.to_bytes())

        # 1110xxxx + 3 bytes: 28-bit positive number
        for integer in range(2097152, 2097152 + 5000):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b11110000000000000000000000000000, 0b11100000000000000000000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b11100000000000000000000000000000), varint.to_bytes())
        for integer in range(268435456 - 5000, 268435456):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b11110000000000000000000000000000, 0b11100000000000000000000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b11100000000000000000000000000000), varint.to_bytes())
        self.assertEqual(binary_to_bytes(0b11101111111111111111111111111111), VarInt(268435455).to_bytes())

        # 111100__ + int (32-bit): 32-bit positive number
        for integer in range(268435456, 268435456 + 5000):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b11110000000000000000000000000000, 0b11100000000000000000000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b1111000000000000000000000000000000000000), varint.to_bytes())
        for integer in range(4294967296 - 5000, 4294967296):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b11110000000000000000000000000000, 0b11100000000000000000000000000000)
            self.assertEqual(binary_to_bytes(integer | 0b1111000000000000000000000000000000000000), varint.to_bytes())
        self.assertEqual(binary_to_bytes(0b1111000011111111111111111111111111111111), VarInt(4294967295).to_bytes())

        # 111101__ + long (64-bit): 64-bit number
        for integer in range(4294967296, 4294967296 + 5000):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b11110000000000000000000000000000, 0b11100000000000000000000000000000)
            self.assertEqual(
                binary_to_bytes(integer | 0b111101000000000000000000000000000000000000000000000000000000000000000000),
                varint.to_bytes())
        # for integer in range(2 ^ 64 - 5000, 2 ^ 64):
        for integer in range(sys.maxsize // 2 - 5000, sys.maxsize // 2):
            varint = VarInt.from_int(integer)
            # self.assertEqual(integer & 0b11110000000000000000000000000000, 0b11100000000000000000000000000000)
            self.assertEqual(
                binary_to_bytes(integer | 0b111101000000000000000000000000000000000000000000000000000000000000000000),
                varint.to_bytes())
        # 9223372036854775807 // 2
        self.assertEqual(binary_to_bytes(
            4611686018427387903 | 0b111101000000000000000000000000000000000000000000000000000000000000000000),
                         VarInt(sys.maxsize // 2).to_bytes())


def binary_to_bytes(binary: bin) -> bytes:
    """Convert a binary format to bytes in the big endian (network) format."""
    return binary.to_bytes(max(binary.bit_length() // 8, 1), 'big')
