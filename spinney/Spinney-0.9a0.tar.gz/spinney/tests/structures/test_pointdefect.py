#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:02:56 2019

@author: arrigoni
"""
import unittest 
import numpy as np
import os
import ase.io
from spinney.tools.formulas import count_elements
from spinney.tools.reactions import calculate_defect_formation_energy
from spinney.defects.kumagai import KumagaiCorr
from spinney.io.vasp import extract_potential_at_core_vasp  
from spinney.structures.pointdefect import PointDefect, DummyAseCalculator
from spinney.constants import wang_term_O
from spinney.thermodynamics.chempots import OxygenChemPot

print('Testing: ', PointDefect.__name__)

# initialize values
base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
d_ti_file = os.path.join(base_path, 'found_Delta_Ti.txt')
with open(d_ti_file, 'r') as f:
    D_Ti = f.readline()
    D_Ti = D_Ti.split()[-2].strip('[').strip(']')
    D_Ti = float(D_Ti) # eV, per Ti atom, Jain correction term
    
## pristine system
path_calcs = os.path.join(base_path, 'calculations_results')
pristine_path = os.path.join(path_calcs, 'pristine')
pristine_outcar = os.path.join(pristine_path, 'OUTCAR')
pristine_atoms = ase.io.read(pristine_outcar)
pristine_energy = pristine_atoms.get_total_energy()
cell = pristine_atoms.get_cell().view()
pos = pristine_atoms.get_scaled_positions()
# add Jain correction
pristine_formula = ase.io.read(os.path.join(pristine_outcar)).get_chemical_formula()
elements = count_elements(pristine_formula)
pristine_energy -= elements['Ti']*D_Ti
pristine_atoms.set_calculator(DummyAseCalculator(pristine_atoms))
pristine_atoms.calc.set_total_energy(pristine_energy)
    
# dictionary of the pristine system
anatase_energy_fu = pristine_energy/9/4
                                     # anatase energy per formula unit
                                     # corrected with Jain term
                                     # note: the value is taken from the
                                     # 3x3x1 supercell with the
                                     # 12-atoms cell
mu_el_pbeu = -2.12037384
mu_el_hse = -3.34818181
pot_pbeu = 10.488932730165455 
pot_hse = 10.496560891972337
offset = pot_hse - pot_pbeu
align = mu_el_hse - mu_el_pbeu + offset
# from BULK calculation
mu_el_pbeu =  3.88278732 
mu_el_hse  =  mu_el_pbeu + align 
    
                              
# O standard state chemical potential, with Wang correction   
o2_atoms = ase.io.read(os.path.join(path_calcs, 'O2', 'OUTCAR'))
ti_atoms = ase.io.read(os.path.join(path_calcs, 'Ti', 'OUTCAR'))
mu_o_orich = o2_atoms.get_total_energy()
# add wang term  
mu_o_orich += wang_term_O
mu_o_orich /= 2
o2_atoms.set_calculator(DummyAseCalculator(o2_atoms))
o2_atoms.calc.set_total_energy(mu_o_orich*2)
    
mu_ti_tirich = ti_atoms.get_total_energy()/ti_atoms.get_number_of_atoms()
mu_ti_orich = anatase_energy_fu - 2*mu_o_orich

e1 = 5.552352 + 13.661
e2 = 5.300101 + 10.170
e_r = np.array([[e1, 0, 0], [0, e1, 0], [0, 0, e2]])

class TestPointDefect_VO(unittest.TestCase):

    def setUp(self):
        self.defects_folders = ['Vac_O_0', 'Vac_O_1', 'Vac_O_2']
        self.charge_states = list(range(0,3))
        # fractional coordinates defect position in supercell
        self.def_pos_Vac_O = np.array([0.33333333, 0.33771634, 0.7044964])
    
    def test_system(self):        
        print('Testing ', 'V_O system')
        for i, folder in enumerate(self.defects_folders):
            charge = self.charge_states[i]
            def_pos = self.def_pos_Vac_O
            outcar_def = os.path.join(path_calcs, folder, 'OUTCAR')
                            
            comp = ase.io.read(outcar_def)
            energy = comp.get_total_energy()
            elements = count_elements(comp.get_chemical_formula())
            energy -= elements['Ti']*D_Ti
            comp.set_calculator(DummyAseCalculator(comp))
            comp.calc.set_total_energy(energy)
            
            pot_def = extract_potential_at_core_vasp(outcar_def)
            pot_prist = extract_potential_at_core_vasp(pristine_outcar)
            
            kuma = KumagaiCorr(comp.get_cell().view(),
                               comp.get_scaled_positions(),
                               pristine_atoms.get_scaled_positions(),
                               def_pos, charge, e_r, pot_def, pot_prist)
            
            pd = PointDefect(comp)
            pd.set_pristine_system(pristine_atoms)
            pd.correction_scheme = 'ko'
            pd.add_correction_scheme_data(potential_pristine=pot_prist,
                                          potential_defective=pot_def)
            pd.set_dielectric_tensor(e_r)
            # O first, Ti second
            pd.set_parent_elements([o2_atoms, ti_atoms])
            pd.set_vbm(mu_el_hse)
            pd.set_defect_charge(charge)
            pd.set_defect_position(np.array(def_pos))
            mu_o = o2_atoms.get_total_energy()/o2_atoms.get_number_of_atoms()
            mu_ti = mu_ti_orich
            pd.set_chemical_potential_values({'O' : mu_o, 'Ti': mu_ti})
            # calculate formation energy
            e_defect = {comp.get_chemical_formula():comp.get_total_energy()}
            e_pristine = {pristine_atoms.get_chemical_formula():
                pristine_atoms.get_total_energy()}
            chem_pots = dict(O=mu_o_orich, Ti=mu_ti_orich, electron=mu_el_hse)
            E_corr = kuma.get_net_correction_energy()
            form_ene = calculate_defect_formation_energy(e_defect, 
                                                         e_pristine,
                                                         chem_pots,
                                                         charge,
                                                         E_corr=E_corr)
            form_ene_int = pd.get_defect_formation_energy(True)
            # another arbitrary value for chemical potentials
            mu_o, mu_ti = (-9.009068135, -7.817217575)
            chem_pots['O'] = mu_o; chem_pots['Ti'] = mu_ti
            form_ene2 = calculate_defect_formation_energy(e_defect, 
                                                         e_pristine,
                                                         chem_pots,
                                                         charge,
                                                         E_corr=E_corr)
            pd.set_chemical_potential_values({'O':mu_o, 'Ti': mu_ti})
            form_ene_int2 = pd.get_defect_formation_energy(True)
            print(folder)
            print('Charge state = ', charge)
            print('Testing formation energy with finite-size corrections')
            condition = abs(form_ene - form_ene_int) < 1e-16
            self.assertTrue(condition)
            print(condition)
            condition = abs(form_ene2 - form_ene_int2) < 1e-16
            self.assertTrue(condition)
            print(condition)
            print('Done')
            print('Testing calculated finite-size corrections')
            print('PC correction')
            pc = kuma.get_correction_energy()
            corr_dict = pd.calculate_finite_size_correction(True)[1]
            pc_int = corr_dict['PC term']
            condition = abs(pc - pc_int) < 1e-16
            self.assertTrue(condition)
            print(condition)
            print('Done')
            print('Alignment correction')
            alig = kuma.get_potential_alignment()
            alig_int = corr_dict['Alignment term']
            condition = abs(alig - alig_int) < 1e-16
            self.assertTrue(condition)
            print(condition)
            print('Done')
            print('-'*20)
            
class TestPointDefect_VO_mu_range(unittest.TestCase):
   
    def setUp(self):
        self.defect_folder = 'Vac_O_0'
        self.charge_state = 0
        # fractional coordinates defect position in supercell
        self.def_pos_Vac_O = np.array([0.33333333, 0.33771634, 0.7044964])
        self.T_range = (300, 500, 1000, 1500)
        self.p_range = (1e-9, 1e-3, 1, 1e3, 1e6)
        o2 = OxygenChemPot()
        self.o2_values = o2.get_ideal_gas_chemical_potential_Shomate(mu_o_orich*2, 
                                                            self.p_range,
                                                            self.T_range)
    def test_system(self):        
        charge = self.charge_state
        def_pos = self.def_pos_Vac_O
        outcar_def = os.path.join(path_calcs, self.defect_folder, 'OUTCAR')
                            
        comp = ase.io.read(outcar_def)
        energy = comp.get_total_energy()
        elements = count_elements(comp.get_chemical_formula())
        energy -= elements['Ti']*D_Ti
        comp.set_calculator(DummyAseCalculator(comp))
        comp.calc.set_total_energy(energy)
        
        e_defect = {comp.get_chemical_formula():comp.get_total_energy()}
        e_pristine = {pristine_atoms.get_chemical_formula():
                      pristine_atoms.get_total_energy()}
            
        pd = PointDefect(comp)
        pd.set_pristine_system(pristine_atoms)
        pd.set_dielectric_tensor(e_r)
        # O first, Ti second
        pd.set_parent_elements([o2_atoms, ti_atoms])
        pd.set_vbm(mu_el_hse)
        pd.set_defect_charge(charge)
        pd.set_defect_position(np.array(def_pos))
        
        for T in range(self.o2_values.shape[0]):
            for p in range(self.o2_values.shape[1]):
                # compare with an instace created anew
                pd_temp = PointDefect(comp)
                pd_temp.set_pristine_system(pristine_atoms)
                pd_temp.set_dielectric_tensor(e_r)
                pd_temp.set_vbm(mu_el_hse)
                pd_temp.set_defect_charge(charge)
                pd_temp.set_defect_position(np.array(def_pos))

                mu_o = self.o2_values[T, p]/2
                mu_ti = anatase_energy_fu - 2*mu_o
                
                pd.set_chemical_potential_values({'O' : mu_o, 'Ti': mu_ti})
                pd_temp.set_chemical_potential_values({'O' : mu_o, 'Ti': mu_ti})
                # calculate formation energy
                chem_pots = dict(O=mu_o, Ti=mu_ti, electron=mu_el_hse)
                form_ene = calculate_defect_formation_energy(e_defect, 
                                                             e_pristine,
                                                             chem_pots,
                                                             charge,
                                                             E_corr=0)
                form_ene_int = pd.get_defect_formation_energy()
                form_ene_int_tmp = pd_temp.get_defect_formation_energy()
                self.assertAlmostEqual(form_ene, form_ene_int, 16)
                self.assertAlmostEqual(form_ene_int_tmp, form_ene_int, 16)

        # try on purpose too large chemical potentials
        mu_o = mu_o_orich + 0.2
        mu_ti = anatase_energy_fu - 2*mu_o
        
        pd.set_chemical_potential_values({'O' : mu_o, 'Ti' : mu_ti})
        try:
            pd.get_defect_formation_energy()
            condition = False
        except ValueError:
            condition = True
        self.assertTrue(condition)
        pd.set_chemical_potential_values({'O' : mu_o, 'Ti' : mu_ti},
                                         force=True)
        chem_pots = dict(O=mu_o, Ti=mu_ti, electron=mu_el_hse)
        form_ene = calculate_defect_formation_energy(e_defect, 
                                                     e_pristine,
                                                     chem_pots,
                                                     charge,
                                                     E_corr=0)
        form_ene_int = pd.get_defect_formation_energy()
        self.assertAlmostEqual(form_ene, form_ene_int, 16)
        
        mu_ti = mu_ti_tirich + 0.01
        mu_o = anatase_energy_fu - mu_ti
        
        pd.set_chemical_potential_values({'O' : mu_o, 'Ti' : mu_ti})
        try:
            pd.get_defect_formation_energy()
            condition = False
        except ValueError:
            condition = True
        self.assertTrue(condition)
        pd.set_chemical_potential_values({'O' : mu_o, 'Ti' : mu_ti},
                                         force=True)
        chem_pots = dict(O=mu_o, Ti=mu_ti, electron=mu_el_hse)
        form_ene = calculate_defect_formation_energy(e_defect, 
                                                     e_pristine,
                                                     chem_pots,
                                                     charge,
                                                     E_corr=0)
        form_ene_int = pd.get_defect_formation_energy()
        self.assertAlmostEqual(form_ene, form_ene_int, 16)

class TestPointDefect_OTi(unittest.TestCase):
  
    def setUp(self):
        self.defects_folders = ['O_Ti_0', 'O_Ti_-1', 'O_Ti_-2', 'O_Ti_-3', 'O_Ti_-4']
        self.charge_states = list(range(0,-5,-1))
        # fractional coordinates defect position in supercell
        self.def_pos_O_Ti = np.array([ 0.33333333,  0.66666667,  0.5])
    
    def test_system(self):        
        print('Testing ', 'O_Ti system')
        for i, folder in enumerate(self.defects_folders):
            charge = self.charge_states[i]
            def_pos = self.def_pos_O_Ti
            outcar_def = os.path.join(path_calcs, folder, 'OUTCAR')
                            
            comp = ase.io.read(outcar_def)
            energy = comp.get_total_energy()
            elements = count_elements(comp.get_chemical_formula())
            energy -= elements['Ti']*D_Ti
            comp.set_calculator(DummyAseCalculator(comp))
            comp.calc.set_total_energy(energy)
            
            pot_def = extract_potential_at_core_vasp(outcar_def)
            pot_prist = extract_potential_at_core_vasp(pristine_outcar)
                
            kuma = KumagaiCorr(comp.get_cell().view(),
                               comp.get_scaled_positions(),
                               pristine_atoms.get_scaled_positions(),
                               def_pos, charge, e_r, pot_def, pot_prist)
            
            pd = PointDefect(comp)
            pd.set_pristine_system(pristine_atoms)
            pd.correction_scheme = 'ko'
            pd.add_correction_scheme_data(potential_pristine=pot_prist,
                                          potential_defective=pot_def)
            pd.set_dielectric_tensor(e_r)
            # O first, Ti second
            pd.set_parent_elements([o2_atoms, ti_atoms])
            pd.set_vbm(mu_el_hse)
            pd.set_defect_charge(charge)
            pd.set_defect_position(np.array(def_pos))
            mu_o = o2_atoms.get_total_energy()/o2_atoms.get_number_of_atoms()
            mu_ti = mu_ti_orich
            pd.set_chemical_potential_values({'O' : mu_o, 'Ti': mu_ti})
            # calculate formation energy
            e_defect = {comp.get_chemical_formula():comp.get_total_energy()}
            e_pristine = {pristine_atoms.get_chemical_formula():
                pristine_atoms.get_total_energy()}
            chem_pots = dict(O=mu_o_orich, Ti=mu_ti_orich, electron=mu_el_hse)
            E_corr = kuma.get_net_correction_energy()
            form_ene = calculate_defect_formation_energy(e_defect, 
                                                         e_pristine,
                                                         chem_pots,
                                                         charge,
                                                         E_corr=E_corr)
            form_ene_int = pd.get_defect_formation_energy(True)  
            # another arbitrary value for chemical potentials
            mu_o, mu_ti = (-9.009068135, -7.817217575)
            chem_pots['O'] = mu_o; chem_pots['Ti'] = mu_ti
            form_ene2 = calculate_defect_formation_energy(e_defect, 
                                                         e_pristine,
                                                         chem_pots,
                                                         charge,
                                                         E_corr=E_corr)
            pd.set_chemical_potential_values({'O' : mu_o, 'Ti': mu_ti})
            form_ene_int2 = pd.get_defect_formation_energy(True)
            print(folder)
            print('Charge state = ', charge)
            print('Testing formation energy with finite-size corrections')
            condition = abs(form_ene - form_ene_int) < 1e-16
            self.assertTrue(condition)
            print(condition)
            condition = abs(form_ene2 - form_ene_int2) < 1e-16
            self.assertTrue(condition)
            print(condition)
            print('Done')
            print('Testing calculated finite-size corrections')
            print('PC correction')
            pc = kuma.get_correction_energy()
            corr_dict = pd.calculate_finite_size_correction(True)[1]
            pc_int = corr_dict['PC term']
            condition = abs(pc - pc_int) < 1e-16
            self.assertTrue(condition)
            print(condition)
            print('Done')
            print('Alignment correction')
            alig = kuma.get_potential_alignment()
            alig_int = corr_dict['Alignment term']
            condition = abs(alig - alig_int) < 1e-16
            self.assertTrue(condition)
            print(condition)
            print('Done')
            print('-'*20)
            
            
if __name__ == '__main__':
    unittest.main()
