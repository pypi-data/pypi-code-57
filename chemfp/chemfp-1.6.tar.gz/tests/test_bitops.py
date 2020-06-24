from __future__ import print_function
import unittest2

import chemfp
from chemfp import bitops
from chemfp.bitops import hex_encode_as_bytes

class TestBitOps(unittest2.TestCase):
    def test_hex_isvalid_with_valid_hex(self):
        for hex_str in ("AB", "ab", "cd", "abcdef0123456789", "ABCDEF0123456789", "AaBbCcDdEeFf", "13"):
            self.assertTrue(bitops.hex_isvalid(hex_str), hex_str)
            
    def test_hex_isvalid_with_invalid_hex(self):
        for bad_str in ("a", "abc", "A", "ABC", "1", "987"):
            self.assertFalse(bitops.hex_isvalid(bad_str), bad_str)
        for bad_str in ("abcd ", "ab d", "AB C", "ag", "`a", "@A"):
            self.assertFalse(bitops.hex_isvalid(bad_str), bad_str)
            
    def test_union(self):
        for (fp1, fp2, expected) in (
            (b"ABC", b"ABC", b"ABC"),
            (b"ABC", b"BBC", b"CBC"),
            (b"ABF", b"BBC", b"CBG"),
            (b"BA", b"12", b"ss")):
            self.assertEqual(bitops.byte_union(fp1, fp2), expected)
            self.assertEqual(
                bitops.hex_union(hex_encode_as_bytes(fp1), hex_encode_as_bytes(fp2)),
                hex_encode_as_bytes(expected))
                                              

    def test_popcount_and_bitlist_with_single_bit(self):
        for bitno in range(65):
            fp = bitops.byte_from_bitlist([bitno], 80)
            self.assertEqual(bitops.byte_popcount(fp), 1, bitno)
            bitlist = bitops.byte_to_bitlist(fp)
            self.assertEqual(bitlist, [bitno])

            hex_fp = bitops.hex_from_bitlist([bitno], 80)
            self.assertEqual(hex_encode_as_bytes(fp), hex_fp)
            self.assertEqual(bitops.hex_popcount(hex_fp), 1, bitno)
            bitlist = bitops.hex_to_bitlist(hex_fp)
            self.assertEqual(bitlist, [bitno])

    def test_popcount_and_bitlist_with_multiple_bits(self):
        bits = [3, 5, 8, 13, 88, 90]
        expected_bits = [3, 5, 8, 10, 13]

        fp = bitops.byte_from_bitlist(bits, 80)
        self.assertEqual(bitops.byte_popcount(fp), 5)
        bitlist = bitops.byte_to_bitlist(fp)
        self.assertEqual(bitlist, expected_bits)

        hex_fp = bitops.hex_from_bitlist(bits, 80)
        self.assertEqual(hex_encode_as_bytes(fp), hex_fp)
        self.assertEqual(bitops.hex_popcount(hex_fp), 5)
        bitlist = bitops.hex_to_bitlist(hex_fp)
        self.assertEqual(bitlist, expected_bits)

    def test_byte_tanimoto(self):
        for (fp1, fp2) in (
                (b"\0\0\0", b"\0\1\2"),
                (b"ABC", b"ABC"),
                (b"ABC", b"BBC"),
                (b"ABF", b"BBC"),
                (b"BA", b"12")):
            intersection = bitops.byte_intersect(fp1, fp2)
            union = bitops.byte_union(fp1, fp2)
            self.assertEqual(bitops.byte_tanimoto(fp1, fp2),
                             bitops.byte_popcount(intersection) / float(bitops.byte_popcount(union)))
        self.assertEqual(bitops.byte_tanimoto(b"\0\0\0\0", b"\0\0\0\0"), 0.0)
        self.assertEqual(bitops.byte_tanimoto(b"\0", b"\0"), 0.0)
        self.assertEqual(bitops.byte_tanimoto(b"", b""), 0.0)

    def test_byte_tanimoto_errors(self):
        with self.assertRaisesRegexp(ValueError, "byte fingerprints must have the same length"):
            bitops.byte_tanimoto(b"as", b"sdf")

    def test_byte_hex_tanimoto(self):
        for (fp1, fp2) in (
                (b"\0\0\0", b"\0\1\2"),
                (b"ABC", b"ABC"),
                (b"ABC", b"BBC"),
                (b"BA", b"12")):
            hex_fp2 = hex_encode_as_bytes(fp2).lower()
            #print(repr(fp1), repr(fp2), repr(hex_fp2), file=open("/dev/tty", "w"))
            self.assertEqual(bitops.byte_tanimoto(fp1, fp2),
                             bitops.byte_hex_tanimoto(fp1, hex_fp2))
            self.assertEqual(bitops.byte_tanimoto(fp1, fp2),
                             bitops.byte_hex_tanimoto(fp1, hex_fp2.upper()))

        self.assertEqual(bitops.byte_hex_tanimoto(b"\0\0\0\0", "00000000"), 0.0)
        self.assertEqual(bitops.byte_hex_tanimoto(b"\0\0\0\0", b"00000000"), 0.0)
        self.assertEqual(bitops.byte_hex_tanimoto(b"\0", "00"), 0.0)
        self.assertEqual(bitops.byte_hex_tanimoto(b"\0", b"00"), 0.0)
        self.assertEqual(bitops.byte_hex_tanimoto(b"", ""), 0.0)
        self.assertEqual(bitops.byte_hex_tanimoto(b"", b""), 0.0)
        
            
    def test_bad_hex_fingerprint_in_binary_op(self):
        for func in (bitops.hex_union,
                     bitops.hex_intersect,
                     bitops.hex_difference,
                     bitops.hex_tanimoto,
                     bitops.hex_tversky,
                     ):
            with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                func("1234", "123p")
            with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                func("123p", "1234")
            with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                func("123g", "1234")
            with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                func("123G", "1234")
            with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                func("123G", "1234")
            with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                func("123F", "123/")

    def test_bad_hex_fingerprint_in_byte_hex_op(self):
        for func in (bitops.byte_hex_tanimoto,
                     bitops.byte_hex_tversky):
            with self.assertRaisesRegexp(ValueError, "the hex fingerprint contains a non-hex character"):
                func(b"12", "123p")
            with self.assertRaisesRegexp(ValueError, "the hex fingerprint contains a non-hex character"):
                func(b"12", b"123p")
                
            with self.assertRaisesRegexp(ValueError, "the hex fingerprint contains a non-hex character"):
                func(b"12", "123@")
            with self.assertRaisesRegexp(ValueError, "the hex fingerprint contains a non-hex character"):
                func(b"12", b"123@")
                
            with self.assertRaisesRegexp(ValueError, "the hex fingerprint contains a non-hex character"):
                func(b"12", "12G4")
            with self.assertRaisesRegexp(ValueError, "the hex fingerprint contains a non-hex character"):
                func(b"12", "1`23")

    def test_bad_length_in_byte_hex_op(self):
        for func in (bitops.byte_hex_tanimoto,
                     bitops.byte_hex_tversky):
            with self.assertRaisesRegexp(ValueError, "hex fingerprint length must be twice the byte fingerprint length"):
                func(b"1", "123p")
            with self.assertRaisesRegexp(ValueError, "hex fingerprint length must be twice the byte fingerprint length"):
                func(b"1", b"123p")
            with self.assertRaisesRegexp(ValueError, "hex fingerprint length must be twice the byte fingerprint length"):
                func(b"1234", "123@")
            with self.assertRaisesRegexp(ValueError, "hex fingerprint length must be twice the byte fingerprint length"):
                func(b"12", "")
            with self.assertRaisesRegexp(ValueError, "hex fingerprint length must be twice the byte fingerprint length"):
                func(b"12", b"")
            with self.assertRaisesRegexp(ValueError, "hex fingerprint length must be twice the byte fingerprint length"):
                func(b"", " ")
                                
    def test_intersect(self):
        for (fp1, fp2, expected) in (
            (b"ABC", b"ABC", b"ABC"),
            (b"ABC", b"BBC", b"@BC"),
            (b"AB", b"12", b"\1\2"),
            (b"BA", b"12", b"\0\0")):
            intersect = bitops.byte_intersect(fp1, fp2)
            self.assertEqual(intersect, expected)
            n = bitops.byte_popcount(intersect)
            self.assertEqual(bitops.byte_intersect_popcount(fp1, fp2), n)

            hex_fp1 = hex_encode_as_bytes(fp1)
            hex_fp2 = hex_encode_as_bytes(fp2)
            hex_intersect = bitops.hex_intersect(hex_fp1, hex_fp2)
            self.assertEqual(hex_intersect, hex_encode_as_bytes(expected))
            self.assertEqual(bitops.hex_intersect_popcount(hex_fp1, hex_fp2), n)
            self.assertEqual(bitops.hex_popcount(hex_intersect), n)

    def test_difference(self):
        for (fp1, fp2, expected) in (
            (b"A", b"C", b"\2"),
            (b"ABC", b"ABC", b"\0\0\0"),
            (b"ABC", b"BBC", b"\3\0\0"),
            (b"BA", b"12", b"ss")):
            self.assertEqual(bitops.byte_difference(fp1, fp2), expected)
            self.assertEqual(
                bitops.hex_difference(hex_encode_as_bytes(fp1), hex_encode_as_bytes(fp2)),
                hex_encode_as_bytes(expected))
        
    def test_empty(self):
        self.assertEqual(bitops.byte_union(b"", b""), b"")
        self.assertEqual(bitops.byte_intersect(b"", b""), b"")
        self.assertEqual(bitops.byte_difference(b"", b""), b"")
        self.assertEqual(bitops.hex_union(b"", b""), b"")
        self.assertEqual(bitops.hex_intersect(b"", b""), b"")
        self.assertEqual(bitops.hex_difference(b"", b""), b"")
        
    def test_failures(self):
        for func in (bitops.byte_union,
                     bitops.byte_intersect,
                     bitops.byte_difference,
                     bitops.byte_intersect_popcount,
                     ):
            with self.assertRaisesRegexp(ValueError, "byte fingerprints must have the same length"):
                func(b"1", b"12")

        for func in (bitops.hex_union,
                     bitops.hex_intersect,
                     bitops.hex_difference,
                     bitops.hex_intersect_popcount,
                     ):
            with self.assertRaisesRegexp(ValueError, "hex fingerprints must have the same length"):
                func(b"12", b"1234")

        for func in (bitops.hex_union,
                     bitops.hex_intersect,
                     bitops.hex_difference,
                     bitops.hex_intersect_popcount,
                     ):
            with self.assertRaisesRegexp(ValueError, "hex string length must be a multiple of 2"):
                func(b"123", b"123")

    # hex_popcount
                
    def test_hex_popcount_bad_character(self):
        s = "000000000000000"
        self.assertEqual(len(s), 15)
        for i in range(len(s)+1):
            for c in "\0\n/:@G`g\xff":
                t = s[:i] + c + s[i:]
                with self.assertRaisesRegexp(ValueError, "hex fingerprint contains a non-hex character"):
                    bitops.hex_popcount(t)

    def test_hex_popcount_bad_length(self):
        with self.assertRaisesRegexp(ValueError, "hex string length must be a multiple of 2"):
            bitops.hex_popcount("000000000000000")

    # hex_intersect_popcount

    def test_hex_intersect_popcount_bad_character(self):
        s = "000000000000000"
        self.assertEqual(len(s), 15)
        for i in range(len(s)+1):
            for c in "\0\n/:@G`g\xff":
                t = s[:i] + c + s[i:]
                with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                    bitops.hex_intersect_popcount(t, "0000000000000000")
                with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                    bitops.hex_intersect_popcount("0000000000000000", t)

    def test_hex_intersect_popcount_bad_length(self):
        with self.assertRaisesRegexp(ValueError, "hex string length must be a multiple of 2"):
            bitops.hex_intersect_popcount("00000000000000001", "00000000000000001")
            
    def test_hex_intersect_popcount_size_mismatch(self):
        with self.assertRaisesRegexp(ValueError, "hex fingerprints must have the same length"):
            bitops.hex_intersect_popcount("0000000000000000", "000000000000000011")
        with self.assertRaisesRegexp(ValueError, "hex fingerprints must have the same length"):
            bitops.hex_intersect_popcount("000000000000000011", "0000000000000000")

    # hex_intersect_popcount
    def test_hex_tanimoto(self):
        s = "000000000000000"
        for i in range(len(s)+1):
            t1 = s[:i] + "a" + s[i:]
            t2 = s[:i] + "b" + s[i:]
            self.assertEqual(bitops.hex_tanimoto(t1, t2), 2/3.)

        self.assertEqual(bitops.hex_tanimoto("A1", "B3"), 3/5.)

    def test_hex_tanimoto_bad_character(self):
        s = "000000000000000"
        self.assertEqual(len(s), 15)
        for i in range(len(s)+1):
            for c in "\0\n/:@G`g\xff":
                t = s[:i] + c + s[i:]
                with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                    bitops.hex_tanimoto(t, "0000000000000000")
                with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
                    bitops.hex_tanimoto("0000000000000000", t)

    def test_hex_tanimoto_bad_length(self):
        with self.assertRaisesRegexp(ValueError, "hex string length must be a multiple of 2"):
            bitops.hex_tanimoto("00000000000000001", "00000000000000001")
            
    def test_hex_tanimoto_size_mismatch(self):
        with self.assertRaisesRegexp(ValueError, "hex fingerprints must have the same length"):
            bitops.hex_tanimoto("0000000000000000", "000000000000000011")
        with self.assertRaisesRegexp(ValueError, "hex fingerprints must have the same length"):
            bitops.hex_tanimoto("000000000000000011", "0000000000000000")

    def test_byte_contains_bit(self):
        for bitno in range(8):
            self.assertFalse(bitops.byte_contains_bit(b"\0", bitno))
        for bitno in range(8):
            self.assertTrue(bitops.byte_contains_bit(b"\xff", bitno))
        for bitno, expected in enumerate((1, 0, 0, 0, 0, 0, 0, 0,
                                          0, 1, 1, 1, 1, 1, 1, 1)):
            self.assertEqual(bitops.byte_contains_bit(b"\1\xfe", bitno), expected, bitno)

    def test_byte_contains_bad_bit(self):
        with self.assertRaisesRegexp(ValueError, "bit index must be non-negative"):
            bitops.byte_contains_bit(b"123", -1)
        for i in (0, 1, 2, 8, 16):
            with self.assertRaisesRegexp(ValueError, "bit index is too large"):
                bitops.byte_contains_bit(b"", i)
        for i in (8, 9, 16, 32):
            with self.assertRaisesRegexp(ValueError, "bit index is too large"):
                bitops.byte_contains_bit(b" ", i)
        
    def test_hex_contains_bit(self):
        for bitno in range(8):
            self.assertFalse(bitops.hex_contains_bit("00", bitno))
        for bitno in range(8):
            self.assertTrue(bitops.hex_contains_bit("ff", bitno))
        for bitno, expected in enumerate((1, 0, 0, 0, 0, 0, 0, 0,
                                          0, 1, 1, 1, 1, 1, 1, 1)):
            self.assertEqual(bitops.hex_contains_bit("01fe", bitno), bool(expected), bitno)

    def test_hex_contains_bit_extensive(self):
        for probe in range(256):
            fp = "%02x" % probe
            for bit in range(8):
                self.assertEqual(bitops.hex_contains_bit(fp, bit), bool(probe & (1<<bit)), (probe, bit))
                
            fp_upper = fp.upper()
            for bit in range(8):
                self.assertEqual(bitops.hex_contains_bit(fp, bit), bool(probe & (1<<bit)), (probe, bit))
                
            fp = "00" + fp
            for bit in range(8):
                self.assertFalse(bitops.hex_contains_bit(fp, bit))
            for bit in range(8, 16):
                self.assertEqual(bitops.hex_contains_bit(fp, bit), bool(probe & (1<<(bit-8))), (probe, bit))

            fp_upper = fp.upper()
            for bit in range(8, 16):
                self.assertEqual(bitops.hex_contains_bit(fp_upper, bit), bool(probe & (1<<(bit-8))), (probe, bit))

        import random
        for probe in [random.randrange(256*256*256) for i in range(50)]:
            fp = "%02x%02x%02x" % (probe%256, (probe//256)%256, probe//256//256)
            for bit in range(24):
                self.assertEqual(bitops.hex_contains_bit(fp, bit), bool(probe & (1<<bit)), (probe, fp, bit))
            fp = fp.upper()
            for bit in range(24):
                self.assertEqual(bitops.hex_contains_bit(fp, bit), bool(probe & (1<<bit)), (probe, fp, bit))
            

    def test_hex_contains_bad_bit(self):
        with self.assertRaisesRegexp(ValueError, "bit index must be non-negative"):
            bitops.hex_contains_bit("1234", -1)
        for i in (0, 1, 2, 8, 16):
            with self.assertRaisesRegexp(ValueError, "bit index is too large"):
                bitops.hex_contains_bit("", i)
        for i in (8, 9, 16, 32):
            with self.assertRaisesRegexp(ValueError, "bit index is too large"):
                bitops.hex_contains_bit("00", i)
        
    def test_hex_contains_bit_with_non_hex(self):
        # The function does not validate
        for i in range(16):
            self.assertFalse(bitops.hex_contains_bit("spqr", i), i)
        
        with self.assertRaisesRegexp(ValueError, "hex string length must be a multiple of 2"):
            bitops.hex_contains_bit("012", 3)

    def test_tversky_basic(self):
        # Test cases from
        # https://github.com/compute-io/tversky-index/blob/master/test/test.js
        fp1 = bitops.byte_from_bitlist([2,5,7,9], 16)
        fp2 = bitops.byte_from_bitlist([3,5,7,11], 16)
        hex_fp1 = hex_encode_as_bytes(fp1)
        hex_fp2 = hex_encode_as_bytes(fp2)
        for alpha, beta in ((0, 0),
                            (1, 1),
                            (1, 3),
                            (4, 2),
                            (5, 5),
                            (10, 10),
                            (20, 30),
                            (35, 25)):
            expected = 20.0 / (20 + alpha*2 + beta*2)
            self.assertEqual(bitops.byte_tversky(fp1, fp2, alpha/10.0, beta/10.0), expected)
            self.assertEqual(bitops.hex_tversky(hex_fp1, hex_fp2, alpha/10.0, beta/10.0), expected)
            self.assertEqual(bitops.byte_hex_tversky(fp1, hex_fp2, alpha/10.0, beta/10.0), expected)

    def test_tversky(self):
        fp1 = b"Andrew"
        fp2 = b"Dalke!"
        A = bitops.byte_popcount(fp1)
        B = bitops.byte_popcount(fp2)
        hex_fp1 = hex_encode_as_bytes(fp1)
        hex_fp2 = hex_encode_as_bytes(fp2)
        for alpha, beta in ((0.0, 0.0),
                            (0.1, 0.1),
                            (0.1, 0.3),
                            (0.4, 0.2),
                            (0.5, 0.5),
                            (1.0, 1.0),
                            (2.0, 3.0),
                            (3.5, 2.5)):
            c = bitops.byte_intersect_popcount(fp1, fp2)
            a = A-c
            b = B-c
            expected = c / (alpha*a + beta*b + c)
            self.assertAlmostEqual(bitops.byte_tversky(fp1, fp2, alpha, beta), expected)
            ## self.assertAlmostEqual(bitops.hex_tversky(hex_fp1, hex_fp2, alpha, beta), expected)
            self.assertAlmostEqual(bitops.byte_hex_tversky(fp1, hex_fp2, alpha, beta), expected)

        # Default implements the Tanimoto
        alpha = beta = 1.0
        expected = c / (alpha*a + beta*b + c)
        self.assertAlmostEqual(bitops.byte_tversky(fp1, fp2), expected)
        self.assertAlmostEqual(bitops.hex_tversky(hex_fp1, hex_fp2), expected)
        self.assertAlmostEqual(bitops.byte_hex_tversky(fp1, hex_fp2), expected)

    def test_tversky_edge_cases(self):
        self.assertEqual(bitops.byte_tversky(b"\0\0\0\0", b"\0\0\0\0", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\0\0\0\0", b"\0\0\0\1", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\0\0\0\1", b"\0\0\0\0", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\0\0\0\1", b"\0\0\0\1", 0.0, 0.0), 1.0)

        self.assertEqual(bitops.byte_tversky(b"\0\0\0\0", b"\0\0\0\0", 0.0, 0.1), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\0\0\0\0", b"\0\0\0\0", 0.1, 0.0), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\0\0\0\0", b"\0\0\0\0", 0.1, 0.1), 0.0)

        self.assertEqual(bitops.byte_tversky(b"\1\0\0\0", b"\0\0\1\0", 0.0, 0.1), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\1\0\0\0", b"\0\0\1\0", 0.1, 0.0), 0.0)
        self.assertEqual(bitops.byte_tversky(b"\1\0\0\0", b"\0\0\1\0", 0.1, 0.1), 0.0)
        
        self.assertEqual(bitops.hex_tversky(b"0000", b"0000", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.hex_tversky(b"0000", b"0001", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.hex_tversky(b"0001", b"0000", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.hex_tversky(b"0001", b"0001", 0.0, 0.0), 1.0)
                
        self.assertEqual(bitops.hex_tversky(b"0000", b"0000", 0.0, 0.1), 0.0)
        self.assertEqual(bitops.hex_tversky(b"0000", b"0000", 0.1, 0.0), 0.0)
        self.assertEqual(bitops.hex_tversky(b"0000", b"0000", 0.1, 0.1), 0.0)

        self.assertEqual(bitops.hex_tversky(b"0000", "0000", 0.0, 0.0), 0.0)  # can mix bytes and strings
        self.assertEqual(bitops.hex_tversky(b"0000", "0001", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.hex_tversky("0001", b"0000", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.hex_tversky("0001", b"0001", 0.0, 0.0), 1.0)
        self.assertEqual(bitops.hex_tversky("0001", "0001", 0.0, 0.0), 1.0)

        
        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", "0000", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", "0001", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\1", "0000", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\1", "0001", 0.0, 0.0), 1.0)
                
        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", "0000", 0.0, 0.1), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", "0000", 0.1, 0.0), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", "0000", 0.1, 0.1), 0.0)

        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", b"0000", 0.0, 0.0), 0.0) # can mix bytes and strings
        self.assertEqual(bitops.byte_hex_tversky(b"\0\0", b"0001", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\1", b"0000", 0.0, 0.0), 0.0)
        self.assertEqual(bitops.byte_hex_tversky(b"\0\1", b"0001", 0.0, 0.0), 1.0)
                
    def test_byte_tversky_errors(self):
        def fake_hex_byte_tversky(fp1, fp2, alpha=1.0, beta=1.0):
            return bitops.byte_hex_tversky(fp1, hex_encode_as_bytes(fp2), alpha, beta)
        
        for tversky in (bitops.byte_tversky, bitops.hex_tversky, fake_hex_byte_tversky):
            with self.assertRaisesRegexp(ValueError, "alpha must be between 0.0 and 100.0, inclusive"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", -0.1)
            with self.assertRaisesRegexp(ValueError, "beta must be between 0.0 and 100.0, inclusive"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", 0.0, -0.1)
            with self.assertRaisesRegexp(ValueError, "alpha must be between 0.0 and 100.0, inclusive"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", -0.1, -0.1)
            with self.assertRaisesRegexp(ValueError, "alpha must be between 0.0 and 100.0, inclusive"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", 100.001, 1.0)
            with self.assertRaisesRegexp(ValueError, "beta must be between 0.0 and 100.0, inclusive"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", 1.0, 100.001)
            with self.assertRaisesRegexp(ValueError, "alpha must be between 0.0 and 100.0, inclusive"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", 100.0001, -0.1)
            nan = float("NaN")
            with self.assertRaisesRegexp(ValueError, "alpha must not be a NaN"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", nan, 1.0)
            with self.assertRaisesRegexp(ValueError, "beta must not be a NaN"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", 1.0, nan)
            with self.assertRaisesRegexp(ValueError, "alpha must not be a NaN"):
                tversky(b"\1\2\3\4", b"\2\3\4\5", nan, nan)
        
        with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
            # alpha=beta=0.0 has a special code path
            bitops.hex_tversky("0000", "0b0!", 0.0, 0.0)
            
        with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
            # alpha=beta=0.0 has a special code path
            bitops.hex_tversky(b"0000", b"0b0!", 0.0, 0.0)
            
        with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
            bitops.hex_tversky("0000", "0b0?")
            
        with self.assertRaisesRegexp(ValueError, "one of the hex fingerprints contains a non-hex character"):
            bitops.hex_tversky(b"0000", b"0b0?")
            
if __name__ == "__main__":
    unittest2.main()
    
