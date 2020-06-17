""" Test request for range creation"""


import os
import unittest
from ...libs.core.read_file import read_file
from ...libs.core.parse_add_range_evcs import check_consistency_single_evc
from ...libs.core.parse_add_range_evcs import create_evcs_from_range
from ...libs.core.parse_add_range_evcs import process_add_range


CONTENT_FILE_PATH = "./tests/test_units/content_files/"


class TestCheckConsistency(unittest.TestCase):
    """ Test Consistency """

    def setUp(self):
        """ Set up environment """
        os.environ["EVC_MANAGER_VERBOSITY"] = "info"
        self.source_file = CONTENT_FILE_PATH + "add_evc_range_request.yaml"
        self.request = read_file(source_file=self.source_file)

    def test_read_source_file(self):
        """ Check if file was read """
        self.assertIsInstance(self.request, dict)

    def test_check_consistency_correct_evcs(self):
        """ Check consistency of each EVC in the file """
        check_consistency_single_evc(self.request["evcs"][0])
        check_consistency_single_evc(self.request["evcs"][1])

    def test_check_consistency_incorrect_evcs(self):
        """ Raise ValueError for incorrect EVCs """
        with self.assertRaises(ValueError):
            for i in range(1, 3):
                check_consistency_single_evc(self.request["evcs"][i])


class TestCreateEVCsFromRange(unittest.TestCase):
    """ Test if we can create EVCs with VLAN range """

    def setUp(self):
        """ Set up environment """
        os.environ["EVC_MANAGER_VERBOSITY"] = "info"
        self.source_file = CONTENT_FILE_PATH + "add_evc_range_request.yaml"
        self.request = read_file(source_file=self.source_file)

    def test_read_source_file(self):
        """ TestCreateEVCsFromRange """
        create_evcs_from_range(self.request["evcs"][0])
        create_evcs_from_range(self.request["evcs"][1])


class TestCreateAllEVCsFromRange(unittest.TestCase):
    """ TestCreateAllEVCsFromRange """

    def setUp(self):
        """ Set up environment """
        os.environ["EVC_MANAGER_VERBOSITY"] = "info"
        self.source_file = CONTENT_FILE_PATH + "add_evc_range_request.yaml"
        self.request = read_file(source_file=self.source_file)

    def test_read_source_file(self):
        """ TestCreateAllEVCsFromRange """
        process_add_range(self.request["evcs"][0:2])


if __name__ == '__main__':
    unittest.main()
