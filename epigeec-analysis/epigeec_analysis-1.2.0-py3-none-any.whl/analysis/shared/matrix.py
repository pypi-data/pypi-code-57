import numpy, pandas
import logging
from analysis.shared.exception.geecanalysiserror import GeecAnalysisError

logging.basicConfig()
logger = logging.getLogger(__name__)

class Not2dMatrixError(GeecAnalysisError):
    pass

class NotSquareMatrixError(GeecAnalysisError):
    pass

class NotSymetricMatrixError(GeecAnalysisError):
    pass

class MatrixValueError(GeecAnalysisError):
    pass

class MatrixIOError(GeecAnalysisError):
    pass

class Matrix:

    def get_matrix(self):
        return self.matrix

    def get_file_names(self):
        return self.file_names

    @property
    def description(self):
        return self._description

    def __init__(self, matrix, file_names, description):
        self.file_names = file_names
        self.headers_dict = {}
        self.matrix = matrix
        self._description = description

        if self.matrix.dtype != numpy.float64:
            raise MatrixValueError("The matrix should be float type.")

        if len(self.matrix.shape) != 2:
            raise Not2dMatrixError("The matrix is not 2 dimentions.")

        if not self.is_square_matrix():
            raise NotSquareMatrixError("The matrix is not a square matrix.")

        if not self.is_symetric():
            raise NotSymetricMatrixError("The matrix is not symetric.")

        for i, file_name in enumerate(self.file_names):
            self.headers_dict[file_name] = i

    def write(self, stream):
        stream.write(str(self))

    @staticmethod
    def parse_matrixfile(matrix_filename):
        with open(matrix_filename, 'r') as matrix_file:
            return Matrix.parse_matrix(matrix_file)

    @staticmethod
    def parse_matrix(matrix_file):
        dframe = pandas.read_csv(matrix_file, delimiter='\t', index_col=0)

        matrix = numpy.nan_to_num(dframe.values)
        file_names = dframe.columns.values.tolist()
        description = dframe.index.name

        if description is None:
            description = ''

        if Matrix.is_float_file_names(file_names):
            logger.warning("The filenames heading the matrix seams to be floats")

        try:
            return Matrix(matrix, file_names, description)
        # Fix the problem of pandas in python 2.7.5
        # with empty lines at the end of file
        # generate lines of zeros
        except NotSquareMatrixError:
            return Matrix(Matrix.remove_zeros_line(matrix), file_names, description)

    @staticmethod
    def remove_zeros_line(matrix):
        return matrix[numpy.where(matrix.any(axis=1))[0]]

    @staticmethod
    def is_float(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float_file_names(file_names):
        """
        Test if all filenames are float.
        """
        return all([Matrix.is_float(num) for num in file_names])

    def is_symetric(self):
        """
        return true if the matrix is symetric
        """
        return numpy.allclose(self.matrix, self.matrix.T, atol=1e-8)

    def is_square_matrix(self):
        """
        Test if the 2 axes are the same dimention.
        """
        return self.matrix.shape[0] == self.matrix.shape[1]

    def sub_matrix(self, file_names):
        """
        args: The headers of rows and colums to obtain in the sub matrix
        return: The sub matrix with only the desired items from the headers
        """
        
        indexes = [self.headers_dict[x] for x in file_names if x in self.headers_dict]
        headers = [self.file_names[i] for i in indexes]
        matrix = self.matrix[numpy.ix_(indexes, indexes)]

        return Matrix(matrix, headers, self.description)

    def __iter__(self):
        return numpy.nditer(self.matrix)

    def to_distance(self):
        return Matrix(1 - self.matrix, list(self.file_names), self.description)

    def __str__(self):
        """
        return formatted GeecMatrix
        """
        return self.__repr__()

    def __repr__(self):
        """
        return formatted GeecMatrix
        """
        description = self.description
        if description is None:
            description = ''

        #header line
        header_str = description + '\t' + '\t'.join(self.file_names)
        matrix_str = ''

        for (i, lines) in enumerate(self.matrix):
            matrix_str += '\n' + self.file_names[i] + '\t' + '\t'.join(str(e) for e in lines)

        return header_str + matrix_str

    def __len__(self):
        return len(self.matrix)

    def __add__(self, other):
        return self.matrix + other.matrix

    def __sub__(self, other):
        return self.matrix - other.matrix
