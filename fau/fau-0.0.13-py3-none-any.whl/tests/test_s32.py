import unittest
from fau import S32


class TestS32(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            S32(-1)

    def test_length_zero_returns_correct_length(self):
        s32 = S32(0)

        self.assertEqual(0, len(s32))

    def test_length_correct(self):
        s32 = S32(7)

        self.assertEqual(7, len(s32))

    def test_initialized_as_zeroes(self):
        s32 = S32(7)

        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(0, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])

    def test_get_negative_index_throws_error(self):
        s32 = S32(7)

        with self.assertRaises(IndexError):
            s32[-1]

    def test_get_index_out_of_range_throws_error(self):
        s32 = S32(7)

        with self.assertRaises(IndexError):
            s32[7]

    def test_set_negative_index_throws_error(self):
        s32 = S32(7)

        with self.assertRaises(IndexError):
            s32[-1] = 5923483

    def test_set_index_out_of_range_throws_error(self):
        s32 = S32(7)

        with self.assertRaises(IndexError):
            s32[7] = 5923483

    def test_set_out_of_range_negative_throws_error(self):
        s32 = S32(7)

        with self.assertRaises(OverflowError):
            s32[3] = -2147483649

    def test_set_out_of_range_positive_throws_error(self):
        s32 = S32(7)

        with self.assertRaises(OverflowError):
            s32[3] = 2147483648

    def test_set_minimum_value(self):
        s32 = S32(7)

        s32[3] = -2147483648

        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(-2147483648, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])

    def test_set_negative(self):
        s32 = S32(7)

        s32[3] = -5923483

        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(-5923483, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])

    def test_set_zero(self):
        s32 = S32(7)

        s32[3] = 5923483
        s32[3] = 0

        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(0, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])

    def test_set_positive(self):
        s32 = S32(7)

        s32[3] = 5923483

        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(5923483, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])

    def test_set_maximum_value(self):
        s32 = S32(7)

        s32[3] = 2147483647

        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(2147483647, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])
