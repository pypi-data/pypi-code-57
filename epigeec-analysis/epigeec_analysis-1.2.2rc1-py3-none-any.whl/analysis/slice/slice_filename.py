from __future__ import absolute_import, division, print_function

from analysis.shared.matrix import Matrix
from analysis.slice.slice_matrix import SliceMatrix

class SliceFilename(object):
    def __init__(self, matrix, file_names):
        self.matrix = matrix
        self.file_names = file_names

    def geec_slice_file_name(self, matrix_filename, file_names, output=None):
        matrix = Matrix.parse_matrixfile(matrix_filename)
        newmatrix = SliceMatrix.slice(matrix, file_names)

        if output:
            with open(output, 'w') as output:
                output.write(str(newmatrix))
        else:
            print(newmatrix, end='')

    def run(self):
        with open(self.file_names, 'r') as f:
            filenames = f.read().split('\n')

        self.geec_slice_file_name(self.matrix, filenames)