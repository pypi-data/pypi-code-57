from unittest import TestCase
from versy import version_file
import tdir


class TestVersionFile(TestCase):
    def test_simple(self):
        with tdir.tdir(
            'setup.py',
            'README',
            'change.txt',
            sub={'bar': 'one', 'VERSION': '0.1.2'},
        ) as td:
            vf = version_file.VersionFile(td, None)
            assert vf.version == '0.1.2'
            assert vf.file.name == 'VERSION'

    def test_in_python(self):
        with tdir.tdir(
            'setup.py',
            'README',
            'change.txt',
            sub={'bar': 'one', 'foo.py': '__version__ = "0.1.2"'},
        ) as td:
            vf = version_file.VersionFile(td, None)
            assert vf.version == '0.1.2'
            assert vf.file.name == 'foo.py'
