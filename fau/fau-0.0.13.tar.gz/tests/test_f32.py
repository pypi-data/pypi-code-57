import unittest
from fau import F32


class TestF32(unittest.TestCase):
    def test_length_negative_throws_error(self):
        with self.assertRaises(OverflowError):
            F32(-1)

    def test_length_zero_returns_correct_length(self):
        f32 = F32(0)

        self.assertEqual(0, len(f32))

    def test_length_correct(self):
        f32 = F32(7)

        self.assertEqual(7, len(f32))

    def test_initialized_as_zeroes(self):
        f32 = F32(7)

        self.assertEqual(0, f32[0])
        self.assertEqual(0, f32[1])
        self.assertEqual(0, f32[2])
        self.assertEqual(0, f32[3])
        self.assertEqual(0, f32[4])
        self.assertEqual(0, f32[5])
        self.assertEqual(0, f32[6])

    def test_get_negative_index_throws_error(self):
        f32 = F32(7)

        with self.assertRaises(IndexError):
            f32[-1]

    def test_get_index_out_of_range_throws_error(self):
        f32 = F32(7)

        with self.assertRaises(IndexError):
            f32[7]

    def test_set_negative_index_throws_error(self):
        f32 = F32(7)

        with self.assertRaises(IndexError):
            f32[-1] = 592.3483

    def test_set_index_out_of_range_throws_error(self):
        f32 = F32(7)

        with self.assertRaises(IndexError):
            f32[7] = 592.3483

    def test_set_negative(self):
        f32 = F32(7)

        f32[3] = -592.3483

        self.assertEqual(0, f32[0])
        self.assertEqual(0, f32[1])
        self.assertEqual(0, f32[2])
        self.assertAlmostEqual(-592.3483, f32[3], 3)
        self.assertEqual(0, f32[4])
        self.assertEqual(0, f32[5])
        self.assertEqual(0, f32[6])

    def test_set_zero(self):
        f32 = F32(7)

        f32[3] = 592.3483
        f32[3] = 0

        self.assertEqual(0, f32[0])
        self.assertEqual(0, f32[1])
        self.assertEqual(0, f32[2])
        self.assertEqual(0, f32[3])
        self.assertEqual(0, f32[4])
        self.assertEqual(0, f32[5])
        self.assertEqual(0, f32[6])

    def test_set_positive(self):
        f32 = F32(7)

        f32[3] = 592.3483

        self.assertEqual(0, f32[0])
        self.assertEqual(0, f32[1])
        self.assertEqual(0, f32[2])
        self.assertAlmostEqual(592.3483, f32[3], 3)
        self.assertEqual(0, f32[4])
        self.assertEqual(0, f32[5])
        self.assertEqual(0, f32[6])
