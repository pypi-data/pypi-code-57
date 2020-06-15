import unittest
import pfp_lgbt 

class FlagsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = pfp_lgbt.Client()
        self.flags = self.client.flags() 

class Flags(FlagsTestCase):
    def test_flag_count(self):
        assert len(self.flags) > 10, 'Flag count is not higher than 10'
    def test_flag_present(self):
        presentCount = 0
        for flag in self.flags: 
            if (flag.name == 'nb') or (flag.name == 'pride') or (flag.name == 'trans'):
                presentCount += 1
        assert presentCount == 3, 'Nb, Pride and Trans flags are not present'
    def test_flag_none_present(self):
        nonePresent = False
        for flag in self.flags: 
            if (flag.name is None) or (flag.default_alpha is None) or (flag.tooltip is None) or (flag.image is None):
                nonePresent = True
        assert nonePresent == False, 'A flag object contains an empty property'