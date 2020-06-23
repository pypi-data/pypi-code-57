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
from sfsdk import imgsettings, techsettings
import multiprocessing
import time
import tempfile
import os

base_dir = tempfile.mkdtemp(prefix='sfsdk-tests-') 

# Needed here for the unittest.skip
containers.load()

class TestSnapshot(unittest.TestCase):

    def setUp(self):
        containers.load()
        imgsettings.load(base_dir)
        techsettings.load(base_dir)

    def test_non_existent(self):

        self.assertRaises(log.FatalMsg, cli.img_snapshot, 
                name = 'non-existent', 
                new_name = 'non-existent-snapshot',
                force = True,
            )

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_snapshot_with_paths(self):

        cli.img_add(
                name = 'sdktestsnapshot', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        imgsettings.settings['images']['sdktestsnapshot']['container']['external_rdp_port'] = '19999'
        imgsettings.settings['images']['sdktestsnapshot']['container']['external_http_port'] = '19998'

        cli.img_build(
                name = 'sdktestsnapshot',
                source= 'default',
                skip_base_img = False
                )
        cli.img_run(
                name = 'sdktestsnapshot',
                force = True
                )

        _, _ = cli.containers.exec_on_container(
                'sdktestsnapshot-inst',  
                """sh -c "mkdir -p /home/sf/exercise/app/ /home/sf/exercise/.metadata/ && touch /home/sf/test /home/sf/exercise/app/test1 /home/sf/exercise/.metadata/test2" """)

        with open(os.path.join(imgsettings.settings['images']['sdktestsnapshot']['build_dir'], '.sfsdk-watch.txt'), 'w+') as stream:
                stream.write("/home/sf/test\n/home/sf/exercise/.metadata/test2")

        cli.img_snapshot(
                name = 'sdktestsnapshot',
                new_name = 'sdktest4',
                force = True,
                )
        cli.img_build(
                name = 'sdktest4',
                source= 'default',
                skip_base_img = False
                )
        cli.img_stop(
                names = [ 'sdktestsnapshot' ],
                )
        cli.img_rm(
                names = [ 'sdktestsnapshot' ],
                force = True
                )

        with open(os.path.join(imgsettings.settings['images']['sdktest4']['build_dir'], 'fs/home/sf/test'), 'r') as stream:
            self.assertEqual(stream.read(), "")

        with open(os.path.join(imgsettings.settings['images']['sdktest4']['build_dir'], 'app/test1'), 'r') as stream:
            self.assertEqual(stream.read(), "")

        with open(os.path.join(imgsettings.settings['images']['sdktest4']['build_dir'], 'fs/home/sf/exercise/.metadata/test2'), 'r') as stream:
            self.assertEqual(stream.read(), "")

        cli.img_build(
                name = 'sdktest4',
                source= 'default',
                skip_base_img = False
                )

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_snapshot_without_newname(self):

        # TODO: removing this shouldn't be necessary
        cli.img_rm(
                names = [ 'sdktestsnapshot' ],
                force = True
                )

        cli.img_add(
                name = 'sdktestsnapshot', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        imgsettings.settings['images']['sdktestsnapshot']['container']['external_rdp_port'] = '19999'
        imgsettings.settings['images']['sdktestsnapshot']['container']['external_http_port'] = '19998'

        cli.img_build(
                name = 'sdktestsnapshot',
                source= 'default',
                skip_base_img = False
                )
        cli.img_run(
                name = 'sdktestsnapshot',
                force = True
                )
        cli.img_snapshot(
                name = 'sdktestsnapshot',
                new_name = None,
                force = True,
                )

        imgsettings.load(base_dir)

        self.assertTrue(imgsettings.settings['images']['sdktestsnapshot-v1'])

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_snapshot_with_versioned_newname(self):
        cli.img_add(
                name = 'sdktestsnapshot', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        imgsettings.settings['images']['sdktestsnapshot']['container']['external_rdp_port'] = '19999'
        imgsettings.settings['images']['sdktestsnapshot']['container']['external_http_port'] = '19998'

        cli.img_build(
                name = 'sdktestsnapshot',
                source= 'default',
                skip_base_img = False
                )
        cli.img_run(
                name = 'sdktestsnapshot',
                force = True
                )
        cli.img_snapshot(
                name = 'sdktestsnapshot',
                new_name = None,
                force = True,
                )

        self.assertTrue(imgsettings.settings['images']['sdktestsnapshot-v1'])

        cli.img_snapshot(
                name = 'sdktestsnapshot',
                new_name = None,
                force = True,
                )

        self.assertTrue(imgsettings.settings['images']['sdktestsnapshot-v2'])

        cli.img_snapshot(
                name = 'sdktestsnapshot',
                new_name = None,
                force = True,
                )

        self.assertTrue(imgsettings.settings['images']['sdktestsnapshot-v3'])

    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_snapshot(self):

        cli.img_add(
                name = 'sdktestsnapshot', 
                from_img = 'sf-python', 
                build_dir = None, 
                from_dir = None,
                app_dir = None)

        imgsettings.settings['images']['sdktestsnapshot']['container']['external_rdp_port'] = '19999'
        imgsettings.settings['images']['sdktestsnapshot']['container']['external_http_port'] = '19998'

        cli.img_build(
                name = 'sdktestsnapshot',
                source= 'default',
                skip_base_img = False
                )
        cli.img_run(
                name = 'sdktestsnapshot',
                force = True
                )
        cli.img_snapshot(
                name = 'sdktestsnapshot',
                new_name = 'sdktest3',
                force = True,
                )
        cli.img_build(
                name = 'sdktest3',
                source= 'default',
                skip_base_img = False
                )
        cli.img_stop(
                names = [ 'sdktestsnapshot' ],
                )
        cli.img_rm(
                names = [ 'sdktestsnapshot' ],
                force = True
                )



    @unittest.skipUnless(containers.image_exists('sf-python'),
                                 "Image sf-python is required")
    def test_img_watch_and_snapshot(self):
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
                """sh -c "mkdir -p /home/sf/exercise/app/ && touch /home/sf/test /home/sf/exercise/app/test1" """)

        time.sleep(5)

        with open(os.path.join(imgsettings.settings['images']['sdktest-watch']['build_dir'], '.sfsdk-watch.txt'), 'r') as stream:
            self.assertEqual(
                    stream.read(), 
                    "/home/sf/test"
                    )

        cli.img_snapshot(
                name = 'sdktest-watch',
                new_name = 'sdktest-watch-snapshot',
                force = True,
                )

        with open(os.path.join(imgsettings.settings['images']['sdktest-watch-snapshot']['build_dir'], 'fs/home/sf/test'), 'r') as stream:
            self.assertEqual(stream.read(), "")

        with open(os.path.join(imgsettings.settings['images']['sdktest-watch-snapshot']['build_dir'], 'app/test1'), 'r') as stream:
            self.assertEqual(stream.read(), "")

        cli.img_build(
                name = 'sdktest-watch-snapshot',
                source= 'default',
                skip_base_img = False
                )

        p.join()

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
