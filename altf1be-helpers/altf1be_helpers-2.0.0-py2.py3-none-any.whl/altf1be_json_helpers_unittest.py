# -*- coding: utf-8 -*-

# Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.
# Licensed under the EUPL License, Version 1.2. See LICENSE in the project root for license information.

import os
import unittest
from altf1be_helpers import AltF1BeJSONHelpers
from datetime import timedelta, datetime


class AltF1BeJSONHelpersTests(unittest.TestCase):

    """ class for running unittests """

    def setUp(self):
        """ Your setUp """

        self.altF1BeJSONHelpers = AltF1BeJSONHelpers()

        self.expected_json_data = '{"name": "altf1be_json_helpers"}'
        self.json_data = self.altF1BeJSONHelpers.load(
            os.path.join(
                "data", "altf1be_sample.json"
            )
        )

    def test_load_json_file(self):
        """ Test the load of a json file

        """

        self.assertEqual(
            self.expected_json_data['name'],
            self.json_data['name']
        )

    def test_save_json_file(self):
        """ Test the storage of a json file

        """

        self.assertEqual(  # TODO implement the test case
            1,
            1
        )

    def test_save_with_datetime_json_file(self):
        """ Test the storage of a json file appended with a date time

        """

        self.assertEqual(  # TODO implement the test case
            1,
            1
        )


suite = unittest.TestLoader().loadTestsFromTestCase(AltF1BeJSONHelpersTests)
unittest.TextTestRunner(verbosity=2).run(suite)
