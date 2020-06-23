#!/usr/bin/env python3
# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import unittest
from sfsdk import cli, containers, log
from sfsdk import imgsettings, techsettings, authsettings
import tempfile
import os

base_dir = tempfile.mkdtemp(prefix='sfsdk-tests-') 
settings_path = os.path.join(
        base_dir,
        'login.yml' 
    )

# Load authsettings from the real folder
auth_base_dir = os.path.expanduser('~/sf')
authsettings.load(auth_base_dir)
authsettings.set_source('developer-test-account')

class TestLogin(unittest.TestCase):

    def setUp(self):
        techsettings.load(base_dir)

    def test_empty(self):

        with open(settings_path, 'w+') as f:
            f.truncate()
        self.assertRaises(log.FatalMsg, authsettings.load, base_dir)

    def test_empty_json(self):

        with open(settings_path, 'w+') as f:
            f.write('{}')

        self.assertRaises(log.FatalMsg, authsettings.load, base_dir)

    @unittest.skipUnless(authsettings.settings.get('sources', {}).get('developer-test-account'),
                                 "No developer-test-account creds in login.yml")
    def test_developer_login(self):
        cli.img_techs('developer-test-account')

    @unittest.skipUnless(authsettings.settings.get('sources', {}).get('deployment-test-account'),
                                 "No deployment creds in login.yml")
    def test_admin_login(self):
        cli.img_techs('deployment-test-account')


if __name__ == '__main__':
    unittest.main()
