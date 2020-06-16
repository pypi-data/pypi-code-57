from contextlib import redirect_stdout
from functools import partial

import pytest
import copy
import os
import io
import pytest
import tempfile
import pyarrow
import pandas
import numpy
import random
import json

from dli.client.exceptions import DataframeStreamingException
from unittest.mock import MagicMock, ANY, patch

from tests.models.conftest import mock_catalogue_filter_search_response_impl


@pytest.fixture
def instance_file(client):
    client._environment.consumption = 'consumption-test.local'

    instance = client.Instance(
        datafile_id='123',
        total_size=1048576
    )

    client._session.get().json.return_value = {
        'data': [{
            'attributes': {
                'path': 'prefix/test.001.csv',
                'metadata': {}
            }
        }]
    }

    files = instance.files()
    file_ = files[0]

    client.session.reset_mock()

    client._session.get().raw.read.side_effect = [
        b'hello world',
        b''
    ]

    yield file_


class TestDataset:

    def test_dataset_instances_is_iterable(self, client):
        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                }
            }
        })

        datafiles = dataset.instances.all()
        assert hasattr(datafiles, '__iter__')

    def test_dataset_download_refers_to_latest_instance(self, client):
        path = './destination_path'
        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                }
            }
        })

        dataset.instances.latest = MagicMock(
            download=MagicMock(return_value='file')
        )

        result = dataset.instances.latest.download(path)

        dataset.instances.latest.download.assert_called_once_with(path)
        assert result == 'file'

    def test_dataset_instances_make_requests_on_iteration(self, client):
        client._session.get().json.side_effect = [
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 1}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 2}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 3}
                }]
            },
        ]
        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                }
            }
        })

        instances = list(dataset.instances.all())
        assert len(instances) == 3

    def test_dataset_instances_make_multiple_iterations(self, client,
                                                        monkeypatch):
        client._session.get().json.side_effect = [
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 1}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 2}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 3}
                }]
            },
        ]
        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                }
            }
        })

        def mock_iter(self):
            if not hasattr(mock_iter, 'call_count'):
                mock_iter.call_count = 0
                mock_iter.cached = False

            if not mock_iter.cached:
                mock_iter.call_count += 1
                mock_iter.cached = True

            yield from [1, 2, 3]

        instances = list(dataset.instances.all())
        assert len(instances) == 3

        instances_from_cache = list(dataset.instances.all())
        assert(len(dataset.instances._paginator.cache) == 3)
        assert(len(instances_from_cache) == 3)

    def test_dataset_filter_prefix(self, client, monkeypatch, instance_file):
        boto_mock = MagicMock()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with tempfile.TemporaryDirectory() as target_dest:
            dataset.download(target_dest)

        assert (
            boto_mock().resource().Bucket()
            .objects.filter.call_args[1]['Prefix']
        ) == 'abc/'

        with tempfile.TemporaryDirectory() as target_dest:
            dataset.download(target_dest, filter_path='/123')

        assert (
            boto_mock().resource().Bucket()
            .objects.filter.call_args[1]['Prefix']
        ) == 'abc/123'

    def test_dataset_is_wrapped_with_analytics_logger(self, client,
                                                      monkeypatch,
                                                      instance_file):
        boto_mock = MagicMock()
        monkeypatch.setattr('dli.aws.Session', boto_mock)

        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with tempfile.TemporaryDirectory() as target_dest:
            dataset.download(target_dest)

        client._analytics_handler.create_event.call_count = 2
        client._analytics_handler.create_event.assert_any_call(
            # Not testing the extract user metadata here
            ANY, ANY,
            'DatasetModel',
            'download',
            {
                'self': dataset,
                'destination_path': target_dest,
                'dataset_id': '1234'
            },
            result_status_code=200
        )
    def test_dataset_info(self, test_client, dataset_request_v2,
                          dictionary_request_v2, fields_request_v2):
        test_client.session.reset_mock()
        test_client._session.get.return_value.json.side_effect = [
            dictionary_request_v2, fields_request_v2
        ]

        dataset = test_client.Dataset._from_v2_response(dataset_request_v2)

        def redirect(fun):
            with io.StringIO() as buf, redirect_stdout(buf):
                fun()
                output = buf.getvalue()
                return output


        assert(
            redirect(dataset.info)
                .replace(" ", "").replace("\n", "")
               ==
            """
                name    type
                ------  -----------------
                col1    String (Nullable)
                col2    String (Nullable)
                col3    String
            """
                .replace(" ", "").replace("\n", "")
        )


class TestFileDownload:

    def test_instance_file_download_simple(self, client, instance_file):
        old_dir = os.path.abspath(os.curdir)

        with tempfile.TemporaryDirectory() as target_dest:
            os.chdir(os.path.abspath(target_dest))
            instance_file.download()
            with open(os.path.join(target_dest, 'prefix/test.001.csv')) as f:
                assert f.read() == 'hello world'

        os.chdir(old_dir)

    def test_instance_file_download_with_path(self, client, instance_file):
        with tempfile.TemporaryDirectory() as target_dest:
            instance_file.download(target_dest)
            with open(os.path.join(target_dest, 'prefix/test.001.csv')) as f:
                assert f.read() == 'hello world'

    def test_instance_file_download_non_existent_path(
        self, client, instance_file
    ):
        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a/b/c/')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'hello world'

    def test_instance_file_download_non_existent_file(
        self, client, instance_file
    ):
        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'hello world'

    def test_instance_file_overwrites(
        self, client, instance_file
    ):
        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'hello world'

        client.session.reset_mock()
        client._session.get().raw.read.side_effect = [
            b'brave new world',
            b''
        ]

        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'brave new world'


class TestInstanceDownload:

    @pytest.fixture
    def instance(self, client):
        client._environment.consumption = 'consumption-test.local'

        instance = client.Instance(
            datafile_id='123'
        )

        client._session.get().json.return_value = {
            'data': [{
                'attributes': {
                    'path': f's3://bucket/prefix/test.00{i}.csv',
                    'metadata': {}
                }
            } for i in range(3)
            ]
        }

        yield instance

    def test_instance_download_all_should_refer_to_download_function(self, instance):
        path = './target'
        instance.download = MagicMock(return_value='file')
        result = instance.download_all(path, flatten=False)

        instance.download.assert_called_once_with(path, False)
        assert result == 'file'

    def test_instance_download_flatten(self, client, monkeypatch, instance):
        client._session.get().raw = io.BytesIO(b'abc')

        with tempfile.TemporaryDirectory() as target_dest:
            to = os.path.join(target_dest, 'a')
            result = instance.download_all(to, flatten=True)
            directory_of_flattened = result[0].split('/test')[0]
            list_dir = sorted(os.listdir(directory_of_flattened))

            assert (
                list_dir ==
                ['test.000.csv', 'test.001.csv', 'test.002.csv']
            )


class TestInstanceDataframe:

    @pytest.fixture
    def test_dataframe(self) -> pandas.DataFrame:
        # Rows:
        # 100 -> 205.5 kB (205,548 bytes) on disk in 0.44 seconds.
        # 10000 -> 9.2 MB (9,234,131 bytes) on disk in 0.67 seconds.

        max_rows = 10000
        # Max columns should match a worst case. For CDS Single Name Pricing
        # Sensitivities and Liquidity there are 164 columns.
        max_columns = 168

        num_column_types = 6

        # Seed the random number generator so that we can reproduce the output.
        numpy.random.seed(0)

        def bools_df():
            return pandas.DataFrame(
                numpy.random.choice(
                    [False, True],
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_bool_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def ints_df():
            return pandas.DataFrame(
                numpy.random.randint(
                    low=0,
                    high=1000000,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_int_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def floats_df():
            return pandas.DataFrame(
                numpy.random.rand(
                    max_rows,
                    int(max_columns / num_column_types)),
                columns=[str(f'column_float_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def string_df():
            import pandas.util.testing
            return pandas.DataFrame(
                numpy.random.choice(
                    pandas.util.testing.RANDS_CHARS,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_str_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def dates_df():
            dates = pandas.date_range(start='1970-01-01', end='2020-01-01')

            return pandas.DataFrame(
                numpy.random.choice(
                    dates,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_date_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def datetimes_df():
            datetimes = pandas.date_range(start='1970-01-01', end='2020-01-01',
                                          freq='H')

            return pandas.DataFrame(
                numpy.random.choice(
                    datetimes,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_datetime_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        df = pandas.concat(
            [bools_df(), ints_df(), floats_df(), string_df(), dates_df(),
             datetimes_df()],
            # Concat columns axis
            axis=1,
            copy=False
        )

        # Randomise the column order so the compression cannot optimise
        # easily based on types as this will mix float columns among the int
        # columns.
        random_column_order = df.columns.tolist()
        random.shuffle(random_column_order)
        df = df[random_column_order]

        assert df.shape[0] == max_rows
        assert df.shape[1] == max_columns

        return df

    @pytest.fixture
    def arrow_ipc_stream(self, test_dataframe):
        sink = pyarrow.BufferOutputStream()
        batch = pyarrow.RecordBatch.from_pandas(test_dataframe)
        writer = pyarrow.RecordBatchStreamWriter(sink, batch.schema)
        writer.write_batch(batch)
        # It's important the IPC stream is closed
        writer.close()
        return io.BytesIO(sink.getvalue().to_pybytes())

    @pytest.fixture
    def dataset(self, client):
        return client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                    'has_access': True,
                }
            }
        })

    def test_dataset_dataframe(self, benchmark, client, arrow_ipc_stream,
                               test_dataframe, dataset):

        dataset._client = MagicMock()
        dataset._client._environment.consumption = 'https://test/'
        dataset._client.session.get().raw = arrow_ipc_stream
        dataset._client.session.get().status_code = 200

        def _bench():
            # reset our fake socket
            arrow_ipc_stream.seek(0)
            return dataset.dataframe()

        # The benchmark code will run several times to get an average runtime.
        df = benchmark(_bench)

        # Check that we can read from the file that was written.
        pandas.testing.assert_frame_equal(test_dataframe, df)

    @pytest.mark.parametrize('value', ['1', 0])
    def test_dataframe_nrows_validation(self, client, arrow_ipc_stream,
                                        test_dataframe, value, dataset):
        dataset._client = MagicMock()
        dataset._client._environment.consumption = 'https://test/'
        dataset._client.session.get().raw = arrow_ipc_stream
        dataset._client.session.get().status_code = 200

        # Expected to pass.
        df = dataset.dataframe(value)
        # Check that we can read from the file that was written.
        pandas.testing.assert_frame_equal(test_dataframe, df)

    @pytest.fixture
    def partitions(self):
        return {
            'data':{
                'attributes': {
                    'partitions': {
                        'a': ["1", "2", "3"],
                        'b': ["4", "5", "6"]
                    }
                }
            }
        }

    def test_dataset_partitions(self, client, partitions):
        dataset = client.Dataset._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                }
            }
        })

        dataset._client = client
        dataset._client._session.get.return_value.json.side_effect = [partitions, {
            'data': {
                'id': '1234',
                'attributes': {
                    'location': {},
                }
            }
        },  partitions]

        msg = dataset.partitions()
        assert(msg == partitions["data"]["attributes"]["partitions"])

        msg = client.get_dataset_partitions(id=dataset.id)
        assert(msg == partitions["data"]["attributes"]["partitions"])


    def test_dataframe_handle_errors(self, client, arrow_ipc_stream,
                                     test_dataframe, dataset):
        error_msg = json.dumps({
            'status': 400,
        }).encode('utf')

        arrow_ipc_stream.seek(0, 2)
        arrow_ipc_stream.write(error_msg)
        arrow_ipc_stream.seek(0)

        dataset._client = MagicMock()
        dataset._client._environment.consumption = 'https://test/'
        dataset._client.session.get().raw = arrow_ipc_stream
        dataset._client.session.get().status_code = 200

        with pytest.raises(DataframeStreamingException):
            dataset.dataframe(1)


class TestDatasetModule:

    def test_dataset_contents(self, capsys, test_client,
                              package_request_index_v2, dataset_request_index_v2,
                              instance_request_v1):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2,
            dataset_request_index_v2, instance_request_v1,
        ]

        pp = test_client.packages(search_term='', only_mine=False)
        ds = pp['Test Package'].datasets()
        d = ds['Test DataSet']
        d.contents()
        captured = capsys.readouterr()
        assert captured.out == '\nINSTANCE 1 (size: 1.00 Mb)\n'

    @pytest.fixture()
    def return_value(self, dataset_request_index_v2):
        return partial(
            mock_catalogue_filter_search_response_impl,
            dataset_request_index_v2
        )

    def test_find_no_params(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets()) == 1

    def test_find_datasets_no_list(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=[])) == 1

    def test_find_datasets_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(only_mine=False)) == 2

    def test_find_datasets_only_mine(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(only_mine=True)) == 1

    def test_find_datasets_no_search_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=None, only_mine=False)) == 2

    def test_find_datasets_no_list_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=[], only_mine=False)) == 2

    def test_find_datasets_no_term_only_mine(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=None, only_mine=True)) == 1

    def test_find_datasets_no_list_only_mine(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=[], only_mine=True)) == 1

    def test_find_datasets_ignore_bad_data_list(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["baddata"], only_mine=False)) == 2

    def test_find_datasets_ignore_multi_bad_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["baddata", "baddata"], only_mine=False)) == 2

    def test_find_datasets_ignore_bad_keep_good_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["short_code=TestDataset", "baddata"], only_mine=False)) == 1

    def test_find_datasets_ignore_bad_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term="baddata", only_mine=False)) == 2

    def test_find_datasets_name_search_match(self, test_client, return_value):
        test_client._session.get = return_value
        # testing search term with only_mine param against valid search term
        assert len(test_client.datasets(
            search_term=["short_code=TestDataset"], only_mine=False)) == 1

    def test_find_datasets_no_search_my_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=[], only_mine=True)) == 1

    def test_find_datasets_no_match(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["short_code=NotTestDataset"], only_mine=True)) == 0

    def test_find_datasets_multi_param_my_data(self, test_client, return_value):
        test_client._session.get = return_value
        # multi-param against only_mine
        assert len(test_client.datasets(
            search_term=["name=Other Dataset"],
            only_mine=True)) == 0

    def test_find_datasets_multi_param_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["name=Test DataSet", "description=description",
                         "organisation_name=IHS Markit"],
            only_mine=False)) == 1

    def test_find_datasets_find_both(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["description=description"],
            only_mine=False)) == 2

    def test_find_datasets_multi_param_no_match(self, test_client, return_value):
        test_client._session.get = return_value
        # multi-param with bad data
        assert len(test_client.datasets(
            search_term=["description=description", "organisation_name=baddata"],
            only_mine=False)) == 0

    def test_find_datasets_like_name(self, test_client, return_value):
        test_client._session.get = return_value
        # 'like' test
        assert len(test_client.datasets(
            search_term=["name like Test"],
            only_mine=True)) == 1

    def test_find_datasets_by_id(self, test_client, return_value):
        test_client._session.get = return_value
        # 'like' test
        assert len(test_client.datasets(
            search_term=["id=5b01376e-975d-11e9-8832-7e5ef76d533f"],
            only_mine=True)) == 1

    def test_find_datasets_override_has_access_return_none(self, test_client, return_value):
        test_client._session.get = return_value
        # test override of param against kwarg of same (accomplish both ways)
        assert len(test_client.datasets(
            search_term=["has_access=True"],
            only_mine=False)) == 0

    def test_datasets_called_twice(self, test_client, package_request_index_v2,
                                   dataset_request_index_v2):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2, dataset_request_index_v2
        ]
        pp = test_client.packages(search_term='', only_mine=False)

        # This should work twice
        assert pp['Test Package'].datasets()
        assert pp['Test Package'].datasets()

    def test_retrieve_instance_given_package_dataset(self, test_client,
                                                     package_request_index_v2,
                                                     dataset_request_index_v2,
                                                     instance_request_v1
                                                     ):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2,
            dataset_request_index_v2, instance_request_v1,
        ]

        pp = test_client.packages(search_term='', only_mine=False)
        ds = pp['Test Package'].datasets()
        d = ds['Test DataSet']
        instances = list(d.instances.all())
        assert (len(instances) == 1)
        assert (instances[0].datafile_id == 1)
