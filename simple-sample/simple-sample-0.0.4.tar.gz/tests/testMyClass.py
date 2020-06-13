"""Test class of MyClass

This is a basic unit test class. There is a test for each public function.
If the functions contained conditions, there would be more tests for each public function.

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/python-prototype for details
"""

import unittest
from simple_sample.myClass import MyClass

class TestMyClass(unittest.TestCase, MyClass):
    """
    This is a basic unit test class. There is a test for each public function.
    If the functions contained conditions, there would be more tests for each public function.
    """
    # mc(MyClass): a class variable with default None
    mc = None
    def __init__(self, *args, **kwargs):
        """
        Initialization of variables
        """
        self.mc = MyClass()
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_my_class_can_be_created(self):
        """
        Verifies if the class MyClass can be created
        """
        self.assertTrue(isinstance(self.mc, MyClass))

    def test_my_class_gets_bar_value(self):
        """
        Verifies if the class MyClass gets the bar value correctly
        """
        self.assertTrue(self.mc.bar())

        mc = MyClass(True)
        self.assertTrue(mc.bar())

        mc = MyClass(False)
        self.assertFalse(mc.bar())

    def test_my_class_gets_baz_value(self):
        """
        Verifies if the class MyClass gets the baz value correctly
        """
        for _ in range(10):
            self.assertTrue(self.mc.baz() in [True, False])

    def test_my_class_gets_foo_value(self):
        """
        Verifies if the class MyClass gets the foo value correctly
        """
        self.assertFalse(self.mc.foo(True))
        self.assertTrue(self.mc.foo(False))

    def test_my_class_gets_qux_value(self):
        """
        Verifies if the class MyClass qux method raises an exception
        """
        with self.assertRaises(NotImplementedError):
            self.mc.qux()

    def test_my_class_gets_fooquux_value(self):
        """
        Verifies if the class MyClass gets the fooquux value correctly
        """
        for _ in range(10):
            self.assertTrue(self.mc.fooquux() in [True, False])

if __name__ == '__main__':
    unittest.main()
