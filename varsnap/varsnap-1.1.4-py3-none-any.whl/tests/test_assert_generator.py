import os
import unittest
from unittest.mock import patch

from varsnap import assert_generator, core


def add(x, y):
    return x + y


null = open(os.devnull, 'w')


class TestResult(unittest.runner.TextTestResult):
    def __init__(self, *args, **kwargs):
        super(TestResult, self).__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super(TestResult, self).addSuccess(test)
        self.successes.append(test)


class TestTest(unittest.TestCase):
    def setUp(self):
        core.CONSUMERS = []

    def tearDown(self):
        core.CONSUMERS = []

    def test_no_consumers(self):
        overall_result, results = assert_generator.test()
        self.assertTrue(overall_result)
        self.assertEqual(results, [])

    @patch('varsnap.core.Consumer.consume')
    def test_consume(self, mock_consume):
        core.Consumer(add)
        mock_consume.return_value = (True, 'abcd')
        overall_result, results = assert_generator.test()
        self.assertTrue(overall_result)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0][0])
        self.assertEqual(results[0][1], 'abcd')

    @patch('varsnap.core.Consumer.consume')
    def test_consume_fail(self, mock_consume):
        core.Consumer(add)
        mock_consume.return_value = (False, 'abcd')
        overall_result, results = assert_generator.test()
        self.assertFalse(overall_result)
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0][0])
        self.assertEqual(results[0][1], 'abcd')


class TestAssertGenerator(unittest.TestCase):
    def setUp(self):
        core.CONSUMERS = []

    def tearDown(self):
        core.CONSUMERS = []

    def run_test_case(self, test_case):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        runner = unittest.TextTestRunner(stream=null, resultclass=TestResult)
        return runner.run(suite)

    @patch('varsnap.core.Consumer.consume')
    def test_generate(self, mock_consume):
        core.Consumer(add)
        mock_consume.return_value = (True, '')
        result = self.run_test_case(assert_generator.TestVarsnap)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.skipped), 0)
        self.assertEqual(len(result.successes), 1)

    @patch('varsnap.core.Consumer.consume')
    def test_generate_failure(self, mock_consume):
        core.Consumer(add)
        mock_consume.return_value = (False, '')
        result = self.run_test_case(assert_generator.TestVarsnap)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(len(result.skipped), 0)
        self.assertEqual(len(result.successes), 0)

    def test_generate_skip(self):
        result = self.run_test_case(assert_generator.TestVarsnap)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.skipped), 1)
        self.assertEqual(len(result.successes), 0)
