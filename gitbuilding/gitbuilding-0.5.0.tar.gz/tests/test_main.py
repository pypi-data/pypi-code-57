import unittest
import io
import os
import sys
import re
import shutil
import threading
import time
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
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestBuild')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        main(['build'])

    @no_logs('BuildUp')
    def test_example_build_html(self):
        temp_dir = os.path.join(gettempdir(), 'GB_ExampleTestHTML')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)
        main(['new'])
        main(['build-html'])

    @no_logs('BuildUp')
    def test_example_serve(self):
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
