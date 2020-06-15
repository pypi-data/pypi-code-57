import unittest
from unittest.mock import patch
import os
from pathlib import Path
from stitch_m import file_handler

base_path = "/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files/"
test_file = base_path + "Fid_T2G3_mosaic.txt"
test_marker_file = base_path + "Fid_T2G3_markers.txt"
bad_file = base_path + "bad_file.txt"

testargs = [test_file, test_marker_file]
bad_testargs = [bad_file, test_marker_file, test_file]

test_config = Path(__file__).resolve().with_name("config.cfg")

class FileCheckerTests(unittest.TestCase):
    @patch('stitch_m.file_handler')
    def test_argument_filtering(self, mocked_file_handler):
        mocked_file_handler.local_config_file.return_value = test_config
        if os.path.exists(base_path):
            for arguments in [testargs, testargs[::-1], bad_testargs]:
                arguments_out = file_handler.argument_organiser(arguments)
                self.assertEqual(arguments_out, testargs)
        else:
            print("Cannot run test without access to dls directories")
