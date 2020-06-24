import unittest
import logging
import io
import os
import sys
import re
import shutil
import threading
import time
import yaml
from tempfile import gettempdir
import requests
from gitbuilding.__main__ import main
from checklogs import no_logs

class MainArgsTestCase(unittest.TestCase):
    """
    Test case for simple arguments into main.
    """
    def setUp(self):
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_no_args(self):
        main([])
        self.assertEqual(self.stdout.getvalue(), 'Invalid gitbuilding command None\n')

    def test_bad_args(self):
        with self.assertRaises(SystemExit):
            main(['foo'])

    def test_version(self):
        main(['--version'])
        self.assertIsNotNone(re.match(r'^[0-9]+\.[0-9]+\.[0-9]+(?:\.dev[0-9]+)?$',
                                      self.stdout.getvalue()))

class RunMainTestCase(unittest.TestCase):
    """
    Test case running main and checking there are no errors.
    This probably creates a lot of weak coverage that needs to be tested
    again, but is important to check that the core functions run without
    errors.
    """

    @no_logs('BuildUp')
    def test_example_build(self):
        """
        Check build with no logs for `gitbuilding new` project
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestBuild')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        main(['build'])

    def test_example_build_missing_dict(self):
        """
        Rename the dictionary. Should warn but not error.
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestBuild_missing_dict')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        os.rename('Parts.yaml', 'Prts.yaml')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    def test_example_build_missing_step(self):
        """
        Rename a step. Should warn but not error.
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestBuild_missing_step')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        os.rename('testpage2.md', 'testpage3.md')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    def test_example_build_invalid_yaml(self):
        """
        Rename a step. Should warn but not error.
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestBuild_invalid_yaml')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        with open('buildconf.yaml', 'w') as yml:
            yml.write('asdas: ? asd?')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    def test_example_build_invalid_data_in_yaml(self):
        """
        Rename a step. Should warn but not error.
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestBuild_invalid_data_in_yaml')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        with open('buildconf.yaml', 'a') as yml:
            yml.write('CustomCategories:\n  CatName: stuff')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            main(['build'])

    @no_logs('BuildUp')
    def test_example_build_html(self):
        """
        Check build HTML site with no logs for `gitbuilding new` project
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestHTML')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        main(['build-html'])

    @no_logs('BuildUp')
    def test_example_serve(self):
        """
        Check serve with no logs for `gitbuilding new` project, but errors when
        starting a second server.
        """
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestServe')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        t_server = threading.Thread(name='Server', target=main, args=(['serve'],))
        t_server.setDaemon(True)
        t_server.start()
        time.sleep(2)
        requests.get('http://localhost:6178')
        with self.assertRaises(Exception):
            # Test that we can't start a second server because the first one is running
            main(['serve'])
