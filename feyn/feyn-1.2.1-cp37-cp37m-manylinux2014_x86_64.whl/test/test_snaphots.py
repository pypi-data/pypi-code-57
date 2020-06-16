import unittest
from unittest.mock import ANY
from datetime import datetime

from feyn import QLattice


class TestSnapshots(unittest.TestCase):
    def setUp(self):
        self.lt = QLattice()
        self.lt.reset()

    # TODO: Remember docstrings for the snapshot features
    # TODO: Finish your project about auto-checking for docstrings during a release
    def test_can_capture_a_snapshot(self):
        snapshot_info = self.lt.snapshots.capture("My lovely QLattice")

        self.assertEqual(snapshot_info.id, ANY)
        self.assertAlmostEqual(snapshot_info.when.timestamp(), datetime.now().timestamp(), places=-1)
        self.assertEqual(snapshot_info.note, "My lovely QLattice")

    def test_can_list_snapshots(self):
        self.lt.snapshots.capture("Snapshot #1")
        self.lt.snapshots.capture("Snapshot #2")
        self.lt.snapshots.capture("Snapshot #3")

        with self.subTest("Should have three snapshots"):
            self.assertGreater(len(self.lt.snapshots), 2)

        with self.subTest("should be ordered with most recent last"):
            self.assertEqual(self.lt.snapshots[-1].note, "Snapshot #3")

        print(self.lt.snapshots)

    def test_can_restore_snapshot(self):
        # Side-effect that adds these 3 registers
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")
        
        snapshot = self.lt.snapshots.capture("testing")
        with self.subTest("Can restore with snapshot instance"):
            self.lt.reset()
            self.assertEqual(len(self.lt.registers),0)

            self.lt.snapshots.restore(snapshot)
            self.assertEqual(len(self.lt.registers),3)

        with self.subTest("Can restore with snapshot id"):
            self.lt.reset()
            self.assertEqual(len(self.lt.registers),0)

            self.lt.snapshots.restore(snapshot.id)
            self.assertEqual(len(self.lt.registers),3)
