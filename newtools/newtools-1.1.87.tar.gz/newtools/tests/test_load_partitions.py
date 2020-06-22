import unittest
from newtools.aws import LoadPartitions, S3List


class TestLoadPartitions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bucket = 'newtools-tests-data'
        cls.prefix = 'load_partition_test_data/'
        cls.s3_list_folders = S3List(cls.bucket)
        cls.load_partitions = LoadPartitions(cls.bucket)

    def test_list_folder(self):
        folders = [{'Prefix': 'load_partition_test_data/year=2019/'}, {'Prefix': 'load_partition_test_data/year=2020/'}]
        test_folders = self.s3_list_folders.list_folders(self.prefix)
        self.assertListEqual(folders, test_folders)

    def test_list_partitions(self):
        partitions_list = [{'Prefix': 'load_partition_test_data/year=2019/month=02/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2019/month=0:2/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/some_more_directory_1/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=02/some_more_directory/'}]
        test_partitions_list = self.load_partitions.list_partitions('load_partition_test_data')
        self.assertListEqual(partitions_list, test_partitions_list)

    def test_list_partitions_error(self):
        with self.assertRaises(ValueError):
            self.load_partitions.list_partitions()

    def test_get_sql(self):
        sql_query_list = [
            "ALTER TABLE load_partition_test_data ADD IF NOT EXISTS PARTITION(year='2019',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=02/some_more_directory/' PARTITION(year='2019',month='0:2') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=0:2/some_more_directory/' PARTITION(year='2020',month='01') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=01/some_more_directory/' PARTITION(year='2020',month='01') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=01/some_more_directory_1/' PARTITION(year='2020',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=02/some_more_directory/'"]
        test_sql_query_list = self.load_partitions.get_sql('load_partition_test_data')
        self.assertListEqual(sql_query_list, test_sql_query_list)

    def test_generate_sql(self):
        partitions_list = [{'Prefix': 'load_partition_test_data/year=2019/month=02/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2019/month=0:2/some_more_directory/'},
                           {'Prefix': 'load_partition_test_data/year=2020/month=01/some_more_directory/'},

                           ]

        sql_query_list = [
            "ALTER TABLE load_partition_test_data ADD IF NOT EXISTS PARTITION(year='2019',month='02') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=02/some_more_directory/' PARTITION(year='2019',month='0:2') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2019/month=0:2/some_more_directory/' PARTITION(year='2020',month='01') LOCATION 's3://newtools-tests-data/load_partition_test_data/year=2020/month=01/some_more_directory/'"]

        sql_query_list_test = self.load_partitions.generate_sql('load_partition_test_data', partitions_list)
        self.assertListEqual(sql_query_list, sql_query_list_test)
