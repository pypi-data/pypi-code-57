from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot


class TestCommander(TestCase):

    def test_with_root_param(self):
        with TemporaryDirectory() as t:
            c = Commander(FilesystemRoot(t))
            o = c.handle('add', '--task', 'a')
            x = Path(t, 'tasks.txt').read_text()
            self.assertEqual(x, 'a\n')

    def test_version_info(self):
        with TemporaryDirectory() as t:
            with mock.patch('sys.version_info', (1, 2, 3)):
                with self.assertRaises(RuntimeError):
                    Commander(FilesystemRoot(t))
