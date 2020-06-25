#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: arrigoni
"""
import numpy as np
import unittest
from spinney.thermodynamics.chempots import OxygenChemPot, ideal_gas_chemical_potential


print('Testing: ', ideal_gas_chemical_potential.__name__)

class TestO2(unittest.TestCase):
    nist_T = np.array([100, 200, 250, 298.15, 300, 350, 400, 450, 500, 600, 
                       700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500,
                       1600,1700,1800,1900, 2000, 2100, 2200, 2300, 2400,
                       2500, 2600, 2700, 2800, 2900, 3000])
    nist_p = 1e5 # Pa
    nist_S = np.array([173.307, 193.485, 199.990, 205.147, 205.329, 
                       209.880, 213.871, 217.445, 220.693, 226.451, 
                       231.466, 235.921, 239.931, 243.578, 246.922,
                       250.010, 252.878, 255.556, 258.068, 260.434,
                       262.672, 264.796, 266.818, 268.748, 270.595,
                       272.366, 274.069, 275.709, 277.290, 278.819,
                       280.297, 281.729, 283.118, 284.466]) # J/mol/K
    nist_S /= 1000 # kJ/mol/K
    
    nist_H_Hrt = np.array([-5.779, -2.868, -1.410, 0., 0.054,
                           1.531, 3.025, 4.543, 6.084, 9.244, 12.499,
                           15.835, 19.241, 22.703, 26.212, 29.761,
                           33.344, 36.957, 40.599, 44.266, 47.958,
                           51.673, 55.413, 59.175, 62.961, 66.769,
                           70.600, 74.453, 78.328, 82.224, 86.141, 
                           90.079, 94.036, 98.013]) # kJ/mol
    nist_G_Grt = nist_H_Hrt - nist_T*nist_S + nist_T[3]*nist_S[3] 

    my_o2 = OxygenChemPot('kJ/mol', 'Pa')
    
    def test_S_O2(self):
        match = []
        for i, T in enumerate(self.nist_T):
            my_S = self.my_o2._S_Shomate_Eq(T)/1000
            if (abs(my_S - self.nist_S[i]) < 1e-3):
                match.append(True)
            else:
                match.append(False)
        self.assertTrue(np.array(match).all())

    def test_H_Hrt_O2(self):
        my_H_rt = self.my_o2._H_Shomate_Eq(self.nist_T[3])
        match = []
        for i, T in enumerate(self.nist_T):
            my_H = self.my_o2._H_Shomate_Eq(T) - my_H_rt
            if (abs(my_H - self.nist_H_Hrt[i]) < 1e-2): # NIST-JANAF tables five ony very few decimal digits
                match.append(True)
            else:
                match.append(False)
        self.assertTrue(np.array(match).all())

    def test_G_Grt_O2(self):
        match = []
        my_Grt = self.my_o2.G_diff_Shomate_Eq(self.nist_T[3])
        for i, T in enumerate(self.nist_T):
            my_G_Grt = self.my_o2.G_diff_Shomate_Eq(T) - my_Grt
            if (abs(my_G_Grt - self.nist_G_Grt[i]) < 1e-2):
                match.append(True)
            else:
                match.append(False)
        self.assertTrue(np.array(match).all())

    def test_mu1(self):
        match = []
        mu_rt = self.my_o2.get_ideal_gas_chemical_potential_Shomate(-10, 1e5, self.nist_T[3])
        for i, T in enumerate(self.nist_T):
            mu = self.my_o2.get_ideal_gas_chemical_potential_Shomate(-10, 1e5, T)
            match.append((abs(mu - mu_rt - self.nist_G_Grt[i]) < 1e-2))
        self.assertTrue(np.array(match).all())

    def test_mu2(self):
        mu_rt = self.my_o2.get_ideal_gas_chemical_potential_Shomate(-10, 1e5, self.nist_T[3])
        mu = self.my_o2.get_ideal_gas_chemical_potential_Shomate(-10, 1e5, self.nist_T)
        match = np.abs(mu[:,0] - mu_rt - self.nist_G_Grt) < 1e-2
        self.assertTrue(match.all())

if __name__ == '__main__':
    unittest.main() 
