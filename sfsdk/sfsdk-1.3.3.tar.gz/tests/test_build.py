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

class TestBuild(unittest.TestCase):

    def setUp(self):
        containers.load()
        imgsettings.load(base_dir)
        techsettings.load(base_dir)

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_build_python(self):
        cli.img_add(
                name = 'sdktestbuildpython', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuildpython',
                source= 'default',
                skip_base_img = False
                )

    @unittest.skipUnless(containers.image_exists('sf-java'),
                                 "Image sf-java is required")
    def test_build_java(self):
        cli.img_add(
                name = 'sdktestbuildjava', 
                from_img = 'sf-java', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuildjava',
                source= 'default',
                skip_base_img = False
                )

        
    @unittest.skipUnless(containers.image_exists('sf-golang'),
                                 "Image sf-golang is required")
    def test_build_golang(self):
        cli.img_add(
                name = 'sdktestbuildgolang', 
                from_img = 'sf-golang', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuildgolang',
                source= 'default',
                skip_base_img = False
                )
        
    @unittest.skipUnless(containers.image_exists('sf-ruby'),
                                 "Image sf-ruby is required")
    def test_build_ruby(self):
        cli.img_add(
                name = 'sdktestbuildruby', 
                from_img = 'sf-ruby', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuildruby',
                source= 'default',
                skip_base_img = False
                )

    @unittest.skipUnless(containers.image_exists('sf-php'),
                                 "Image sf-php is required")
    def test_build_php(self):
        cli.img_add(
                name = 'sdktestbuildphp', 
                from_img = 'sf-php', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuildphp',
                source= 'default',
                skip_base_img = False
                )

    @unittest.skipUnless(containers.image_exists('sf-dotnet'),
                                 "Image sf-dotnet is required")
    def test_build_dotnet(self):
        cli.img_add(
                name = 'sdktestbuilddotnet', 
                from_img = 'sf-dotnet', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuilddotnet',
                source= 'default',
                skip_base_img = False
                )

    @unittest.skipUnless(containers.image_exists('sf-solidity'),
                                 "Image sf-solidity is required")
    def test_build_solidity(self):
        cli.img_add(
                name = 'sdktestbuildsolidity', 
                from_img = 'sf-solidity', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestbuildsolidity',
                source= 'default',
                skip_base_img = False
                )

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
