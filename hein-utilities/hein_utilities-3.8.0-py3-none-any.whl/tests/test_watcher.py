"""unit tests for Watcher class"""
import unittest
import os
from hein_utilities.files import Watcher


class TestWatcher(unittest.TestCase):
    def test_patterns(self):
        watch = Watcher(
            os.getcwd(),
            '.py',
            exclude_subfolders=['dist', 'build'],
        )
        self.assertNotEqual(
            len(watch),
            0,
        )

        # update partial match
        watch.watchfor = 'watcher.py'
        self.assertNotEqual(
            len(watch),
            0
        )
        # switch to exact matching (there should be no matches now)
        watch.match_exact = True
        self.assertEqual(
            len(watch),
            0
        )

        # update watch for to match exact file
        watch.watchfor = 'test_watcher.py'
        self.assertEqual(
            len(watch),
            1
        )
