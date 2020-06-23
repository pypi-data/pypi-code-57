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
from sfsdk import imgsettings, techsettings
from sfsdk import cli, containers, log
import tempfile
import os

base_dir = tempfile.mkdtemp(prefix='sfsdk-tests-')

# Needed here for the unittest.skip
containers.load()

class TestAdd(unittest.TestCase):

    def setUp(self):
        containers.load()
        imgsettings.load(base_dir)
        techsettings.load(base_dir)

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_duplicate(self):
        cli.img_add(
                name = 'sdktestadd', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        
        self.assertRaises(log.FatalMsg, cli.img_add, 
                name = 'sdktestadd', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None
            )

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_app_dir(self):

        app_dir = os.path.join(base_dir, 'test-app-dir')
        app_file = os.path.join(app_dir, 'file.java')
        os.makedirs(app_dir)

        with open(app_file, 'w+') as stream:
            stream.write('1')
        
        cli.img_add(
                name = 'sdktestadd-app-dir', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = app_dir)

        with open(os.path.join(imgsettings.settings['images']['sdktestadd-app-dir']['build_dir'], 'app', 'file.java'), 'r') as stream:
            self.assertEqual(stream.read(), "1")

    def tearDown(self):

        for container in containers.dockerc.containers.list(all=True):
            if container.name.startswith('sdktest'):
                container.remove(force=True)

        for img in containers.dockerc.images.list():
            for tag in img.tags:
                if tag.startswith('sdktest'):
                    containers.dockerc.images.remove(tag, force=True)

        containers.dockerc.close()

if __name__ == '__main__':
    unittest.main()
