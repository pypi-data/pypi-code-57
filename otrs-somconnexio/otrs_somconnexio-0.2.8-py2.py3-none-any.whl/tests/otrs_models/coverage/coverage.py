import unittest

from otrs_somconnexio.otrs_models.coverage.coverage import Coverage


class CoverageTestCase(unittest.TestCase):

    def test_get_selector_values(self):
        Coverage.VALUES = ["foo", "bar"]

        selector_values = Coverage.get_selector_values()

        for val in selector_values:
            self.assertEqual(val[0], val[1])

        self.assertEqual(selector_values[0][0], "foo")
        self.assertEqual(selector_values[0][1], "foo")
        self.assertEqual(selector_values[1][0], "bar")
        self.assertEqual(selector_values[1][1], "bar")
