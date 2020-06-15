import unittest
from unittest.mock import patch
import os
import tifffile as tf
import numpy as np
from pathlib import Path

import stitch_m
from stitch_m import file_handler

base_path = "/dls/science/groups/das/ExampleData/B24_test_data/StitchM_test_data/files/"
test_files = (base_path + "B15Grid2.txt", base_path + "B8G1-IR_mosaic.txt", base_path + "B8G2-IR_mosaic.txt", base_path + "Fid_T2G3_mosaic.txt", base_path + "Yo10_G3_mosaic.txt")
test_marker_files = (base_path + "B15_location_markers.txt", base_path + "B8G1-IR_markers.txt", base_path + "B8G2-IR_markers.txt", base_path + "Fid_T2G3_markers.txt", base_path + "Yo10_G3_mosaic_MARKERS.txt")
# # Reduced tuple for quick tests:
# test_files = (base_path + "Fid_T2G3_mosaic.txt",)
# test_marker_files = (base_path + "Fid_T2G3_markers.txt",)

expected_outputs = [path.replace(".txt", "_expected_output.ome.tiff") for path in test_files]
expected_marked_outputs = [path.replace(".txt", "_expected_output_marked.ome.tiff") for path in test_files]
test_config = Path(__file__).resolve().with_name("config.cfg")


class StitchMTests(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        for file in test_files:
            output_path = file.replace('.txt', '.ome.tiff')
            if os.path.isfile(output_path):
                os.remove(output_path)
            output_path = file.replace('.txt', '_marked.ome.tiff')
            if os.path.isfile(output_path):
                os.remove(output_path)

    @patch('stitch_m.file_handler')
    def test_end_to_end_simple(self, mocked_file_handler):
        mocked_file_handler.local_config_file.return_value = test_config
        if os.path.exists(base_path):
            for i in range(len(test_files)):
                test_file = test_files[i]
                stitch_m.stitch_and_save(test_file)
                output_path = test_file.replace('.txt', '.ome.tiff')
                self.assertTrue(os.path.isfile(output_path), msg=f"{output_path} not found")
                output_image = tf.imread(output_path)

                expected_file = expected_outputs[i]
                expected_image = tf.imread(expected_file)

                self.assertTrue((output_image == expected_image).all(), msg=f"Not true for {test_file}")
        else:
            print("Cannot run test without access to dls directories")

    @patch('stitch_m.file_handler')
    def test_end2end_with_markers(self, mocked_file_handler):
        mocked_file_handler.local_config_file.return_value = test_config
        if os.path.exists(base_path):
            for i in range(len(test_files)):
                test_file = test_files[i]
                stitch_m.stitch_and_save(test_file, test_marker_files[i])
                output_path = test_file.replace('.txt', '_marked.ome.tiff')
                self.assertTrue(os.path.isfile(output_path), msg=f"{output_path} not found")
                output_image = np.asarray(tf.imread(output_path))

                expected_file = expected_marked_outputs[i]
                expected_image = np.asarray(tf.imread(expected_file))

                self.assertTrue((output_image == expected_image).all(), msg=f"Not true for {test_file}")
        else:
            print("Cannot run test without access to dls directories")

