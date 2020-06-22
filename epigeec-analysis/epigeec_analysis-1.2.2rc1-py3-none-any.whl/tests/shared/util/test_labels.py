import unittest

from tests.context import analysis
from analysis.shared.util.labels import int_label_to_letter_label, letter_label_to_int_label

class TestLabels(unittest.TestCase):
    def test_int_label_to_letter_label(self):
        self.assertEqual(int_label_to_letter_label(1), 'A')
        self.assertEqual(int_label_to_letter_label(26), 'Z')
        self.assertEqual(int_label_to_letter_label(27), 'AA')
        self.assertEqual(int_label_to_letter_label(28), 'AB')

    def test_letter_label_to_int_label(self):
        self.assertEqual(letter_label_to_int_label('A'), 1)
        self.assertEqual(letter_label_to_int_label('Z'), 26)
        self.assertEqual(letter_label_to_int_label('AA'), 27)
        self.assertEqual(letter_label_to_int_label('AB'), 28)
