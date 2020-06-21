import os
import unittest
from unittest.mock import MagicMock, patch

from typing import Any, List

from varsnap import assert_generator, core


def add(x: int, y: int) -> int:
    return x + y


null = open(os.devnull, 'w')


class TestResult(unittest.runner.TextTestResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TestResult, self).__init__(*args, **kwargs)
        self.successes: List[Any] = []

    def addSuccess(self, test: Any) -> None:
        super(TestResult, self).addSuccess(test)
        self.successes.append(test)


class TestTest(unittest.TestCase):
    def setUp(self) -> None:
        core.CONSUMERS = []

    def tearDown(self) -> None:
        core.CONSUMERS = []

    def test_no_consumers(self) -> None:
        all_matches, all_logs = assert_generator.test()
        self.assertEqual(all_matches, None)
        self.assertEqual(all_logs, "")

    @patch('varsnap.core.Consumer.consume')
    def test_consume(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = True
        mock_consume.return_value = [trial]
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches)
        self.assertEqual(all_logs, '')

    @patch('varsnap.core.Consumer.consume')
    def test_consume_fail(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = False
        trial.report = 'abcd'
        mock_consume.return_value = [trial]
        all_matches, all_logs = assert_generator.test()
        self.assertFalse(all_matches)
        self.assertEqual(all_logs, 'abcd')


class TestAssertGenerator(unittest.TestCase):
    def setUp(self) -> None:
        core.CONSUMERS = []

    def tearDown(self) -> None:
        core.CONSUMERS = []

    def run_test_case(self, test_case: Any) -> Any:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        runner = unittest.TextTestRunner(stream=null, resultclass=TestResult)
        return runner.run(suite)

    @patch('varsnap.core.Consumer.consume')
    def test_generate(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = True
        mock_consume.return_value = [trial]
        result = self.run_test_case(assert_generator.TestVarsnap)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.skipped), 0)
        self.assertEqual(len(result.successes), 1)

    @patch('varsnap.core.Consumer.consume')
    def test_generate_failure(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = False
        mock_consume.return_value = [trial]
        result = self.run_test_case(assert_generator.TestVarsnap)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(len(result.skipped), 0)
        self.assertEqual(len(result.successes), 0)

    def test_generate_skip(self) -> None:
        result = self.run_test_case(assert_generator.TestVarsnap)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(len(result.skipped), 1)
        self.assertEqual(len(result.successes), 0)
