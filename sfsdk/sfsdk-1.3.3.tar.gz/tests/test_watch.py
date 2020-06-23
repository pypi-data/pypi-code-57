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
from sfsdk import cli, containers, log, imgsettings, techsettings
import tempfile
import os
import multiprocessing
import time

base_dir = tempfile.mkdtemp(prefix='sfsdk-tests-') 

# Needed here for the unittest.skip
containers.load()

class TestWatch(unittest.TestCase):

    def setUp(self):

        containers.load()
        imgsettings.load(base_dir)
        techsettings.load(base_dir)

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_watch_container(self):
        cli.img_add(
                name = 'sdktest-watch', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        imgsettings.settings['images']['sdktest-watch']['container']['external_rdp_port'] = '19999'
        imgsettings.settings['images']['sdktest-watch']['container']['external_http_port'] = '19998'

        cli.img_build(
                name = 'sdktest-watch',
                source= 'default',
                skip_base_img = False
                )
        cli.img_run(
                name = 'sdktest-watch',
                force = True
                )

        # Can't use cli.img_watch here because it doesn't exit
        cli.containers.watch_container('sdktest-watch-inst')
        _, output = cli.containers.exec_on_container(
                'sdktest-watch-inst',  
                """sh -c "touch /home/sf/test && sleep 2 && cat /tmp/sfsdkwatch.json | jq -r '.[0]'" """)
        self.assertEqual(output, "/home/sf/test")

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_img_watch(self):
        cli.img_add(
                name = 'sdktest-watch', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        imgsettings.settings['images']['sdktest-watch']['container']['external_rdp_port'] = '19999'
        imgsettings.settings['images']['sdktest-watch']['container']['external_http_port'] = '19998'

        cli.img_build(
                name = 'sdktest-watch',
                source= 'default',
                skip_base_img = False
                )
        cli.img_run(
                name = 'sdktest-watch',
                force = True
                )

        # Prepare the container to reduce waiting time
        exit_code, output = cli.containers.exec_on_container( 
                'sdktest-watch-inst',  
                "sh -c \
                'apt-get update && \
                apt-get install -y python-watchdog'")
        self.assertEqual(exit_code, 0)

        # Run watch
        p = multiprocessing.Process(target=cli.img_watch, args=('sdktest-watch','/home/sf', 10))
        p.start()

        time.sleep(5)
        
        exit_code, output = cli.containers.exec_on_container(
                'sdktest-watch-inst',  
                """sh -c "touch /home/sf/test" """)

        time.sleep(10)

        with open(os.path.join(imgsettings.settings['images']['sdktest-watch']['build_dir'], '.sfsdk-watch.txt'), 'r') as stream:
            self.assertEqual(stream.read(), "/home/sf/test")

        p.join()

    def tearDown(self):

        imgsettings.remove_image('sdktest-watch', force = True)

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
