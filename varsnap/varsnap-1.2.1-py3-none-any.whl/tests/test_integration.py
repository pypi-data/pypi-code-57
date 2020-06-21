import os
import unittest

from varsnap import assert_generator, core
from typing import Callable, List


def generate_reference_function() -> Callable[[int, int], int]:
    def example(x: int, y: int) -> int:
        return x * y
    example.__qualname__ = 'example'
    return example


def generate_test_function() -> Callable[[int, int], int]:
    def example(x: int, y: int) -> int:
        return x * y + 1
    example.__qualname__ = 'example'
    return example


def set_producer() -> None:
    os.environ[core.ENV_VARSNAP] = 'true'
    os.environ[core.ENV_ENV] = 'production'
    os.environ[core.ENV_PRODUCER_TOKEN] = 'producer-umakrqit4l021plfg75q'
    os.environ[core.ENV_CONSUMER_TOKEN] = ''


def set_consumer() -> None:
    os.environ[core.ENV_VARSNAP] = 'true'
    os.environ[core.ENV_ENV] = 'development'
    os.environ[core.ENV_PRODUCER_TOKEN] = ''
    os.environ[core.ENV_CONSUMER_TOKEN] = 'consumer-tz1ffce4u9lepxjamw6b'


def reset() -> None:
    core.PRODUCERS = []
    core.CONSUMERS = []


class TestTest(unittest.TestCase):
    def test_generate_reference_function(self) -> None:
        f = generate_reference_function()
        self.assertEqual(f(2, 3), 6)
        self.assertEqual(f(4, 5), 20)
        self.assertEqual(f(6, 7), 42)

    def test_generate_test_function(self) -> None:
        f = generate_test_function()
        self.assertEqual(f(2, 3), 7)
        self.assertEqual(f(4, 5), 21)
        self.assertEqual(f(6, 7), 43)

    def test_comparison(self) -> None:
        f1 = generate_reference_function()
        f2 = generate_test_function()
        self.assertNotEqual(f1(2, 3), f2(2, 3))
        self.assertNotEqual(f1(4, 5), f2(4, 5))
        self.assertNotEqual(f1(6, 7), f2(6, 7))
        self.assertEqual(core.get_signature(f1), core.get_signature(f2))


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        reset()

    def assert_in_line(self, strings: List[str], content: str) -> None:
        lines = content.split("\n")
        for snippet in strings:
            lines = [c for c in lines if snippet in c]
        self.assertTrue(
            len(lines) > 0,
            '"%s" is not in "%s"' % (str(strings), content)
        )

    def test_produce_consume(self) -> None:
        f = core.varsnap(generate_reference_function())
        set_producer()
        f(2, 3)
        f(4, 5)
        f(6, 7)
        set_consumer()
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches)
        self.assertEqual(all_logs, '')

    def test_produce_consume_fail(self) -> None:
        f = core.varsnap(generate_reference_function())
        set_producer()
        f(2, 3)
        f(4, 5)
        f(6, 7)
        reset()
        set_consumer()
        f = core.varsnap(generate_test_function())
        all_matches, all_logs = assert_generator.test()
        self.assertFalse(all_matches)
        self.assert_in_line(['Report URL', 'www.varsnap.com'], all_logs)
        self.assert_in_line(['Function:', 'example'], all_logs)
        self.assert_in_line(['Function input args:', '(2, 3)'], all_logs)
        self.assert_in_line(['kwargs', '{}'], all_logs)
        self.assert_in_line(['Production function outputs', '6'], all_logs)
        self.assert_in_line(['Your function outputs', '7'], all_logs)
        self.assert_in_line(['Matching outputs:', 'False'], all_logs)
