
import unittest
import numpy as np
from scipy.sparse import dok_matrix
import mfa_problem_matrices


class SUModelMatricesTests(unittest.TestCase):
    def test_to_reduced_row_echelon_form(self):
        m  = np.array([[ 1, 2, -1,  -4,0,0],
                       [ 2, 3, -1, -11,0,0],
                       [ 0, 0, 0, 0,0,0 ],
                       [ -2, 0, -3,  22,0,0]])
        S = dok_matrix(m, dtype=np.float32)
        Scsr = S.tocsc()
        result = mfa_problem_matrices.to_reduced_row_echelon_form(Scsr)
        result = result.toarray().tolist()
        ref_result = [[1,0,0,-8,0,0],
                      [0,1,0, 1,0,0],
                      [0,0,1,-2,0,0],
                      [0,0,0,0,0,0]]
        self.assertEqual(result,ref_result)

    def test_ineq_red(self):
        pass

    def test_extract_Bsecond_and_determinable_cols(self):
        m  = np.array([[ 1, 0, 0,  0,0],
                       [ 0, 1, 0, 2,0],
                       [ 0, 0, 0,  1,0]])
        S = dok_matrix(m)
        Scsc = S.tocsc()
        result = mfa_problem_matrices.extract_determinable_variables(m,0.1,True)
        ref_result_0 = [0,3]
        ref_result_1 = [0,2]
        self.assertEqual(result[0],ref_result_0)
        self.assertEqual(result[1],ref_result_1)

    def test_define_constraints_properties(self):
        m  = np.array([[ 0,  1, 0,   1],
                       [ 1,  0, 0,  -1],
                       [ -1, 0, -1,  0]])
        result = mfa_problem_matrices.define_constraints_properties(m)
        ref_result = [
            [[1,3],[0,3],[0,2]],
            [[1,1],[1,1],[1,1]],
            [[1,1],[1,-1],[-1,-1]],
            {0:{1:0,2:0},1:{0:0},2:{2:1},3:{0:1,1:1}}
        ]
        self.assertEqual(result[0],ref_result[0])
        self.assertEqual(result[1],ref_result[1])
        self.assertEqual(result[2],ref_result[2])
        self.assertEqual(result[3],ref_result[3])

       
if __name__ == '__main__':
    unittest.main()

