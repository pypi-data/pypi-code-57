from argparse import Namespace
from importlib import resources
import os.path
import tempfile
import unittest
from unittest.mock import patch
import warnings

import dipas.test.sequences
import dipas.tools.madx_to_html


class TestMADXToHTML(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore')

    def test(self):
        for sequence in ('cryring', 'hades', 'sis18'):
            with resources.path('dipas.test.sequences', f'{sequence}.seq') as path:
                with tempfile.TemporaryDirectory() as td:
                    with patch('dipas.tools.madx_to_html.parser',
                               Namespace(parse_args=lambda: Namespace(infile=path, outfile=os.path.join(td, 'test'),
                                                                      paramodi=None))):
                        self.assertEqual(dipas.tools.madx_to_html.main(), 0)


if __name__ == '__main__':
    unittest.main()
