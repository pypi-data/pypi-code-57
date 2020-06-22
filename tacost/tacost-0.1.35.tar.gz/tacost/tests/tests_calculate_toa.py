# -*- coding: utf-8 -*-
"""Tests for calculate TOA
Created on Thu May 21 00:16:21 2020

@author: tbeleyur
"""
import numpy as np
import unittest 
from tacost.calculate_toa import *

from tacost.make_positions import generate_LMU_emitted_positions

class Test2DArray(unittest.TestCase):
    
    def setUp(self):
        self.sim_pos = generate_LMU_emitted_positions()
        
    def test_2d(self):
        mic_0 = np.array([0,0,1])
        mic_1 = np.array([0,1,0])

        array_geom = np.row_stack((mic_0, mic_1))
        calculate_mic_arrival_times(self.sim_pos, array_geometry=array_geom)

class TestArbit3DArray(unittest.TestCase):
    def setUp(self):
        self.sim_pos = generate_LMU_emitted_positions()
    
    def test_arbit3d(self):
        rand_geom = np.random.random_integers(0.1,10,27).reshape(-1,3)
        calculate_mic_arrival_times(self.sim_pos, array_geometry=rand_geom)
        
        
        



if __name__ == '__main__':
    unittest.main()


