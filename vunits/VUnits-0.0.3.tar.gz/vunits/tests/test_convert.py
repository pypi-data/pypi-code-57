import os
import unittest

import numpy as np
import pandas as pd

from vunits.constants import T0
from vunits import convert as c
from vunits.quantity import Quantity

class TestConvert(unittest.TestCase):
    def setUp(self):
        # Read excel sheet with answers
        os.chdir(os.path.dirname(__file__))
        self.ans = pd.read_excel('test_convert.xlsx',
                                 sheet_name='ans',
                                 index_col=0, header=0)

    def test_convert_temp(self):
        # Test all combinations for temperature conversion
        self.assertAlmostEqual(c.convert_temp(T0('K'), initial='K',
                                              final='oC'),
                               self.ans.at['test_convert_temp', 0])
        self.assertAlmostEqual(c.convert_temp(T0('K'), initial='K',
                                              final='oF'),
                               self.ans.at['test_convert_temp', 1])
        self.assertAlmostEqual(c.convert_temp(T0('K'), initial='K',
                                              final='R'),
                               self.ans.at['test_convert_temp', 2])

        self.assertAlmostEqual(c.convert_temp(T0('oC'), initial='oC',
                                              final='K'),
                               self.ans.at['test_convert_temp', 3])
        self.assertAlmostEqual(c.convert_temp(T0('oC'), initial='oC',
                                              final='oF'),
                               self.ans.at['test_convert_temp', 4])
        self.assertAlmostEqual(c.convert_temp(T0('oC'), initial='oC',
                                              final='R'),
                               self.ans.at['test_convert_temp', 5])

        self.assertAlmostEqual(c.convert_temp(T0('oF'), initial='oF',
                                              final='K'),
                               self.ans.at['test_convert_temp', 6])
        self.assertAlmostEqual(c.convert_temp(T0('oF'), initial='oF',
                                              final='oC'),
                               self.ans.at['test_convert_temp', 7])
        self.assertAlmostEqual(c.convert_temp(T0('oF'), initial='oF',
                                              final='R'),
                               self.ans.at['test_convert_temp', 8])

        self.assertAlmostEqual(c.convert_temp(T0('R'), initial='R',
                                              final='K'),
                               self.ans.at['test_convert_temp', 9])
        self.assertAlmostEqual(c.convert_temp(T0('R'), initial='R',
                                              final='oC'),
                               self.ans.at['test_convert_temp', 10])
        self.assertAlmostEqual(c.convert_temp(T0('R'), initial='R',
                                              final='oF'),
                               self.ans.at['test_convert_temp', 11])

    def test_convert_unit(self):
        # Test a unit conversion with multiple-based units
        self.assertAlmostEqual(c.convert_unit(initial='m', final='cm'),
                               self.ans.at['test_convert_unit', 0])
        # Test that convert_temp is called if temperature units passed
        self.assertAlmostEqual(c.convert_unit(num=T0('K'), initial='K',
                                              final='oC'),
                               self.ans.at['test_convert_unit', 1])
        # Test if error raised when units in different set
        with self.assertRaises(ValueError):
            c.convert_unit(initial='cm', final='J')
        # Test if error raised when unaccepted unit inputted
        with self.assertRaises(ValueError):
            c.convert_unit(initial='arbitrary unit', final='J')
        with self.assertRaises(ValueError):
            c.convert_unit(initial='cm', final='arbitrary unit')

    def test_energy_to_freq(self):
        E = Quantity.from_units(0.1, 'eV')
        freq = Quantity.from_units(self.ans.at['test_energy_to_freq', 0], 'Hz')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.energy_to_freq(E), freq('Hz'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.energy_to_freq(E('J')), freq('Hz'))
        self.assertAlmostEqual(c.energy_to_freq(E('eV'), units_in='eV'),
                               freq('Hz'))
        self.assertAlmostEqual(c.energy_to_freq(E, units_out='min-1'),
                               freq('min-1'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.energy_to_freq(E, return_quantity=True), freq)

    def test_energy_to_temp(self):
        E = Quantity.from_units(0.1, 'eV')
        temp = Quantity.from_units(self.ans.at['test_energy_to_temp', 0], 'K')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.energy_to_temp(E), temp('K'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.energy_to_temp(E('J')), temp('K'))
        self.assertAlmostEqual(c.energy_to_temp(E('eV'), units_in='eV'),
                               temp('K'))
        self.assertAlmostEqual(c.energy_to_temp(E, units_out='oC'),
                               temp('oC'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.energy_to_temp(E, return_quantity=True), temp)

    def test_energy_to_wavenumber(self):
        E = Quantity.from_units(0.1, 'eV')
        wavenumber = Quantity.from_units(
                self.ans.at['test_energy_to_wavenumber', 0], 'cm-1')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.energy_to_wavenumber(E),
                               wavenumber('cm-1'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.energy_to_wavenumber(E('J')),
                               wavenumber('cm-1'))
        self.assertAlmostEqual(c.energy_to_wavenumber(E('eV'), units_in='eV'),
                               wavenumber('cm-1'))
        self.assertAlmostEqual(c.energy_to_wavenumber(E, units_out='m-1'),
                               wavenumber('m-1'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.energy_to_wavenumber(E, return_quantity=True),
                         wavenumber)

    def test_freq_to_energy(self):
        freq = Quantity.from_units(2.4e13, 'Hz')
        E = Quantity.from_units(self.ans.at['test_freq_to_energy', 0], 'J')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.freq_to_energy(freq), E('J'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.freq_to_energy(freq('Hz')), E('J'))
        self.assertAlmostEqual(
                c.freq_to_energy(freq('min-1'), units_in='min-1'), E('J'))
        self.assertAlmostEqual(
                c.freq_to_energy(freq, units_out='eV'), E('eV'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.freq_to_energy(freq, return_quantity=True), E)

    def test_freq_to_temp(self):
        freq = Quantity.from_units(2.4e13, 'Hz')
        temp = Quantity.from_units(self.ans.at['test_freq_to_temp', 0], 'K')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.freq_to_temp(freq), temp('K'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.freq_to_temp(freq('Hz')), temp('K'))
        self.assertAlmostEqual(
                c.freq_to_temp(freq('min-1'), units_in='min-1'), temp('K'))
        self.assertAlmostEqual(
                c.freq_to_temp(freq, units_out='oC'), temp('oC'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.freq_to_temp(freq, return_quantity=True), temp)

    def test_freq_to_wavenumber(self):
        freq = Quantity.from_units(2.4e13, 'Hz')
        wavenumber = Quantity.from_units(
                self.ans.at['test_freq_to_wavenumber', 0], 'cm-1')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.freq_to_wavenumber(freq), wavenumber('cm-1'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.freq_to_wavenumber(freq('Hz')),
                               wavenumber('cm-1'))
        self.assertAlmostEqual(
                c.freq_to_wavenumber(freq('min-1'), units_in='min-1'),
                wavenumber('cm-1'))
        self.assertAlmostEqual(c.freq_to_wavenumber(freq, units_out='m-1'),
                               wavenumber('m-1'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.freq_to_wavenumber(freq, return_quantity=True),
                               wavenumber)

    def test_inertia_to_temp(self):
        inertia = Quantity.from_units(3.5E-49, 'kg m2')
        temp = Quantity.from_units(self.ans.at['test_inertia_to_temp', 0], 'K')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.inertia_to_temp(inertia), temp('K'), places=6)
        # Check that inputted floats work
        self.assertAlmostEqual(c.inertia_to_temp(inertia('kg m2')), temp('K'),
                               places=6)
        self.assertAlmostEqual(
                c.inertia_to_temp(inertia('g cm2'), units_in='g cm2'),
                temp('K'), places=6)
        self.assertAlmostEqual(c.inertia_to_temp(inertia, units_out='oC'),
                               temp('oC'), places=6)
        # Check if successfully outputs Quantity objects
        # self.assertAlmostEqual(c.inertia_to_temp(inertia, return_quantity=True),
        #                        temp, places=2)

    def test_temp_to_energy(self):
        temp = Quantity.from_units(1150., 'K')
        E = Quantity.from_units(self.ans.at['test_temp_to_energy', 0], 'J')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.temp_to_energy(temp), E('J'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.temp_to_energy(temp('K')), E('J'))
        self.assertAlmostEqual(c.temp_to_energy(temp('oC'), units_in='oC'),
                               E('J'))
        self.assertAlmostEqual(c.temp_to_energy(temp, units_out='eV'),
                               E('eV'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.temp_to_energy(temp, return_quantity=True),
                         E)

    def test_temp_to_freq(self):
        temp = Quantity.from_units(1150., 'K')
        freq = Quantity.from_units(
                self.ans.at['test_temp_to_freq', 0], 'Hz')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.temp_to_freq(temp), freq('Hz'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.temp_to_freq(temp('K')),
                               freq('Hz'))
        self.assertAlmostEqual(
                c.temp_to_freq(temp('oC'), units_in='oC'),
                freq('Hz'))
        self.assertAlmostEqual(c.temp_to_freq(temp, units_out='min-1'),
                               freq('min-1'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.temp_to_freq(temp, return_quantity=True),
                               freq)

    def test_temp_to_wavenumber(self):
        temp = Quantity.from_units(1150., 'K')
        wavenumber = Quantity.from_units(
                self.ans.at['test_temp_to_wavenumber', 0], 'cm-1')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.temp_to_wavenumber(temp), wavenumber('cm-1'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.temp_to_wavenumber(temp('K')),
                               wavenumber('cm-1'))
        self.assertAlmostEqual(
                c.temp_to_wavenumber(temp('oC'), units_in='oC'),
                wavenumber('cm-1'))
        self.assertAlmostEqual(c.temp_to_wavenumber(temp, units_out='m-1'),
                               wavenumber('m-1'))
        # Check if successfully outputs Quantity objects
        # Unsure why but Quantity objects were not compatible despite magnitude
        # and units agreeing. Separating tests
        wavenumber_out = c.temp_to_wavenumber(temp, return_quantity=True)
        self.assertAlmostEqual(wavenumber_out.mag, wavenumber.mag)
        self.assertTrue(wavenumber_out.units.equals(wavenumber.units))

    def test_wavenumber_to_energy(self):
        wavenumber = Quantity.from_units(800., 'cm-1')
        energy = Quantity.from_units(
                self.ans.at['test_wavenumber_to_energy', 0], 'J')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.wavenumber_to_energy(wavenumber), energy('J'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.wavenumber_to_energy(wavenumber('cm-1')),
                               energy('J'))
        self.assertAlmostEqual(
                c.wavenumber_to_energy(wavenumber('m-1'), units_in='m-1'),
                energy('J'))
        self.assertAlmostEqual(
                        c.wavenumber_to_energy(wavenumber, units_out='eV'),
                        energy('eV'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.wavenumber_to_energy(wavenumber, return_quantity=True),
                               energy)

    def test_wavenumber_to_freq(self):
        wavenumber = Quantity.from_units(800., 'cm-1')
        freq = Quantity.from_units(
                self.ans.at['test_wavenumber_to_freq', 0], 'Hz')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.wavenumber_to_freq(wavenumber), freq('Hz'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.wavenumber_to_freq(wavenumber('cm-1')),
                               freq('Hz'))
        self.assertAlmostEqual(
                c.wavenumber_to_freq(wavenumber('m-1'), units_in='m-1'),
                freq('Hz'))
        self.assertAlmostEqual(
                c.wavenumber_to_freq(wavenumber, units_out='min-1'),
                freq('min-1'))
        # Check if successfully outputs Quantity objects
        self.assertEqual(c.wavenumber_to_freq(wavenumber, return_quantity=True),
                         freq)

    def test_wavenumber_to_inertia(self):
        wavenumber = Quantity.from_units(800., 'cm-1')
        inertia = Quantity.from_units(
                self.ans.at['test_wavenumber_to_inertia', 0], 'kg m2')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.wavenumber_to_inertia(wavenumber),
                               inertia('kg m2'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.wavenumber_to_inertia(wavenumber('cm-1')),
                               inertia('kg m2'))
        self.assertAlmostEqual(
                c.wavenumber_to_inertia(wavenumber('m-1'), units_in='m-1'),
                inertia('kg m2'))
        self.assertAlmostEqual(c.wavenumber_to_inertia(wavenumber, units_out='g cm2'),
                               inertia('g cm2'))
        # Check if successfully outputs Quantity objects
        self.assertAlmostEqual(
                c.wavenumber_to_inertia(wavenumber, return_quantity=True),
                inertia)

    def test_wavenumber_to_temp(self):
        wavenumber = Quantity.from_units(800., 'cm-1')
        temp = Quantity.from_units(
                self.ans.at['test_wavenumber_to_temp', 0], 'K')
        # Check that Quantity objects work
        self.assertAlmostEqual(c.wavenumber_to_temp(wavenumber),
                               temp('K'))
        # Check that inputted floats work
        self.assertAlmostEqual(c.wavenumber_to_temp(wavenumber('cm-1')),
                               temp('K'))
        self.assertAlmostEqual(
                c.wavenumber_to_temp(wavenumber('m-1'), units_in='m-1'),
                temp('K'))
        self.assertAlmostEqual(
                c.wavenumber_to_temp(wavenumber, units_out='oC'),
                temp('oC'))
        # Check if successfully outputs Quantity objects
        # Unsure why but Quantity objects were not compatible despite magnitude
        # and units agreeing. Separating tests
        temp_out = c.wavenumber_to_temp(wavenumber, return_quantity=True)
        self.assertAlmostEqual(temp_out.mag, temp.mag)
        self.assertTrue(temp_out.units.equals(temp.units))

    def test_debye_to_einstein(self):
        debye_temp = Quantity.from_units(200., 'K')
        einstein_temp = Quantity.from_units(
                self.ans.at['test_debye_to_einstein', 0], 'K')
        # Check that func works with floats
        self.assertAlmostEqual(c.debye_to_einstein(debye_temp('K')),
                               einstein_temp('K'))
        # Check that func works with Quantity objects
        self.assertAlmostEqual(c.debye_to_einstein(debye_temp),
                               einstein_temp)

    def test_einstein_to_debye(self):
        einstein_temp = Quantity.from_units(161., 'K')
        debye_temp = Quantity.from_units(
                self.ans.at['test_einstein_to_debye', 0], 'K')
        # Check that func works with floats
        self.assertAlmostEqual(c.einstein_to_debye(einstein_temp('K')),
                               debye_temp('K'))
        # Check that func works with Quantity objects
        self.assertAlmostEqual(c.einstein_to_debye(einstein_temp),
                               debye_temp)

if __name__ == '__main__':
    unittest.main()