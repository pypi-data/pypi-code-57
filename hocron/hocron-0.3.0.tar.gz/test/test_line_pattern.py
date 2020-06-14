import re
import unittest

from hocron import LinePattern


class TestLinePattern(unittest.TestCase):

    def test_line_pattern(self):
        line_pattern = LinePattern(['EUR', re.compile('\d\d\.\d\d')])  # noqa 
        matched_words = line_pattern.match(['EUR', '45.12'])

        self.assertTrue(matched_words)
        self.assertEquals(
            matched_words,
            ['EUR', '45.12']
        )

    def test_match(self):
        line_pattern = LinePattern(['Datum', re.compile('\d\d.\d\d.\d\d')])  # noqa
        exact_match = line_pattern.match(
            ['Datum', '08.06,20', '17:13', 'Uhr']
        )
        self.assertTrue(
            exact_match
        )

    def test_exact_match_1(self):
        line_pattern = LinePattern(['EUR', re.compile('\d\d\.\d\d')])  # noqa 

        self.assertTrue(
            line_pattern.exact_match(['EUR', '45.12'])
        )

        self.assertFalse(
            line_pattern.exact_match(['EUR', '45,12'])
        )

        self.assertFalse(
            line_pattern.exact_match(['45.12', 'EUR'])
        )

    def test_exact_match_2(self):
        line_pattern = LinePattern(['Datum', re.compile('\d\d.\d\d.\d\d')])  # noqa
        self.assertTrue(
            line_pattern.exact_match(
                ['Datum', '08.06,20']
            )
        )


if __name__ == '__main__':
    unittest.main()
