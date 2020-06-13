# -*- coding: utf-8 -*-

import os
import shutil

import pandas as pd
import pytest
from ruamel.yaml import YAML

from great_expectations.core import ExpectationSuite
from great_expectations.core.batch import Batch
from great_expectations.core.util import nested_update
from great_expectations.data_context.types.base import DataContextConfigSchema
from great_expectations.data_context.util import file_relative_path
from great_expectations.datasource import PandasDatasource
from great_expectations.datasource.types.batch_kwargs import (
    BatchMarkers,
    PathBatchKwargs,
)
from great_expectations.exceptions import BatchKwargsError
from great_expectations.validator.validator import Validator

yaml = YAML()


@pytest.fixture(scope="module")
def test_folder_connection_path(tmp_path_factory):
    df1 = pd.DataFrame({"col_1": [1, 2, 3, 4, 5], "col_2": ["a", "b", "c", "d", "e"]})
    path = str(tmp_path_factory.mktemp("test_folder_connection_path"))
    df1.to_csv(os.path.join(path, "test.csv"))

    return str(path)


def test_standalone_pandas_datasource(test_folder_connection_path):
    datasource = PandasDatasource(
        "PandasCSV",
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": test_folder_connection_path,
            }
        },
    )

    assert datasource.get_available_data_asset_names() == {
        "subdir_reader": {"names": [("test", "file")], "is_complete_list": True}
    }
    manual_batch_kwargs = PathBatchKwargs(
        path=os.path.join(str(test_folder_connection_path), "test.csv")
    )

    generator = datasource.get_batch_kwargs_generator("subdir_reader")
    auto_batch_kwargs = generator.yield_batch_kwargs("test")

    assert manual_batch_kwargs["path"] == auto_batch_kwargs["path"]

    # Include some extra kwargs...
    auto_batch_kwargs.update(
        {"reader_options": {"sep": ",", "header": 0, "index_col": 0}}
    )
    batch = datasource.get_batch(batch_kwargs=auto_batch_kwargs)
    assert isinstance(batch, Batch)
    dataset = batch.data
    assert (dataset["col_1"] == [1, 2, 3, 4, 5]).all()
    assert len(dataset) == 5

    # A datasource should always return an object with a typed batch_id
    assert isinstance(batch.batch_kwargs, PathBatchKwargs)
    assert isinstance(batch.batch_markers, BatchMarkers)


def test_create_pandas_datasource(
    data_context_parameterized_expectation_suite, tmp_path_factory
):
    basedir = tmp_path_factory.mktemp("test_create_pandas_datasource")
    name = "test_pandas_datasource"
    class_name = "PandasDatasource"
    data_context_parameterized_expectation_suite.add_datasource(
        name,
        class_name=class_name,
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": str(basedir),
            }
        },
    )

    data_context_config = data_context_parameterized_expectation_suite.get_config()

    assert name in data_context_config["datasources"]
    assert data_context_config["datasources"][name]["class_name"] == class_name
    # assert data_context_config["datasources"][name]["type"] == type_

    # We should now see updated configs
    # Finally, we should be able to confirm that the folder structure is as expected
    with open(
        os.path.join(
            data_context_parameterized_expectation_suite.root_directory,
            "great_expectations.yml",
        ),
        "r",
    ) as data_context_config_file:
        data_context_file_config = yaml.load(data_context_config_file)

    assert (
        data_context_file_config["datasources"][name]
        == DataContextConfigSchema().dump(data_context_config)["datasources"][name]
    )

    # We should have added a default generator built from the default config
    assert (
        data_context_file_config["datasources"][name]["batch_kwargs_generators"][
            "subdir_reader"
        ]["class_name"]
        == "SubdirReaderBatchKwargsGenerator"
    )


def test_pandas_datasource_custom_data_asset(
    data_context_parameterized_expectation_suite, test_folder_connection_path
):
    name = "test_pandas_datasource"
    class_name = "PandasDatasource"

    data_asset_type_config = {
        "module_name": "custom_pandas_dataset",
        "class_name": "CustomPandasDataset",
    }
    data_context_parameterized_expectation_suite.add_datasource(
        name,
        class_name=class_name,
        data_asset_type=data_asset_type_config,
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": str(test_folder_connection_path),
            }
        },
    )

    # We should now see updated configs
    with open(
        os.path.join(
            data_context_parameterized_expectation_suite.root_directory,
            "great_expectations.yml",
        ),
        "r",
    ) as data_context_config_file:
        data_context_file_config = yaml.load(data_context_config_file)

    assert (
        data_context_file_config["datasources"][name]["data_asset_type"]["module_name"]
        == "custom_pandas_dataset"
    )
    assert (
        data_context_file_config["datasources"][name]["data_asset_type"]["class_name"]
        == "CustomPandasDataset"
    )

    # We should be able to get a dataset of the correct type from the datasource.
    data_context_parameterized_expectation_suite.create_expectation_suite(
        expectation_suite_name="test"
    )
    batch = data_context_parameterized_expectation_suite.get_batch(
        expectation_suite_name="test",
        batch_kwargs=data_context_parameterized_expectation_suite.build_batch_kwargs(
            datasource=name, batch_kwargs_generator="subdir_reader", name="test"
        ),
    )
    assert type(batch).__name__ == "CustomPandasDataset"
    res = batch.expect_column_values_to_have_odd_lengths("col_2")
    assert res.success is True


def test_pandas_source_read_csv(
    data_context_parameterized_expectation_suite, tmp_path_factory
):
    basedir = tmp_path_factory.mktemp("test_create_pandas_datasource")
    shutil.copy(file_relative_path(__file__, "../test_sets/unicode.csv"), basedir)
    data_context_parameterized_expectation_suite.add_datasource(
        "mysource",
        module_name="great_expectations.datasource",
        class_name="PandasDatasource",
        reader_options={"encoding": "utf-8"},
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": str(basedir),
            }
        },
    )

    data_context_parameterized_expectation_suite.create_expectation_suite(
        expectation_suite_name="unicode"
    )
    batch = data_context_parameterized_expectation_suite.get_batch(
        data_context_parameterized_expectation_suite.build_batch_kwargs(
            "mysource", "subdir_reader", "unicode"
        ),
        "unicode",
    )
    assert len(batch["Μ"] == 1)
    assert "😁" in list(batch["Μ"])

    data_context_parameterized_expectation_suite.add_datasource(
        "mysource2",
        module_name="great_expectations.datasource",
        class_name="PandasDatasource",
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": str(basedir),
            }
        },
    )

    batch = data_context_parameterized_expectation_suite.get_batch(
        data_context_parameterized_expectation_suite.build_batch_kwargs(
            "mysource2", "subdir_reader", "unicode"
        ),
        "unicode",
    )
    assert "😁" in list(batch["Μ"])

    data_context_parameterized_expectation_suite.add_datasource(
        "mysource3",
        module_name="great_expectations.datasource",
        class_name="PandasDatasource",
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": str(basedir),
                "reader_options": {"encoding": "utf-16"},
            }
        },
    )

    with pytest.raises(UnicodeError, match="UTF-16 stream does not start with BOM"):
        batch = data_context_parameterized_expectation_suite.get_batch(
            data_context_parameterized_expectation_suite.build_batch_kwargs(
                "mysource3", "subdir_reader", "unicode"
            ),
            "unicode",
        )

    with pytest.raises(LookupError, match="unknown encoding: blarg"):
        batch_kwargs = data_context_parameterized_expectation_suite.build_batch_kwargs(
            "mysource3", "subdir_reader", "unicode"
        )
        batch_kwargs.update({"reader_options": {"encoding": "blarg"}})
        batch = data_context_parameterized_expectation_suite.get_batch(
            batch_kwargs=batch_kwargs, expectation_suite_name="unicode"
        )

    with pytest.raises(LookupError, match="unknown encoding: blarg"):
        batch = data_context_parameterized_expectation_suite.get_batch(
            expectation_suite_name="unicode",
            batch_kwargs=data_context_parameterized_expectation_suite.build_batch_kwargs(
                "mysource",
                "subdir_reader",
                "unicode",
                reader_options={"encoding": "blarg"},
            ),
        )

    batch = data_context_parameterized_expectation_suite.get_batch(
        batch_kwargs=data_context_parameterized_expectation_suite.build_batch_kwargs(
            "mysource2",
            "subdir_reader",
            "unicode",
            reader_options={"encoding": "utf-8"},
        ),
        expectation_suite_name="unicode",
    )
    assert "😁" in list(batch["Μ"])


def test_invalid_reader_pandas_datasource(tmp_path_factory):
    basepath = str(tmp_path_factory.mktemp("test_invalid_reader_pandas_datasource"))
    datasource = PandasDatasource(
        "mypandassource",
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": basepath,
            }
        },
    )

    with open(
        os.path.join(basepath, "idonotlooklikeacsvbutiam.notrecognized"), "w"
    ) as newfile:
        newfile.write("a,b\n1,2\n3,4\n")

    with pytest.raises(BatchKwargsError) as exc:
        datasource.get_batch(
            batch_kwargs={
                "path": os.path.join(basepath, "idonotlooklikeacsvbutiam.notrecognized")
            }
        )
        assert "Unable to determine reader for path" in exc.value.message

    with pytest.raises(BatchKwargsError) as exc:
        datasource.get_batch(
            batch_kwargs={
                "path": os.path.join(
                    basepath, "idonotlooklikeacsvbutiam.notrecognized"
                ),
                "reader_method": "blarg",
            }
        )
        assert "Unknown reader method: blarg" in exc.value.message

    batch = datasource.get_batch(
        batch_kwargs={
            "path": os.path.join(basepath, "idonotlooklikeacsvbutiam.notrecognized"),
            "reader_method": "read_csv",
            "reader_options": {"header": 0},
        }
    )
    assert batch.data["a"][0] == 1


def test_read_limit(test_folder_connection_path):
    datasource = PandasDatasource(
        "PandasCSV",
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": test_folder_connection_path,
            }
        },
    )

    batch_kwargs = PathBatchKwargs(
        {
            "path": os.path.join(str(test_folder_connection_path), "test.csv"),
            "reader_options": {"sep": ",", "header": 0, "index_col": 0},
        }
    )
    nested_update(batch_kwargs, datasource.process_batch_parameters(limit=1))

    batch = datasource.get_batch(batch_kwargs=batch_kwargs)
    assert isinstance(batch, Batch)
    dataset = batch.data
    assert (dataset["col_1"] == [1]).all()
    assert len(dataset) == 1

    # A datasource should always return an object with a typed batch_id
    assert isinstance(batch.batch_kwargs, PathBatchKwargs)
    assert isinstance(batch.batch_markers, BatchMarkers)


def test_process_batch_parameters():
    batch_kwargs = PandasDatasource("test").process_batch_parameters(limit=1)
    assert batch_kwargs == {"reader_options": {"nrows": 1}}

    batch_kwargs = PandasDatasource("test").process_batch_parameters(
        dataset_options={"caching": False}
    )
    assert batch_kwargs == {"dataset_options": {"caching": False}}


def test_pandas_datasource_processes_dataset_options(test_folder_connection_path):
    datasource = PandasDatasource(
        "PandasCSV",
        batch_kwargs_generators={
            "subdir_reader": {
                "class_name": "SubdirReaderBatchKwargsGenerator",
                "base_directory": test_folder_connection_path,
            }
        },
    )
    batch_kwargs = datasource.build_batch_kwargs(
        "subdir_reader", data_asset_name="test"
    )
    batch_kwargs["dataset_options"] = {"caching": False}
    batch = datasource.get_batch(batch_kwargs)
    validator = Validator(batch, ExpectationSuite(expectation_suite_name="foo"))
    dataset = validator.get_dataset()
    assert dataset.caching is False
