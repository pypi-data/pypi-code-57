from typing import Iterator, List
import unittest
from fau import ArraySet, U8, S8, U16, S16, U32, S32, F32


class TestArraySet(unittest.TestCase):
    def test_u8_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.u8(-1, 7)

    def test_u8_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.u8(0, 7)

    def test_u8_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.u8(4294967295, 7)

    def test_u8_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.u8(4294967296, 7)

    def test_u8_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        u8 = arraySet.u8(2238122160, 7)

        self.assertIsInstance(u8, U8)
        self.assertEqual(7, len(u8))
        self.assertEqual(0, u8[0])
        self.assertEqual(0, u8[1])
        self.assertEqual(0, u8[2])
        self.assertEqual(0, u8[3])
        self.assertEqual(0, u8[4])
        self.assertEqual(0, u8[5])
        self.assertEqual(0, u8[6])

    def test_u8_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_u8_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_u8_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_u8_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_u8_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_u8_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_u8_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u8(2238122160, 3)

    def test_s8_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.s8(-1, 7)

    def test_s8_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.s8(0, 7)

    def test_s8_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.s8(4294967295, 7)

    def test_s8_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.s8(4294967296, 7)

    def test_s8_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        s8 = arraySet.s8(2238122160, 7)

        self.assertIsInstance(s8, S8)
        self.assertEqual(7, len(s8))
        self.assertEqual(0, s8[0])
        self.assertEqual(0, s8[1])
        self.assertEqual(0, s8[2])
        self.assertEqual(0, s8[3])
        self.assertEqual(0, s8[4])
        self.assertEqual(0, s8[5])
        self.assertEqual(0, s8[6])

    def test_s8_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_s8_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_s8_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_s8_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_s8_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_s8_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_s8_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s8(2238122160, 3)

    def test_u16_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.u16(-1, 7)

    def test_u16_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.u16(0, 7)

    def test_u16_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.u16(4294967295, 7)

    def test_u16_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.u16(4294967296, 7)

    def test_u16_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        u16 = arraySet.u16(2238122160, 7)

        self.assertIsInstance(u16, U16)
        self.assertEqual(7, len(u16))
        self.assertEqual(0, u16[0])
        self.assertEqual(0, u16[1])
        self.assertEqual(0, u16[2])
        self.assertEqual(0, u16[3])
        self.assertEqual(0, u16[4])
        self.assertEqual(0, u16[5])
        self.assertEqual(0, u16[6])

    def test_u16_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_u16_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_u16_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_u16_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_u16_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_u16_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_u16_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u16(2238122160, 3)

    def test_s16_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.s16(-1, 7)

    def test_s16_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.s16(0, 7)

    def test_s16_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.s16(4294967295, 7)

    def test_s16_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.s16(4294967296, 7)

    def test_s16_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        s16 = arraySet.s16(2238122160, 7)

        self.assertIsInstance(s16, S16)
        self.assertEqual(7, len(s16))
        self.assertEqual(0, s16[0])
        self.assertEqual(0, s16[1])
        self.assertEqual(0, s16[2])
        self.assertEqual(0, s16[3])
        self.assertEqual(0, s16[4])
        self.assertEqual(0, s16[5])
        self.assertEqual(0, s16[6])

    def test_s16_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_s16_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_s16_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_s16_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_s16_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_s16_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_s16_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s16(2238122160, 3)

    def test_u32_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.u32(-1, 7)

    def test_u32_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.u32(0, 7)

    def test_u32_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.u32(4294967295, 7)

    def test_u32_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.u32(4294967296, 7)

    def test_u32_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        u32 = arraySet.u32(2238122160, 7)

        self.assertIsInstance(u32, U32)
        self.assertEqual(7, len(u32))
        self.assertEqual(0, u32[0])
        self.assertEqual(0, u32[1])
        self.assertEqual(0, u32[2])
        self.assertEqual(0, u32[3])
        self.assertEqual(0, u32[4])
        self.assertEqual(0, u32[5])
        self.assertEqual(0, u32[6])

    def test_u32_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_u32_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_u32_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_u32_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_u32_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_u32_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_u32_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.u32(2238122160, 3)

    def test_s32_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.s32(-1, 7)

    def test_s32_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.s32(0, 7)

    def test_s32_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.s32(4294967295, 7)

    def test_s32_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.s32(4294967296, 7)

    def test_s32_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        s32 = arraySet.s32(2238122160, 7)

        self.assertIsInstance(s32, S32)
        self.assertEqual(7, len(s32))
        self.assertEqual(0, s32[0])
        self.assertEqual(0, s32[1])
        self.assertEqual(0, s32[2])
        self.assertEqual(0, s32[3])
        self.assertEqual(0, s32[4])
        self.assertEqual(0, s32[5])
        self.assertEqual(0, s32[6])

    def test_s32_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_s32_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_s32_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_s32_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_s32_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_s32_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_s32_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.s32(2238122160, 3)

    def test_f32_negative_identifier_throws_exception(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.f32(-1, 7)

    def test_f32_identifier_zero(self):
        arraySet = ArraySet()

        arraySet.f32(0, 7)

    def test_f32_identifier_at_limit(self):
        arraySet = ArraySet()

        arraySet.f32(4294967295, 7)

    def test_f32_identifier_out_of_range(self):
        arraySet = ArraySet()

        with self.assertRaises(OverflowError):
            arraySet.f32(4294967296, 7)

    def test_f32_returns_array_of_zeroes(self):
        arraySet = ArraySet()

        f32 = arraySet.f32(2238122160, 7)

        self.assertIsInstance(f32, F32)
        self.assertEqual(7, len(f32))
        self.assertEqual(0, f32[0])
        self.assertEqual(0, f32[1])
        self.assertEqual(0, f32[2])
        self.assertEqual(0, f32[3])
        self.assertEqual(0, f32[4])
        self.assertEqual(0, f32[5])
        self.assertEqual(0, f32[6])

    def test_f32_throws_exception_when_identifier_already_in_use_by_u8(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_f32_throws_exception_when_identifier_already_in_use_by_s8(self):
        arraySet = ArraySet()
        arraySet.s8(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_f32_throws_exception_when_identifier_already_in_use_by_u16(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_f32_throws_exception_when_identifier_already_in_use_by_s16(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_f32_throws_exception_when_identifier_already_in_use_by_u32(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_f32_throws_exception_when_identifier_already_in_use_by_s32(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_f32_throws_exception_when_identifier_already_in_use_by_f32(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        with self.assertRaises(AttributeError):
            arraySet.f32(2238122160, 3)

    def test_write_outputs_empty_when_no_arrays_exist(self):
        arraySet = ArraySet()

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_empty_when_u8_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_u8_when_values_fit_within_s8(self):
        arraySet = ArraySet()
        u8 = arraySet.u8(2238122160, 7)
        u8[2] = 0x7F
        u8[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x7F, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u8_when_values_fit_within_u8(self):
        arraySet = ArraySet()
        u8 = arraySet.u8(2238122160, 7)
        u8[2] = 0xCD
        u8[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xCD, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_empty_when_s8_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.u8(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_s8_when_values_fit_within_s8(self):
        arraySet = ArraySet()
        s8 = arraySet.s8(2238122160, 7)
        s8[1] = -1
        s8[2] = 127
        s8[3] = 37
        s8[4] = -128

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x01,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0xFF, 0x7F, 0x25, 0x80,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s8_when_values_fit_within_u8(self):
        arraySet = ArraySet()
        s8 = arraySet.s8(2238122160, 7)
        s8[2] = 127
        s8[3] = 37

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x01,
                0xB0, 0x08, 0x67, 0x85,
                0x04, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x7F, 0x25,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_empty_when_u16_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.u16(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_u16_when_values_fit_within_s8(self):
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0x7F
        u16[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x7F, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u16_when_values_fit_within_u8_at_lower_bound(self):
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0x80
        u16[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x80, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u16_when_values_fit_within_u8_at_upper_bound(self):
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0xFF
        u16[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xFF, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u16_when_values_exceed_u8(self):
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0x100
        u16[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x22, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u16_when_values_fit_within_u16(self):
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0xFFFF
        u16[4] = 0x6DE5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xE5, 0x6D,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u16_when_values_fit_within_u16_and_last_byte_zero(self):  # noqa: E501
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0x7FFF
        u16[4] = 0x00E5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0x7F, 0x00, 0x00, 0xE5, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_empty_when_s16_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.s16(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_s16_when_values_fit_within_s8(self):
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[1] = -1
        s16[2] = 127
        s16[3] = 37
        s16[4] = -128

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x01,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0xFF, 0x7F, 0x25, 0x80,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s16_when_values_fit_within_u8(self):
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[2] = 0xCD
        s16[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xCD, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s16_when_values_exceed_s8_negatively(self):
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[2] = -0x81
        s16[4] = 0x64

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF, 0x00, 0x00, 0x64, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s16_when_values_exceed_s8_positively(self):
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[2] = 0x80
        s16[4] = -0x64

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x9C, 0xFF,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s16_when_values_fit_within_s16(self):
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[1] = -0x0001
        s16[2] = 0x7FFF
        s16[3] = -0x8000
        s16[4] = 0x64E5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x7F, 0x00, 0x80, 0xE5, 0x64,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s16_when_values_fit_within_u16(self):
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[2] = 0x7FFF
        s16[4] = 0x6DE5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0x7F, 0x00, 0x00, 0xE5, 0x6D,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s16_when_values_fit_within_s16_and_last_byte_zero(self):  # noqa: E501
        arraySet = ArraySet()
        s16 = arraySet.s16(2238122160, 7)
        s16[1] = -0x0001
        s16[2] = 0x7FFF
        s16[3] = -0x8000
        s16[4] = 0x00E5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x7F, 0x00, 0x80, 0xE5, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_empty_when_u32_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.u32(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_u32_when_values_fit_within_s8(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0x7F
        u32[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x7F, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u8_at_lower_bound(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0x80
        u32[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x80, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u8_at_upper_bound(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0xFF
        u32[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xFF, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u16_at_lower_bound(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0x100
        u32[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x22, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u16_at_upper_bound(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0xFFFF
        u32[4] = 0x6DE5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xE5, 0x6D,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_exceed_u16(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0x10000
        u32[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x04,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x01, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x22, 0x00, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fill_until_end(self):
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0xFFFFFFFF
        u32[4] = 0x6DE5392A

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x04,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0x00, 0x00, 0x00, 0x00,
                0x2A, 0x39, 0xE5, 0x6D,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u32_with_one_trailing_zero(self):  # noqa: E501
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0xFFFFFFFF
        u32[4] = 0x00E5392A

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x04,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0x00, 0x00, 0x00, 0x00,
                0x2A, 0x39, 0xE5, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u32_with_two_trailing_zeroes(self):  # noqa: E501
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0xFFFFFFFF
        u32[4] = 0x0000392A

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x04,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0x00, 0x00, 0x00, 0x00,
                0x2A, 0x39, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_u32_when_values_fit_within_u32_with_three_trailing_zeroes(self):  # noqa: E501
        arraySet = ArraySet()
        u32 = arraySet.u32(2238122160, 7)
        u32[2] = 0xFFFFFFFF
        u32[4] = 0x0000002A

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x04,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0x00, 0x00, 0x00, 0x00,
                0x2A, 0x00, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_empty_when_s32_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.s32(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_s32_when_values_fit_within_s8(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[1] = -1
        s32[2] = 127
        s32[3] = 37
        s32[4] = -128

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x01,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0xFF, 0x7F, 0x25, 0x80,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_u8(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0xCD
        s32[4] = 0x22

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x00,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xCD, 0x00, 0x22,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_exceed_s8_negatively(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = -0x81
        s32[4] = 0x33

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF, 0x00, 0x00, 0x33, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_exceed_s8_positively(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0x80
        s32[4] = -0x32

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0xCE, 0xFF,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_u16(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0xFFFF
        s32[4] = 0x6DE5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xE5, 0x6D,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_exceed_u16_negatively(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0xFFFF
        s32[4] = -0x0001

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_exceed_u16_positively(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0x10000
        s32[4] = 0x6DE5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x01, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xE5, 0x6D, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_s16(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[1] = -0x0001
        s32[2] = 0x7FFF
        s32[3] = -0x8000
        s32[4] = 0x64E5

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x03,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0xFF, 0xFF, 0xFF, 0x7F, 0x00, 0x80, 0xE5, 0x64,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_exceed_s16_negatively(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = -0x8001
        s32[4] = 0x343D

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0x7F, 0xFF, 0xFF,
                0x00, 0x00, 0x00, 0x00,
                0x3D, 0x34, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_exceed_s16_positively(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0x8000
        s32[4] = -0xDE32

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x80, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xCE, 0x21, 0xFF, 0xFF,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_u32(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[2] = 0x7FFFFFFF
        s32[4] = 0x6DE5392A

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0x7F,
                0x00, 0x00, 0x00, 0x00,
                0x2A, 0x39, 0xE5, 0x6D,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_s32(self):
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[1] = -0x00000001
        s32[2] = 0x7FFFFFFF
        s32[3] = -0x80000000
        s32[4] = 0x6893E7A2

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0xFF, 0xFF, 0xFF, 0x7F,
                0x00, 0x00, 0x00, 0x80,
                0xA2, 0xE7, 0x93, 0x68,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_s32_with_one_trailing_zero(self):  # noqa: E501
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[1] = -0x00000001
        s32[2] = 0x7FFFFFFF
        s32[3] = -0x80000000
        s32[4] = 0x0093E7A2

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0xFF, 0xFF, 0xFF, 0x7F,
                0x00, 0x00, 0x00, 0x80,
                0xA2, 0xE7, 0x93, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_s32_with_two_trailing_zeroes(self):  # noqa: E501
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[1] = -0x00000001
        s32[2] = 0x7FFFFFFF
        s32[3] = -0x80000000
        s32[4] = 0x0000E7A2

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0xFF, 0xFF, 0xFF, 0x7F,
                0x00, 0x00, 0x00, 0x80,
                0xA2, 0xE7, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_s32_when_values_fit_within_s32_with_three_trailing_zeroes(self):  # noqa: E501
        arraySet = ArraySet()
        s32 = arraySet.s32(2238122160, 7)
        s32[1] = -0x00000001
        s32[2] = 0x7FFFFFFF
        s32[3] = -0x80000000
        s32[4] = 0x000000A2

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x05,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0xFF, 0xFF, 0xFF, 0x7F,
                0x00, 0x00, 0x00, 0x80,
                0xA2, 0x00, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_empty_when_f32_contains_no_non_default_values(self):
        arraySet = ArraySet()
        arraySet.f32(2238122160, 7)

        bytes = arraySet.write()

        self.assert_bytes([0xFF], bytes)

    def test_write_returns_f32_when_contains_non_default_values(self):
        arraySet = ArraySet()
        f32 = arraySet.f32(2238122160, 7)
        f32[2] = -14.37
        f32[4] = 7742.483

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x06,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x85, 0xEB, 0x65, 0xC1,
                0x00, 0x00, 0x00, 0x00,
                0xDD, 0xF3, 0xF1, 0x45,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_f32_when_contains_non_default_values_with_one_trailing_zero(self):  # noqa: E501
        arraySet = ArraySet()
        f32 = arraySet.f32(2238122160, 7)
        f32[2] = -14.37
        f32[4] = 2.22198e-38

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x06,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x85, 0xEB, 0x65, 0xC1,
                0x00, 0x00, 0x00, 0x00,
                0xC3, 0xF3, 0xF1, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_f32_when_contains_non_default_values_with_two_trailing_zeroes(self):  # noqa: E501
        arraySet = ArraySet()
        f32 = arraySet.f32(2238122160, 7)
        f32[2] = -14.37
        f32[4] = 8.74817e-41

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x06,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x85, 0xEB, 0x65, 0xC1,
                0x00, 0x00, 0x00, 0x00,
                0xDD, 0xF3, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_f32_when_contains_non_default_values_with_three_trailing_zeroes(self):  # noqa: E501
        arraySet = ArraySet()
        f32 = arraySet.f32(2238122160, 7)
        f32[2] = -14.37
        f32[4] = 3.09687e-43

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x06,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x85, 0xEB, 0x65, 0xC1,
                0x00, 0x00, 0x00, 0x00,
                0xDD, 0x00, 0x00, 0x00,
                0xFF,
            ],
            bytes
        )

    def test_write_returns_all_non_default_arrays_in_order(self):
        arraySet = ArraySet()
        u16 = arraySet.u16(2238122160, 7)
        u16[2] = 0xFFFF
        u16[4] = 0x6DE5
        arraySet.u32(6787806, 5)
        s32 = arraySet.s32(902562636, 10)
        s32[1] = -0x00000001
        s32[2] = 0x7FFFFFFF
        s32[3] = -0x80000000
        s32[8] = 0x6893E7A2

        bytes = arraySet.write()

        self.assert_bytes(
            [
                0x02,
                0xB0, 0x08, 0x67, 0x85,
                0x05, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0xE5, 0x6D,
                0x05,
                0x4C, 0x03, 0xCC, 0x35,
                0x09, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xFF, 0xFF, 0xFF, 0xFF,
                0xFF, 0xFF, 0xFF, 0x7F,
                0x00, 0x00, 0x00, 0x80,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00,
                0xA2, 0xE7, 0x93, 0x68,
                0xFF,
            ],
            bytes
        )

    def assert_bytes(self, expected: List[int], actual: Iterator[int]) -> None:
        actualBytes = list(actual)

        self.assertEqual(expected, actualBytes)
