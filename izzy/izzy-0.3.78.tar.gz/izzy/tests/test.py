"""
test.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""


from izzy.tests import TestGeneric, TestMetrics

from hypothesis import settings
import sys
import unittest

# Define test cases
# TODO see if there's an easier way to look for these cases (without manually updating a list)
test_cases = [
    TestGeneric,
    TestMetrics
]

# Hypothesis settings
settings.register_profile('lenient', deadline=None)
settings.load_profile('lenient')


# Function to run tests
def test():
    # Create a test suite
    suite = unittest.TestSuite()

    # Load all our test cases into the suite
    loader = unittest.TestLoader()
    for test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(test_case))

    # Create test runner and run
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # If the test was not successful, exit with a code
    if not result.wasSuccessful():
        sys.exit(1)
