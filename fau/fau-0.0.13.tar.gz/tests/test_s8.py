import unittest
from fau import S8


class TestS8(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            S8(-1)

    def test_length_zero_returns_correct_length(self):
        s8 = S8(0)

        self.assertEqual(0, len(s8))

    def test_length_correct(self):
        s8 = S8(7)

        self.assertEqual(7, len(s8))

    def test_initialized_as_zeroes(self):
        s8 = S8(7)

        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(0, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])

    def test_get_negative_index_throws_error(self):
        s8 = S8(7)

        with self.assertRaises(IndexError):
            s8[-1]

    def test_get_index_out_of_range_throws_error(self):
        s8 = S8(7)

        with self.assertRaises(IndexError):
            s8[7]

    def test_set_negative_index_throws_error(self):
        s8 = S8(7)

        with self.assertRaises(IndexError):
            s8[-1] = 144

    def test_set_index_out_of_range_throws_error(self):
        s8 = S8(7)

        with self.assertRaises(IndexError):
            s8[7] = 144

    def test_set_out_of_range_negative_throws_error(self):
        s8 = S8(7)

        with self.assertRaises(OverflowError):
            s8[3] = -129

    def test_set_out_of_range_positive_throws_error(self):
        s8 = S8(7)

        with self.assertRaises(OverflowError):
            s8[3] = 128

    def test_set_minimum_value(self):
        s8 = S8(7)

        s8[3] = -128

        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(-128, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])

    def test_set_negative(self):
        s8 = S8(7)

        s8[3] = -34

        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(-34, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])

    def test_set_zero(self):
        s8 = S8(7)

        s8[3] = 34
        s8[3] = 0

        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(0, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])

    def test_set_positive(self):
        s8 = S8(7)

        s8[3] = 34

        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(34, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])

    def test_set_maximum_value(self):
        s8 = S8(7)

        s8[3] = 127

        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(127, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])
