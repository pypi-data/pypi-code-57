# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 13:59:36 2019

@author: arrigoni

"""
import unittest 
import spinney.tools.formulas as cf


print('Testing: ', cf.__name__)
       
class TestGetFormulaUnit(unittest.TestCase):
    # formula:formula_unit
    test_compounds = {
                      'S8'       :  'S',
                      'MnO'      :  'MnO',
                      'H4S2O8'   :  'H2SO4',
                      'C6H6'*2   :  'CHCH',
                      'CH3COOH'  :  'CH3COOH',
                      'H6O3'     :  'H2O',
                      'Ti9O15'   :  'Ti3O5'
                      }
    
    def test_get_fu(self):
        for key, value in self.test_compounds.items():       
            result = cf.get_formula_unit(key)
            self.assertEqual(value, result)
            
            
class TestCountElements(unittest.TestCase):
   
    def setUp(self):
        self.test_compounds = {
                      'S8'       :  {'S' : 8, 'tot' : 8},
                      'MnO'      :  {'Mn' : 1, 'O' : 1, 'tot' : 2},
                      'H4S2O8'   :  {'H' : 4, 'S' : 2, 'O' : 8, 'tot' : 14},
                      'C6H6'*2   :  {'C' : 12, 'H' : 12, 'tot' : 24},
                      'CH3COOH'  :  {'C' : 2, 'H' : 4, 'O' : 2, 'tot' : 8},
                      'H6O3'     :  {'H' : 6, 'O' : 3, 'tot' : 9},
                      'Ti9O15'   :  {'Ti' : 9, 'O' : 15, 'tot' : 24}
                      }
    
    def test_count_elements(self):
        for key in self.test_compounds.keys():
            elements, tot = cf.count_elements(key, total=True)
            tot_flag = abs(tot - self.test_compounds[key]['tot']) < 1e-15
            del self.test_compounds[key]['tot']
            self.assertTrue(tot_flag)
            
            for key2, value2 in self.test_compounds[key].items():
                flag = abs(elements[key2] - value2) < 1e-15
                self.assertTrue(flag)


class TestGetNumberFu(unittest.TestCase):
    test_compounds = {
                      'S8'       :  8,
                      'MnO'      :  1,
                      'H4S2O8'   :  2,
                      'C6H6'*2   :  6,
                      'CH3COOH'  :  1,
                      'H6O3'     :  3,
                      'Ti9O15'   :  3
                      }
    
    def test_number_basic_fu(self):
        for key, value in self.test_compounds.items():
            number_fu = cf.get_number_fu(key)
            self.assertTrue(abs(number_fu - value) < 1e-15)
        
        
if __name__ == '__main__':
    unittest.main()
            
    
