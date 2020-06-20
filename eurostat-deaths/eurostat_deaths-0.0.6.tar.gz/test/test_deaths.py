
import os
import pickle
import re
import unittest

import eurostat_deaths as eurostat

class TestDeaths(unittest.TestCase):
    def test_deaths_output(self):
        data = eurostat.deaths()
        print(data)
        
__all__ = ["TestDeaths"]