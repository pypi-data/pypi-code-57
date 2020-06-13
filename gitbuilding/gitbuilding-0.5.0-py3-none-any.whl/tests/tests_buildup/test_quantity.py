import unittest
from fractions import Fraction
from gitbuilding.buildup.quantity import Quantity

class QuantityTestCase(unittest.TestCase):

    def test_parse_numbers(self):
        in_out = [("34", 34),
                  ("1", 1),
                  ("1.24", 1.24),
                  ("0.25", 0.25),
                  ("1/5", Fraction(1, 5)),
                  ("1 1/3", Fraction(4, 3))]

        for in_string, value in in_out:
            quantity = Quantity(in_string)
            self.assertEqual(quantity.type, quantity.NUMERICAL)
            self.assertEqual(quantity.value, value)

    def test_parse_number_units(self):
        in_out = [('1 1/3 cups', Fraction(4, 3), 'cups'),
                  ('1 fl. oz.', 1, 'fl. oz.'),
                  ('1/2 pinch', Fraction(1, 2), 'pinch'),
                  ('.25 m^2', .25, 'm^2'),
                  ('5 ml', 5, 'ml')]

        for in_string, value, unit in in_out:
            quantity = Quantity(in_string)
            self.assertEqual(quantity.type, quantity.NUMERICAL_UNIT)
            self.assertEqual(quantity.value, value)
            self.assertEqual(quantity.unit, unit)

    def test_parse_string(self):
        input_str = ['Some stuff',
                     'things',
                     'a pinch']

        for string in input_str:
            quantity = Quantity(string)
            self.assertEqual(quantity.type, quantity.DESCRIPTIVE)
            self.assertEqual(quantity.description, string)

    def test_parse_string_warn(self):
        input_str = ['3.2.1things',
                     '.this',
                     '.']

        for string in input_str:
            with self.assertLogs('BuildUp'):
                quantity = Quantity(string)
            self.assertEqual(quantity.type, quantity.DESCRIPTIVE)
            self.assertEqual(quantity.description, string)

    def test_equal(self):
        self.assertEqual(Quantity('1 1/5 barrels'),
                         Quantity('6/5 barrels'))

    def test_addition(self):
        in_out = [('1 1/3 cups', '2 1/2 cups', '3 5/6 cups'),
                  ('1', '1/2', '1.5')]
        for in1, in2, output in in_out:
            self.assertEqual(Quantity(in1)+Quantity(in2),
                             Quantity(output))

    def test_addition_warn(self):
        inputs = [('foo', 'bar'),
                  ('1 foo', '1 bar')]
        for in1, in2 in inputs:
            with self.assertLogs('BuildUp'):
                total = Quantity(in1)+Quantity(in2)
            self.assertEqual(total.description, 'Some')
