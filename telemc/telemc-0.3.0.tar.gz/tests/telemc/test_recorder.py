import os
import tempfile
import time
import unittest
from queue import Queue

from telemc.recorder import TelemetryRecorder, TelemetryFileRecorder
from tests.testutil import RedisResource


class TelemetryRecorderTest(unittest.TestCase):
    redis = RedisResource()

    def setUp(self) -> None:
        self.redis.setUp()

    def tearDown(self) -> None:
        self.redis.tearDown()

    def test_recorder(self):
        queue = Queue()

        class TestTelemetryRecorder(TelemetryRecorder):
            def _record(self, t):
                queue.put(t)

        recorder = TestTelemetryRecorder(self.redis.rds)
        recorder.start()

        self.redis.rds.publish('telem/unittest/cpu', '1001 41')
        self.redis.rds.publish('telem/unittest/cpu', '1002 42')

        telemetry = queue.get(timeout=2)
        self.assertEqual('1001', telemetry.timestamp)
        self.assertEqual('cpu', telemetry.metric)
        self.assertEqual('unittest', telemetry.node)
        self.assertEqual('41', telemetry.value)

        telemetry = queue.get(timeout=2)
        self.assertEqual('1002', telemetry.timestamp)
        self.assertEqual('cpu', telemetry.metric)
        self.assertEqual('unittest', telemetry.node)
        self.assertEqual('42', telemetry.value)

        recorder.stop(timeout=2)


class TelemetryFileRecorderTest(unittest.TestCase):
    redis = RedisResource()

    def setUp(self) -> None:
        self.redis.setUp()
        self.tmp = tempfile.mktemp(prefix='telemc', suffix='.csv')

    def tearDown(self) -> None:
        self.redis.tearDown()
        os.remove(self.tmp)

    def test_file_recorder(self):
        recorder = TelemetryFileRecorder(self.redis.rds, self.tmp, flush_every=1)
        recorder.start()

        time.sleep(1)  # wait for subscriber to start (takes a while to open the file)

        self.redis.rds.publish('telem/unittest/cpu', '1001 41')
        self.redis.rds.publish('telem/unittest/cpu', '1002 42')
        self.redis.rds.publish('telem/unittest/cpu', '1003 43')

        recorder.stop(timeout=2)

        with open(self.tmp) as fd:
            lines = fd.readlines()

        self.assertEqual('1001,41,unittest,cpu,\n', lines[0])
        self.assertEqual('1002,42,unittest,cpu,\n', lines[1])
        self.assertEqual('1003,43,unittest,cpu,\n', lines[2])
        self.assertEqual(3, len(lines))
