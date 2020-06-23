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
import yaml
import tempfile
import os

base_dir = tempfile.mkdtemp(prefix='sfsdk-tests-')

# Needed here for the unittest.skip
containers.load()

class TestRun(unittest.TestCase):

    def setUp(self):
        imgsettings.load(base_dir)
        techsettings.load(base_dir)

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_run_new_no_force(self):
        cli.img_add(
                name = 'sdktestrunpython', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        cli.img_build(
                name = 'sdktestrunpython',
                source= 'default',
                skip_base_img = False
                )

        try:
            cli.img_run(
                    name = 'sdktestrunpython',
                    force = False
                    )
        except log.FatalMsg:
            self.fail("Unexpected Exception")


# TODO: fix this
    # @unittest.skipUnless(containers.image_exists('sf-python'),
    #                              "Image sf-python is required")
    # def test_run_with_environment(self):
    #     cli.img_add(
    #             name = 'sdktestrunpython2', 
    #             from_img = 'sf-python', 
    #             build_dir = None, 
    #             from_dir = None,
    #             app_dir = None)

    #     settings = {}
    #     with open(os.path.join(base_dir, 'images.yml'), 'r') as yaml_file:
    #         settings = yaml.safe_load(yaml_file)

    #     settings['images']['sdktestrunpython2']['container']['environment']['SSH_KEY'] = 'bogus'

    #     with open(os.path.join(base_dir, 'images.yml'), 'w') as yaml_file:
    #         yaml.dump(settings, yaml_file)

    #     cli.img_build(
    #             name = 'sdktestrunpython2',
    #             source= 'default',
    #             skip_base_img = False
    #             )

    #     try:
    #         cli.img_run(
    #                 name = 'sdktestrunpython2',
    #                 force = False
    #                 )
    #     except log.FatalMsg:
    #         self.fail("Unexpected Exception")

    #     _, output = cli.containers.exec_on_container(
    #             'sdktestrunpython2-inst',  
    #             """sh -c "$SSH_KEY" """)
    #     self.assertEqual(output, "bogus")

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
