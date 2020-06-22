# Copyright (c) 2017 Microsoft Corporation.  All rights reserved.
import os
import pathlib
import pickle
import unittest

import azureml.dataprep as dprep

from azureml.automl.core.shared.constants import Tasks
from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.runtime.shared.streaming_dataset import DatasetMetadataKeys, StreamingDataset


class StreamingDatasetTests(unittest.TestCase):
    """Tests for StreamingDataset."""

    initialized = False

    def __init__(self, *args, **kwargs):
        super(StreamingDatasetTests, self).__init__(*args, **kwargs)

        tests_dir_path = pathlib.Path(__file__).parent.parent.absolute()
        test_data_file = os.path.join(tests_dir_path, 'test_data', 'ts_utils', 'a10.csv')

        dflow = dprep.auto_read_file(test_data_file)
        dflow_valid, dflow = dflow.random_split(0.1, seed=42)

        label_column_name = 'quantity'
        self.X = dflow.drop_columns([label_column_name])
        self.y = dflow.keep_columns([label_column_name])
        self.X_valid = dflow_valid.drop_columns([label_column_name])
        self.y_valid = dflow_valid.keep_columns([label_column_name])

        feature_column_names = self.X.head(1).columns.values
        raw_data_snapshot = 'raw_data'

        self.classification_dataset = StreamingDataset(
            training_data=dflow, dataset_metadata={DatasetMetadataKeys.label_column_name: label_column_name,
                                                   DatasetMetadataKeys.feature_column_names: feature_column_names,
                                                   DatasetMetadataKeys.raw_data_snapshot: raw_data_snapshot},
            validation_data=dflow_valid, task=Tasks.CLASSIFICATION)
        self.regression_dataset = StreamingDataset(
            training_data=dflow, dataset_metadata={DatasetMetadataKeys.label_column_name: label_column_name,
                                                   DatasetMetadataKeys.feature_column_names: feature_column_names,
                                                   DatasetMetadataKeys.raw_data_snapshot: raw_data_snapshot},
            validation_data=dflow_valid, task=Tasks.REGRESSION)

    def test_get_class_labels(self):
        classes = self.classification_dataset.get_class_labels()
        self.assertLess(2, len(classes))

    def test_get_is_sparse(self):
        self.assertEqual(False, self.classification_dataset.get_is_sparse())

    def test_get_num_classes(self):
        num_classes = self.classification_dataset.get_num_classes()
        self.assertLess(2, num_classes)

    def test_get_num_classes_regression(self):
        with self.assertRaises(DataException):
            self.regression_dataset.get_num_classes()

    def test_get_problem_info(self):
        problem_info = self.classification_dataset.get_problem_info()
        self.assertEqual(False, problem_info.is_sparse)
        self.assertEqual(["date"], problem_info.feature_column_names)
        self.assertEqual("quantity", problem_info.label_column_name)
        self.assertEqual(True, problem_info.enable_streaming)

    def test_get_subsampled_dataset(self):
        initial_row_count = self.classification_dataset.get_X().shape[0]
        self.assertEqual(initial_row_count, 178)

        subsampled_dataset = self.classification_dataset.get_subsampled_dataset(50, 42)
        subsampled_row_count = subsampled_dataset.get_X().shape[0]
        self.assertEqual(subsampled_row_count, 86)
        self.assertEqual(subsampled_dataset.get_X().shape[0], subsampled_dataset.get_y().shape[0])
        self.assertEqual(None, subsampled_dataset.get_weight())

    def test_get_train_class_labels(self):
        classes = self.classification_dataset.get_train_class_labels()
        self.assertLess(2, len(classes))

    def test_get_X(self):
        X = self.classification_dataset.get_X()
        self.assertTrue(X.to_pandas_dataframe().equals(self.X.to_pandas_dataframe()))

    def test_get_y(self):
        y = self.classification_dataset.get_y()
        self.assertTrue(y.to_pandas_dataframe().equals(self.y.to_pandas_dataframe()))

    def test_get_X_valid(self):
        X_valid = self.classification_dataset.get_X_valid()
        self.assertTrue(X_valid.to_pandas_dataframe().equals(self.X_valid.to_pandas_dataframe()))

    def test_get_y_valid(self):
        y_valid = self.classification_dataset.get_y_valid()
        self.assertTrue(y_valid.to_pandas_dataframe().equals(self.y_valid.to_pandas_dataframe()))

    def test_get_train_set(self):
        X, y, sample_weight = self.classification_dataset.get_train_set()
        self.assertTrue(X.to_pandas_dataframe().equals(self.X.to_pandas_dataframe()))
        self.assertTrue(y.to_pandas_dataframe().equals(self.y.to_pandas_dataframe()))
        self.assertIsNone(sample_weight)

    def test_get_valid_set(self):
        X_valid, y_valid, sample_weight_valid = self.classification_dataset.get_valid_set()
        self.assertTrue(X_valid.to_pandas_dataframe().equals(self.X_valid.to_pandas_dataframe()))
        self.assertTrue(y_valid.to_pandas_dataframe().equals(self.y_valid.to_pandas_dataframe()))
        self.assertIsNone(sample_weight_valid)

    def test_pickle(self):
        pickled_dataset = pickle.dumps(self.classification_dataset)
        unpickled_dataset = pickle.loads(pickled_dataset)
        X, _, _ = unpickled_dataset.get_train_set()
        unpickled_X_rows = X.head(1000)
        original_X_rows = X.head(1000)
        self.assertTrue(original_X_rows.equals(unpickled_X_rows))

    def test_valid_metadata_keys(self):
        metadata_keys = {DatasetMetadataKeys.feature_column_names: ['col1'],
                         DatasetMetadataKeys.label_column_name: ['label'],
                         DatasetMetadataKeys.raw_data_snapshot: 'raw_data'}
        errors = DatasetMetadataKeys.validate_dataset_metadata(metadata_keys)
        self.assertFalse(errors, 'Expected no errors for a valid dataset metadata: {}'.format(errors))

    def test_invalid_metadata_keys(self):
        errors = DatasetMetadataKeys.validate_dataset_metadata({})
        self.assertTrue(len(errors) > 0,
                        'Expected a non-empty list of errors for the required keys of an empty metadata.')


if __name__ == '__main__':
    unittest.main()
