
import unittest

import eurostat_deaths as eurostat

class TestPopulations(unittest.TestCase):
    def test_populations_output(self):
        data = eurostat.populations(chunksize = 10)
        # columns
        self.assertIn("sex", data.columns)
        self.assertIn("age", data.columns)
        self.assertIn("geo\\time", data.columns)
        self.assertTrue(all(str(y) in data.columns for y in range(2014,2020)))
        
            
            

__all__ = ["TestPopulations"]