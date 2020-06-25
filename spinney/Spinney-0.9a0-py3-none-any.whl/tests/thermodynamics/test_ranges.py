#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:28:03 2019

@author: arrigoni
"""
import numpy as np
import unittest
from spinney.thermodynamics.chempots import Range

print('Testing: ', Range.__name__)

class TestP1(unittest.TestCase):
    """ Find the minimum and maximum values of x and y such that these
    constraints are satisfied:
        
        2x - 3y <= 12
        x + 5y <= 20
        x > -2
        2x + y = 2
        
    Solution:
        x_min = -1.11111111111111
        x_max = 2.25
        y_min = -2.5
        y_max = 4.222222222222222
        
    """
    x_min = -1.11111111111111
    x_max = 2.25
    y_min = -2.5
    y_max = 4.222222222222222
    
    coeff_equalities = ((2, 1), )
    const_equalities = (2, )
    coeff_inequalities = ((2, -3), (1, 5))
    const_inequalities = (12, 20)
    bounds = ((-2, None), (None, None))
    
    def test_values(self):
        rang = Range(self.coeff_equalities, self.const_equalities,
                     self.coeff_inequalities,
                     self.const_inequalities, self.bounds)
        values = rang.variables_extrema
        solution = np.array([[self.x_min, self.x_max],
                             [self.y_min, self.y_max]])
        condition = np.allclose(values, solution, 1e-8)
        self.assertTrue(condition)
    
class TestP2(unittest.TestCase):
    """ Find the minimum and maximum values of x and y such that these
    constraints are satisfied:
        
        2x - y >= -3
        4x + y <= 5
        y >= 0
        x + y = 0
        
    Solution:
        x_min = -1
        x_max = 0
        y_min = 0
        y_max = 1
        
    """
    x_min = -1
    x_max = 0
    y_min = 0
    y_max = 1
    
    # NOTE: modify signs so that each inequality is represented as ax + by < c
    coeff_equalities = ((1, 1), )
    const_equalities = (0, )
    coeff_inequalities = ((-2, 1), (4, 1))
    const_inequalities = (3, 5)
    bounds = ((None, None), (0, None))
    
    def test_values(self):
        rang = Range(self.coeff_equalities, self.const_equalities,
                     self.coeff_inequalities,
                     self.const_inequalities, self.bounds)
        values = rang.variables_extrema
        solution = np.array([[self.x_min, self.x_max],
                             [self.y_min, self.y_max]])
        condition = np.allclose(values, solution, 1e-8)
        self.assertTrue(condition)
        
class TestP3(unittest.TestCase):
    """ Find the minimum and maximum values of x and y such that these
    constraints are satisfied:
        
        -x + y >= -2
        3x + y <= 5
        y >= 1
        2x - y = 0
        x >= 0
        x <= 1
        
    Solution:
        x_min = 0.5
        x_max = 1
        y_min = 1
        y_max = 2
        
    """
    x_min = 0.5
    x_max = 1
    y_min = 1
    y_max = 2
    
    # NOTE: modify signs so that each inequality is represented as ax + by < c
    coeff_equalities = ((2, -1), )
    const_equalities = (0, )
    coeff_inequalities = ((1, -1), (3, 1))
    const_inequalities = (2, 5)
    bounds = ((0, 1), (1, None))
    
    def test_values(self):
        rang = Range(self.coeff_equalities, self.const_equalities,
                     self.coeff_inequalities,
                     self.const_inequalities, self.bounds)
        values = rang.variables_extrema
        solution = np.array([[self.x_min, self.x_max],
                             [self.y_min, self.y_max]])
        condition = np.allclose(values, solution, 1e-8)
        self.assertTrue(condition)
        
class TestP4(unittest.TestCase):
    """ Find the minimum and maximum values of x, y and z such that these
    constraints are satisfied:
        
        x + y + z = 1
        x + y <= 1
        x + z <= 1
        x >= 0
        y >= 0
        z >= 0
        
    Solution:
        x_min = 0
        x_max = 1
        y_min = 0
        y_max = 1
        z_min = 0
        z_max = 1
    """
    x_min = 0
    x_max = 1
    y_min = 0
    y_max = 1
    z_min = 0
    z_max = 1

    # NOTE: modify signs so that each inequality is represented as ax + by < c
    coeff_equalities = ((1, 1, 1), )
    const_equalities = (1, )
    coeff_inequalities = ((1, 1, 0), (1, 0, 1))
    const_inequalities = (1, 1)
    bounds = ((0, None), (0, None), (0, None))
    
    def test_values(self):
        rang = Range(self.coeff_equalities, self.const_equalities,
                     self.coeff_inequalities,
                     self.const_inequalities, self.bounds)
        values = rang.variables_extrema
        solution = np.array([[self.x_min, self.x_max],
                             [self.y_min, self.y_max],
                             [self.z_min, self.z_max]])
        condition = np.allclose(values, solution, 1e-8)
        self.assertTrue(condition)

class TestP5(unittest.TestCase):
    """ Find the minimum and maximum values of x, y and z such that these
    constraints are satisfied:
        
        z - x - y = 0
        x + y >= 2
        x + y <= 3
        x - y <= 5
        x - y >= -3
        x >= 0
        y >= 0
        z >= 0
        
    Solution:
        x_min = 2
        x_max = 5
        y_min = 2
        y_max = 3
        z_min = 4
        z_max = 8
    """
    x_min = 0
    x_max = 3
    y_min = 0
    y_max = 3
    z_min = 2
    z_max = 3

    # NOTE: modify signs so that each inequality is represented as ax + by < c
    coeff_equalities = ((-1, -1, 1), )
    const_equalities = (0, )
    coeff_inequalities = ((-1, -1, 0), (1, 1, 0), (1, -1, 0), (-1, 1, 0))
    const_inequalities = (-2, 3, 5, 3)
    bounds = ((0, None), (0, None), (0, None))
    
    def test_values(self):
        rang = Range(self.coeff_equalities, self.const_equalities,
                     self.coeff_inequalities,
                     self.const_inequalities, self.bounds)
        values = rang.variables_extrema
        solution = np.array([[self.x_min, self.x_max],
                             [self.y_min, self.y_max],
                             [self.z_min, self.z_max]])
        condition = np.allclose(values, solution, 1e-8)
        self.assertTrue(condition)

if __name__ == '__main__':
    unittest.main()
