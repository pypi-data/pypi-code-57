import unittest
from tests.context import analysis

import numpy as np
from analysis.shared.matrix import Matrix
from analysis.slice.slice_matrix import SliceMatrix

HEADER = ['A', 'B', 'C', 'D', 'E']
NP_MATRIX = np.ones(
    (
        len(HEADER),
        len(HEADER)),
    dtype=np.float64)
DESCRIPTION = 'UNITTEST'

class TestSliceMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = Matrix(NP_MATRIX, HEADER, DESCRIPTION)

    def tearDown(self):
        self.matrix = None

    def test_cutting(self):
        header = ['A', 'C', 'E']
        should_be = ['A', 'C', 'E']
        
        matrix = SliceMatrix.slice(self.matrix, header)

        self.assertEqual(matrix.get_file_names(), should_be)

    def test_reordering(self):
        header = ['B', 'A', 'E', 'D', 'C']
        should_be = ['B', 'A', 'E', 'D', 'C']

        matrix = SliceMatrix.slice(self.matrix, header)

        self.assertEqual(matrix.get_file_names(), should_be)

    def test_emptying(self):
        header = []
        should_be = []

        matrix = SliceMatrix.slice(self.matrix, header)

        self.assertEqual(matrix.get_file_names(), should_be)

    def test_not_string_header(self):
        header = [1, 1.2, object(), None]
        should_be = []

        matrix = SliceMatrix.slice(self.matrix, header)

        self.assertEqual(matrix.get_file_names(), should_be)

    def test_not_in_matrix_header(self):
        header = ['NOT_IN_HEADER']
        should_be = []

        matrix = SliceMatrix.slice(self.matrix, header)

        self.assertEqual(matrix.get_file_names(), should_be)

    def test_partialy_in_matrix_header(self):
        header = ['A', 'B', 'C', 'NOT_IN_HEADER']
        should_be = ['A', 'B', 'C']

        matrix = SliceMatrix.slice(self.matrix, header)

        self.assertEqual(matrix.get_file_names(), should_be)
