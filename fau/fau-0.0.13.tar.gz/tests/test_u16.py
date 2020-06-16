import unittest
from fau import U16


class TestU16(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            U16(-1)

    def test_length_zero_returns_correct_length(self):
        u16 = U16(0)

        self.assertEqual(0, len(u16))

    def test_length_correct(self):
        u16 = U16(7)

        self.assertEqual(7, len(u16))

    def test_initialized_as_zeroes(self):
        u16 = U16(7)

        self.assertEqual(0, u16[0])
        self.assertEqual(0, u16[1])
        self.assertEqual(0, u16[2])
        self.assertEqual(0, u16[3])
        self.assertEqual(0, u16[4])
        self.assertEqual(0, u16[5])
        self.assertEqual(0, u16[6])

    def test_get_negative_index_throws_error(self):
        u16 = U16(7)

        with self.assertRaises(IndexError):
            u16[-1]

    def test_get_index_out_of_range_throws_error(self):
        u16 = U16(7)

        with self.assertRaises(IndexError):
            u16[7]

    def test_set_negative_index_throws_error(self):
        u16 = U16(7)

        with self.assertRaises(IndexError):
            u16[-1] = 42343

    def test_set_index_out_of_range_throws_error(self):
        u16 = U16(7)

        with self.assertRaises(IndexError):
            u16[7] = 42343

    def test_set_negative_throws_error(self):
        u16 = U16(7)

        with self.assertRaises(OverflowError):
            u16[3] = -1

    def test_set_out_of_range_throws_error(self):
        u16 = U16(7)

        with self.assertRaises(OverflowError):
            u16[3] = 65536

    def test_set_zero(self):
        u16 = U16(7)

        u16[3] = 42343
        u16[3] = 0

        self.assertEqual(0, u16[0])
        self.assertEqual(0, u16[1])
        self.assertEqual(0, u16[2])
        self.assertEqual(0, u16[3])
        self.assertEqual(0, u16[4])
        self.assertEqual(0, u16[5])
        self.assertEqual(0, u16[6])

    def test_set_positive(self):
        u16 = U16(7)

        u16[3] = 42343

        self.assertEqual(0, u16[0])
        self.assertEqual(0, u16[1])
        self.assertEqual(0, u16[2])
        self.assertEqual(42343, u16[3])
        self.assertEqual(0, u16[4])
        self.assertEqual(0, u16[5])
        self.assertEqual(0, u16[6])

    def test_set_maximum_value(self):
        u16 = U16(7)

        u16[3] = 65535

        self.assertEqual(0, u16[0])
        self.assertEqual(0, u16[1])
        self.assertEqual(0, u16[2])
        self.assertEqual(65535, u16[3])
        self.assertEqual(0, u16[4])
        self.assertEqual(0, u16[5])
        self.assertEqual(0, u16[6])
