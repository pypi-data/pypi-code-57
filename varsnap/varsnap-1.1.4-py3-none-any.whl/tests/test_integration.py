import os
import unittest

from varsnap import assert_generator, core


def generate_reference_function():
    def example(x, y):
        return x * y
    example.__qualname__ = 'example'
    return example


def generate_test_function():
    def example(x, y):
        return x * y + 1
    example.__qualname__ = 'example'
    return example


def set_producer():
    os.environ[core.ENV_VARSNAP] = 'true'
    os.environ[core.ENV_ENV] = 'production'
    os.environ[core.ENV_PRODUCER_TOKEN] = 'producer-umakrqit4l021plfg75q'
    os.environ[core.ENV_CONSUMER_TOKEN] = ''


def set_consumer():
    os.environ[core.ENV_VARSNAP] = 'true'
    os.environ[core.ENV_ENV] = 'development'
    os.environ[core.ENV_PRODUCER_TOKEN] = ''
    os.environ[core.ENV_CONSUMER_TOKEN] = 'consumer-tz1ffce4u9lepxjamw6b'


def reset():
    core.PRODUCERS = []
    core.CONSUMERS = []


class TestTest(unittest.TestCase):
    def test_generate_reference_function(self):
        f = generate_reference_function()
        self.assertEqual(f(2, 3), 6)
        self.assertEqual(f(4, 5), 20)
        self.assertEqual(f(6, 7), 42)

    def test_generate_test_function(self):
        f = generate_test_function()
        self.assertEqual(f(2, 3), 7)
        self.assertEqual(f(4, 5), 21)
        self.assertEqual(f(6, 7), 43)

    def test_comparison(self):
        f1 = generate_reference_function()
        f2 = generate_test_function()
        self.assertNotEqual(f1(2, 3), f2(2, 3))
        self.assertNotEqual(f1(4, 5), f2(4, 5))
        self.assertNotEqual(f1(6, 7), f2(6, 7))
        self.assertEqual(core.get_signature(f1), core.get_signature(f2))


class TestIntegration(unittest.TestCase):
    def setUp(self):
        reset()

    def test_produce_consume(self):
        f = core.varsnap(generate_reference_function())
        set_producer()
        f(2, 3)
        f(4, 5)
        f(6, 7)
        set_consumer()
        overall_result, results = assert_generator.test()
        self.assertTrue(overall_result)
        for result in results:
            self.assertTrue(result[0])

    def test_produce_consume_fail(self):
        f = core.varsnap(generate_reference_function())
        set_producer()
        f(2, 3)
        f(4, 5)
        f(6, 7)
        reset()
        set_consumer()
        f = core.varsnap(generate_test_function())
        overall_result, results = assert_generator.test()
        for result in results:
            self.assertFalse(result[0])
        self.assertFalse(overall_result)
