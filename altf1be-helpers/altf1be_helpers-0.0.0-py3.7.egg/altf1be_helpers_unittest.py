# -*- coding: utf-8 -*-

# Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.
# Licensed under the EUPL License, Version 1.2. See LICENSE in the project root for license information.

import os
import unittest
from altf1be_helpers import AltF1BeHelpers
from datetime import timedelta, datetime


class AltF1BeHelpersTests(unittest.TestCase):

    """ class for running unittests """

    def setUp(self):
        """ Your setUp """

        self.expected_unicode_to_ascii = "ee a iii ou &e(SSe!caaQwxs $ u `"
        self.unicode_to_ascii = AltF1BeHelpers.unicode_to_ascii(
            "éè à iïî où &é'(§è!çàaQwxs $ µ `"
        )

        self.expected_is_interactive = False
        self.is_interactive = AltF1BeHelpers.is_interactive()

        self.expected_range_of_dates = [
            datetime.now() + timedelta(0),
            datetime.now() + timedelta(1)
        ]
        self.range_of_dates = AltF1BeHelpers.daterange(
            datetime.now() - timedelta(2),
            datetime.now() - timedelta(0)
        )

        self.expected_url_without_secrets = "/data/2.5/uvi/history?appid=HIDDEN_DATA&lat=lat&lon=lon&cnt=cnt&start=start_date&end=end_date"
        self.url_without_secrets = AltF1BeHelpers.hide_secrets_from_url(
            url="/data/2.5/uvi/history?appid=a_secret_api_key&lat=lat&lon=lon&cnt=cnt&start=start_date&end=end_date"
        )

    def test_unicode_to_ascii(self):
        """test the conversion from unicode to ascii

        """

        self.assertEqual(self.expected_unicode_to_ascii, self.unicode_to_ascii)

    def test_is_interactive(self):
        """ Test if the current environment is interactive"""

        self.assertEqual(
            self.expected_is_interactive,
            self.is_interactive
        )

    # def test_range_of_dates(self):
    #     """ Test if the range of dates contains 2 dates: today and yesterday"""

    #     for index, element in enumerate(self.range_of_dates):
    #         self.assertEqual(
    #             self.expected_range_of_dates[index].strftime("%Y-%m-%d"),
    #             self.range_of_dates[index].strftime("%Y-%m-%d")
    #         )

    def test_url_without_secrets(self):
        """ Test that the the country_iso_set is equal to what is expected"""

        self.assertEqual(
            self.expected_url_without_secrets,
            self.url_without_secrets
        )


suite = unittest.TestLoader().loadTestsFromTestCase(AltF1BeHelpersTests)
unittest.TextTestRunner(verbosity=2).run(suite)
