import unittest
import pysftp
import os

from tmg.data.ftp import Client
from tests.setup import setup


def setUpModule():
    setup.start_sftp_instance()
    setup.upload_ftp_files()


def tearDownModule():
    setup.remove_ftp_files()
    setup.stop_sftp_instance()


class TestFTP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFTP, self).__init__(*args, **kwargs)
        self.setup = setup

    def test_list_files(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        connection = pysftp.Connection(
            host=self.setup.ftp_hostname,
            username=self.setup.ftp_username,
            password=self.setup.ftp_password,
            port=self.setup.ftp_port,
            cnopts=cnopts
        )

        test_client = Client(
            connection_string=f"{self.setup.ftp_username}:{self.setup.ftp_password}@{self.setup.ftp_hostname}:{self.setup.ftp_port}"
        )

        self.assertListEqual(
            connection.listdir(),
            test_client.list_files()
        )

        self.assertListEqual(
            connection.listdir('test_dir/test_subdir'),
            test_client.list_files('test_dir/test_subdir')

        )

    def test_upload_file(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        connection = pysftp.Connection(
            host=self.setup.ftp_hostname,
            username=self.setup.ftp_username,
            password=self.setup.ftp_password,
            port=self.setup.ftp_port,
            cnopts=cnopts
        )

        test_client = Client(
            connection_string=f"{self.setup.ftp_username}:{self.setup.ftp_password}@{self.setup.ftp_hostname}:{self.setup.ftp_port}"
        )

        test_client.upload_file('tests/data/sample.csv')
        self.assertTrue(connection.exists('sample.csv'))

        test_client.upload_file('tests/data/sample.csv', remote_path='test_dir')
        self.assertTrue(connection.exists('test_dir/sample.csv'))

        test_client.upload_file('tests/data/sample.csv', remote_path='test_dir/test_subdir/rename_sample.csv')
        self.assertTrue(connection.exists('test_dir/test_subdir/rename_sample.csv'))

    def test_download_file(self):
        test_client = Client(
            connection_string=f"{self.setup.ftp_username}:{self.setup.ftp_password}@{self.setup.ftp_hostname}:{self.setup.ftp_port}"
        )

        test_client.download_file('test_dir/download_sample.csv')
        self.assertTrue(os.path.exists('download_sample.csv'))

        test_client.download_file('test_dir/download_sample.csv', local_path='tests/data')
        self.assertTrue(os.path.exists('tests/data/download_sample.csv'))

        test_client.download_file('test_dir/download_sample.csv', local_path='tests/data/rename_sample.csv')
        self.assertTrue(os.path.exists('tests/data/rename_sample.csv'))

    def test_change_file_permission(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        connection = pysftp.Connection(
            host=self.setup.ftp_hostname,
            username=self.setup.ftp_username,
            password=self.setup.ftp_password,
            port=self.setup.ftp_port,
            cnopts=cnopts
        )

        test_client = Client(
            connection_string=f"{self.setup.ftp_username}:{self.setup.ftp_password}@{self.setup.ftp_hostname}:{self.setup.ftp_port}"
        )

        test_client.change_file_permission('test_dir/permission_change.csv')
        self.assertEqual(oct(connection.stat('test_dir/permission_change.csv').st_mode)[-3:], '777')

        test_client.change_file_permission('test_dir/permission_change2.csv', 533)
        self.assertEqual(oct(connection.stat('test_dir/permission_change2.csv').st_mode)[-3:], '533')

    def test_delete_file(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        connection = pysftp.Connection(
            host=self.setup.ftp_hostname,
            username=self.setup.ftp_username,
            password=self.setup.ftp_password,
            port=self.setup.ftp_port,
            cnopts=cnopts
        )

        test_client = Client(
            connection_string=f"{self.setup.ftp_username}:{self.setup.ftp_password}@{self.setup.ftp_hostname}:{self.setup.ftp_port}"
        )

        test_client.delete_file('test_dir/delete_sample.csv')

        self.assertFalse(connection.exists('test_dir/delete_sample.csv'))

    def test_close(self):
        test_client = Client(
            connection_string=f"{self.setup.ftp_username}:{self.setup.ftp_password}@{self.setup.ftp_hostname}:{self.setup.ftp_port}"
        )

        test_client.close()
        self.assertFalse(test_client.connection._sftp_live)
