import sys
import unittest
from unittest.mock import patch, MagicMock, ANY

import stitch_m


class TestPackageFunctions(unittest.TestCase):
    @patch('stitch_m.run.main_run')
    def test_module_stitch_and_save_method(self, stitch_m_run):
        args = ["path_to/mosaic.txt", None]
        stitch_m.stitch_and_save(args[0])
        stitch_m_run.assert_called_once_with(ANY, *args)

    @patch('stitch_m.run.main_run')
    def test_module_stitch_and_save_method_with_marker_file(self, stitch_m_run):
        args = ["path_to/mosaic.txt", "path_to/markers.txt"]
        stitch_m.stitch_and_save(*args)
        stitch_m_run.assert_called_once_with(ANY, *args)
