import unittest
import os

start_dir = os.path.abspath(os.path.dirname(__file__)) 

def my_suite():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern='test_*.py')

    return suite
