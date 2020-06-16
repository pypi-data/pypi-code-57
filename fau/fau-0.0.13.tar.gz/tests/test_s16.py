import unittest
from fau import S16


class TestS16(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            S16(-1)

    def test_length_zero_returns_correct_length(self):
        s16 = S16(0)

        self.assertEqual(0, len(s16))

    def test_length_correct(self):
        s16 = S16(7)

        self.assertEqual(7, len(s16))

    def test_initialized_as_zeroes(self):
        s16 = S16(7)

        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(0, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])

    def test_get_negative_index_throws_error(self):
        s16 = S16(7)

        with self.assertRaises(IndexError):
            s16[-1]

    def test_get_index_out_of_range_throws_error(self):
        s16 = S16(7)

        with self.assertRaises(IndexError):
            s16[7]

    def test_set_negative_index_throws_error(self):
        s16 = S16(7)

        with self.assertRaises(IndexError):
            s16[-1] = 5983

    def test_set_index_out_of_range_throws_error(self):
        s16 = S16(7)

        with self.assertRaises(IndexError):
            s16[7] = 5983

    def test_set_out_of_range_negative_throws_error(self):
        s16 = S16(7)

        with self.assertRaises(OverflowError):
            s16[3] = -32769

    def test_set_out_of_range_positive_throws_error(self):
        s16 = S16(7)

        with self.assertRaises(OverflowError):
            s16[3] = 32768

    def test_set_minimum_value(self):
        s16 = S16(7)

        s16[3] = -32768

        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(-32768, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])

    def test_set_negative(self):
        s16 = S16(7)

        s16[3] = -5983

        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(-5983, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])

    def test_set_zero(self):
        s16 = S16(7)

        s16[3] = 5983
        s16[3] = 0

        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(0, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])

    def test_set_positive(self):
        s16 = S16(7)

        s16[3] = 5983

        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(5983, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])

    def test_set_maximum_value(self):
        s16 = S16(7)

        s16[3] = 32767

        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(32767, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])
