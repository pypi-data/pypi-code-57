"""Test class of MyClassInterface

This is a basic unit test class. There is a test for each public function.
If the functions contained conditions, there would be more tests for each public function.

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/python-prototype for details
"""

import unittest
from simple_sample.myClassInterface import MyClassInterface

class TestMyClassInterface(unittest.TestCase, MyClassInterface):
    """
    This is a basic unit test class. There is a test for each public function.
    If the functions contained conditions, there would be more tests for each public function.
    """
    # mci(MyClassInterface): a class variable with default None
    mci = None
    def __init__(self, *args, **kwargs):
        """
        Initialization of variables
        """
        self.mci = MyClassInterface()
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_my_class_interface_can_be_created(self):
        """
        Verifies if the class MyClassInterface can be created
        """
        self.assertTrue(isinstance(self.mci, MyClassInterface))

    def test_my_class_interface_gets_bar_value(self):
        """
        Verifies if the class MyClassInterface bar method return None
        """
        self.assertIsNone(self.mci.bar())

    def test_my_class_interface_gets_qux_value(self):
        """
        Verifies if the class MyClassInterface qux method raises an exception
        """
        with self.assertRaises(NotImplementedError):
            self.mci.qux()

if __name__ == '__main__':
    unittest.main()
