
from datetime import datetime, timedelta
import sys
import unittest

import pandas as pd

# tested component
sys.path.append(".")
import covid19czechia as CZ

class TestMzcr(unittest.TestCase):
    def test_age_to_group(self, *args, **kwargs):
        grouper = CZ.age_to_group

        self.assertEqual(grouper(0), grouper(1))
        self.assertEqual(grouper(2), grouper(4))
        self.assertEqual(grouper(5), grouper(9))
        self.assertEqual(grouper(11), grouper(12))
        self.assertEqual(grouper(75), grouper(77))
        self.assertEqual(grouper(95), grouper(99))
        
        self.assertNotEqual(grouper(0), grouper(5))
        self.assertNotEqual(grouper(9), grouper(10))
        self.assertNotEqual(grouper(99), grouper(100))
    
    def test_covid_deaths(self, *args, **kwargs):
        data = CZ.deaths_covid(*args, **kwargs)
        
        # datatype
        self.assertIsInstance(data, pd.DataFrame)
        # columns
        self.assertIn("week", data.columns)
        self.assertIn("age_group", data.columns)
        self.assertIn("sex", data.columns)
        self.assertIn("deaths", data.columns)
        # datatypes
        self.assertEqual(str(data["week"].dtypes), "int64")
        self.assertTrue( all(isinstance(a,str) for a in data["age_group"]) )
        self.assertTrue( all(isinstance(s,str) for s in data["sex"]) )
        self.assertEqual(str(data["deaths"].dtypes), "int64")
        # values
        self.assertGreaterEqual(data["week"].min(), 1)
        self.assertLessEqual(data["week"].max(), 53)
        age_groups = [f"{i}_{i+4}" for i in range(0,145)]
        self.assertTrue( all(a in age_groups for a in data['age_group']) )
        self.assertTrue( all(s in ["M","F"] for s in data['sex']) )
        self.assertGreaterEqual(data["deaths"].min(), 0)
        
        return data
    
    def test_covid_deaths_level1(self):
        data = self.test_covid_deaths(level = 1)
    def _check_administrative_unit_column(self, col):
        self.assertTrue( all(isinstance(r,str) for r in col) )
        self.assertTrue( all(r[:2] == "CZ" for r in col))
        
    def test_covid_deaths_level2(self):
        data = self.test_covid_deaths(level = 2)
        
        self.assertIn("region", data.columns)
        self._check_administrative_unit_column(data['region'])
        self.assertTrue( all(r[2:].isnumeric() for r in data['region']) )
        
    def test_covid_deaths_level3(self):
        data = self.test_covid_deaths(level = 3)
        
        self.assertIn("region", data.columns)
        self.assertIn("district", data.columns)
        self._check_administrative_unit_column(data['region'])
        self.assertTrue( all(r[2:].isnumeric() for r in data['region']) )
        self._check_administrative_unit_column(data['district'])
        self.assertTrue( all(r[2:-1].isnumeric() for r in data['district']) )
        self.assertTrue( all((r[-1].isupper() and r[-1].isalpha()) or r[-1].isnumeric() for r in data['district']) )
            