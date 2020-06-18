import unittest
import numpy as np 
import sys
import logging
sys.path.append("..")
from macopt import Macopt

from scipy.optimize import rosen_der, rosen

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_rosenbrock(self):
        def gradient(x):
            grad = rosen_der(x)
            convergence = np.linalg.norm(grad)
            return grad, convergence

        x_init = np.random.rand(2)

        minimizer = Macopt(gradient, x_init)
        result =  minimizer.minimize()
        print(result)
        self.assertTrue( np.all(np.isclose(result['x'], np.array([1., 1.]), 1e-6)) )



if __name__ == '__main__':
    unittest.main()
