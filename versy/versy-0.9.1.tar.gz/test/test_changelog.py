from unittest import TestCase
from versy import changelog
import safer
import tdir


class TestChangeLog(TestCase):
    def setUp(self):
        self.results = []

    def test_simple(self):
        with tdir.tdir('setup.py', 'README') as td:
            cl = changelog.ChangeLog(td, '0.2.1', None, safer.printer, 'one')
            cl.new()

            actual = (td / 'CHANGELOG').read_text().splitlines()
            expected = ['## v0.2.1', '', '* one']
            assert expected[0].startswith(expected[0])
            assert actual[1:] == expected[1:]

            cl = changelog.ChangeLog(td, '0.2.1', None, safer.printer, 'two')

            with self.assertRaises(ValueError) as m:
                cl.new()
            assert m.exception.args[0].endswith('already exists')

            cl.update('0.3.0')
            actual = (td / 'CHANGELOG').read_text().splitlines()
            expected = [
                '## v0.3.0',
                '',
                '* two',
                '',
                '## v0.2.1',
                '',
                '* one',
            ]
            assert len(expected) == len(actual)
            for e, a in zip(expected, actual):
                if e.startswith('##'):
                    assert a.startswith(e)
                else:
                    assert a == e
