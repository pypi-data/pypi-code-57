#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 13:42:02 2019

@author: arrigoni
"""
import unittest
from math import gcd
from functools import reduce
import numpy as np
import sys
import os
import time
import ase.io
from spinney.defects.madelung import calculate_madelung_constant
from spinney.defects.madelung import Ewald

def find_gcd(list):
    return reduce(gcd, list)

print('Testing: ', Ewald.__name__)

class MadelungTestCase(unittest.TestCase):
    """ Test the Ewald summation by calculating the Madelung's constant.
    Madelung's constants values taken from:
        R. Hoppe, Angew. Chem. Internat. Edit. 5, 95 (1965)
        and 
    """
    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        structures_path    = os.path.join(base_dir, 'resources')
        self.poscar_rocksalt    = os.path.join(structures_path, 'POSCAR_NaCl')
        charges_rocksalt   = [1,1,1,1,-1,-1,-1,-1]
        self.poscar_CsCl        = os.path.join(structures_path, 'POSCAR_CsCl')
        charges_CsCl       = [1,-1]
        self.poscar_fluorite    = os.path.join(structures_path, 'POSCAR_CaF2')
        charges_fluorite   = [2,2,2,2,-1,-1,-1,-1,-1,-1,-1,-1]
        self.poscar_zincblende  = os.path.join(structures_path, 'POSCAR_AlAs')
        charges_zincblende = [3,-3]
        self.poscar_wurtzite   = os.path.join(structures_path, 'POSCAR_ZnO_w')
        charges_wurtzite   = [2, 2, -2, -2]
        self.poscar_rutile      = os.path.join(structures_path, 'POSCAR_TiO2_rutile')
        charges_rutile     = [4,4,-2,-2,-2,-2]

        self.poscars  = [self.poscar_rocksalt,  self.poscar_CsCl,  self.poscar_fluorite,
                    self.poscar_zincblende,  self.poscar_wurtzite,  self.poscar_rutile]
        self.charges  = [charges_rocksalt, charges_CsCl, charges_fluorite,
                   charges_zincblende, charges_wurtzite, charges_rutile]
        self.madelung = [1.74756,          1.76267,      5.03879,
                    1.63805,            1.64132,          4.7656]
        # Note: for more complex structure, e.g wurtzite and rutile, which posses
        # other independent structure parameters, the Madelung constant will be 
        # affected by these parameters and a comparison with the tabulated value
        # is useless without knowing the employed structure. In this case we 
        # just print the difference
        self.dec = 4

    def testCompareMadelung(self):
        ''' Check for the Ewald class
        '''
        print("From Ewlad class\n")
        for poscar, charge, M in zip(self.poscars, self.charges, self.madelung):
            structure = ase.io.read(poscar)
            ew = Ewald(structure.get_cell(),
                       structure.get_scaled_positions(),
                       charge, 1, direct_cutoff=10, reciprocal_cutoff=1)
            Z = find_gcd(charge)
            U = ew.get_madelung_energy()
            result = calculate_madelung_constant(U, structure, Z)
            if poscar == self.poscar_wurtzite or poscar == self.poscar_rutile:
                print('Relative difference with tabulated value '
                      'for wurtzite/rutile:')
                print((result - M)/M*100, '%')
                sys.stdout.flush()
            else:
                self.assertAlmostEqual(M, result, places=self.dec)
            
if __name__ == '__main__':
    unittest.main()

