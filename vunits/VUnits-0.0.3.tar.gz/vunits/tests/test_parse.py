import os
import unittest

from vunits.quantity import Quantity
from vunits.parse import _parse_unit

class TestParse(unittest.TestCase):
    def test_parse_unit(self):
        self.assertEqual(_parse_unit(mag=1., units='m'),
                         Quantity(mag=1., m=1.))
        self.assertEqual(_parse_unit(mag=5., units='m'),
                         Quantity(mag=5., m=1.))
        self.assertEqual(_parse_unit(mag=1., units='cm'),
                         Quantity(mag=0.01, m=1.))
        self.assertEqual(_parse_unit(mag=1., units='m/s'),
                         Quantity(mag=1., m=1., s=-1))
        self.assertEqual(_parse_unit(mag=1., units='m s-1'),
                         Quantity(mag=1., m=1., s=-1))
        self.assertEqual(_parse_unit(mag=1., units='m s^-1'),
                         Quantity(mag=1., m=1., s=-1))
        self.assertEqual(_parse_unit(mag=1., units='meter second^-1'),
                         Quantity(mag=1., m=1., s=-1))
        self.assertEqual(_parse_unit(mag=1., units='meters second^-1'),
                         Quantity(mag=1., m=1., s=-1))
        self.assertEqual(_parse_unit(mag=1., units='centimeter second^-1'),
                         Quantity(mag=0.01, m=1., s=-1))


if __name__ == '__main__':
    unittest.main()