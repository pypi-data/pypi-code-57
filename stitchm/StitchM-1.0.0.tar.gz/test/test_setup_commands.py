import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY
import subprocess

from stitch_m.file_handler import create_user_config, create_Windows_shortcut, _create_lnk_file


class TestSetupFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set maximum difference string length to None (infinite)
        cls.maxDiff = None


    # ------------------
    # Test config setup:

    @patch('shutil.copyfile')
    def test_setup_config(self, mocked_copyfile):
        local_config_file = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stitch_m", "config.cfg"))
        if os.name == "posix":
            user_config_location = Path(os.path.expanduser("~/.config/stitch_m/config.cfg"))
        elif os.name == "nt":
            user_config_location = Path(os.path.expanduser("~/AppData/Local/stitch_m/config.cfg"))
        else:
            raise OSError

        create_user_config()

        mocked_copyfile.assert_called_once_with(local_config_file, user_config_location)

    @patch('stitch_m.file_handler.get_user_config_path')
    @patch('logging.error')
    def test_setup_config_fail_bad_path(self, mocked_error_log, mocked_get_config):
        local_config_file = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stitch_m", "config.cfg"))
        mocked_get_config.return_value = (Path(os.path.expanduser("~/.fake_dir/oh_no/thisisbad.cfg")), [])

        create_user_config()

        mocked_error_log.assert_called_once_with("Unable to create user config file due to directory issues", exc_info=True)


    # ------------------
    # Test Windows shortcut setup:

    @patch("os.name")
    @patch('logging.error')
    def test_setup_win_exits_on_linux(self, mocked_error_log, mocked_os_name):
        mocked_os_name.return_value = "posix"
        create_Windows_shortcut()
        mocked_error_log.assert_called_once_with("This command is only valid on Windows installations.")

    @patch('stitch_m.file_handler._create_lnk_file')
    def test_setup_windows_shortcut_function_called(self, mocked_shortcut_creator):
        # Only run this test if on Windows
        if os.name == "nt":
            create_Windows_shortcut()
            mocked_shortcut_creator.assert_called_once_with(Path(os.environ["HOMEDRIVE"]) / os.environ["HOMEPATH"] / "Desktop" / "StitchM.lnk")
    

    @patch('stitch_m.file_handler._create_lnk_file')
    def test_setup_windows_shortcut_test_created_(self, mocked_shortcut_creator):
        # Only run this test if on Windows
        if os.name == "nt":
            test_shortcut_path = Path(".") / "test_shortcut.lnk"
            _create_lnk_file(test_shortcut_path)
            link_created = test_shortcut_path.exists()
            if link_created:
                os.remove(test_shortcut_path)
            self.assertTrue(link_created)


