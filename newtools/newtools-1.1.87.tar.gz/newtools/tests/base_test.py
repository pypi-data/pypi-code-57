"""
(c) Dativa 2012-2020, all rights reserved

This code is licensed under MIT license (see license.txt for details)
"""

import os
import shutil
import glob
from unittest import TestCase
from newtools.optional_imports import pandas as pd
from newtools.optional_imports import s3fs

from newtools import optional_imports


class BaseTest(TestCase):
    create_test_data = False
    test_dir = os.path.join(os.path.dirname(__file__), "test_data")
    tempdir = os.path.join(test_dir, "temp")

    def setUp(self):
        try:
            pd.set_option("display.max_rows", 100, "display.max_columns", 100)
        except ImportError:
            pass

        try:
            os.makedirs(self.tempdir)
        except FileExistsError:
            self.tearDown()
            self.setUp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def compare_files(self, expected_path):
        for file in glob.glob(os.path.join(self.tempdir, "*")):

            if file.endswith(".gz"):
                old_file = file
                file = file.replace(".gz", "")
                import gzip
                with gzip.open(old_file, "rb") as f_in:
                    with open(file, "wb") as f_out:
                        f_out.write(f_in.read())

            print(file)
            if self.create_test_data:
                shutil.copyfile(file, os.path.join(expected_path, os.path.split(file)[1]))
            with open(os.path.join(expected_path,
                                   os.path.split(file)[1])) as expected_file:
                with open(file, "r") as actual_file:
                    self.assertEqual(expected_file.readlines(),
                                     actual_file.readlines(),
                                     "actual file(right) is not as expected (left)")


class TestBase(BaseTest):
    """
    Get full coverage by testing the error cases on the optional imports. The actual tests themselves wouldn't run
    if these didn't work

    """

    def test_import_retry(self):
        @optional_imports.AwsRetry.backoff()
        def banana():
            pass

        banana()

    def test_dummy_awsretry(self):
        @optional_imports.DummyAWSRetry.backoff()
        def apple():
            pass

        apple()

    def test_never_imports(self):
        optional_imports.NEVER_IMPORT = True

        my_s3fs = optional_imports.get_s3fs()
        with self.assertRaisesRegex(ImportError, "s3fs is not installed. Failed calling S3FileSystem()"):
            my_s3fs.S3FileSystem.read_timeout = 600

        with self.assertRaisesRegex(ImportError,
                                    "dativa.tools.SqlClient is not installed. Failed calling dativa.tools.SqlClient()"):
            optional_imports.get_sql_client()(1, 2, 3)

        optional_imports.NEVER_IMPORT = False

        self.assertEqual(optional_imports.get_s3fs(), s3fs)
