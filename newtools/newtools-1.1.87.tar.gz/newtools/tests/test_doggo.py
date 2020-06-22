# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

import unittest
import os
import pyarrow as pa

from time import sleep
import multiprocessing
from random import random
import gzip

from newtools.optional_imports import pandas as pd
from newtools.optional_imports import numpy as np
from newtools.optional_imports import boto3

from newtools import PandasDoggo, FileDoggo, S3Location, DoggoFileSystem, DoggoLock, DoggoWait
from .base_test import BaseTest


class TestDoggos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data', 'pandas_doggo_tests')

    def test_read_csv_local(self):
        """read a local csv"""

        expected_df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                               4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                                    'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = os.path.join(self.base_path, 'csv', 'generic', 'email_test.csv')
        session = boto3.Session()
        fh = PandasDoggo(boto_session=session)
        df = fh.load(pth)
        pd.testing.assert_frame_equal(df, expected_df)

    def test_read_csv_local_gzip(self):
        pth = os.path.join(self.base_path, 'csv', 'gzip', 'test.csv.gz')

        fh = PandasDoggo()
        df = fh.load_csv(pth, compression='gzip')
        print(df.to_csv(index=0))

    def test_write_csv_local_gzip(self):
        pth_in = os.path.join(self.base_path, 'csv', 'gzip', 'uncompressed.csv')
        pth_out = os.path.join(self.base_path, 'csv', 'gzip', 'write.csv.gzip')
        pth_exp = os.path.join(self.base_path, 'csv', 'gzip', 'write_target.csv.gzip')
        fh = PandasDoggo()
        df = fh.load_csv(pth_in)

        fh.save_csv(df, pth_out, compression='gzip', index=0)
        with gzip.open(pth_out) as r, gzip.open(pth_exp) as exp:
            self.assertEqual(r.read().decode('utf-8'), exp.read().decode('utf-8'))

        os.remove(pth_out)

    def test_write_csv_local_gzip_infer(self):
        pth_in = os.path.join(self.base_path, 'csv', 'gzip', 'uncompressed.csv')
        pth_out = os.path.join(self.base_path, 'csv', 'gzip', 'write.csv.gzip')
        pth_exp = os.path.join(self.base_path, 'csv', 'gzip', 'write_target.csv.gzip')
        fh = PandasDoggo()
        df = fh.load_csv(pth_in)

        fh.save(df, pth_out, index=0)
        with gzip.open(pth_out) as r, gzip.open(pth_exp) as exp:
            self.assertEqual(r.read().decode('utf-8'), exp.read().decode('utf-8'))

        os.remove(pth_out)

    def test_read_csv_local_gzip_infer(self):
        pth = os.path.join(self.base_path, 'csv', 'gzip', 'test.csv.gz')

        fh = PandasDoggo()
        df = fh.load(pth)

    def test_read_csv_local_zip_infer(self):
        with self.assertRaises(NotImplementedError):
            pth = os.path.join(self.base_path, 'csv', 'gzip', 'test.csv.zip')
            fh = PandasDoggo()
            df = fh.load(pth)

    def test_write_csv_local(self):
        df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                      4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                           'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = os.path.join(self.base_path, 'csv', 'generic', 'email_test_copy.csv')
        expected_pth = os.path.join(self.base_path, 'csv', 'generic', 'email_test.csv')
        fh = PandasDoggo()
        fh.save(df, pth, index=None)
        with open(pth) as p, open(expected_pth) as p2:
            self.assertEqual(p.read().strip(), p2.read().strip())

        os.remove(pth)

    def test_read_pq_local(self):
        fh = PandasDoggo()
        pth = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df = fh.load(pth)

    def test_write_pq_local(self):
        fh = PandasDoggo()
        df = pd.read_csv(os.path.join(self.base_path, 'parquet', 'emails.csv'))
        fh.save_parquet(df, os.path.join(self.base_path, 'parquet', 'emails.parquet'))
        os.remove(os.path.join(self.base_path, 'parquet', 'emails.parquet'))

    def test_read_pq_local_with_args(self):
        fh = PandasDoggo()
        pth = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df = fh.load_parquet(pth, columns=['country', 'birthdate', 'salary', 'title'])
        self.assertEqual(sorted(list(df.columns)), sorted(['country', 'birthdate', 'salary', 'title']))

    def test_pq_schema_int64(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data.parquet')
        test_df = pd.DataFrame(
            {"col1": [1, 2, 3, 4, 5], "col2": ["a", "s", "6", "7", "t"]})
        fields = [
            pa.field("col1", pa.int64()),
            pa.field("col2", pa.string())
        ]
        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        pd.testing.assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_int32(self):
        # Tests the down casting of int64 to int32 without explicit conversion
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data.parquet')
        test_df = pd.DataFrame(
            {"col1": [1, 2, 3, 4, 128], "col2": ["a", "s", "6", "7", "t"]})
        fields = [
            pa.field("col1", pa.int32()),
            pa.field("col2", pa.string())
        ]
        test_df = test_df.astype({"col1": 'Int32'})
        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        pd.testing.assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_int32_nulls(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data_nulls.parquet')
        test_df = pd.DataFrame(
            {"col1": pd.Series([1, 2, 3, 4, 128, pd.NA, None], dtype='Int32'),
             "col2": ["a", "s", "6", "7", "t", 'pd.NA', 'None']})
        fields = [
            pa.field("col1", pa.int32()),
            pa.field("col2", pa.string())
        ]

        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        pd.testing.assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_int64_nulls(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data_nulls.parquet')
        test_df = pd.DataFrame(
            {"col1": pd.Series([1, 2, 3, 4, 128, pd.NA, None], dtype='Int64'),
             "col2": ["a", "s", "6", "7", "t", 'pd.NA', 'None']})
        fields = [
            pa.field("col1", pa.int64()),
            pa.field("col2", pa.string())
        ]

        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        pd.testing.assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_pq_schema_datetime(self):
        new_file_path = os.path.join(self.base_path,
                                     'parquet',
                                     'new_data.parquet')
        rng = pd.date_range('2015-02-24', periods=5, freq='23H')
        test_df = pd.DataFrame({'Date': rng, 'Val': np.random.randn(len(rng))})

        test_df['Date'] = pd.to_datetime(test_df['Date'], unit='D')
        fields = [
            pa.field("Date", pa.timestamp('ms')),
            pa.field("Val", pa.float64())
        ]
        my_schema = pa.schema(fields)
        fh = PandasDoggo()

        fh.save_parquet(test_df, new_file_path, schema=my_schema)

        pd.testing.assert_frame_equal(test_df, fh.load_parquet(new_file_path))
        os.remove(new_file_path)

    def test_read_csv_s3(self):
        """read a csv from s3"""
        expected_df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                               4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                                    'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = S3Location('gd.dativa.test').join('generic', 'email_test.csv')
        session = boto3.Session()
        fh = PandasDoggo(boto_session=session)
        df = fh.load(pth)
        pd.testing.assert_frame_equal(df, expected_df)

    def test_write_csv_s3(self):
        df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                      4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                           'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = S3Location('gd.dativa.test').join('generic', 'email_test_copy.csv')
        expected_pth = S3Location('gd.dativa.test').join('generic', 'email_test.csv')
        fh = PandasDoggo()
        fh.save(df, pth, index=None)
        with FileDoggo(pth) as p, FileDoggo(expected_pth) as p2:
            self.assertEqual(p.read().strip(), p2.read().strip())

        s3 = boto3.resource('s3')
        obj = s3.Object(pth.bucket, pth.key)
        obj.delete()

    def test_write_csv_s3_gzip(self):
        df = pd.DataFrame({'e-mail': {0: 'n@gmail.com', 1: 'p@gmail.com', 2: 'h@gmail.com', 3: 's@gmail.com',
                                      4: 'l@gmail.com', 5: 'v@gmail.com', 6: None},
                           'number': {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0}})
        pth = S3Location('gd.dativa.test').join('generic', 'email_test_copy.csv.gz')

        fh = PandasDoggo()

        fh.save(df, pth, index=None, compression="gzip")

        pd.testing.assert_frame_equal(fh.load_csv(pth), df)

        s3 = boto3.resource('s3')
        obj = s3.Object(pth.bucket, pth.key)
        obj.delete()

    def test_read_pq_s3(self):
        fh = PandasDoggo()

        df_s3 = fh.load_parquet('s3://07092018pqtest/data.parquet')

        pth_local = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df_l = fh.load_parquet(pth_local)

        pd.testing.assert_frame_equal(df_s3, df_l)

    def test_write_pq_s3(self):
        fh = PandasDoggo()
        pth_local = os.path.join(self.base_path, 'parquet', 'data.parquet')
        df_l = fh.load_parquet(pth_local)
        s3 = boto3.resource('s3')
        obj = s3.Object('07092018pqtest', 'write.parquet')
        obj.delete()  # just in case
        fh.save(df_l, 's3://07092018pqtest/write.parquet')

        obj.load()  # checks that it was written
        obj.delete()

    def test_cant_guess_format(self):
        fh = PandasDoggo()
        with self.assertRaises(ValueError):
            fh.load('some_text_file')

    def test_invalid_format_detected(self):
        fh = PandasDoggo()
        with self.assertRaises(ValueError):
            fh.load('some_text_file.dat')
        with self.assertRaises(ValueError):
            fh.save(pd.DataFrame(), 'some_text_file.dat')

    def test_invalid_format_passed(self):
        fh = PandasDoggo()
        with self.assertRaises(ValueError):
            fh.load('some_text_file.dat', file_format='bees?')

    def test_whos_a_good_boi_den(self):
        with self.assertRaises(ValueError):
            with FileDoggo('some_path_to_a_file', mode='justusewb', is_s3=True) as f:
                f.write('should have read the docs')


class TestCSVDoggo(unittest.TestCase):
    pass


class TestDoggoFileSystem(BaseTest):

    def _test(self, root):
        dfs = DoggoFileSystem()

        testdir = dfs.join(root, str(random()))

        file_1 = dfs.join(testdir, "temp_1.txt")
        file_2 = dfs.join(testdir, "tests", "temp_2.txt")

        self.assertEqual(dfs.split(file_1), (testdir, "temp_1.txt"))

        self.assertFalse(dfs.exists(file_1))
        self.assertFalse(dfs.exists(file_2))

        with dfs.open(file_1, "wb") as f:
            f.write(b"woof")

        self.assertTrue(dfs.exists(file_1))
        self.assertFalse(dfs.exists(file_2))

        dfs.cp(file_1, file_2)
        self.assertTrue(dfs.exists(file_1))
        self.assertTrue(dfs.exists(file_2))

        paths = dfs.glob(dfs.join(testdir, "**"))
        self.assertIn(file_1, paths)
        self.assertIn(file_2, paths)

        dfs.rm(file_2)
        self.assertTrue(dfs.exists(file_1))
        self.assertFalse(dfs.exists(file_2))

        dfs.mv(file_1, file_2)
        self.assertFalse(dfs.exists(file_1))
        self.assertTrue(dfs.exists(file_2))

        self.assertEqual(dfs.size(file_2), 4)

    def test_s3(self):
        self._test(S3Location("s3://07092018pqtest/fs/"))

        dfs = DoggoFileSystem()
        self.assertEqual(dfs.split("s3://07092018pqtest/temp.txt"), ("s3://07092018pqtest/", "temp.txt"))

    def test_file(self):
        self._test(self.tempdir)

    def test_bad_copy(self):
        with self.assertRaises(NotImplementedError):
            DoggoFileSystem().cp("s3://07092018pqtest/fs/file.tmp",
                                 os.path.join(self.tempdir, "file.tmp"))


class TestDoggoWait(unittest.TestCase):
    def test_basic(self):
        dw = DoggoWait(wait_period=1, time_out_seconds=2)

        with self.assertRaises(ValueError):
            dw.timed_out()

        dw.start_timeout()
        self.assertEqual(dw.timed_out(), False)
        dw.check_timeout()
        dw.wait()
        with self.assertRaises(TimeoutError):
            dw.check_timeout()


def check_lock(file):
    test_str = str(random())
    with DoggoLock(file, wait_period=1, time_out_seconds=2, maximum_age=5):
        with open(file, "wt") as f:
            f.write(test_str)

        with open(file, "rt") as f:
            assert f.read() == test_str

        sleep(0.1)


class TestDoggoLock(BaseTest):
    def test_lock_timeout(self):
        file = os.path.join(self.tempdir, 'test_lock_timeout.tmp')
        with DoggoLock(file, wait_period=1, time_out_seconds=5, maximum_age=10):
            with self.assertRaises(TimeoutError):
                with DoggoLock(file, wait_period=1, time_out_seconds=5, maximum_age=10):
                    pass

    def test_basic(self):
        file = os.path.join(self.tempdir, 'test_basic.tmp')
        check_lock(file)
        check_lock(file)

    def test_lock_ages(self):
        file = os.path.join(self.tempdir, 'test_lock_ages.tmp')
        lock_1 = DoggoLock(file, wait_period=1, time_out_seconds=2, maximum_age=5)
        lock_2 = DoggoLock(file, wait_period=1, time_out_seconds=2, maximum_age=5)

        lock_1.acquire()

        with self.assertRaises(TimeoutError):
            lock_2.acquire()

        sleep(5)

        lock_2.acquire()

        lock_1.release()
        lock_2.release()

    def test_lock_multiprocess(self):
        file = os.path.join(self.tempdir, 'test_lock_multiprocess.tmp')
        pool = multiprocessing.Pool()

        for _ in range(0, 100):
            pool.apply_async(check_lock,
                             (file,))

        pool.close()
        pool.join()
