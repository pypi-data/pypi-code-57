import unittest
from io import StringIO
import numpy as np

from tests.context import analysis
from analysis.shared.matrix import Matrix, NotSymetricMatrixError, MatrixValueError

MATRIX_BASIC = u'''\tENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\tENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\tENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\tENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\tENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\tENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2
ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514\t0.9652\t0.966\t0.9656
ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212\t0.9596\t0.9887\t0.9629
ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.929\t0.9253\t0.9406
ENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.953\t0.9878
ENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.9601
ENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\t1.0'''
MATRIX_BASIC_HEADERS = ['ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4', 'ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f', 'ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df', 'ENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0', 'ENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7', 'ENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2']
MATRIX_BASIC_MD5SUMS = ['3847bb31fbec071306b5c2ce502458c4', '4fe8dec76ed3d303e0dcc68e38c96f6f', 'a773fa2c902e52ed2e0cf3fb3f4394df', '0b04a1ffef60af4e5802c1038f902eb0', '6ed513f3a5e97687b04cd10c1ed619a7', '0f87a2acadf34fee74c5de9c1f33ebb2']
MATRIX_BASIC_NPMATRIX = np.array(
[[1.0, 0.9699, 0.9514, 0.9652, 0.966, 0.9656],
[0.9699, 1.0, 0.9212, 0.9596, 0.9887, 0.9629],
[0.9514, 0.9212, 1.0, 0.929, 0.9253, 0.9406],
[0.9652, 0.9596, 0.929, 1.0, 0.953, 0.9878],
[0.966, 0.9887, 0.9253, 0.953, 1.0, 0.9601],
[0.9656, 0.9629, 0.9406, 0.9878, 0.9601, 1.0]])
MATRIX_BASIC_DISTANCE_NPMATRIX = np.array(
[[0.0, 0.030100000000000016, 0.04859999999999998, 0.03480000000000005, 0.03400000000000003, 0.034399999999999986],
[0.030100000000000016, 0.0, 0.07879999999999998, 0.04039999999999999, 0.011299999999999977, 0.03710000000000002],
[0.04859999999999998, 0.07879999999999998, 0.0, 0.07099999999999995, 0.07469999999999999, 0.05940000000000001],
[0.03480000000000005, 0.04039999999999999, 0.07099999999999995, 0.0, 0.04700000000000004, 0.012199999999999989],
[0.03400000000000003, 0.011299999999999977, 0.07469999999999999, 0.04700000000000004, 0.0, 0.03990000000000005],
[0.034399999999999986, 0.03710000000000002, 0.05940000000000001, 0.012199999999999989, 0.03990000000000005, 0.0]])

MATRIX_REDUCED = u'''\tENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\tENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\tENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df
ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514
ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212
ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0'''
MATRIX_REDUCED_HEADERS = ['ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4', 'ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f', 'ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df']
MATRIX_REDUCED_MD5SUMS = ['3847bb31fbec071306b5c2ce502458c4', '4fe8dec76ed3d303e0dcc68e38c96f6f', 'a773fa2c902e52ed2e0cf3fb3f4394df']
MATRIX_REDUCED_NPMATRIX = np.array(
[[1.0, 0.9699, 0.9514],
[0.9699, 1.0, 0.9212],
[0.9514, 0.9212, 1.0]])

MATRIX_UNSYMETRIC = u'''\tENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\tENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\tENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\tENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\tENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\tENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2
ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\t1.0\t0.0\t0.0\t0.0\t0.0\t0.0
ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.0\t0.0\t0.0\t0.0
ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.0\t0.0\t0.0
ENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.0\t0.0
ENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.0
ENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\t1.0'''

MATRIX_MD5SUMS = u'''\t3847bb31fbec071306b5c2ce502458c4\t4fe8dec76ed3d303e0dcc68e38c96f6f\ta773fa2c902e52ed2e0cf3fb3f4394df\t0b04a1ffef60af4e5802c1038f902eb0\t6ed513f3a5e97687b04cd10c1ed619a7\t0f87a2acadf34fee74c5de9c1f33ebb2
3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514\t0.9652\t0.966\t0.9656
4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212\t0.9596\t0.9887\t0.9629
a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.929\t0.9253\t0.9406
0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.953\t0.9878
6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.9601
0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\t1.0'''

MATRIX_NAN = u'''\tENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\tENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\tENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\tENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\tENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\tENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2
ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514\t0.9652\t0.966\t0.9656
ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212\t0.9596\t0.9887\t0.9629
ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.929\t0.9253\t0.9406
ENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.953\t0.9878
ENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.9601
ENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\tNaN'''
MATRIX_NAN_NPMATRIX = np.array(
[[1.0, 0.9699, 0.9514, 0.9652, 0.966, 0.9656],
[0.9699, 1.0, 0.9212, 0.9596, 0.9887, 0.9629],
[0.9514, 0.9212, 1.0, 0.929, 0.9253, 0.9406],
[0.9652, 0.9596, 0.929, 1.0, 0.953, 0.9878],
[0.966, 0.9887, 0.9253, 0.953, 1.0, 0.9601],
[0.9656, 0.9629, 0.9406, 0.9878, 0.9601, 0.0]])

MATRIX_BASIC_WITH_EXTRA_SPACE = u'''\tENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\tENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\tENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\tENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\tENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\tENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2
ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514\t0.9652\t0.966\t0.9656
ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212\t0.9596\t0.9887\t0.9629
ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.929\t0.9253\t0.9406
ENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.953\t0.9878
ENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.9601
ENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\t1.0

'''

MATRIX_PARAMETERS = u'assembly=hg19, bin=1000, nbUserDatasets=0, include=all, exclude=blklst, metric=pearson'
MATRIX_BASIC_WITH_MATRIX_PARAMETERS = MATRIX_PARAMETERS+ u'''\tENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\tENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\tENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\tENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\tENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\tENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2
ENCSR255XTC.density.mm10.bw_3847bb31fbec071306b5c2ce502458c4\t1.0\t0.9699\t0.9514\t0.9652\t0.966\t0.9656
ENCSR343TXK.density.mm10.bw_4fe8dec76ed3d303e0dcc68e38c96f6f\t0.9699\t1.0\t0.9212\t0.9596\t0.9887\t0.9629
ENCSR609OHJ.density.mm10.bw_a773fa2c902e52ed2e0cf3fb3f4394df\t0.9514\t0.9212\t1.0\t0.929\t0.9253\t0.9406
ENCSR465PYP.density.mm10.bw_0b04a1ffef60af4e5802c1038f902eb0\t0.9652\t0.9596\t0.929\t1.0\t0.953\t0.9878
ENCSR302LIV.density.mm10.bw_6ed513f3a5e97687b04cd10c1ed619a7\t0.966\t0.9887\t0.9253\t0.953\t1.0\t0.9601
ENCSR032HKE.density.mm10.bw_0f87a2acadf34fee74c5de9c1f33ebb2\t0.9656\t0.9629\t0.9406\t0.9878\t0.9601\t1.0'''

MATRIX_JUNK_NON_FLOAT = u'''\tb\tc
b\tb\tc
c\tb\tc'''

class TestMatrix(unittest.TestCase):

    def test_parse_matrix(self):
        # good matrix
        good_matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC))

        self.assertTrue(np.allclose(good_matrix.get_matrix(), MATRIX_BASIC_NPMATRIX))
        self.assertEqual(good_matrix.get_file_names(), MATRIX_BASIC_HEADERS)

        # unsymetric_matrix
        with self.assertRaises(NotSymetricMatrixError):
            unsymetric_matrix = Matrix.parse_matrix(StringIO(MATRIX_UNSYMETRIC))

        # md5sums matrix
        md5sums_matrix = Matrix.parse_matrix(StringIO(MATRIX_MD5SUMS))

        self.assertTrue(np.allclose(md5sums_matrix.get_matrix(), MATRIX_BASIC_NPMATRIX))
        self.assertEqual(md5sums_matrix.get_file_names(), MATRIX_BASIC_MD5SUMS)

        # nan matrix
        nan_matrix = Matrix.parse_matrix(StringIO(MATRIX_NAN))

        self.assertTrue(np.allclose(nan_matrix.get_matrix(), MATRIX_NAN_NPMATRIX))

        # extra space matrix
        extra_space_matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC_WITH_EXTRA_SPACE))
        self.assertTrue(np.allclose(extra_space_matrix.get_matrix(), MATRIX_BASIC_NPMATRIX))
        self.assertEqual(extra_space_matrix.get_file_names(), MATRIX_BASIC_HEADERS)

        # junk non float
        with self.assertRaises(MatrixValueError):
            junk_non_float = Matrix.parse_matrix(StringIO(MATRIX_JUNK_NON_FLOAT))

        # parameters
        param_matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC_WITH_MATRIX_PARAMETERS))
        self.assertEqual(param_matrix.description, MATRIX_PARAMETERS)

        self.assertEqual(good_matrix.description, '')

    def test_sub_matrix(self):
        basix_matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC))

        # empty md5 matrix
        empty_md5 = basix_matrix.sub_matrix([])
        self.assertFalse(empty_md5)
        self.assertFalse(empty_md5.get_file_names())

        # good md5 matrix
        good_md5_matrix = basix_matrix.sub_matrix(MATRIX_REDUCED_HEADERS)
        self.assertTrue(np.allclose(good_md5_matrix.get_matrix(), MATRIX_REDUCED_NPMATRIX))
        self.assertEqual(good_md5_matrix.get_file_names(), MATRIX_REDUCED_HEADERS)

        # bad md5 matrix
        bad_md5_matrix = good_md5_matrix.sub_matrix(MATRIX_BASIC_HEADERS)
        self.assertTrue(np.allclose(bad_md5_matrix.get_matrix(), MATRIX_REDUCED_NPMATRIX))
        self.assertEqual(bad_md5_matrix.get_file_names(), MATRIX_REDUCED_HEADERS)

    def test_to_distance(self):
        basic_matrix = Matrix.parse_matrix(StringIO(MATRIX_BASIC))
        distance_matrix = basic_matrix.to_distance()

        self.assertTrue(np.allclose(basic_matrix.get_matrix(), MATRIX_BASIC_NPMATRIX))
        self.assertTrue(np.allclose(distance_matrix.get_matrix(), MATRIX_BASIC_DISTANCE_NPMATRIX))
        self.assertFalse(np.allclose(basic_matrix.get_matrix(), distance_matrix.get_matrix()))
