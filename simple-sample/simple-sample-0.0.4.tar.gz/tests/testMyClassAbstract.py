"""Test class of MyClassAbstract

This is a basic unit test class.
It is not possible to instantiate a class with an abstract method,
so missing the method for testing the other method.

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/python-prototype for details
"""

import unittest
from simple_sample.myClassAbstract import MyClassAbstract

class TestMyClassAbstract(unittest.TestCase):
    """
    This is a basic unit test class.
    It is not possible to instantiate a class with an abstract method,
    so missing the method for testing the other method.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization of variables
        """
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_my_class_abstract_can_be_created(self):
        """
        Verifies if the class MyClassAbstract raises an exception
        """
        with self.assertRaises(TypeError):
            MyClassAbstract()

if __name__ == '__main__':
    unittest.main()
