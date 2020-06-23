import numpy as np

class Matrix_Algebra():
    
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.row1 = np.size(matrix1, 0)
        self.row2 = np.size(matrix2, 0)
        self.col1 = np.size(matrix1, 1)
        self.col2 = np.size(matrix2, 1)
        
    def add(self, matrix1, matrix2):
        matrix3 = np.zeros((self.row1, self.col1))
        if self.row1 == self.row2 && self.col1 == self.col2:
            for i in range(self.row1):
                for j in range(self.col1):
                    matrix3[i][j] = self.matrix1[i][j] + self.matrix2[i][j]
            return matrix3
        else:
            return TypeError:
        
    def sub(self, matrix1, matrix2):
        matrix3 = np.zeros((self.row1, self.col1))
        if self.row1 == self.row2 && self.col1 == self.col2:
            for i in range(self.row1):
                for j in range(self.col1):
                    matrix3[i][j] = self.matrix1[i][j] - self.matrix2[i][j]
            return matrix3
        else:
            return KeyError
    
    def mult(self, matrix1, matrix2):
        matrix3 = np.zeros((self.row1, self.col2))
        if self.col1 == self.row2:
            for i in range(self.row1):
                for j in range(self.col2):
                    for k in range(self.row2):
                        matrix3[i][j] += self.matrix1[i][k] * self.matrix2[k][j]
            return matrix3
        else:
            return KeyError
            