# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 15:01:40 2019

@author: arrigoni
"""
import unittest
import spinney.tools.reactions as react


print('Testing: ', react.__name__)

class TestCalculateReactionEnergy(unittest.TestCase):

    def setUp(self):
        reaction1 = {
                  'reactants' : [('Ti', 1), ('O2', 1)],
                  'products'  : [('TiO2', 1)]
                 }
        energies1 = {
                  'reactants' : [['Ti2', -15.63423475], ['O2', -9.87427267]],
                  'products'  : [['Ti2O4', -46.28829396]]
                 }
        value1 = -5.452756935 
        value1wang = -6.8127569349999995 
    
        reaction2 = {
                  'reactants' : [('Ti', 2), ('O2', 3/2)],
                  'products'  : [('Ti2O3', 1)]
                 }
        energies2 = {
                  'reactants' : [['Ti2', -15.63423475], ['O2', -9.87427267]],
                  'products'  : [['Ti4O6', -77.19234261]]
                 }
        value2 = -8.150527550000001
        value2wang = -10.19052755
    
        reaction3 = {
                  'reactants' : [('Ti', 3), ('O2', 5/2)],
                  'products'  : [('Ti3O5', 1)]
                 }
        energies3 = {
                  'reactants' : [['Ti2', -15.63423475], ['O2', -9.87427267]],
                  'products'  : [['Ti6O10', -123.90815209]]
                 }
        value3 = -13.817042245000003
        value3wang = -17.217042245000002
    
        reaction4 = {
                  'reactants' : [('Ti', 1), ('O2', 1)],
                  'products'  : [('TiO2', 1)]
                 }
        energies4 = {
                  'reactants' : [('Ti', -15.63423475*0.5), ('O2', -9.87427267)],
                  'products'  : [('TiO2', -46.28829396*0.5)]
                 }
        value4 = -5.452756935
    
        reaction5 = {
                  'reactants' : [('Ti2', 1), ('O2', 2)],
                  'products'  : [('Ti2O4', 1)]
                 }
        energies5 = {
                  'reactants' : [('Ti2', -15.63423475), ('O2', -9.87427267)],
                  'products'  : [('Ti2O4', -46.28829396)]
                 }
        value5 = -5.452756935*2 # Formation energy of Ti2O4 from Ti2 and O2
    
        self.reactions = [reaction1, reaction2, reaction3, reaction4, reaction5]
        self.energies = [energies1, energies2, energies3, energies4, energies5]
        self.values = [value1, value2, value3, value4, value5]
        self.valueswang = [value1wang, value2wang, value3wang]
    
    def test_energies(self):
        for i in range(len(self.reactions)):
            reaction_energy = react.calculate_reaction_energy(self.reactions[i],
                                                              self.energies[i])
            
            self.assertTrue(abs(reaction_energy - self.values[i]) < 1e-12)
            
            if i < 3:
                self.energies[i]['reactants'][1][1] += 1.36 # Wang term
                energy = react.calculate_reaction_energy(self.reactions[i],
                                                         self.energies[i])
                
                self.assertTrue(abs(energy - self.valueswang[i]) < 1e-12)
    
    
if __name__ == '__main__':
    unittest.main()
