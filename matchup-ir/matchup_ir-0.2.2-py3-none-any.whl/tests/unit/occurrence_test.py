import unittest

from matchup.structure.occurrence import Occurrence
from matchup.presentation.text import Term


class OccurrenceTest(unittest.TestCase):
    def setUp(self):
        self._occurrence = Occurrence("d3.txt", Term("brasil", "1-15"))

    def test_add_position(self):
        self.assertEqual(self._occurrence.frequency, 1)

        self._occurrence.add(position="2-15")

        self.assertEqual(self._occurrence.frequency, 2)

