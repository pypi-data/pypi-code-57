#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 10:52:34 2019

@author: arrigoni
"""
import unittest 
import numpy as np
import os
import spinney.defects.concentration as conc
from spinney.constants import _N_a

print('Testing: ', conc.__name__)

class TestEqFermiLevelIntrinsic(unittest.TestCase):
    """ Tests the equilibrium Fermi Level value for intrinsic semiconductors.
    At each temperature, the value is such that the concentration of 
    free electrons equals the concentration of free holes.
    """
    def setUp(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.T_range = np.linspace(500, 1000, 100)

        dos_ticosb = os.path.join(base_dir, 'resources', 'dos_ticosb')
        dos_ticosb = np.loadtxt(dos_ticosb)[:,0:2]
        dos_ticosb[:,1] /= 4 # for f.u. per cell
        self.dos_ticosb = dos_ticosb
        self.vbm_ticosb =  6.299
        self.eg_ticosb = 1.03
        volume_ticosb = 202.9621167/4*(1e-8)**3 # cm^3 for cell with 4 TiCoSb units
        self.fu_per_v_ticosb = 1/volume_ticosb

        self.Eq_ticosb = conc.EquilibriumConcentrations(None, None,
                                               self.vbm_ticosb, self.eg_ticosb,
                                               {'electron':self.fu_per_v_ticosb,
                                                'hole':self.fu_per_v_ticosb},
                                                self.dos_ticosb, self.T_range)

        dos_tio2_up = os.path.join(base_dir, 'resources', 'dos_tio2_up')
        dos_tio2_up = np.loadtxt(dos_tio2_up)
        dos_tio2_up[:,1] /= 4
        dos_tio2_down = os.path.join(base_dir, 'resources', 'dos_tio2_down')
        dos_tio2_down = np.loadtxt(dos_tio2_down)
        dos_tio2_down[:,1] /= 4
        self.dos_tio2_up = dos_tio2_up
        self.dos_tio2_down = dos_tio2_down
        self.vbm_tio2 = 3.82060651
        self.eg_tio2 = 2.9721
        volume_tio2 = 136.07709707985427/4*(1e-8)**3 # cm^3 For Ti4O8 PBE+U=5.8 anatase
        self.fu_per_v_tio2 = 1/volume_tio2
        self.Eq_tio2 = conc.EquilibriumConcentrations(None, None,
                                             self.vbm_tio2, self.eg_tio2,
                                             {'electron':self.fu_per_v_tio2,
                                              'hole':self.fu_per_v_tio2},
                                              self.dos_tio2_up, self.T_range,
                                              dos_down=self.dos_tio2_down)
    
    def test_carriers_concentrations_ticosb(self):
        eq_mus = self.Eq_ticosb.equilibrium_fermi_level
        nel_fu = []
        nho_fu = []
        for i, mu in enumerate(eq_mus):
            elec = conc.ConductionElectron(self.dos_ticosb, self.vbm_ticosb,
                                           self.vbm_ticosb + self.eg_ticosb,
                                           mu, self.T_range[i])
            nel_fu.append(elec.get_conduction_electron_number())
            hole = conc.ValenceHole(self.dos_ticosb, self.vbm_ticosb,
                                           self.vbm_ticosb + self.eg_ticosb,
                                           mu, self.T_range[i])
            nho_fu.append(hole.get_valence_holes_number())
        nel_fu = np.array(nel_fu)
        nho_fu = np.array(nho_fu)
        
        nel_conc = self.Eq_ticosb.get_equilibrium_electron_concentrations()
        nho_conc = self.Eq_ticosb.get_equilibrium_hole_concentrations()
        # no. electrons per fu = no. holes per fu
        self.assertTrue(np.allclose(nel_fu, nho_fu, 1e-12))
        # no. electrons per mole per cm^3 = no. holes per mole per cm^3
        self.assertTrue(np.allclose(nel_conc/_N_a, nho_conc/_N_a, 1e-12))
        
    def test_carriers_concentrations_tio2(self):
        eq_mus = self.Eq_tio2.equilibrium_fermi_level
        nel_fu = []
        nho_fu = []
        for i, mu in enumerate(eq_mus):
            elec = conc.ConductionElectron(self.dos_tio2_up, self.vbm_tio2, 
                                           self.vbm_tio2 + self.eg_tio2,
                                           mu, self.T_range[i],
                                           dos_down=self.dos_tio2_down)
            nel_fu.append(elec.get_conduction_electron_number())
            hole = conc.ValenceHole(self.dos_tio2_up, self.vbm_tio2, 
                                           self.vbm_tio2 + self.eg_tio2,
                                           mu, self.T_range[i],
                                           dos_down=self.dos_tio2_down)
            nho_fu.append(hole.get_valence_holes_number())
        nel_fu = np.array(nel_fu)
        nho_fu = np.array(nho_fu)
        
        nel_conc = self.Eq_tio2.get_equilibrium_electron_concentrations()
        nho_conc = self.Eq_tio2.get_equilibrium_hole_concentrations()
        # no. electrons per fu = no. holes per fu
        self.assertTrue(np.allclose(nel_fu, nho_fu, 1e-12))
        # no. electrons per mole per cm^3 = no. holes per mole per cm^3
        self.assertTrue(np.allclose(nel_conc/_N_a, nho_conc/_N_a, 1e-12))
        
if __name__=='__main__':
    unittest.main()
