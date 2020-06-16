import unittest
from fau import U8


class TestU8(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            U8(-1)

    def test_length_zero_returns_correct_length(self):
        u8 = U8(0)

        self.assertEqual(0, len(u8))

    def test_length_correct(self):
        u8 = U8(7)

        self.assertEqual(7, len(u8))

    def test_initialized_as_zeroes(self):
        u8 = U8(7)

        self.assertEqual(0, u8[0])
        self.assertEqual(0, u8[1])
        self.assertEqual(0, u8[2])
        self.assertEqual(0, u8[3])
        self.assertEqual(0, u8[4])
        self.assertEqual(0, u8[5])
        self.assertEqual(0, u8[6])

    def test_get_negative_index_throws_error(self):
        u8 = U8(7)

        with self.assertRaises(IndexError):
            u8[-1]

    def test_get_index_out_of_range_throws_error(self):
        u8 = U8(7)

        with self.assertRaises(IndexError):
            u8[7]

    def test_set_negative_index_throws_error(self):
        u8 = U8(7)

        with self.assertRaises(IndexError):
            u8[-1] = 144

    def test_set_index_out_of_range_throws_error(self):
        u8 = U8(7)

        with self.assertRaises(IndexError):
            u8[7] = 144

    def test_set_negative_throws_error(self):
        u8 = U8(7)

        with self.assertRaises(OverflowError):
            u8[3] = -1

    def test_set_out_of_range_throws_error(self):
        u8 = U8(7)

        with self.assertRaises(OverflowError):
            u8[3] = 256

    def test_set_zero(self):
        u8 = U8(7)

        u8[3] = 144
        u8[3] = 0

        self.assertEqual(0, u8[0])
        self.assertEqual(0, u8[1])
        self.assertEqual(0, u8[2])
        self.assertEqual(0, u8[3])
        self.assertEqual(0, u8[4])
        self.assertEqual(0, u8[5])
        self.assertEqual(0, u8[6])

    def test_set_positive(self):
        u8 = U8(7)

        u8[3] = 144

        self.assertEqual(0, u8[0])
        self.assertEqual(0, u8[1])
        self.assertEqual(0, u8[2])
        self.assertEqual(144, u8[3])
        self.assertEqual(0, u8[4])
        self.assertEqual(0, u8[5])
        self.assertEqual(0, u8[6])

    def test_set_maximum_value(self):
        u8 = U8(7)

        u8[3] = 255

        self.assertEqual(0, u8[0])
        self.assertEqual(0, u8[1])
        self.assertEqual(0, u8[2])
        self.assertEqual(255, u8[3])
        self.assertEqual(0, u8[4])
        self.assertEqual(0, u8[5])
        self.assertEqual(0, u8[6])
