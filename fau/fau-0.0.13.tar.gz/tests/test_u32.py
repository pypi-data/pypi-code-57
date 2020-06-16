import unittest
from fau import U32


class TestU32(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            U32(-1)

    def test_length_zero_returns_correct_length(self):
        u32 = U32(0)

        self.assertEqual(0, len(u32))

    def test_length_correct(self):
        u32 = U32(7)

        self.assertEqual(7, len(u32))

    def test_initialized_as_zeroes(self):
        u32 = U32(7)

        self.assertEqual(0, u32[0])
        self.assertEqual(0, u32[1])
        self.assertEqual(0, u32[2])
        self.assertEqual(0, u32[3])
        self.assertEqual(0, u32[4])
        self.assertEqual(0, u32[5])
        self.assertEqual(0, u32[6])

    def test_get_negative_index_throws_error(self):
        u32 = U32(7)

        with self.assertRaises(IndexError):
            u32[-1]

    def test_get_index_out_of_range_throws_error(self):
        u32 = U32(7)

        with self.assertRaises(IndexError):
            u32[7]

    def test_set_negative_index_throws_error(self):
        u32 = U32(7)

        with self.assertRaises(IndexError):
            u32[-1] = 3423047

    def test_set_index_out_of_range_throws_error(self):
        u32 = U32(7)

        with self.assertRaises(IndexError):
            u32[7] = 3423047

    def test_set_negative_throws_error(self):
        u32 = U32(7)

        with self.assertRaises(OverflowError):
            u32[3] = -1

    def test_set_out_of_range_throws_error(self):
        u32 = U32(7)

        with self.assertRaises(OverflowError):
            u32[3] = 4294967296

    def test_set_zero(self):
        u32 = U32(7)

        u32[3] = 3423047
        u32[3] = 0

        self.assertEqual(0, u32[0])
        self.assertEqual(0, u32[1])
        self.assertEqual(0, u32[2])
        self.assertEqual(0, u32[3])
        self.assertEqual(0, u32[4])
        self.assertEqual(0, u32[5])
        self.assertEqual(0, u32[6])

    def test_set_positive(self):
        u32 = U32(7)

        u32[3] = 3423047

        self.assertEqual(0, u32[0])
        self.assertEqual(0, u32[1])
        self.assertEqual(0, u32[2])
        self.assertEqual(3423047, u32[3])
        self.assertEqual(0, u32[4])
        self.assertEqual(0, u32[5])
        self.assertEqual(0, u32[6])

    def test_set_maximum_value(self):
        u32 = U32(7)

        u32[3] = 4294967295

        self.assertEqual(0, u32[0])
        self.assertEqual(0, u32[1])
        self.assertEqual(0, u32[2])
        self.assertEqual(4294967295, u32[3])
        self.assertEqual(0, u32[4])
        self.assertEqual(0, u32[5])
        self.assertEqual(0, u32[6])
