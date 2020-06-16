
import unittest
import math
import numpy as np
import cvxpy as cvx

class MFAProblemsMiscTests(unittest.TestCase):
    def test_eigen(self):
        pass
    def test_solver(self):
        size=3
        measured = np.array([1,1,0])
        sigmas = np.array([1,2,1])
        vector = np.array([10,3,1])
        solve_typ = "OSQP"
        cons = {}
        cons['lb'], cons['ub'] = np.array([0,0,0]), np.array([20,20,5])
        cons['li'], cons['ui'] = np.array([-1]), np.array([1])
        cons['Ai'] = np.array([[1,-1,-1]])
        X = cvx.Variable(size)
        # definition of obj function
        mat1 = np.diag(measured)
        mat2 = np.diag(np.divide(np.ones(size), np.sqrt(sigmas)))
        mat = np.multiply(mat1, mat2)

        size = 3
        measured = [1, 1, 0]
        sigmas = [1, 2, 1]
        vector = [10, 3, 1]
        cons = {}
        cons['lb'], cons['ub'] = [0, 0, 0], [20, 20, 5]
        cons['li'], cons['ui'] = [-1], [1]
        cons['Ai'] = np.array([[1, -1, -1]])
        X = cvx.Variable(size)
        # definition of obj function
        mat = [[measured[i]/math.sqrt(sigmas[i]) if i==j else 0 for j in range(size)] \
            for i in range(size)]

        obj = cvx.Minimize(cvx.sum_squares(mat @ (X - vector) ))
        # definition of constraints
        const = []
        const.append(X >= cons['lb'])
        const.append(X <= cons['ub'])
        const.append(cons['Ai'] @ X >= cons['li'])
        const.append(cons['Ai'] @ X <= cons['ui'])
        # Problem
        prob = cvx.Problem(obj, const)
        # Solve
        if solve_typ == "OSQP":
            prob.solve(solver=cvx.OSQP, verbose=False)
        else:
            prob.solve(solver=cvx.MOSEK, verbose=False)



       
if __name__ == '__main__':
    unittest.main()

