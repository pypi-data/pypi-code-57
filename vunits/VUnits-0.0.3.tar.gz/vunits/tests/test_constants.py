# -*- coding: utf-8 -*-
"""
vunits.test_constants
Tests for vunits.constants file
"""

import os
import unittest

import numpy as np
import pandas as pd

from vunits import constants as c


class TestConstants(unittest.TestCase):

    def setUp(self):
        # Read excel sheet with answers
        os.chdir(os.path.dirname(__file__))
        self.ans = pd.read_excel('test_constants.xlsx',
                                 sheet_name='ans',
                                 index_col=0, header=0)

    def test_R(self):
        # Test R for a handful of units
        units = ('J/mol/K', 'kJ/mol/K', 'L atm/mol/K', 'kcal/mol/K',
                 'eV/molecule/K')
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.R(unit), self.ans.at['test_R', i])

        # Test R raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.R('arbitrary unit')

    def test_h(self):
        # Test h for a handful of units
        units = ('J s', 'kJ s', 'eV s', 'Eh s', 'Ha s',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.h(unit), self.ans.at['test_h', i])

        # Test h raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.h('arbitrary unit')

    def test_h_bar(self):
        # Test h_bar for a handful of units
        units = ('J s', 'kJ s', 'eV s', 'Eh s', 'Ha s',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.h_bar(unit), self.ans.at['test_h_bar', i])

        # Test h_bar raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.h_bar('arbitrary unit')

    def test_kb(self):
        # Test kb for a handful of units
        units = ('J/K', 'kJ/K', 'eV/K', 'cal/K', 'kcal/K', 'Eh/K', 'Ha/K',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.kb(unit), self.ans.at['test_kb', i])

        # Test kb raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.kb('arbitrary unit')

    def test_c(self):
        # Test c for a handful of units
        units = ('m/s', 'cm/s',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.c(unit), self.ans.at['test_c', i])

        # Test c raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.c('arbitrary unit')

    def test_m_e(self):
        # Test m_e for a handful of units
        units = ('kg', 'g', 'amu',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.m_e(unit), self.ans.at['test_m_e', i])

        # Test m_e raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.m_e('arbitrary unit')

    def test_m_p(self):
        # Test m_p for a handful of units
        units = ('kg', 'g', 'amu',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.m_p(unit), self.ans.at['test_m_p', i])

        # Test m_p raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.m_p('arbitrary unit')

    def test_m_n(self):
        # Test m_n for a handful of units
        units = ('kg', 'g', 'amu',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.m_n(unit), self.ans.at['test_m_n', i])

        # Test m_n raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.m_n('arbitrary unit')

    def test_P0(self):
        # Test P0 for a handful of units
        units = ('bar', 'atm', 'Pa', 'kPa', 'MPa', 'psi', 'mmHg', 'Torr',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.P0(unit), self.ans.at['test_P0', i])

        # Test P0 raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.P0('arbitrary unit')

    def test_T0(self):
        # Test T0 for a handful of units
        units = ('K', 'oC', 'R', 'oF',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.T0(unit), self.ans.at['test_T0', i])

        # Test T0 raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.T0('arbitrary unit')

    def test_V0(self):
        # Test V0 for a handful of units
        units = ('m3/mol', 'cm3/mol', 'mL/mol', 'L/mol',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.V0(unit), self.ans.at['test_V0', i])

        # Test V0 raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.V0('arbitrary unit')

    def test_N0(self):
        # Test N0 for a handful of units
        self.assertAlmostEqual(c.N0(), self.ans.at['test_N0', 0])

        # Test N0 raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.N0('arbitrary unit')

    def test_Na(self):
        # Test Na for a handful of units
        units = ('mol-1',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.Na(unit), self.ans.at['test_Na', i])

        # Test Na raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.Na('arbitrary unit')

    def test_e(self):
        # Test e for a handful of units
        units = ('C',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.e(unit), self.ans.at['test_e', i])

        # Test e raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.e('arbitrary unit')

    def test_F(self):
        # Test F for a handful of units
        units = ('C/mol',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.F(unit), self.ans.at['test_F', i])

        # Test F raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.F('arbitrary unit')

    def test_G(self):
        # Test G for a handful of units
        units = ('m3 kg-1 s-2',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.G(unit), self.ans.at['test_G', i])

        # Test G raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.G('arbitrary unit')

    def test_eps_0(self):
        # Test eps_0 for a handful of units
        units = ('F/m',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.eps_0(unit), self.ans.at['test_eps_0', i])

        # Test eps_0 raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.eps_0('arbitrary unit')

    def test_mu_0(self):
        # Test mu_0 for a handful of units
        units = ('H/m',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.mu_0(unit), self.ans.at['test_mu_0', i])

        # Test mu_0 raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.mu_0('arbitrary unit')

    def test_R_inf(self):
        # Test R_inf for a handful of units
        units = ('J', 'mJ',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.R_inf(unit), self.ans.at['test_R_inf', i])

        # Test R_inf raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.R_inf('arbitrary unit')

    def test_r_bohr(self):
        # Test r_bohr for a handful of units
        units = ('m',)
        for i, unit in enumerate(units):
            self.assertAlmostEqual(c.r_bohr(unit),
                                   self.ans.at['test_r_bohr', i])

        # Test r_bohr raises an error when an supported unit is passed
        with self.assertRaises(ValueError):
            c.r_bohr('arbitrary unit')

if __name__ == '__main__':
    unittest.main()
