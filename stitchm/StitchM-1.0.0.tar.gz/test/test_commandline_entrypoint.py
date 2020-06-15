import os
import sys
import unittest
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock, ANY
from subprocess import Popen, PIPE, STDOUT
from time import sleep

import stitch_m
from stitch_m import __version__

from stitch_m.scripts import command_line

class TestEntryPointCommandline(unittest.TestCase):
# Before these running tests, the module must be installed in development mode using:
# `pip install --editable . --user` (from the project folder)
# it can be uninstalled at the end using:
# `pip uninstall StitchM`
# IF TESTING ON WINDOWS: make sure the correct python installation is set as the default in PATH

    @classmethod
    def setUpClass(cls):
        # Set maximum difference string length to None (infinite)
        cls.maxDiff = None
        # Add local intall to path for testing with development install
        if os.name == "posix":
            os.environ["PATH"] += os.pathsep + os.path.join(os.path.expanduser("~"), ".local", "bin")
    
    @patch('argparse.ArgumentParser.print_help')
    def test_command_line_function(self, mocked_printhelp):
        sys.argv = ["StitchM"]
        command_line.cl_run()

        mocked_printhelp.assert_called_once()

    @patch('argparse.ArgumentParser.print_help')
    def test_command_line_function_setup_subpaser(self, mocked_printhelp):
        sys.argv = ["StitchM", "setup"]
        command_line.cl_run()

        mocked_printhelp.assert_called_once()

    @patch('stitch_m.scripts.command_line.create_user_config')
    def test_command_line_function_setup_config(self, mocked_config_creator):
        local_config_file = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stitch_m", "config.cfg"))

        sys.argv = ["StitchM", "setup", "--config"]
        command_line.cl_run()

        mocked_config_creator.assert_called_once()


    @patch('stitch_m.scripts.command_line.create_Windows_shortcut')
    def test_command_line_function_setup_windows_shortcut(self, mocked_shortcut_creator):
        local_config_file = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stitch_m", "config.cfg"))

        sys.argv = ["StitchM", "setup", "-win"]
        command_line.cl_run()

        mocked_shortcut_creator.assert_called_once()

    @patch('stitch_m.scripts.command_line.main_run')
    def test_command_line_function_with_args(self, main_run):
        main_run.return_value = None
        mosaic_arg = "mosaic_path"
        marker_arg = "marker_path"
        sys.argv =["StitchM", "--mosaic", mosaic_arg, "--markers", marker_arg]
        command_line.cl_run()

        main_run.assert_called_once_with(ANY, mosaic_arg, marker_arg)

    def test_command_line_method(self):
        args = ["path_to/mosaic"]
        run_args = ["StitchM", "--mosaic", args[0]]
        with Popen(run_args, text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"Invalid arguments: {args[0]}, None", stdout, msg=f"Actual stdout: {stdout}")

    def test_command_line_method_invalid_path(self):
        args = ["path_to/mosaic.txt"]
        run_args = ["StitchM", "--mosaic", args[0]]
        with Popen(run_args, text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"Mosaic file path cannot be resolved", stdout, msg=f"Actual stdout: {stdout}")

    def test_command_line_method_with_marker_file(self):
        args = ["path_to/mosaic", "path_to/markers"]
        run_args = ["StitchM", "--mosaic", args[0], "--markers", args[1]]
        with Popen(run_args, text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"Invalid arguments: {args[0]}, {args[1]}", stdout, msg=f"Actual stdout: {stdout}")

    def test_command_line_method_version_number(self):
        run_args = ["StitchM", "--version"]
        with Popen(run_args, text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertEqual(f"StitchM {stitch_m.__version__}", stdout, msg=f"Actual stdout: {stdout}")

    def test_command_line_method_setup_subparser(self):
        run_args = ["StitchM", "setup"]
        with Popen(run_args, text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
            sleep(2)
            stdout, _ = p.communicate("pressed key", timeout=5)
        stdout = stdout.strip("\r\n").strip("\n")
        self.assertIn(f"StitchM setup [-win] [-cfg] [-h]", stdout, msg=f"Actual stdout: {stdout}")
