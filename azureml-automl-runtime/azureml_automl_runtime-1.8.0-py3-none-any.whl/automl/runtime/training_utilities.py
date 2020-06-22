# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities used during AutoML training."""
import warnings
from typing import Any, cast, Callable, Dict, List, Optional, Set, Tuple, Union

import logging
import numpy as np
import pandas as pd
import scipy
from sklearn.base import TransformerMixin
from sklearn.utils import validation as sk_validation

import azureml.dataprep as dprep

from azureml.automl.core.constants import FeatureType as _FeatureType
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.config_utilities import _check_validation_config
from azureml.automl.core.constants import FeaturizationConfigMode
from azureml.automl.runtime import dataprep_utilities, frequency_fixer
from azureml.automl.runtime._automl_settings_utilities import rule_based_validation
from azureml.automl.runtime.column_purpose_detection import ColumnPurposeDetector
from azureml.automl.runtime.data_context import TransformedDataContext
from azureml.automl.runtime.shared.utilities import _get_num_unique
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.automl.core.shared import constants
from azureml.automl.core.shared import utilities, logging_utilities
from azureml.automl.core.shared.exceptions import (AllLabelsMissingException,
                                                   ConfigException,
                                                   DataException,
                                                   DataFormatException,
                                                   DataSamplesSizeException,
                                                   DataShapeException,
                                                   EmptyDataException,
                                                   FeaturizationOffException,
                                                   InsufficientDataException,
                                                   InvalidDataTypeException,
                                                   LabelMissingException,
                                                   OutOfBoundDataException,
                                                   OutOfRangeException,
                                                   ScenarioNotSupportedException,
                                                   UnhashableEntryException,
                                                   InvalidValueException)
from azureml.automl.core.shared.forecasting_exception import (DataFrameFrequencyException,
                                                              DropSpecialColumn,
                                                              WrongShapeDataError,
                                                              InvalidTsdfArgument,
                                                              GrainAndTimeOverlapException,
                                                              GrainAbsent,
                                                              DataFrameTimeNotContinuous,
                                                              DataFrameFrequencyChanged,
                                                              DataFrameMissingColumnException,
                                                              DuplicatedIndexException)
from azureml.automl.runtime.shared import utilities as runtime_utilities
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.shared._cv_splits import _CVSplits
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import SubsampleCacheStrategy, ClientDatasets, DatasetBase
from azureml.automl.runtime.shared.streaming_dataset import StreamingDataset, DatasetMetadataKeys
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType
from azureml.dataprep.api.dataflow import DataflowValidationError
from .data_transformation import _add_raw_column_names_to_X
from azureml.automl.runtime.featurizer.transformer import TimeSeriesPipelineType, TimeSeriesTransformer
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal
from azureml.automl.runtime.featurizer.transformer.timeseries import forecasting_heuristic_utils
from azureml.automl.runtime.frequency_fixer import fix_data_set_regularity_may_be
from azureml.automl.runtime.shared import memory_utilities
from enum import Enum
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig

logger = logging.getLogger(__name__)

try:
    from azureml.dataprep import DataPrepException as DprepException
except ImportError:
    # TODO Task 748385. Clean up this branch once dataprep min version is updated to 1.6.0
    from azureml.dataprep import ExecutionError as DprepException

logger = logging.getLogger(__name__)


class ErrorLinks(Enum):
    """Constants to store the link to correct the errors."""
    DUPLICATED_INDEX = 'https://aka.ms/ForecastingConfigurations'


class SmallDataSetLimit:
    """Constants for the small dataset limit."""

    WARNING_SIZE = 100
    MINIMAL_TRAIN_SIZE = 50
    MINIMAL_VALIDATION_SIZE = int(MINIMAL_TRAIN_SIZE / 10)


class LargeDatasetLimit:
    """Constants for limiting large datasets."""

    MAX_ROWS_TO_SUBSAMPLE = 100000

    # Number of rows to  use for doing validations on the data
    VALIDATION_SUBSAMPLE_SIZE = 5000


MASKED = '[Masked]'


def auto_blacklist(input_data, automl_settings):
    """
    Add appropriate files to blacklist automatically.

    :param input_data:
    :param automl_settings: The settings used for this current run.
    :return:
    """
    if automl_settings.auto_blacklist:
        X = input_data['X']
        if scipy.sparse.issparse(X) or X.shape[0] > constants.MAX_SAMPLES_BLACKLIST:
            if automl_settings.blacklist_algos is None:
                automl_settings.blacklist_algos = \
                    constants.MAX_SAMPLES_BLACKLIST_ALGOS
            else:
                for blacklist_algo in constants.MAX_SAMPLES_BLACKLIST_ALGOS:
                    if blacklist_algo not in automl_settings.blacklist_algos:
                        automl_settings.blacklist_algos.append(blacklist_algo)
            automl_settings.blacklist_samples_reached = True


def set_task_parameters(y, automl_settings):
    """
    Set this task's parameters based on some heuristics if they aren't provided.

    TODO: Move this code into AutoML settings or something. Client shouldn't have to think about this stuff.

    :param automl_settings: The settings used for this current run
    :param y: The list of possible output values
    :return:
    """
    if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
        #  Guess number of classes if the user did not explicitly provide it
        if not automl_settings.num_classes or not isinstance(
                automl_settings.num_classes, int):
            automl_settings.num_classes = _get_num_unique(pd.Series(y))
        return

    if automl_settings.task_type == constants.Tasks.REGRESSION:
        numpy_unserializable_ints = (np.int8, np.int16, np.int32, np.int64,
                                     np.uint8, np.uint16, np.uint32, np.uint64)

        #  Guess min and max of y if the user did not explicitly provide it
        if not automl_settings.y_min or not isinstance(automl_settings.y_min,
                                                       float):
            automl_settings.y_min = np.min(y)
            if isinstance(automl_settings.y_min, numpy_unserializable_ints):
                automl_settings.y_min = int(automl_settings.y_min)
        if not automl_settings.y_max or not isinstance(automl_settings.y_max,
                                                       float):
            automl_settings.y_max = np.max(y)
            if isinstance(automl_settings.y_max, numpy_unserializable_ints):
                automl_settings.y_max = int(automl_settings.y_max)
        if automl_settings.y_max == automl_settings.y_min:
            raise InsufficientDataException("Minimum and maximum value of the label column is the same. "
                                            "Multiple values of the label column are required.", has_pii=False)
        return
    raise NotImplementedError()  # PII safe to raise directly


def format_training_data(
        X=None, y=None, sample_weight=None, X_valid=None, y_valid=None, sample_weight_valid=None,
        cv_splits_indices=None, user_script=None,
        training_data=None, validation_data=None, label_column_name=None, weight_column_name=None,
        cv_split_column_names=None, is_adb_run=False, automl_settings=None, logger=None, verifier=None):
    """
    Create a dictionary with training and validation data from all supported input formats.

    :param X: Training features.
    :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y: Training labels.
    :type y: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param sample_weight: Sample weights for training data.
    :type sample_weight: pandas.DataFrame pr numpy.ndarray or azureml.dataprep.Dataflow
    :param X_valid: validation features.
    :type X_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param y_valid: validation labels.
    :type y_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param sample_weight_valid: validation set sample weights.
    :type sample_weight_valid: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param cv_splits_indices:
        Indices where to split training data for cross validation.
        Each row is a separate cross fold and within each crossfold, provide 2 arrays,
        the first with the indices for samples to use for training data and the second
        with the indices to use for validation data. i.e [[t1, v1], [t2, v2], ...]
        where t1 is the training indices for the first cross fold and v1 is the validation
        indices for the first cross fold.
    :type cv_splits_indices: numpy.ndarray
    :param training_data: The training data to be used within the experiment.
    :type training_data: pandas.DataFrame or azureml.core.Dataset
        or azureml.data.dataset_definition.DatasetDefinition or azureml.data.TabularDataset
    :param validation_data: The validation data to be used within the experiment.
    :type validation_data: pandas.DataFrame or azureml.core.Dataset
        or azureml.data.dataset_definition.DatasetDefinition or azureml.data.TabularDataset
    :param label_column_name: The name of the label column.
    :type label_column_name: str
    :param weight_column_name: The name of the sample weight column.
    :type weight_column_name: str
    :param cv_split_column_names: List of names for columns that contain custom cross validation split.
    :type cv_split_column_names: list(str)
    :param user_script: File path to script containing get_data()
    :param is_adb_run: True if this is being called from an ADB/local experiment
    :param automl_settings: automl settings
    :param logger: logger
    :param verifier: Verifier Manager instance.
    :type verifier: Optional[VerifierManager]
    :return:
    """
    data_dict = None
    x_raw_column_names = None
    reset_index_msg = "Reset dataframe index to avoid potential conflicts if time/grain column is part of an index."

    if X is None and y is None and training_data is None:
        if data_dict is None:
            data_dict = _extract_user_data(user_script)
        X = data_dict.get('X')
        y = data_dict.get('y')
        sample_weight = data_dict.get('sample_weight')
        X_valid = data_dict.get('X_valid')
        y_valid = data_dict.get('y_valid')
        sample_weight_valid = data_dict.get('sample_weight_valid')
        cv_splits_indices = data_dict.get("cv_splits_indices")
        x_raw_column_names = data_dict.get("x_raw_column_names")
    elif training_data is not None and label_column_name is not None:
        if isinstance(training_data, pd.DataFrame):
            x_raw_column_names = training_data.columns.values
            X, y, sample_weight, cv_splits_indices = _extract_data_from_combined_dataframe(
                training_data=training_data, label_column_name=label_column_name,
                sample_weight_column_name=weight_column_name, cv_split_column_names=cv_split_column_names
            )

            if validation_data is not None:
                X_valid, y_valid, sample_weight_valid, _ = _extract_data_from_combined_dataframe(
                    training_data=validation_data, label_column_name=label_column_name,
                    sample_weight_column_name=weight_column_name
                )
        elif isinstance(training_data, dprep.Dataflow):
            X, y, sample_weight, cv_splits_indices = _extract_data_from_combined_dataflow(
                training_data=training_data, label_column_name=label_column_name,
                sample_weight_column_name=weight_column_name, cv_split_column_names=cv_split_column_names
            )

            if validation_data is not None:
                X_valid, y_valid, sample_weight_valid, _ = _extract_data_from_combined_dataflow(
                    training_data=validation_data, label_column_name=label_column_name,
                    sample_weight_column_name=weight_column_name
                )
            x_raw_column_names = X.head(1).columns.values

    # Get the raw column names
    if isinstance(X, pd.DataFrame):
        # reset index in case a customer's df contains index column(s)
        X.reset_index(inplace=True, drop=True)
        forecasting_heuristic_utils._log_warn_maybe(reset_index_msg)
        # Cache the raw column names if available
        x_raw_column_names = X.columns.values
    else:
        if is_adb_run:
            # Hack to make sure we get a pandas DF and not a numpy array in ADB
            # The two retrieval functions should be rationalized in future releases
            dataframe_retrieve_func = dataprep_utilities.retrieve_pandas_dataframe
        else:
            dataframe_retrieve_func = dataprep_utilities.retrieve_numpy_array
        X = dataframe_retrieve_func(X)
        if X_valid is not None:
            X_valid = dataframe_retrieve_func(X_valid)

        y = dataprep_utilities.retrieve_numpy_array(y)
        if y_valid is not None:
            y_valid = dataprep_utilities.retrieve_numpy_array(y_valid)

        if sample_weight is not None:
            sample_weight = dataprep_utilities.retrieve_numpy_array(sample_weight)
        if sample_weight_valid is not None:
            sample_weight_valid = dataprep_utilities.retrieve_numpy_array(sample_weight_valid)

        if cv_splits_indices is not None and cv_split_column_names is None:
            # cv_splits_indices NOT derived from cv_split_column_names so it still needs to resolve
            cv_splits_indices = dataprep_utilities.resolve_cv_splits_indices(cv_splits_indices)

        if isinstance(X, pd.DataFrame):
            # reset index in case a customer's df contains index column(s)
            X.reset_index(inplace=True, drop=True)
            forecasting_heuristic_utils._log_warn_maybe(reset_index_msg)
            x_raw_column_names = X.columns.values

    # reset index in case a customer's df contains index column(s)
    if X_valid is not None and isinstance(X_valid, pd.DataFrame):
        X_valid.reset_index(inplace=True, drop=True)
        forecasting_heuristic_utils._log_warn_maybe(reset_index_msg)

    if automl_settings is None or \
            (automl_settings.featurization == FeaturizationConfigMode.Off and not automl_settings.is_timeseries):
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(X_valid, pd.DataFrame):
            X_valid = X_valid.values
    y = _convert_to_numpy_maybe(y, 'y')
    y_valid = _convert_to_numpy_maybe(y_valid, 'y_valid')
    if isinstance(sample_weight, pd.DataFrame):
        sample_weight = sample_weight.values
    if isinstance(sample_weight_valid, pd.DataFrame):
        sample_weight_valid = sample_weight_valid.values
    if automl_settings is not None:

        # When data were read try to fix the frequency.
        if automl_settings.is_timeseries and X_valid is None:
            _check_dimensions(X, y, None, None, None, None)
            X, y, failed, was_corrected = fix_data_set_regularity_may_be(
                X, y,
                automl_settings.time_column_name,
                automl_settings.grain_column_names)
            if verifier:
                verifier.update_data_verifier_frequency_inference(failed, was_corrected)

        # auto cv needs the input X and y have same rows
        _check_dimensions(
            X=X, y=y, X_valid=X_valid, y_valid=y_valid,
            sample_weight=sample_weight, sample_weight_valid=sample_weight_valid)

        X, y, sample_weight, X_valid, y_valid, sample_weight_valid = rule_based_validation(
            automl_settings=automl_settings,
            X=X,
            y=y,
            sample_weight=sample_weight,
            X_valid=X_valid,
            y_valid=y_valid,
            sample_weight_valid=sample_weight_valid,
            cv_splits_indices=cv_splits_indices,
            verifier=verifier
        )

    data_dict = {
        'X': X,
        'y': y,
        'X_valid': X_valid,
        'y_valid': y_valid,
        'cv_splits_indices': cv_splits_indices,
        'x_raw_column_names': x_raw_column_names,
        'sample_weight': sample_weight,
        'sample_weight_valid': sample_weight_valid}
    return data_dict


def _convert_to_numpy_maybe(
        y: Optional[Union[np.ndarray, pd.DataFrame, pd.Series]],
        ds_name: str) -> Optional[np.ndarray]:
    """
    Try to convert y to numpy array.

    If y can not be converted to np.ndarray or has wrong shape the DataException is raised.
    :param y: The data set to be converted.
    :param ds_name: The name of the data set to convert.
    :raises: DataException
    """
    if y is None:
        return y
    if isinstance(y, pd.DataFrame):
        _check_y_shape(y, 'y')
        return y[y.columns[0]].values
    if isinstance(y, pd.Series):
        return y.values
    return y


def _check_y_shape(y: pd.DataFrame, ds_name: str) -> None:
    """
    Check if y data frame has only one column.

    :param y: The y dataframe.
    :param name: The name of a data set.
    :raises: DataShapeException
    """
    if y.shape[1] > 1:
        msg = ("Dimension mismatch for {} data. "
               "Expecting 1 dimensional array, "
               "but received {} dimensional data.")
        raise DataShapeException(
            msg.format(ds_name, y.shape[1]),
            target="y_shape",
            reference_code="64d623bb-72fc-4b93-885c-3838373d7c59",
            has_pii=False)


def validate_training_data(X: DataInputType,
                           y: DataInputType,
                           X_valid: Optional[DataInputType],
                           y_valid: Optional[DataInputType],
                           sample_weight: Optional[DataInputType],
                           sample_weight_valid: Optional[DataInputType],
                           cv_splits_indices: Optional[np.ndarray],
                           automl_settings: AutoMLBaseSettings,
                           check_sparse: bool = False,
                           logger: Optional[logging.Logger] = None,
                           x_raw_column_names: Optional[np.ndarray] = None) -> None:
    """
    Validate that training data and parameters have been correctly provided.

    :param X:
    :param y:
    :param X_valid:
    :param y_valid:
    :param sample_weight:
    :param sample_weight_valid:
    :param cv_splits_indices:
    :param automl_settings:
    :param check_sparse:
    :param x_raw_column_names: Raw column names as list of str.
    """
    # if using incremental learning, validate and subsample data inputs. subsampling the input Dataflows
    # to numpy arrays this allows the validation flow (which can handle numpy arrays but not
    # Dataflows directly at the moment) to proceed.

    check_x_y(X, y, automl_settings, x_valid=X_valid, y_valid=y_valid,
              check_sparse=check_sparse, logger=logger)

    # Ensure at least one form of validation is specified
    if not ((X_valid is not None) or automl_settings.n_cross_validations or
            (cv_splits_indices is not None) or automl_settings.validation_size):
        raise EmptyDataException(
            "No form of validation was provided. Please specify the data "
            "or type of validation you would like to use.",
            target="validation_data",
            has_pii=False)

    # validate sample weights if not None
    if sample_weight is not None:
        check_sample_weight(X, sample_weight, automl_settings)

    if sample_weight_valid is not None:
        check_sample_weight(X_valid, sample_weight_valid, automl_settings, True)

    _check_dimensions(
        X=X, y=y, X_valid=X_valid, y_valid=y_valid,
        sample_weight=sample_weight, sample_weight_valid=sample_weight_valid)

    _check_validation_config(X_valid=X_valid,
                             y_valid=y_valid,
                             sample_weight=sample_weight,
                             sample_weight_valid=sample_weight_valid,
                             cv_splits_indices=cv_splits_indices,
                             n_cross_validations=automl_settings.n_cross_validations,
                             validation_size=automl_settings.validation_size)

    if automl_settings.n_cross_validations is not None:
        if y.shape[0] < automl_settings.n_cross_validations:
            msg = "Number of training rows ({}) is less than total requested CV splits ({}). " \
                  "Please reduce the number of splits requested."
            raise ConfigException(msg.format(y.shape[0], automl_settings.n_cross_validations))\
                .with_generic_msg(msg.format(MASKED, MASKED))

    # streaming uses subsampling + streaming does not use pandas, so the following isn't applicable - hence skip
    if automl_settings.featurization != FeaturizationConfigMode.Off and not automl_settings.enable_streaming:
        _check_data_can_be_preprocessed(X, X_valid, x_raw_column_names)

    metrics_checks(X, y, automl_settings, X_valid, y_valid)

    _validate_exp_timeout_for_data(X, automl_settings)
    _validate_featurization_config(automl_settings.featurization, x_raw_column_names)

    _validate_all_column_not_ignored(X, x_raw_column_names, automl_settings)


def validate_streaming_data(
        training_data: dprep.Dataflow,
        automl_settings: AutoMLBaseSettings,
        validation_data: Optional[dprep.Dataflow] = None) -> None:
    """
    If streaming is enabled, we do a best effort based validation of the inputs (due to potentially large data
    sizes), in order to not run out of memory.

    Note: We should refactor this method to have a strong contract in terms of what's expected as inputs. Currently,
    validation_data is optional, but under most (known) circumstances, this is always passed down from the caller.
    This is losely enforced as of now, i.e. it can be None, given the user had specified a validation_size. But for
    streaming, we always do a split of training data into validation data, either based on heuristics, or user given
    validation_size. This should be strongly enforced after subsequent refactorings.

    :param training_data: Input training data provided by the user
    :param automl_settings: AutoML configuration
    :param validation_data: Optional Validation data that the user can provide
    :return: None, if the validation succeeds
    """

    input_must_be_dataflow_warning = "If using incremental learning, {} needs to be an Azure ML Dataflow"

    if not isinstance(training_data, dprep.Dataflow):
        raise InvalidDataTypeException(
            input_must_be_dataflow_warning.format('training_data'), target="training_data",
            reference_code=ReferenceCodes._STREAMING_INVALID_TRAINING_DATATYPE, has_pii=False)

    if validation_data is not None and not isinstance(validation_data, dprep.Dataflow):
        raise InvalidDataTypeException(
            input_must_be_dataflow_warning.format('validation_data'), target="validation_data",
            reference_code=ReferenceCodes._STREAMING_INVALID_VALIDATION_DATATYPE, has_pii=False)

    label_column_name = automl_settings.label_column_name
    weight_column_name = automl_settings.weight_column_name

    columns_list = [label_column_name]
    if weight_column_name:
        columns_list.append(weight_column_name)

    X = training_data.drop_columns(columns_list)
    y = training_data.keep_columns(label_column_name)

    X_valid = None  # type: Optional[DataInputType]
    y_valid = None  # type: Optional[DataInputType]
    # We don't need to set X_valid / y_valid in case the user specified validation_size, since in this case the
    # validation data is just a part of the overall training data.
    if automl_settings.validation_size == 0 and validation_data:
        X_valid = validation_data.drop_columns(columns_list)
        y_valid = validation_data.keep_columns(label_column_name)

    sample_weight = None  # type: Optional[DataInputType]
    sample_weight_valid = None  # type: Optional[DataInputType]
    if weight_column_name:
        sample_weight = training_data.keep_columns(weight_column_name)
        if automl_settings.validation_size == 0 and validation_data:
            sample_weight_valid = validation_data.keep_columns(weight_column_name)

    X, y, X_valid, y_valid, sample_weight, sample_weight_valid = _incremental_learning_validate_and_subsample_inputs(
        X, y, X_valid, y_valid, sample_weight, sample_weight_valid)

    validate_training_data(X=X, y=y, X_valid=X_valid, y_valid=y_valid, sample_weight=sample_weight,
                           sample_weight_valid=sample_weight_valid, cv_splits_indices=None,
                           automl_settings=automl_settings)


def _incremental_learning_validate_and_subsample_inputs(
    X: dprep.Dataflow,
    y: dprep.Dataflow,
    X_valid: Optional[dprep.Dataflow] = None,
    y_valid: Optional[dprep.Dataflow] = None,
    sample_weight: Optional[dprep.Dataflow] = None,
    sample_weight_valid: Optional[dprep.Dataflow] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    If using incremental learning, validate and subsample data inputs.
    Subsampling the input Dataflows to numpy arrays this allows the validation flow (which
    can handle numpy arrays but not Dataflows directly at the moment) to proceed.

    :param X:
    :param y:
    :param X_valid:
    :param y_valid:
    :param sample_weight:
    :param sample_weight_valid:
    """
    try:
        # validate that y is only a single column
        y_column_count = len(y.head(1).columns)
        if y_column_count != 1:
            msg = 'y must contain only a single column, but {} columns were found'
            raise DataShapeException(msg.format(y_column_count)).with_generic_msg(msg.format(MASKED))

        # validate that column names are unique between X and y
        # (this is required, b/c we append the columns of X and y together to get a single merged Dataflow
        # that nimbus learners require as input. if X and y have shared column names, this merge throws an error)
        X_column_names = X.head(1).columns.tolist()
        y_column_name = y.head(1).columns[0]
        if y_column_name in X_column_names:
            msg = 'The label column name {} was found in X. Please rename this column in X'
            raise LabelMissingException(
                msg.format(y_column_name),
                target="label_column_name", reference_code="21e7224b-fb15-42de-ac1c-85f10798911d",
                has_pii=True).with_generic_msg(msg.format(MASKED))

        # validate that the Datatypes are the same for X and y (for training, validation and sample weight data)
        for train, valid in [(X, X_valid), (y, y_valid), (sample_weight, sample_weight_valid)]:
            _check_datatypes(train, valid)

        # generate subsampled numpy arrays
        X = X.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).to_pandas_dataframe().values
        y = y.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).to_pandas_dataframe().iloc[:, 0].values
        if X_valid is not None:
            X_valid = X_valid.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).to_pandas_dataframe().values
        if y_valid is not None:
            y_valid = y_valid.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).to_pandas_dataframe().iloc[:, 0].values
        if sample_weight is not None:
            sample_weight = (sample_weight.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).
                             to_pandas_dataframe().iloc[:, 0].values)
        if sample_weight_valid is not None:
            sample_weight_valid = (sample_weight_valid.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).
                                   to_pandas_dataframe().iloc[:, 0].values)
    except DprepException as e:
        logging_utilities.log_traceback(e, logger)
        dataprep_utilities.dataprep_error_handler(e)

    return X, y, X_valid, y_valid, sample_weight, sample_weight_valid


def _check_datatypes(training_data: dprep.Dataflow, validation_data: dprep.Dataflow) -> None:
    if training_data is not None and validation_data is not None:
        train_dtypes = (training_data.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).dtypes.items())
        valid_dtypes = (validation_data.take(LargeDatasetLimit.VALIDATION_SUBSAMPLE_SIZE).dtypes.items())

        for (train_col, train_datatype), (valid_col, valid_datatype) in zip(train_dtypes, valid_dtypes):
            if train_datatype != valid_datatype and train_col == valid_col:
                msg_format = 'Datatype for column {} was detected as {} in the training set, but was found ' \
                             'to be {} in the validation set. Please ensure that the datatypes between ' \
                             'training and validation sets are aligned.'
                msg = msg_format.format(train_col, train_datatype, valid_datatype)
                generic_msg = msg_format.format(MASKED, MASKED, MASKED)
                raise InvalidDataTypeException(msg).with_generic_msg(generic_msg)


def validate_training_data_dict(data_dict: Dict[str, Any],
                                automl_settings: AutoMLBaseSettings,
                                logger: Optional[logging.Logger] = None,
                                check_sparse: bool = False) -> None:
    """
    Validate that training data and parameters have been correctly provided.

    :param data_dict: Key-Value pair containing information about user provided data
    :param automl_settings: AutoML configuration
    :param logger:
    :param check_sparse:
    :return:
    """
    if automl_settings.enable_streaming:
        if data_dict.get('cv_splits_indices') is not None:
            raise ConfigException("Streaming is enabled due to the size of the data."
                                  "'cv_splits_indices' option is not supported. Please re-run without that setting.",
                                  has_pii=False)

        training_data = data_dict.get('training_data')
        validation_data = data_dict.get('validation_data')

        validate_streaming_data(training_data, automl_settings, validation_data)
        if logger:
            logger.info("Streaming was enabled, successfully validated data.")
        return

    X = data_dict.get('X', None)
    y = data_dict.get('y', None)
    sample_weight = data_dict.get('sample_weight', None)
    X_valid = data_dict.get('X_valid', None)
    y_valid = data_dict.get('y_valid', None)
    sample_weight_valid = data_dict.get('sample_weight_valid', None)
    cv_splits_indices = data_dict.get('cv_splits_indices', None)
    x_raw_column_names = data_dict.get('x_raw_column_names', None)
    validate_training_data(X, y, X_valid, y_valid, sample_weight, sample_weight_valid, cv_splits_indices,
                           automl_settings, check_sparse=check_sparse, x_raw_column_names=x_raw_column_names)
    if automl_settings.is_timeseries:
        validate_timeseries_training_data(automl_settings, X, y, X_valid, y_valid,
                                          sample_weight, sample_weight_valid, cv_splits_indices,
                                          x_raw_column_names)


def metrics_checks(x: DataInputType,
                   y: DataInputType,
                   automl_settings: AutoMLBaseSettings,
                   x_valid: Optional[DataInputType] = None,
                   y_valid: Optional[DataInputType] = None) -> None:
    """
    Validate input data for metrics.

    :param x: input data. dataframe/ array/ sparse matrix
    :param y: input labels. dataframe/series/array
    :param automl_settings: automl settings
    :raise: InsufficientDataException if data is not suitable for metrics calculations
    :return:
    """
    if y_valid is not None:
        # since we subsample the data for streaming following calculations may be inaccurate - hence skip them
        if automl_settings.task_type == constants.Tasks.CLASSIFICATION and not automl_settings.enable_streaming:
            primary_metric = automl_settings.primary_metric
            if primary_metric == constants.Metric.AUCWeighted:
                in_valid = set(y_valid[~pd.isnull(y_valid)])
                if len(in_valid) == 1:
                    remaining_metrics = utilities.get_primary_metrics(constants.Tasks.CLASSIFICATION).copy()
                    remaining_metrics.remove(primary_metric)
                    msg = ("y_valid is single valued. "
                           "Please make sure that y_valid is well represented with all classes "
                           "for classification task. Or please try one of {} as primary metrics")
                    raise InsufficientDataException(
                        msg.format(remaining_metrics)).with_generic_msg(msg.format(MASKED))


def check_x_y(x: DataInputType,
              y: DataInputType,
              automl_settings: AutoMLBaseSettings,
              x_valid: Optional[DataInputType] = None,
              y_valid: Optional[DataInputType] = None,
              check_sparse: bool = False,
              logger: Optional[logging.Logger] = None) -> None:
    """
    Validate input data.

    :param x: input data. dataframe/ array/ sparse matrix
    :param y: input labels. dataframe/series/array
    :param automl_settings: automl settings
    :raise: DataException if data does not conform to accepted types and shapes
    :return:
    """

    if logger is not None:
        logger.info('Checking X and y.')

    is_timeseries = automl_settings.is_timeseries

    if x is None:
        raise EmptyDataException("X should not be None", has_pii=False)

    if y is None:
        raise EmptyDataException("y should not be None", has_pii=False)

    is_featurization_enabled = automl_settings.featurization != FeaturizationConfigMode.Off

    if isinstance(x, pd.DataFrame):
        if len(x.columns) != len(set(x.columns)):
            raise DataFormatException("There are duplicate column names in your raw data", has_pii=False)
        if x_valid is not None and isinstance(x, pd.DataFrame) and isinstance(x_valid, pd.DataFrame):
            if len(x.columns.intersection(x_valid.columns)) != len(x.columns):
                raise DataFormatException(
                    "Validation data does not have the same set of columns as training data", has_pii=False)

    if x_valid is not None:
        error_msg = "Training and validation data don't have the same number of columns. " \
            "Training data has {0} columns and validation data has {1} columns."
        if len(x.shape) > 1:
            if len(x_valid.shape) > 1 and x.shape[1] != x_valid.shape[1]:
                raise DataShapeException(error_msg.format(x.shape[1], x_valid.shape[1]), has_pii=False)
            elif len(x_valid.shape) == 1 and x.shape[1] != 1:
                raise DataShapeException(error_msg.format(x.shape[1], 1), has_pii=False)
        elif len(x_valid.shape) > 1 and x_valid.shape[1] != 1:
            raise DataShapeException(error_msg.format(1, x_valid.shape[1]), has_pii=False)

    if not (((is_featurization_enabled or is_timeseries) and isinstance(x, pd.DataFrame)) or
            isinstance(x, np.ndarray) or scipy.sparse.issparse(x)):
        raise InvalidDataTypeException(
            "x should be dataframe with featurization set or numpy array"
            " or sparse matrix", has_pii=False)

    if (check_sparse and scipy.sparse.issparse(x) and
        (automl_settings.enable_onnx_compatible_models is True or
         automl_settings.enable_onnx_compatible_models == "True")):
        raise InvalidDataTypeException(
            "x should not be a sparse matrix when enable_onnx_compatible_models is True."
            "ONNX currently does not support sparse data.", has_pii=False)

    if not isinstance(y, np.ndarray):
        raise InvalidDataTypeException("y should be numpy array", has_pii=False)

    if len(y.shape) > 2 or (len(y.shape) == 2 and y.shape[1] != 1):
        raise DataShapeException("y should be a vector Nx1", has_pii=False)

    if y is not None:
        if len(runtime_utilities._get_indices_missing_labels_output_column(y)) == y.shape[0]:
            raise AllLabelsMissingException("y has all missing labels", has_pii=False)

    if y_valid is not None:
        if len(runtime_utilities._get_indices_missing_labels_output_column(y_valid)) == y_valid.shape[0]:
            raise AllLabelsMissingException("y_valid has all missing labels", has_pii=False)

    if automl_settings.task_type == constants.Tasks.REGRESSION:
        if not utilities._check_if_column_data_type_is_numerical(
                runtime_utilities._get_column_data_type_as_str(y)):
            raise InvalidDataTypeException(
                "Please make sure y is numerical before fitting for "
                "regression", has_pii=False)

    # If text data is not being preprocessed or featurized, then raise an error
    if not is_featurization_enabled and not is_timeseries:
        without_featurization_error_str = \
            "The training data contains {}, {} or {} data. Please turn on featurization by setting it as 'auto' " \
            "or giving custom featurization settings".format(
                _FeatureType.DateTime.lower(),
                _FeatureType.Categorical.lower(),
                _FeatureType.Text.lower())
        all_columns_excluded_str = "x should contain at least one column with at least two unique values to train."

        # counter to keep track of how many numerical columns are marked as Ignore or AllNan type
        numeric_column_drop_set_counter = 0
        if isinstance(x, pd.DataFrame):
            for column in x.columns:
                if not utilities._check_if_column_data_type_is_numerical(
                        runtime_utilities._get_column_data_type_as_str(x[column].values)):
                    raise InvalidDataTypeException(without_featurization_error_str, has_pii=False)
                elif _is_numeric_x_part_of_drop_set(x[column]):
                    numeric_column_drop_set_counter += 1
            if numeric_column_drop_set_counter == len(x.columns):
                raise EmptyDataException(all_columns_excluded_str, has_pii=False)
        elif isinstance(x, np.ndarray):
            if len(x.shape) == 1:
                if not utilities._check_if_column_data_type_is_numerical(
                        runtime_utilities._get_column_data_type_as_str(x)):
                    raise FeaturizationOffException(without_featurization_error_str)
                elif _is_numeric_x_part_of_drop_set(pd.Series(x)):
                    raise EmptyDataException(all_columns_excluded_str, has_pii=False)
            else:
                for index in range(x.shape[1]):
                    if not utilities._check_if_column_data_type_is_numerical(
                            runtime_utilities._get_column_data_type_as_str(x[:, index])):
                        raise FeaturizationOffException(without_featurization_error_str)
                    elif _is_numeric_x_part_of_drop_set(pd.Series(x[:, index])):
                        numeric_column_drop_set_counter += 1
                if numeric_column_drop_set_counter == x.shape[1]:
                    raise EmptyDataException(all_columns_excluded_str, has_pii=False)

    # since we subsample the data for streaming following calculations may be inaccurate - hence skip them
    if automl_settings.task_type == constants.Tasks.CLASSIFICATION and not automl_settings.enable_streaming:
        y_ravel = y.ravel()
        unique_classes = _get_num_unique(y_ravel)
        if unique_classes < 2:
            raise InsufficientDataException(
                "At least two distinct classes are required for a classification task. "
                "Please check the target feature y.", has_pii=False)
        elif unique_classes == y_ravel.shape[0]:
            raise InsufficientDataException(
                "For a classification task, the label cannot be unique for every sample.",
                has_pii=False)

    # not check x Nan if featurization is enabled.
    check_x_nan = not is_featurization_enabled
    # not check NaN in y data as we will automatically remove these data in the data_transformation.py.
    check_y_nan = False
    # always check x contains inf or not.
    check_x_inf = True
    # check y contains inf data raise errors and only in regression.
    check_y_inf = automl_settings.task_type != constants.Tasks.CLASSIFICATION
    _check_data_nan_inf(
        x, input_data_name="X", check_nan=check_x_nan, check_inf=check_x_inf)
    _check_data_nan_inf(y, input_data_name="y", check_nan=check_y_nan, check_inf=check_y_inf)
    # forecasting task has its own check for minimal data check here for regression and classification.
    if not automl_settings.is_timeseries:
        _check_data_minimal_size(x, x_valid, automl_settings)
    if x_valid is not None:
        _check_data_nan_inf(
            x_valid, input_data_name="X_valid", check_nan=check_x_nan, check_inf=check_x_inf)
    if y_valid is not None:
        _check_data_nan_inf(
            y_valid, input_data_name="y_valid", check_nan=check_y_nan, check_inf=check_y_inf)


def _is_numeric_x_part_of_drop_set(x: pd.Series) -> bool:
    # Numerical column with feature type of Ignore or AllNan does not go through featurization.
    # If dataset contains all numerical with Ignore or AllNan, then we should alert the user.
    non_na_raw_column = x.dropna()
    return not non_na_raw_column.shape[0] or non_na_raw_column.unique().shape[0] == 1


def _check_data_minimal_size(X: DataInputType, X_valid: DataInputType, automl_settings: AutoMLBaseSettings) -> None:
    """Check if the data is larger than minimum size."""

    if X.shape[0] < SmallDataSetLimit.MINIMAL_TRAIN_SIZE:
        msg = "The input data X has {} data points which is less than the minimum requirement size of {}. " \
              "Please add more data to avoid future exceptions."
        raise DataSamplesSizeException(
            msg.format(X.shape[0], SmallDataSetLimit.MINIMAL_TRAIN_SIZE),
            target="X").with_generic_msg(msg.format(MASKED, SmallDataSetLimit.MINIMAL_TRAIN_SIZE))
    if X_valid is not None and X_valid.shape[0] < SmallDataSetLimit.MINIMAL_VALIDATION_SIZE:
        msg = "The input data X_valid has {} data points which is less than the minimum requirement size of {}. "\
              "Please add more data to avoid future exceptions."
        raise DataSamplesSizeException(
            msg.format(X_valid.shape[0], SmallDataSetLimit.MINIMAL_VALIDATION_SIZE),
            target="X_valid").with_generic_msg(msg.format(MASKED, SmallDataSetLimit.MINIMAL_VALIDATION_SIZE))
    if X.shape[0] < SmallDataSetLimit.WARNING_SIZE:
        warnings.warn(
            "The input data X has {} data points which is less than the recommended "
            "minimum data size {}. Please consider adding more data points to ensure better model accuracy.".
            format(X.shape[0], SmallDataSetLimit.WARNING_SIZE)
        )


def _check_data_nan_inf(data: DataInputType,
                        input_data_name: str,
                        check_nan: bool,
                        check_inf: bool = True) -> None:
    """Check if data contains nan or inf. If contains NaN, give out warning. If contains inf, raise exception."""
    if isinstance(data, pd.DataFrame):
        data_type = data.dtypes.dtype
    else:
        data_type = data.dtype
    is_integer_data = data_type.char in np.typecodes['AllInteger']
    n_top_indices = 20
    try:
        # The sklearn validation can be found here. If a dataset failed sklearn validation, it cannot be trained
        # by most of our pipeline.
        # https://github.com/scikit-learn/scikit-learn/blob/0.19.X/sklearn/utils/validation.py
        sk_validation.assert_all_finite(data)
        if check_nan and is_integer_data:
            # if the data is all integer, we will have a nan check beyond what sklearn does.
            input_data = data.data if scipy.sparse.issparse(data) else data
            if any(np.isnan(input_data)):
                raise ValueError
    except ValueError:
        # looking for nan and inf for the data. If the data contains other type, it will used in other checks.
        if data_type.char in np.typecodes['AllFloat'] or (check_nan and is_integer_data):
            if check_nan:
                nan_indices = _get_data_indices_by_mask_function(data, np.isnan)
                if nan_indices.shape[0] > 0:
                    print(
                        "WARNING: The following coordinates{} [{}] contains {} NaN(np.NaN) data in {}. "
                        "Please consider dropping these rows.".
                        format(_construct_coord_indices_str(nan_indices, n_top_indices),
                               "" if nan_indices.shape[0] < n_top_indices else "(first detected in each column)",
                               nan_indices.shape[0],
                               input_data_name)
                    )
            if check_inf:
                inf_indices = _get_data_indices_by_mask_function(data, np.isinf)
                if inf_indices.shape[0] > 0:
                    msg = ("The following coordinates{} [{}] contains {} infinity(np.inf) data in {}. "
                           "Please consider dropping these rows.")
                    raise OutOfBoundDataException(
                        msg.
                        format(_construct_coord_indices_str(inf_indices, n_top_indices),
                               "" if inf_indices.shape[0] < n_top_indices else "(first detected in each column)",
                               inf_indices.shape[0],
                               input_data_name)
                    ).with_generic_msg(msg.format(MASKED, MASKED, MASKED, MASKED))


def _construct_coord_indices_str(data_indices: np.ndarray, n_top_indices: int = 20) -> str:
    """Contruct a string with top 20 indices."""
    if data_indices.ndim == 1 or data_indices.shape[1] == 1:
        indices = sorted(data_indices)
    else:
        indices = sorted(data_indices, key=lambda x: (x[1], x[0]))
    if len(indices) <= n_top_indices:
        print_indices = data_indices
        return ", ".join([str(idx) for idx in print_indices])
    else:
        if data_indices.ndim == 1:
            print_indices = data_indices[:n_top_indices]
        else:
            col_idx_dict = {}  # type: Dict[int, List[np.ndarray]]
            for idx in indices:
                if idx[1] not in col_idx_dict:
                    col_idx_dict[idx[1]] = [idx]
                else:
                    col_idx_dict[idx[1]].append(idx)
            top_indices = sorted(col_idx_dict.keys(), key=lambda x: len(col_idx_dict[x]))
            if len(top_indices) > n_top_indices:
                print_indices = [col_idx_dict[idx][0] for idx in top_indices[:n_top_indices]]
            else:
                print_indices = [col_idx_dict[idx][0] for idx in top_indices]
        return ", ".join([str(idx) for idx in print_indices]) + "..."


def _get_data_indices_by_mask_function(data: DataInputType,
                                       mask_function: 'Callable[..., Optional[Any]]') -> np.ndarray:
    """Obtain the indices list where the data entry in data has the mask function evaluated as True."""
    if isinstance(data, np.ndarray) or isinstance(data, pd.DataFrame):
        return np.argwhere(mask_function(data))
    elif scipy.sparse.issparse(data):
        coo_data = scipy.sparse.coo_matrix(data)
        return np.array(
            [(coo_data.row[i], coo_data.col[i]) for i in np.argwhere(mask_function(coo_data.data)).ravel()])


def check_sample_weight(x: DataInputType,
                        sample_weight: np.ndarray,
                        automl_settings: AutoMLBaseSettings,
                        is_validation_data: bool = False) -> None:
    """
    Validate sample_weight.

    :param x:
    :param sample_weight:
    :param x_name:
    :param sample_weight_name:
    :param automl_settings:
    :raise DataException if sample_weight has problems
    :return:
    """
    sample_weight_name = "sample_weight_valid" if is_validation_data else "sample_weight"
    x_name = "X_valid" if is_validation_data else "X"
    if not isinstance(sample_weight, np.ndarray):
        raise InvalidDataTypeException(
            sample_weight_name + " should be numpy array",
            has_pii=False,
            target="check_sample_weight",
            reference_code=ReferenceCodes._VALIDATE_SAMPLE_WEIGHTS_NDARRAY
        )

    if x.shape[0] != len(sample_weight):
        raise DataShapeException(
            sample_weight_name + " length should match length of " + x_name,
            has_pii=False,
            target="check_sample_weight",
            reference_code=ReferenceCodes._VALIDATE_SAMPLE_WEIGHTS_NUM_RECORD
        )

    if len(sample_weight.shape) > 1:
        raise DataShapeException(
            sample_weight_name + " should be a unidimensional vector",
            has_pii=False,
            target="check_sample_weight",
            reference_code=ReferenceCodes._VALIDATE_SAMPLE_WEIGHTS_SHAPE
        )

    if automl_settings.primary_metric in \
            constants.Metric.SAMPLE_WEIGHTS_UNSUPPORTED_SET:
        raise ScenarioNotSupportedException(
            sample_weight_name + " is not supported for these primary metrics: {0}"
            .format(constants.Metric.SAMPLE_WEIGHTS_UNSUPPORTED_SET),
            has_pii=False,
            target="check_sample_weight",
            reference_code=ReferenceCodes._VALIDATE_SAMPLE_WEIGHTS_METRIC
        )

    sample_weight_dtype = runtime_utilities._get_column_data_type_as_str(sample_weight)
    if not utilities._check_if_column_data_type_is_numerical(sample_weight_dtype):
        raise InvalidDataTypeException(
            sample_weight_name + " is of type {}. "
            "Please make sure sample weight consists of non-negative numerical values.".format(sample_weight_dtype),
            has_pii=False,
            target="check_sample_weight",
            reference_code=ReferenceCodes._VALIDATE_SAMPLE_WEIGHTS_IS_NUMERIC
        )

    sample_weight_min = np.amin(sample_weight)
    if sample_weight_min < 0:
        raise OutOfRangeException(
            sample_weight_name + " contains negative value(s). "
            "Please make sure sample weight caontains values greater than or equal to 0.",
            has_pii=False,
            target="check_sample_weight",
            reference_code=ReferenceCodes._VALIDATE_SAMPLE_WEIGHTS_IN_RANGE
        )


def validate_timeseries_training_data(automl_settings: AutoMLBaseSettings,
                                      X: DataInputType,
                                      y: DataInputType,
                                      X_valid: Optional[DataInputType] = None,
                                      y_valid: Optional[DataInputType] = None,
                                      sample_weight: Optional[np.ndarray] = None,
                                      sample_weight_valid: Optional[np.ndarray] = None,
                                      cv_splits_indices: Optional[np.ndarray] = None,
                                      x_raw_column_names: Optional[np.ndarray] = None) -> None:
    """
    Quick check of the timeseries input values, no tsdf is required here.

    :param X: Training data.
    :type X: pandas.DataFrame or numpy.ndarray or azureml.dataprep.Dataflow
    :param automl_settings: automl settings
    """
    if automl_settings.grain_column_names is None:
        grain_set = set()  # type: Set[str]
    else:
        grain_set = set(automl_settings.grain_column_names)
    if automl_settings.drop_column_names is not None:
        drop_set = set(automl_settings.drop_column_names) if isinstance(
            automl_settings.drop_column_names, list) else set([automl_settings.drop_column_names])
        if (automl_settings.time_column_name in drop_set):
            raise DropSpecialColumn("Time column cannot be dropped. Please remove it from the drop column list.",
                                    has_pii=False)
            # Check if grain columns are overlapped with drop columns.
        if automl_settings.grain_column_names is not None:
            if drop_set.intersection(grain_set):
                raise DropSpecialColumn("Grain column cannot be dropped. Please remove it from the drop column list.",
                                        has_pii=False)
    if automl_settings.time_column_name in grain_set:
        raise GrainAndTimeOverlapException(
            "Time column name is present in the grain columns. Please remove it from grain list.", has_pii=False)

    if automl_settings.n_cross_validations is None and X_valid is None:
        raise InvalidTsdfArgument(
            "Time-series only supports rolling-origin cross validation and train/validate splits."
            "Provide either a n_cross_validations parameter or a validation dataset.",
            has_pii=False)
    elif cv_splits_indices is not None or \
            (automl_settings.validation_size is not None and automl_settings.validation_size > 0.0):
        if cv_splits_indices is not None:
            error_validation_config = "cv_splits_indices"
        else:
            error_validation_config = "validation_size"
        msg = ("The {} parameter is incompatible with time-series when using rolling-origin cross validation. "
               "Please remove the {} parameter.")
        raise InvalidTsdfArgument(
            msg.format(error_validation_config, error_validation_config),
        ).with_generic_msg(msg.format('[Masked]', '[Masked]'))
    else:
        lags, window_size, max_horizon = _get_auto_parameters_maybe(automl_settings, X, y)
        min_points = utilities.get_min_points(
            window_size,
            lags,
            max_horizon,
            automl_settings.n_cross_validations)
        if X.shape[0] < min_points:
            # Uncomment when the forecasting exceptions are PII safe
            pii_message = (
                "The data points should have at least {} for a valid training with cv {}, max_horizon {}, lags {} "
                "and rolling window size {}. The current dataset has only {} points. Please consider reducing your "
                "horizon, the number of cross validations, lags or rolling window size."
                .format(
                    min_points, automl_settings.n_cross_validations, max_horizon,
                    lags, window_size, X.shape[0]
                )
            )
            raise WrongShapeDataError(
                exception_message="The data provided is insufficient for training.",
                pii_message=pii_message)
        tsdf = _check_timeseries_input_and_get_tsdf(
            X, y, x_raw_column_names, automl_settings, max_horizon, min_points, is_validation_data=False)
        tsdf_valid = None
        if X_valid is not None:
            tsdf_valid = _check_timeseries_input_and_get_tsdf(
                X_valid,
                y_valid,
                x_raw_column_names,
                automl_settings,
                max_horizon,
                min_points=0,
                is_validation_data=True)
            _validate_timeseries_train_valid_tsdf(tsdf, tsdf_valid, bool(window_size + max(lags)))


def _validate_featurization_config(featurization: Union[str, Dict[str, Any]],
                                   x_raw_column_name: Optional[np.ndarray]) -> None:
    """
    Check if columns with custom purpose or featurization are present in the column list.

    :param featurization: The featurization config object.
    :param x_raw_column_name: the data frame column names.
    :raises: InvalidValueException
    """
    if x_raw_column_name is None:
        return
    if isinstance(featurization, FeaturizationConfig):
        if featurization.column_purposes is not None:
            for col in featurization.column_purposes.keys():
                if col not in x_raw_column_name:
                    msg = ("The column \'{}\' specified in the "
                           "FeaturizationConfig purpose columns "
                           "is not present in the data frame.")
                    raise InvalidValueException(
                        msg.format(col),
                        reference_code=ReferenceCodes._VALIDATE_FEATURIZATION_PURPOSE_TIMESERIES).with_generic_msg(
                            msg.format('[Masked]'))
        if featurization.transformer_params is not None:
            for _, col_param_list in featurization.transformer_params.items():
                for col_param in col_param_list:
                    if col_param[0] not in x_raw_column_name:
                        msg = ("The column '{}' specified in the "
                               "FeaturizationConfig's custom transforms "
                               "is not present in the data frame.")
                        raise InvalidValueException(
                            msg.format(col_param[0]),
                            reference_code=ReferenceCodes._VALIDATE_FEATURIZATION_TRANSFORM_TIMESERIES
                        ).with_generic_msg(
                            msg.format('[Masked]'))


def _get_auto_parameters_maybe(automl_settings: AutoMLBaseSettings,
                               X: DataInputType,
                               y: DataInputType) -> Tuple[List[int], int, int]:
    """
    Return the parameters which should b e estimated heuristically.

    Now 09/18/2019 it is lags, window_size and max_horizon.
    :param automl_settings: The settings of the run.
    :param X: The input data frame. If the type of input is not a data frame no heursitics will be estimated.
    :param y: The expected data.
    """
    # quick check of the data, no need of tsdf here.
    window_size = automl_settings.window_size if automl_settings.window_size is not None else 0
    lags = automl_settings.lags[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] \
        if automl_settings.lags is not None else [0]  # type: List[Union[str, int]]
    # We need to get the heuristics to estimate the minimal number of points needed for training.
    max_horizon = automl_settings.max_horizon
    if not isinstance(X, pd.DataFrame):
        # No heuristics is possible.
        # This will lead to more sensible error from TimeSeriesTransformer.
        if window_size == TimeSeries.AUTO:
            window_size = TimeSeriesInternal.WINDOW_SIZE_DEFDAULT
        if lags == [TimeSeries.AUTO]:
            lags = [TimeSeriesInternal.TARGET_LAGS_DEFAULT]
        if max_horizon == TimeSeries.AUTO:
            max_horizon = TimeSeriesInternal.MAX_HORIZON_DEFAULT
        return cast(List[int], lags), window_size, max_horizon
    # Estimate heuristics if needed.
    if max_horizon == constants.TimeSeries.AUTO:
        max_horizon = forecasting_heuristic_utils.get_heuristic_max_horizon(
            X,
            automl_settings.time_column_name,
            automl_settings.grain_column_names)
    if window_size == constants.TimeSeries.AUTO or lags == [constants.TimeSeries.AUTO]:
        X[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y
        heuristics_lags, heuristics_rw = forecasting_heuristic_utils.analyze_pacf_per_grain(
            X,
            automl_settings.time_column_name,
            TimeSeriesInternal.DUMMY_TARGET_COLUMN,
            automl_settings.grain_column_names)
        # Make sure we have removed the y back from the data frame.
        X.drop(TimeSeriesInternal.DUMMY_TARGET_COLUMN, axis=1, inplace=True)
        if window_size == constants.TimeSeries.AUTO:
            window_size = heuristics_rw
        if lags == [constants.TimeSeries.AUTO]:
            lags = [heuristics_lags]
    return cast(List[int], lags), window_size, max_horizon


def _check_tsdf_frequencies(frequencies_grain_names: Dict[pd.DateOffset, List[List[str]]]) -> None:
    # pd.DateOffset can not compare directly. need a start time.
    if len(frequencies_grain_names) == 0:
        return
    date_offsets = [offset for offset in frequencies_grain_names.keys()]
    all_freq_equal = all([offset == date_offsets[0] for offset in date_offsets])
    if not all_freq_equal:
        msg = ("More than one series is in the input data, and their frequencies differ. "
               "Please separate series by frequency and build separate models. "
               "If frequencies were incorrectly inferred, please fill in gaps in series.")
        raise DataFrameFrequencyException(msg, has_pii=False)


def _check_grain_min_points(data_points: int,
                            min_points: int,
                            automl_settings: AutoMLBaseSettings,
                            grain_names: Optional[Union[List[str], str]] = None) -> None:
    if hasattr(
            automl_settings,
            TimeSeries.SHORT_SERIES_HANDLING) and getattr(
            automl_settings,
            TimeSeries.SHORT_SERIES_HANDLING):
        # If we are going to remove short series, do not validate for it.
        # If all series are too short, grain dropper will throw an error.
        return
    if data_points < min_points:

        window_size = automl_settings.window_size if automl_settings.window_size is not None else 0
        lags = automl_settings.lags[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] \
            if automl_settings.lags is not None else 0
        if grain_names is None:
            # In fact this code will never be executed:
            # the condition if X.shape[0] < min_points:
            # will happen before and will catch this situation.
            pii_message = (
                "The data provided is insufficient for training: for a valid training with cv {},  max_horizon {}, "
                "lags {} and rolling window size {}. The current dataset has only {} points. Please consider "
                "reducing max_horizon, the number of cross validations, lags or rolling window size.". format(
                    automl_settings.n_cross_validations, automl_settings.max_horizon, lags, window_size, data_points))
            raise InsufficientDataException(
                pii_message).with_generic_msg("The data provided is insufficient for training.")
        else:
            if not isinstance(grain_names, list):
                grain_names = [grain_names]
            pii_message = (
                "The data provided is insufficient for training grain: [{}] for a valid training with cv {}, "
                "max_horizon {} lags {} and rolling window size {}. The current grain has only {} points. "
                "Please consider reducing max_horizon, n_cross_validations, or lags, rolling window size or "
                "dropping that particular grain.". format(
                    ",".join(
                        [
                            str(grain) for grain in grain_names]),
                    automl_settings.n_cross_validations,
                    automl_settings.max_horizon,
                    lags,
                    window_size,
                    data_points))
            raise InsufficientDataException(
                pii_message).with_generic_msg("The data provided is insufficient for some training grains.")


def check_memory_limit(X: DataInputType, y: DataInputType) -> None:
    """
    Check the memory availiability.

    :param X: The dataframe with predictors.
    :param y: The data set with targets.

    """
    # We need to estimate the amount of memory, used by the data set and if
    # there is a risk of out of memory we need to raise an exception here.
    avail_memory = None  # Optional[int]
    try:
        # Make this code safe.
        avail_memory = memory_utilities.get_available_physical_memory()
    except Exception:
        pass
    if avail_memory is not None:
        memory_per_df = memory_utilities.get_data_memory_size(X)
        if y is not None:
            memory_per_df += memory_utilities.get_data_memory_size(y)
        # We have found that the amount of memory needed to process the data frame is
        # approximately 10 * data frame size.
        needed_memory = memory_per_df * 10
        if avail_memory < needed_memory:
            msg = ("There is not enough memory on the machine to process this data set. "
                   "Data set size is {}, the amount of available memory is {}. "
                   "To efficiently run AutoML at least {} of memory is required. "
                   "Please install more memory or use bigger virtual machine to generate model on this data set.")
            raise DataShapeException(msg.format(memory_per_df, avail_memory, needed_memory)).with_generic_msg(
                msg.format('[Masked]', '[Masked]', '[Masked]'))


def _check_timeseries_input_and_get_tsdf(
    X: DataInputType,
    y: DataInputType,
    x_raw_column_names: np.ndarray,
    automl_settings: AutoMLBaseSettings,
    max_horizon: int,
    min_points: int = 0,
    is_validation_data: bool = False
) -> TimeSeriesDataFrame:
    if isinstance(X, pd.DataFrame):
        df = X
    else:
        if x_raw_column_names is not None:
            # check if there is any conflict in the x_raw_column_names
            _check_timeseries_input_column_names(x_raw_column_names)
            # generate dataframe for tsdf.
            df = _add_raw_column_names_to_X(x_raw_column_names, X)
        else:
            # if x_raw_column_name is None, then the origin input data is ndarray.
            raise InvalidDataTypeException(
                "Timeseries only support pandas DataFrame as input X. The raw input X is {}.".format(
                    "sparse" if scipy.sparse.issparse(X) else "ndarray"
                )).with_generic_msg("Timeseries only support pandas DataFrame as input X.")
    # Check if we have enough memory.
    check_memory_limit(df, y)
    timeseries_param_dict = utilities._get_ts_params_dict(automl_settings)
    _check_columns_present(df, cast(Dict[str, str], timeseries_param_dict))
    # Convert time column to datetime only if all columns are already present.
    if timeseries_param_dict is not None:
        time_param = timeseries_param_dict.get(TimeSeries.TIME_COLUMN_NAME)
        if isinstance(time_param, str):
            frequency_fixer.convert_to_datetime(df, time_param)
    # Check not supported datatypes and warn
    _check_supported_data_type(df)
    if timeseries_param_dict is not None:
        feat_config = timeseries_param_dict.pop("featurization_config", None)
        tst = TimeSeriesTransformer(pipeline_type=TimeSeriesPipelineType.FULL,
                                    logger=None, featurization_config=feat_config, **timeseries_param_dict)
    else:
        raise InvalidTsdfArgument("Invalid forecasting parameters were provided.", has_pii=False)
    _check_time_index_duplication(df, automl_settings.time_column_name, automl_settings.grain_column_names)
    _check_valid_pd_time(df, automl_settings.time_column_name)
    tsdf = tst.construct_tsdf(df, y)
    tsdf.sort_index(inplace=True)
    frequencies_grain_names = {}   # type: Dict[pd.DateOffset, List[List[str]]]
    if automl_settings.grain_column_names is not None:
        # to deal the problem that user has no input grain
        try:
            freq_by_grain = tsdf.infer_freq_by_grain()
            for data_tuple in tsdf.groupby_grain():
                grain_name_str = data_tuple[0]
                err_msg = ("Time series frequency cannot be inferred for grain (series) [{}]. "
                           "Please ensure that each time series' time stamps are regularly spaced. "
                           "Filling with default values such as 0 may be needed for very sparse series."
                           ).format(grain_name_str)
                tsdf_grain = data_tuple[1]
                data_points = tsdf_grain.shape[0]

                if not is_validation_data or tsdf_grain.shape[0] > 1:
                    # if validation data is only one data point, no need to check freq.
                    freq = freq_by_grain[grain_name_str]
                    if tsdf_grain.shape[0] != 1:
                        # We can not establish the frequency only if tsdf_grain has only one value.
                        if freq is None:
                            raise DataFrameFrequencyException(err_msg).with_generic_msg(
                                "Frequency cannot be inferred for the [masked] grain.")

                        # Check alignment with the inferred frequency
                        _check_timeseries_alignment_single_grain(grain_name_str, tsdf_grain, freq)

                        if freq in frequencies_grain_names:
                            frequencies_grain_names[freq].append(grain_name_str)
                        else:
                            frequencies_grain_names[freq] = [grain_name_str]
                    # check min data points for train and max_horizon for validation
                    data_points = tsdf_grain.ts_value.count()
                    if not is_validation_data:
                        _check_grain_min_points(
                            data_points, min_points, automl_settings, grain_names=grain_name_str)
                        if tsdf_grain.shape[0] != 1:
                            _check_cv_gap_exist(tsdf_grain,
                                                max_horizon,
                                                automl_settings.n_cross_validations,
                                                grain_name_str, freq)
                if is_validation_data:
                    if data_points < max_horizon:
                        print(("WARNING: Validation set has fewer data points ({}) "
                               "than max_horizon ({}) for one of grains (series). "
                               "We will be unable to estimate error and predictive quantiles at some horizons. "
                               "Please consider increasing the validation data to the length of max horizon.").
                              format(data_points, max_horizon))
                    elif data_points > max_horizon:
                        print(("WARNING: Validation set has more data points {} "
                               "than max_horizon {} for one of grains (series). "
                               "Not all validation data will be used in the training. "
                               "Please consider decreasing the validation data to the length of max horizon.").
                              format(data_points, max_horizon))

        except DataException:
            # If we already have a descriptive Exception, raise it.
            raise
        except Exception:
            # If not, raise generic exception.
            raise DataFrameFrequencyException(
                "A non-specific error occurred checking frequencies across grains (series).", has_pii=False)

        _check_tsdf_frequencies(frequencies_grain_names)
    # check all the tsdf at the end.
    if not is_validation_data:
        tsdf_freq = tsdf.infer_freq()
        data_points = tsdf.ts_value.count()
        _check_grain_min_points(data_points, min_points, automl_settings)
        _check_cv_gap_exist(tsdf, max_horizon, automl_settings.n_cross_validations, freq=tsdf_freq)
    return tsdf


def _check_cv_gap_exist(tsdf: TimeSeriesDataFrame,
                        max_horizon: int,
                        n_cross_validations: Optional[int] = None,
                        grain_name: Optional[str] = None,
                        freq: Optional[pd.DateOffset] = None) -> None:
    """
    Check if one of the cross validation splits lacks the data.

    :param tsdf: One grain of a time series data frame.
    :param max_horizon: The maximal horizon, used for prediction.
    :param n_cross_validations: The number of cross validations.
    :param grain_name: The grain being analyzed if any.
    """
    if n_cross_validations is not None:
        if freq is None:
            freq = tsdf.infer_freq()
        for i in range(n_cross_validations):
            # In this code we are estimating the number of missing values in the cross
            # validation fold.
            # if this amount is bigger then some arbitrary number, currently 25%
            # the validation is considered to be failed.
            expected_dates = pd.date_range(start=tsdf.time_index.max() - (i + max_horizon) * freq,
                                           end=tsdf.time_index.max() - i * freq,
                                           freq=freq)
            # Compare the expected dates with the real dates.
            missing_dates = sorted([str(val) for val in set(expected_dates).difference(set(tsdf.time_index))])
            n_absent_in_cv = len(missing_dates)
            # Currently we have commented out the exceptions, because the check is strict.
            # In future we want to replace the exceptions by guard rails.
            if n_absent_in_cv == max_horizon:
                missing_dates_str = ", ".join(missing_dates)
                if grain_name is None:
                    exception_msg = (
                        "Missing timestamp(s) {} in data. "
                        "One of the validation folds will be empty "
                        "because the data at the end of time series are missing")
                    exception_msg = exception_msg.format(missing_dates_str)
                    # deEx = DataException(
                    #    exception_msg.format(missing_dates_str)).with_generic_msg(
                    #        exception_msg.format(MASKED))
                else:
                    exception_msg = ("Missing timestamp(s) {} in data in grain {}. "
                                     "One of the validation folds will be empty "
                                     "because the data at the end of time series are missing")
                    exception_msg = exception_msg.format(missing_dates_str, grain_name)
                    # deEx = DataException(
                    #    exception_msg.format(missing_dates_str, grain_name)).with_generic_msg(
                    #        exception_msg.format(MASKED, MASKED))
                # raise deEx
                # Warning is commented, because the warning text may be logged.
                # warnings.warn(exception_msg)


def _check_valid_pd_time(df: pd.DataFrame, time_column_name: str) -> None:
    try:
        pd.to_datetime(df[time_column_name])
    except pd.tslib.OutOfBoundsDatetime:
        raise OutOfBoundDataException(
            "Date/time is out of our usable range. "
            "Please drop any rows with date/time less than {} or greater than {}."
            .format(pd.Timestamp.min, pd.Timestamp.max), has_pii=False)
    except ValueError:
        raise InvalidDataTypeException(
            "One or more rows have an invalid date/time. "
            "Please ensure you can run `pandas.to_datetime(X)`.", has_pii=False)


def _check_time_index_duplication(df: pd.DataFrame,
                                  time_column_name: str,
                                  grain_column_names: Optional[List[str]] = None) -> None:
    group_by_col = [time_column_name]
    if grain_column_names is not None:
        if isinstance(grain_column_names, str):
            grain_column_names = [grain_column_names]
        group_by_col.extend(grain_column_names)
    duplicateRowsDF = df[df.duplicated(subset=group_by_col, keep=False)]
    if duplicateRowsDF.shape[0] > 0:
        if grain_column_names is not None and len(grain_column_names) > 0:
            message = ("Found duplicated rows for {0} and {1} combinations. "
                       "Please make sure the grain setting is correct so that each grain represents "
                       "one time-series, or clean the data to make sure there are no duplicates "
                       "before passing to AutoML. For more information on grains and forecasting "
                       "configurations visit {2}.".
                       format([time_column_name], grain_column_names, ErrorLinks.DUPLICATED_INDEX.value))
            raise DuplicatedIndexException(exception_message="Duplicates in time and grain combinations.",
                                           pii_message=message)
            """
            print(duplicateRowsDF.iloc[:2, :][group_by_col])
            """
        else:
            message = ("The specified time column, '{}', contains rows "
                       "with duplicate timestamps. If your data contains "
                       "multiple time series, review the grain column setting "
                       "to define the time series identifiers for your data. "
                       "For more information on grains and forecasting "
                       "configurations visit {}.".
                       format([time_column_name], ErrorLinks.DUPLICATED_INDEX.value))
            raise DuplicatedIndexException(exception_message="Duplicates in time index.",
                                           pii_message=message)
            """
            print(duplicateRowsDF.iloc[:2, :][group_by_col])
            """


def _check_timeseries_alignment_single_grain(grain_level: Any, tsdf: TimeSeriesDataFrame,
                                             freq: pd.DateOffset) -> None:
    """
    Check if single timeseries (single grain) is aligned to the given frequency.

    :param tsdf: The time series dataframe to be tested.
    :param freq: Frequency to check alignment against.
    """
    time_index = tsdf.time_index
    if not isinstance(time_index[0], pd.Timestamp):
        raise InvalidDataTypeException('The time column in dataframe has incorrect type. '
                                       'Please make sure it contains dates.', has_pii=False)

    onfreq_time = pd.date_range(start=time_index.min(), end=time_index.max(), freq=freq)
    if not set(time_index).issubset(onfreq_time):
        error_message = (
            'The frequency is not consistent with the rest of the '
            'data for the following grain(s) [{}]. The expected frequency '
            'is a data point every \'{}\'. Review the grains and ensure '
            'consistent frequency alignment across all grains.')

        raise DataFrameFrequencyException(
            exception_message=error_message.format(
                '[Masked]', '[Masked]'
            ),
            pii_message=error_message.format(
                grain_level, freq))


def _validate_timeseries_train_valid_tsdf(tsdf_train: TimeSeriesDataFrame,
                                          tsdf_valid: TimeSeriesDataFrame,
                                          has_lookback_features: bool) -> None:
    train_grain_data_dict = {grain: tsdf for grain, tsdf in tsdf_train.groupby_grain()}
    valid_grain_data_dict = {grain: tsdf for grain, tsdf in tsdf_valid.groupby_grain()}
    train_grain = set([g for g in train_grain_data_dict.keys()])
    valid_grain = set([g for g in valid_grain_data_dict.keys()])
    # check grain is the same for train and valid.
    grain_difference = train_grain.symmetric_difference(valid_grain)
    if len(grain_difference) > 0:
        grain_in_train_not_in_valid = list(filter(lambda x: x in train_grain, grain_difference))
        grain_in_valid_not_in_train = list(filter(lambda x: x in valid_grain, grain_difference))
        error_msg_list = []
        if len(grain_in_train_not_in_valid) > 0:
            error_msg_list.append(
                "Grain {} found in training data but not in validation data.".format(
                    ",".join(["[{}]".format(grain) for grain in grain_in_train_not_in_valid])
                )
            )
        if len(grain_in_valid_not_in_train) > 0:
            error_msg_list.append(
                "Grain {} found in validation data but not in training data.".format(
                    ",".join(["[{}]".format(grain) for grain in grain_in_valid_not_in_train])
                )
            )
        raise GrainAbsent(
            exception_message="Training and validation datasets contain different sets of grains",
            pii_message=" ".join(error_msg_list))
    # check per grain contiguous and frequency.
    for grain, tsdf in train_grain_data_dict.items():
        tsdf_valid = valid_grain_data_dict[grain]
        if has_lookback_features and tsdf.time_index.max() + tsdf.infer_freq() != tsdf_valid.time_index.min():
            error_message = "Training and validation data are not contiguous in grain(s)."
            raise DataFrameTimeNotContinuous(
                error_message, has_pii=False)
        if tsdf_valid.shape[0] > 1:
            if tsdf.infer_freq() != tsdf_valid.infer_freq():
                error_message = "For grain {}, training data and validation data have different frequency."
                raise DataFrameFrequencyChanged(
                    exception_message=error_message.format('[Masked]'),
                    pii_message=error_message.format(grain))


def _check_timeseries_input_column_names(x_raw_column_names: np.ndarray) -> None:
    for col in x_raw_column_names:
        if col in constants.TimeSeriesInternal.RESERVED_COLUMN_NAMES:
            print("Column name {} is in the reserved column names list, please change that column name.".format(col))
            raise DataFormatException(
                "Column name is in the reserved column names list, please change that column name.",
                has_pii=False
            )


def _check_columns_present(df: pd.DataFrame, timeseries_param_dict: Dict[str, str]) -> None:
    """Determine if df has the correct column names for timeseries."""
    msg = ("One or more columns for `{}` were not found. Please check that these columns "
           "are present in your dataframe. You can run `<X>.columns`.")

    def check_a_in_b(a: Union[str, List[str]], b: List[str]) -> List[str]:
        """
        checks a is in b.

        returns any of a not in b.
        """
        if isinstance(a, str):
            a = [a]

        set_a = set(a)
        set_b = set(b)
        return list(set_a - set_b)

    missing_col_names = []          # type: List[str]
    # check time column in df
    col_name = timeseries_param_dict.get(constants.TimeSeries.TIME_COLUMN_NAME)
    if col_name is not None:
        missing_col_names = check_a_in_b(col_name, df.columns)
    # raise if missing
    if len(missing_col_names) != 0:
        raise DataFrameMissingColumnException(
            pii_message=msg.format(constants.TimeSeries.TIME_COLUMN_NAME),
            target=DataFrameMissingColumnException.TIME_COLUMN)

    # check grain column(s) in df
    col_names = timeseries_param_dict.get(constants.TimeSeries.GRAIN_COLUMN_NAMES)
    if col_names is not None:
        missing_col_names = check_a_in_b(col_names, df.columns)
    # raise if missing
    if len(missing_col_names) != 0:
        raise DataFrameMissingColumnException(
            pii_message=msg.format(constants.TimeSeries.GRAIN_COLUMN_NAMES),
            target=DataFrameMissingColumnException.GRAIN_COLUMN)

    # check drop column(s) in df
    missing_drop_cols = []         # type: List[str]
    col_names = timeseries_param_dict.get(constants.TimeSeries.DROP_COLUMN_NAMES)
    if col_names is not None:
        missing_drop_cols += check_a_in_b(col_names, df.columns)

    # warn if missing
    if len(missing_drop_cols) != 0:
        warnings.warn("The columns to drop were not found and will be ignored.")


def _check_supported_data_type(df: pd.DataFrame) -> None:
    supported_datatype = set([np.number, np.dtype(object), pd.Categorical.dtype, np.datetime64])
    unknown_datatype = set(df.infer_objects().dtypes) - supported_datatype
    if(len(unknown_datatype) > 0):
        warnings.warn("Following datatypes: {} are not recognized".
                      format(unknown_datatype))


def _check_dimensions(X: DataInputType,
                      y: DataInputType,
                      X_valid: DataInputType,
                      y_valid: DataInputType,
                      sample_weight: DataInputType,
                      sample_weight_valid: DataInputType) -> None:
    """
    Check dimensions of data inputs.

    :param X: Training Data
    :param y: Labels
    :param X_valid: Validation Data
    :param y_valid: Validation Labels
    :param sample_weight: Training sample weights
    :param sample_weight_valid: Validation sample weights
    :return: None
    """
    dimension_error_message = "Dimension mismatch for {0} data. " \
                              "Expecting {1} dimensional array, " \
                              "but received {2} dimensional data."
    unrecognized_data_type_message = 'Unrecognized type of input for {}: {}'

    feature_dimensions = 2
    label_dimensions = 1

    # if the data is not in these 4 type, we will bypass the test
    x_dim = None
    y_dim = None
    x_valid_dim = None
    y_valid_dim = None
    sample_weight_dim = None
    sample_weight_valid_dim = None
    x_shape = None
    y_shape = None
    x_valid_shape = None
    y_valid_shape = None
    sample_weight_shape = None
    sample_weight_valid_shape = None

    if X is not None:
        if isinstance(X, pd.DataFrame) or isinstance(X, np.ndarray) or scipy.sparse.issparse(X):
            x_shape = X.shape
            x_dim = X.ndim
        elif isinstance(X, dprep.Dataflow):
            # calculating shape on Dataflows can be very expensive, as it calculates the profile of the underlying data
            # we'd probably need a different design to do this check on dataflows
            x_shape = X.shape
            x_dim = x_shape[1]
        else:
            raise InvalidDataTypeException(
                unrecognized_data_type_message.format('X', type(X).__name__)).with_generic_msg(
                    unrecognized_data_type_message.format('X', MASKED))

    if X_valid is not None:
        if isinstance(X_valid, pd.DataFrame) or isinstance(X_valid, np.ndarray) or scipy.sparse.issparse(X_valid):
            x_valid_shape = X_valid.shape
            x_valid_dim = X_valid.ndim
        elif isinstance(X_valid, dprep.Dataflow):
            x_valid_shape = X_valid.shape
            x_valid_dim = x_valid_shape[1]
        else:
            raise InvalidDataTypeException(
                unrecognized_data_type_message.format(
                    'X_valid', type(X_valid).__name__)).with_generic_msg(
                unrecognized_data_type_message.format(
                    'X_valid', MASKED))

    if y is not None:
        if isinstance(y, pd.DataFrame) or scipy.sparse.issparse(y) or isinstance(y, dprep.Dataflow):
            y_shape = y.shape
            y_dim = y.shape[1]
        elif isinstance(y, np.ndarray):
            y_shape = y.shape
            y_dim = y.ndim
        else:
            raise InvalidDataTypeException(
                unrecognized_data_type_message.format('y', type(y).__name__)).with_generic_msg(
                    unrecognized_data_type_message.format('y', MASKED))

    if y_valid is not None:
        if isinstance(y_valid, pd.DataFrame) or scipy.sparse.issparse(y_valid) or isinstance(y_valid, dprep.Dataflow):
            y_valid_shape = y_valid.shape
            y_valid_dim = y_valid.shape[1]
        elif isinstance(y_valid, np.ndarray):
            y_valid_shape = y_valid.shape
            y_valid_dim = y_valid.ndim
        else:
            raise InvalidDataTypeException(
                unrecognized_data_type_message.format(
                    'y_valid', type(y_valid).__name__)).with_generic_msg(
                unrecognized_data_type_message.format('y_valid', MASKED))

    if sample_weight is not None:
        if isinstance(sample_weight, pd.DataFrame) or \
                scipy.sparse.issparse(sample_weight) or \
                isinstance(sample_weight, dprep.Dataflow):
            sample_weight_shape = sample_weight.shape
            sample_weight_dim = sample_weight.shape[1]
        elif isinstance(sample_weight, np.ndarray):
            sample_weight_shape = sample_weight.shape
            sample_weight_dim = sample_weight.ndim
        else:
            raise InvalidDataTypeException(
                unrecognized_data_type_message.format('sample_weight', type(sample_weight).__name__)).with_generic_msg(
                    unrecognized_data_type_message.format('sample_weight', MASKED))

    if sample_weight_valid is not None:
        if isinstance(sample_weight_valid, pd.DataFrame) or \
                scipy.sparse.issparse(sample_weight_valid) or \
                isinstance(sample_weight_valid, dprep.Dataflow):
            sample_weight_valid_shape = sample_weight_valid.shape
            sample_weight_valid_dim = sample_weight_valid.shape[1]
        elif isinstance(sample_weight_valid, np.ndarray):
            sample_weight_valid_shape = sample_weight_valid.shape
            sample_weight_valid_dim = sample_weight_valid.ndim
        else:
            raise InvalidDataTypeException(
                unrecognized_data_type_message.
                format('sample_weight_valid', type(sample_weight_valid).__name__)).with_generic_msg(
                    unrecognized_data_type_message.format('sample_weight_valid', MASKED)
            )

    if x_dim is not None and x_dim > feature_dimensions:
        raise DataShapeException(
            dimension_error_message
            .format("X", feature_dimensions, x_dim)).with_generic_msg(
                dimension_error_message.format("X", MASKED, MASKED)
        )
    if y_dim is not None and y_dim != label_dimensions:
        raise DataShapeException(
            dimension_error_message
            .format("y", label_dimensions, y_dim)).with_generic_msg(
                dimension_error_message.format("y", MASKED, MASKED))
    if x_valid_dim is not None and x_valid_dim > feature_dimensions:
        raise DataShapeException(
            dimension_error_message
            .format("X_valid", feature_dimensions, x_valid_dim)).with_generic_msg(
                dimension_error_message.format("X_valid", MASKED, MASKED))
    if y_valid_dim is not None and y_valid_dim != label_dimensions:
        raise DataShapeException(
            dimension_error_message
            .format("y_valid", label_dimensions, y_valid_dim)).with_generic_msg(
            dimension_error_message.format("y_valid", MASKED, MASKED))
    if sample_weight_dim is not None and sample_weight_dim != label_dimensions:
        raise DataShapeException(
            dimension_error_message
            .format("sample_weight", label_dimensions, sample_weight_dim)).with_generic_msg(
                dimension_error_message.format("sample_weight", MASKED, MASKED))
    if sample_weight_valid_dim is not None and sample_weight_valid_dim != label_dimensions:
        raise DataShapeException(
            dimension_error_message.format(
                "sample_weight_valid", label_dimensions, sample_weight_valid_dim)).with_generic_msg(
                    dimension_error_message.format("sample_weight_valid", MASKED, MASKED))

    if x_shape is not None and y_shape is not None and x_shape[0] != y_shape[0]:
        raise DataSamplesSizeException(
            "X and y data do not have the same number of samples. "
            "X has {0} samples and y has {1} samples."
            .format(x_shape[0], y_shape[0])).with_generic_msg("X and y data do not have the same number of samples.")
    if x_valid_shape is not None and y_valid_shape is not None and \
            x_valid_shape[0] != y_valid_shape[0]:
        raise DataSamplesSizeException(
            "X_valid and y_valid data do not have the same number "
            "of samples. X_valid has {0} samples and "
            "y_valid has {1} samples."
            .format(x_valid_shape[0], y_valid_shape[0]))\
            .with_generic_msg("X_valid and y_valid do not have the same number of samples.")
    if sample_weight_shape is not None and y_shape is not None and \
            sample_weight_shape[0] != y_shape[0]:
        raise DataSamplesSizeException(
            "sample_weight and y data do not have the same number "
            "of samples. sample_weight has {0} samples and "
            "y has {1} samples."
            .format(sample_weight_shape[0], y_shape[0]))\
            .with_generic_msg("sample_weight and y do not have the same number of samples.")
    if sample_weight_valid_shape is not None and y_valid_shape is not None and\
            sample_weight_valid_shape[0] != y_valid_shape[0]:
        raise DataSamplesSizeException(
            "sample_weight_valid and y_valid data do not have the same number "
            "of samples. sample_weight_valid has {0} samples and y_valid "
            "has {1} samples.".format(sample_weight_valid_shape[0], y_valid_shape[0]))\
            .with_generic_msg("sample_weight_valid and y_valid do not have the same number of samples.")
    if x_shape is not None and y_shape is not None and x_shape[0] == 0:
        raise DataSamplesSizeException("X and y data do not have any samples.", has_pii=False)
    if x_valid_shape is not None and y_valid_shape is not None and x_valid_shape[0] == 0:
        raise DataSamplesSizeException("X_valid and y_valid data do not have any samples.", has_pii=False)


def _is_sparse_matrix_int_type(sparse_matrix: DataInputType) -> bool:
    """
    Check if a sparse matrix is in integer format.

    :param sparse_matrix:
    :return:
    """
    if sparse_matrix is not None and scipy.sparse.issparse(sparse_matrix):
        numpy_int_types = [np.int32, np.int64, np.int16, np.int8,
                           np.uint32, np.uint64, np.uint16, np.uint8]

        if sparse_matrix.dtype in numpy_int_types:
            return True

    return False


def _upgrade_sparse_matrix_type(sparse_matrix: DataInputType) -> DataInputType:
    """
    Convert sparse matrix in integer format into floating point format.

    This function will create a copy of the sparse matrix in when the conversion happens.
    :param sparse_matrix:
    :return:
    """
    if sparse_matrix is not None and scipy.sparse.issparse(sparse_matrix):
        if sparse_matrix.dtype == np.int32 or sparse_matrix.dtype == np.int16 or \
                sparse_matrix.dtype == np.int8 or sparse_matrix.dtype == np.uint32 or \
                sparse_matrix.dtype == np.uint16 or sparse_matrix.dtype == np.uint8:
            return sparse_matrix.astype(np.float32)
        elif sparse_matrix.dtype == np.int64 or sparse_matrix.dtype == np.uint64:
            return sparse_matrix.astype(np.float64)
        else:
            return sparse_matrix

    return sparse_matrix


def init_client_dataset_from_fit_iteration_params(fit_iteration_parameters_dict: Dict[str, Any],
                                                  automl_settings: AutoMLBaseSettings,
                                                  cache_store: Optional[CacheStore] = None,
                                                  remote: bool = False,
                                                  init_all_stats: bool = False,
                                                  keep_in_memory: bool = False) -> ClientDatasets:
    """
    Get a ClientDatasets object from fit_iteration_parameters

    TODO: This method needs to be deprecated. ClientDatasets should be consolidated to only use transformed data ctx

    :param fit_iteration_parameters_dict: Dictionary that contains input data
    :param automl_settings:  AutoML settings config
    :param cache_store: Underlying cache store to use, will default to local FileStore
    :param remote: remote or local run flag
    :param init_all_stats: Initialize all the stats
    :param keep_in_memory: Whether to flush the data to the cache store or keep it in-memory
    :return: ClientDatasets
    """
    cv_splits = _CVSplits(X=fit_iteration_parameters_dict.get('X'),
                          y=fit_iteration_parameters_dict.get('y'),
                          frac_valid=automl_settings.validation_size,
                          cv_splits_indices=fit_iteration_parameters_dict.get('cv_splits_indices'),
                          is_time_series=automl_settings.is_timeseries,
                          timeseries_param_dict=utilities._get_ts_params_dict(automl_settings))

    dataset = _get_client_dataset(fit_iteration_parameters_dict.get('X'),
                                  fit_iteration_parameters_dict.get('y'),
                                  cache_store=cache_store,
                                  sample_weight=fit_iteration_parameters_dict.get('sample_weight'),
                                  X_valid=fit_iteration_parameters_dict.get('X_valid'),
                                  y_valid=fit_iteration_parameters_dict.get('y_valid'),
                                  sample_weight_valid=fit_iteration_parameters_dict.get('sample_weight_valid'),
                                  cv_splits=cv_splits,
                                  num_classes=automl_settings.num_classes,
                                  task_type=automl_settings.task_type,
                                  y_min=automl_settings.y_min,
                                  y_max=automl_settings.y_max,
                                  init_all_stats=init_all_stats,
                                  remote=remote)

    dataset.x_raw_column_names = fit_iteration_parameters_dict.get('x_raw_column_names')

    if not keep_in_memory:
        dataset.cache_dataset(keep_in_memory)

    return dataset


def init_dataset(
    transformed_data_context: Union[TransformedDataContext, StreamingTransformedDataContext],
    cache_store: CacheStore,
    automl_settings: AutoMLBaseSettings,
    remote: bool = False,
    init_all_stats: bool = False,
    keep_in_memory: bool = False
) -> DatasetBase:
    """
    Initialize the dataset.

    :param transformed_data_context: transformed_data_context contains X,y & other data's.
    :param cache_store: cache store
    :param automl_settings: automl settings
    :param remote: remote or local run flag
    :param init_all_stats: init all stats
    :param keep_in_memory: Whether to flush the data to the cache store or keep it in-memory
    :return: DatasetBase
    """
    if isinstance(transformed_data_context, StreamingTransformedDataContext):
        return init_streaming_dataset(
            transformed_data_context=transformed_data_context,
            automl_settings=automl_settings
        )

    elif isinstance(transformed_data_context, TransformedDataContext):
        return init_client_dataset(
            transformed_data_context=transformed_data_context,
            cache_store=cache_store,
            automl_settings=automl_settings,
            remote=remote,
            init_all_stats=init_all_stats,
            keep_in_memory=keep_in_memory)


def init_client_dataset(transformed_data_context: TransformedDataContext,
                        cache_store: CacheStore,
                        automl_settings: AutoMLBaseSettings,
                        remote: bool = False,
                        init_all_stats: bool = False,
                        keep_in_memory: bool = False) -> ClientDatasets:
    """
    Get the client dataset.

    :param transformed_data_context: transformed_data_context contains X,y & other data's.
    :param cache_store: cache store
    :param automl_settings: automl settings
    :param remote: remote or local run flag
    :param init_all_stats: init all stats
    :param keep_in_memory: Whether to flush the data to the cache store or keep it in-memory
    :return: ClientDatasets
    """

    dataset = _get_client_dataset(transformed_data_context.X,
                                  transformed_data_context.y,
                                  cache_store=cache_store,
                                  sample_weight=transformed_data_context.sample_weight,
                                  X_valid=transformed_data_context.X_valid,
                                  y_valid=transformed_data_context.y_valid,
                                  sample_weight_valid=transformed_data_context.sample_weight_valid,
                                  cv_splits=transformed_data_context.cv_splits,
                                  num_classes=automl_settings.num_classes,
                                  task_type=automl_settings.task_type,
                                  y_min=automl_settings.y_min,
                                  y_max=automl_settings.y_max,
                                  init_all_stats=init_all_stats,
                                  remote=remote,
                                  transformers=transformed_data_context.transformers)
    dataset.timeseries = transformed_data_context.timeseries
    dataset.timeseries_param_dict = transformed_data_context.timeseries_param_dict
    dataset.x_raw_column_names = transformed_data_context.x_raw_column_names
    dataset.raw_data_type = transformed_data_context._get_raw_data_type()
    dataset.raw_data_snapshot_str = transformed_data_context._get_raw_data_snapshot_str()

    if automl_settings.n_cross_validations is None and transformed_data_context.X_valid is None:
        # set the value for num_auto_cv_splits if no other mode of Validation is specified
        n_cv = transformed_data_context._get_num_cv_splits()
        dataset.num_auto_cv_splits = None if n_cv == 0 else n_cv

    if not keep_in_memory:
        dataset.cache_dataset(keep_in_memory)

    return dataset


def _get_client_dataset(X: DataInputType,
                        y: DataSingleColumnInputType,
                        cache_store: Optional[CacheStore] = None,
                        sample_weight: Optional[DataInputType] = None,
                        X_valid: Optional[DataInputType] = None,
                        y_valid: Optional[DataSingleColumnInputType] = None,
                        sample_weight_valid: Optional[DataInputType] = None,
                        cv_splits: Optional[_CVSplits] = None,
                        num_classes: Optional[int] = None,
                        task_type: str = constants.Tasks.CLASSIFICATION,
                        y_min: Optional[float] = None,
                        y_max: Optional[float] = None,
                        init_all_stats: bool = False,
                        remote: bool = True,
                        transformers: Optional[Dict[str, TransformerMixin]] = None) -> ClientDatasets:
    assert_failures = []
    default_dataset_name = 'NoName'

    if cv_splits:
        frac_valid = cv_splits.get_fraction_validation_size()
        cv_splits_indices = cv_splits.get_custom_split_indices()
        num_cv_folds = cv_splits.get_num_k_folds()
    else:
        frac_valid = None
        cv_splits_indices = None
        num_cv_folds = None

    subsample_cache_strategy = SubsampleCacheStrategy.Classic if remote \
        else SubsampleCacheStrategy.Preshuffle

    dataset = ClientDatasets(subsample_cache_strategy=subsample_cache_strategy, cache_store=cache_store)
    logger.info('Created ClientDataset.')

    if X_valid is not None:
        training_type = _get_training_type(
            constants.TrainingType.TrainAndValidation)

        if not (num_cv_folds == 0 or num_cv_folds is None):
            assert_failures.append(
                'n_cross_validations cannot be specified when X_valid is provided.')

        if not (frac_valid == 0.0 or frac_valid is None):
            assert_failures.append(
                'validation_size cannot be specified when X_valid is provided.')

        if y_valid is None:
            assert_failures.append(
                'y_valid must also be provided when X_valid is provided.')

        if len(assert_failures) > 0:
            raise ConfigException("Bad fit parameters. Please review documentation for fit. " +
                                  ' '.join(assert_failures))

        logger.info('Parsing simple train validate dataset.')
        dataset.parse_simple_train_validate(name=default_dataset_name,
                                            X=X,
                                            y=y,
                                            sample_weight=sample_weight,
                                            X_valid=X_valid,
                                            y_valid=y_valid,
                                            sample_weight_valid=sample_weight_valid,
                                            task=task_type,
                                            y_min=y_min,
                                            y_max=y_max,
                                            init_all_stats=init_all_stats,
                                            transformers=transformers)

    else:
        if (num_cv_folds == 0 or num_cv_folds is None) and cv_splits_indices is None:
            training_type = _get_training_type(
                constants.TrainingType.TrainAndValidation)
        else:
            if cv_splits_indices is not None:
                num_cv_folds = len(cv_splits_indices)
            training_type = _get_training_type(
                constants.TrainingType.MeanCrossValidation, num_cv_folds)

        if len(assert_failures) > 0:
            msg = "Bad fit parameters. Please review documentation for fit."
            raise ConfigException(msg + ' '.join(assert_failures)).with_generic_msg(msg)

        logger.info('Parsing cross validation dataset.')
        dataset.parse_data(name=default_dataset_name,
                           X=X,
                           y=y,
                           sample_weight=sample_weight,
                           cv_splits=cv_splits,
                           num_classes=num_classes,
                           task=task_type,
                           y_min=y_min,
                           y_max=y_max,
                           init_all_stats=init_all_stats,
                           transformers=transformers)

    dataset.training_type = training_type

    return dataset


def init_streaming_dataset(
    transformed_data_context: StreamingTransformedDataContext,
    automl_settings: AutoMLBaseSettings
) -> StreamingDataset:
    """
    Initialize a streaming dataset (a dataset where where all data may not fit into memory at once).

    :param transformed_data_context: The transformed data context.
    :param automl_settings: AutoML settings
    :return: A StreamingDataset
    """
    if automl_settings.label_column_name is None:
        raise ConfigException('label_column_name property is required for StreamingDataset', has_pii=False)

    featurized_column_names = transformed_data_context.get_featurized_column_names()

    dataset_metadata = {DatasetMetadataKeys.feature_column_names: featurized_column_names,
                        DatasetMetadataKeys.label_column_name: automl_settings.label_column_name,
                        DatasetMetadataKeys.weight_column_name: automl_settings.weight_column_name,
                        DatasetMetadataKeys.raw_data_snapshot: transformed_data_context.raw_data_snapshot}

    featurization_transformer = transformed_data_context.get_featurization_transformer()

    return StreamingDataset(task=automl_settings.task_type,
                            training_data=transformed_data_context.training_data,
                            dataset_metadata=dataset_metadata,
                            validation_data=transformed_data_context.validation_data,
                            y_min=automl_settings.y_min,
                            y_max=automl_settings.y_max,
                            featurization_transformer=featurization_transformer)


def _get_training_type(training_type: str, folds: int = 0) -> str:
    """
    Determine what type of training and validation to do based on user inputs.
    """
    # TODO: make this simpler
    valid_training_types = (constants.TrainingType.TrainAndValidation,
                            constants.TrainingType.MeanCrossValidation)
    if training_type not in valid_training_types:
        raise ConfigException(
            "%s and %s are the only supported training types." % valid_training_types, has_pii=False)
    is_cv = training_type == constants.TrainingType.MeanCrossValidation
    if not ((is_cv and folds) or (not is_cv and not folds)):
        raise ConfigException("Cannot specify number of folds "
                              "if training type is not %s" % constants.TrainingType.MeanCrossValidation, has_pii=False)
    if folds < 0 or folds == 1:
        raise ConfigException(
            "Cross validation folds must be greater than 1, got %d" % folds)\
            .with_generic_msg("Cross validation folds must be greater than 1.")
    return training_type


def _extract_user_data(user_script: Any) -> Dict[str, Optional[Union[np.ndarray, List[str], float, List[int]]]]:
    """
    Extract data from user's module containing get_data().

    This method automatically runs during an automated machine learning experiment.
    Arguments:
        user_script {module} -- Python module containing get_data() function.

    Raises:
        DataException -- Get data script was not defined and X, y inputs were not provided.
        DataException -- Could not execute get_data() from user script.
        DataException -- Could not extract data from user script.

    Returns:
        dict -- Dictionary containing
        X_train, y_train, sample_weight, X_valid, y_valid,
        sample_weight_valid, cv_splits_indices.

    """
    if user_script is None:
        raise EmptyDataException(
            "Get data script was not defined and X,"
            " y inputs were not provided.", has_pii=False)
    try:
        output = user_script.get_data()         # type: Union[Dict[str, Any], Tuple[Any, Any, Any, Any]]
    except Exception as ex:
        msg = ("Could not execute get_data() from user script."
               "Exception: {}")
        raise ScenarioNotSupportedException(msg.format(ex)).with_generic_msg(msg.format(MASKED)) from None
    if isinstance(output, dict):
        return _extract_data_from_dict(output)
    elif isinstance(output, tuple):
        return _extract_data_from_tuple(output)
    else:
        raise InvalidDataTypeException(
            "The output of get_data() from user script is not a dict or a tuple.", has_pii=False)


def _extract_data_from_dict(output: Dict[str, Any]) -> \
        Dict[str, Optional[Union[np.ndarray, List[str], float, List[int]]]]:
    """
    Extract user data if it is passed as a dictionary.

    Arguments:
        output {dict} -- dictionary containing user data and metadata.

    Raises:
        DataException -- Invalid data or encountered processing issues.

    Returns:
        dict -- Dictionary containing AutoML relevant data.

    """
    X = utilities.get_value_from_dict(output, ['X'], None)
    y = utilities.get_value_from_dict(output, ['y'], None)
    sample_weight = utilities.get_value_from_dict(output, ['sample_weight'], None)
    X_valid = utilities.get_value_from_dict(output, ['X_valid'], None)
    y_valid = utilities.get_value_from_dict(output, ['y_valid'], None)
    sample_weight_valid = utilities.get_value_from_dict(
        output, ['sample_weight_valid'], None)
    X_test = utilities.get_value_from_dict(output, ['X_test'], None)
    y_test = utilities.get_value_from_dict(output, ['y_test'], None)
    data = utilities.get_value_from_dict(output, ['data_train'], None)
    columns = utilities.get_value_from_dict(output, ['columns'], None)
    label = utilities.get_value_from_dict(output, ['label'], None)
    cv_splits_indices = utilities.get_value_from_dict(
        dictionary=output,
        names=["cv_splits_indices"], default_value=None)
    x_raw_column_names = None

    if data is not None:
        if label is None and X is None and y is None:
            raise EmptyDataException(
                'Pandas data array received without a label. Please add a ''label'' element to the '
                'get_data() output.', has_pii=False)
        if not isinstance(label, list):
            assert(isinstance(label, str) or isinstance(label, int))
            label = [label]
        y_extracted = data[label].values
        X_extracted = data[data.columns.difference(label)]
        if columns is not None:
            X_extracted = X_extracted[X_extracted.columns.intersection(
                columns)]

        if X is None and y is None:
            X = X_extracted
            y = y_extracted
        else:
            if np.array_equiv(X, X_extracted.values):
                raise InvalidDataTypeException(
                    "Different values for X and data were provided. "
                    "Please return either X and y or data and label.", has_pii=False)
            if np.array_equiv(y, y_extracted.values):
                raise InvalidDataTypeException(
                    "Different values for y and label were provided. "
                    "Please return either X and y or data and label.", has_pii=False)
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
        X = X.values
    if isinstance(X_valid, pd.DataFrame):
        X_valid = X_valid.values
    if isinstance(X_test, pd.DataFrame):
        X_test = X_test.values
    if isinstance(y, pd.DataFrame):
        y = y.values
    if isinstance(y_valid, pd.DataFrame):
        y_valid = y_valid.values
    if isinstance(y_test, pd.DataFrame):
        y_test = y_test.values

    if X is None:
        raise EmptyDataException(
            "Could not retrieve X train data from get_data() call. "
            "Please ensure you are either returning either "
            "{X_train: <numpy array>, y_train: <numpy array>"
            "or {data: <pandas dataframe>, label: <string>", has_pii=False)
    if y is None:
        raise EmptyDataException(
            "Could not retrieve y train data from get_data() call. "
            "Please ensure you are either returning either "
            "{X_train: <numpy array>, y_train: <numpy array>"
            "or {data: <pandas dataframe>, label: <string>", has_pii=False)

    if (X_valid is None) is not (y_valid is None):
        raise EmptyDataException(
            'Received only one of X_valid or y_valid.'
            'Either both or neither value should be provided.', has_pii=False)

    return {
        "X": X,
        "y": y,
        "x_raw_column_names": x_raw_column_names,
        "sample_weight": sample_weight,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": sample_weight_valid,
        "X_test": X_test,
        "y_test": y_test,
        "cv_splits_indices": cv_splits_indices,
    }


def _extract_data_from_tuple(
        output: Tuple[Union[pd.DataFrame, np.ndarray], Union[pd.DataFrame, np.ndarray],
                      Union[pd.DataFrame, np.ndarray], Union[pd.DataFrame, np.ndarray]]) \
        -> Dict[str, Optional[Union[np.ndarray, List[str], float, List[int]]]]:
    """
    Extract user data if it is passed as a tuple.

    Arguments:
        output {tuple} -- tuple containing user data.

    Raises:
        DataException -- Could not extract X, y from get_data() in user script. get_data only output {0} values.

    Returns:
        tuple -- tuple containing X_train, y_train, X_test, y_test

    """
    X_valid, y_valid = None, None
    if len(output) < 2:
        msg = ("Could not extract X, y from get_data() in user "
               "script. get_data only output {0} values.")
        raise EmptyDataException(msg.format(len(output))).with_generic_msg(msg.format(MASKED)) from None
    x_raw_column_names = None
    X = output[0]
    y = output[1]
    if isinstance(X, pd.DataFrame):
        x_raw_column_names = X.columns.values
        X = X.values
    if isinstance(y, pd.DataFrame):
        y = y.values

    if len(output) >= 4:
        X_valid = output[2]
        y_valid = output[3]
        if isinstance(y_valid, pd.DataFrame):
            y_valid = y_valid.values
        if isinstance(X_valid, pd.DataFrame):
            X_valid = X_valid.values

    return {
        "X": X,
        "y": y,
        "sample_weight": None,
        "x_raw_column_names": x_raw_column_names,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "sample_weight_valid": None,
        "X_test": None,
        "y_test": None,
        "cv_splits_indices": None,
    }


def _extract_data_from_combined_dataframe(
        training_data: pd.DataFrame,
        label_column_name: str,
        sample_weight_column_name: Optional[str] = None,
        cv_split_column_names: Optional[List[str]] = None
) -> Tuple[Any, Any, Any, Any]:
    """
    Extract user data from a Pandas dataframe if it contains both training features & labels.

    :param training_data: The Pandas dataframe to extract X, y, sample_valid from.
    :param label_column_name: Name of the label column used to extract y.
    :param sample_weight_column_name: Name of the sample weight column.
    :param cv_split_column_names: List of names of the cv split columns.
    :return: A Dictionary with keys being X, y, sample_weight, cv_splits_indices extracted from training_data.
    """
    col_names_to_drop = [label_column_name]
    sample_weight = None
    cv_splits_indices = None

    if sample_weight_column_name is not None:
        col_names_to_drop.append(sample_weight_column_name)
        if sample_weight_column_name not in training_data.columns:
            msg = ('The sample weight column {} is not found in input data, '
                   'please double check')
            raise LabelMissingException(
                msg.format(sample_weight_column_name),
                reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFRAME_SAMPLE_WEIGHT_MISSING
            ).with_generic_msg(msg.format(MASKED))
        sample_weight = training_data[sample_weight_column_name].values

    if cv_split_column_names is not None:
        col_names_to_drop.extend(cv_split_column_names)
        for cv_split_column_name in cv_split_column_names:
            if cv_split_column_name not in training_data.columns:
                raise LabelMissingException(
                    'CV split column {} not found in input data. '
                    'Please double check cv_split_column_names and try again.'
                    .format(cv_split_column_name),
                    reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFRAME_CV_SPLIT_COLUMNS_MISSING
                ).with_generic_msg(
                    'CV split column not found in input data. '
                    'Please double check cv_split_column_names and try again.'
                )
        cv_split_columns = training_data[cv_split_column_names]
        cv_splits_indices = _convert_cv_split_columns_to_cv_splits_indices(cv_split_columns)

    X = training_data[training_data.columns.difference(col_names_to_drop)]
    if label_column_name not in training_data.columns:
        raise LabelMissingException('The label column {} is not found in input data, '
                                    'please double check'.format(label_column_name))\
            .with_generic_msg("The label column was not found in the input data.")
    y = training_data[label_column_name].values

    return X, y, sample_weight, cv_splits_indices


def _extract_data_from_combined_dataflow(
        training_data: dprep.Dataflow,
        label_column_name: str,
        sample_weight_column_name: Optional[str] = None,
        cv_split_column_names: Optional[List[str]] = None
) -> Tuple[Any, Any, Any, Any]:
    """
    Extract user data from a Dataflow if it contains both training features & labels.

    :param training_data: The Dataflow to extract X, y, sample_valid from.
    :param label_column_name: Name of the label column used to extract y.
    :param sample_weight_column_name: Name of the sample weight column.
    :param cv_split_column_names: List of names of the cv split columns.
    :return: A Dictionary with keys being X, y, sample_weight, cv_splits_indices extracted from training_data.
    """
    col_names_to_drop = [label_column_name]
    sample_weight = None
    cv_splits_indices = None

    if sample_weight_column_name is not None:
        col_names_to_drop.append(sample_weight_column_name)
        try:
            sample_weight = training_data.keep_columns([sample_weight_column_name], validate_column_exists=True)
        except DataflowValidationError:
            msg = ('The sample weight column {} is not found in input data, '
                   'please double check')
            raise EmptyDataException(
                msg.format(sample_weight_column_name),
                reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFLOW_SAMPLE_WEIGHT_MISSING,
                has_pii=True).with_generic_msg(msg.format(MASKED))

    if cv_split_column_names is not None:
        col_names_to_drop.extend(cv_split_column_names)
        try:
            cv_split_columns = training_data.keep_columns(cv_split_column_names, validate_column_exists=True)
            cv_splits_indices = _convert_cv_split_columns_to_cv_splits_indices(cv_split_columns)
        except DataflowValidationError:
            raise EmptyDataException(
                'CV split column not found in input data. '
                'Please double check cv_split_column_names and try again.',
                reference_code=ReferenceCodes._EXTRACT_DATA_FROM_COMBINED_DATAFLOW_CV_SPLIT_COLUMNS_MISSING,
                has_pii=False)

    X = training_data.drop_columns(col_names_to_drop)
    try:
        y = training_data.keep_columns([label_column_name], validate_column_exists=True)
    except DataflowValidationError:
        raise LabelMissingException('The label column {} is not found in input data, '
                                    'please double check'.format(label_column_name))\
            .with_generic_msg("The label column was not found in the input data.")
    return X, y, sample_weight, cv_splits_indices


def _convert_cv_split_columns_to_cv_splits_indices(
        cv_split_columns: Union[dprep.Dataflow, pd.DataFrame]
) -> List[Tuple[Any, Any]]:
    cv_splits_indices = []
    if isinstance(cv_split_columns, pd.DataFrame):
        cv_split_columns_numpy = cv_split_columns.values
    else:
        cv_split_columns_numpy = dataprep_utilities.retrieve_numpy_array(cv_split_columns)
    if cv_split_columns_numpy.ndim == 1:
        training_indices, validation_indices = _get_column_to_cv_splits_indices(cv_split_columns_numpy)
        cv_splits_indices.append([training_indices, validation_indices])
    else:
        for i in range(cv_split_columns_numpy.shape[1]):
            column = cv_split_columns_numpy[:, i]
            training_indices, validation_indices = _get_column_to_cv_splits_indices(column)
            cv_splits_indices.append([training_indices, validation_indices])
    return cv_splits_indices


def _get_column_to_cv_splits_indices(column: np.ndarray) -> Tuple[Any, Any]:
    msg = "CV Split column contains data other than 1 or 0. Please check your cv split columns and try again."

    try:
        training_indices, = np.where(column.astype(int) == 1)
        validation_indices, = np.where(column.astype(int) == 0)
    except ValueError:
        raise DataFormatException.create_without_pii(
            msg,
            reference_code=ReferenceCodes._CV_SPLIT_COLUMN_CONVERSION_ASTYPE_INT_FAIL,
            target="GetColumnToCVSplitsIndices"
        )

    # verify number of indices extracted equal number of total rows
    if len(training_indices) + len(validation_indices) != len(column):
        raise DataFormatException.create_without_pii(
            msg,
            reference_code=ReferenceCodes._CV_SPLIT_COLUMN_CONVERSION_INCORRECT_INT_VALUE,
            target="GetColumnToCVSplitsIndices"
        )

    return training_indices, validation_indices


def _get_model_exp_property(
        automl_run: Any,
        logger: Optional[Union[logging.Logger, logging.LoggerAdapter]] = None) -> bool:
    try:
        from azureml.train.automl.runtime._remote_script import model_exp_wrapper
        automl_algo_name = automl_run.get_properties().get('run_algorithm')
        if automl_algo_name != 'StackEnsemble' and automl_algo_name != 'VotingEnsemble':
            if_model_is_explainable = True

            if logger is not None and not if_model_is_explainable:
                logger.warning(automl_algo_name + ' is not explainable for AutoML run ' + str(automl_run.id))

            return if_model_is_explainable
        else:
            ensemble_algo_names_list_str = automl_run.get_tags().get('ensembled_algorithms')
            if ensemble_algo_names_list_str is not None:
                if_ensemble_model_is_explainable = True
                if logger is not None and not if_ensemble_model_is_explainable:
                    logger.warning(automl_algo_name + ' is not explainable for AutoML run ' + str(automl_run.id))

                return if_ensemble_model_is_explainable
            else:
                return True
    except Exception:
        return False


def _check_data_can_be_preprocessed(X: DataInputType,
                                    X_valid: DataInputType,
                                    x_raw_column_names: Optional[np.ndarray] = None) -> None:
    if scipy.sparse.issparse(X):
        return
    n_x_col = 1 if len(X.shape) == 1 else X.shape[1]
    if x_raw_column_names is None and isinstance(X, np.ndarray):
        x_raw_column_names = np.arange(n_x_col)
    elif x_raw_column_names is None:
        # if pandas df, try to use columns_names from dataframe
        x_raw_column_names = X.columns

    for col_num, col_name in zip(range(n_x_col), x_raw_column_names):
        _check_column_can_be_preprocessed(_get_column_by_column_number(X, col_num), col_name, False)
        if X_valid is not None:
            _check_column_can_be_preprocessed(_get_column_by_column_number(X_valid, col_num), col_name, True)


def _check_column_can_be_preprocessed(series: pd.Series, col_name: str, is_valid_data: bool) -> None:
    try:
        # TODO: Check if this is true for all cases
        # preprocess need pandas.unique can be run properly.
        series.unique()
    except TypeError:
        input_type = "X_valid" if is_valid_data else "X"
        raise UnhashableEntryException(
            "The input {} column {} has data that cannot "
            "be preprocessed. Please check your input.".format(input_type, col_name))\
            .with_generic_msg("An input column has data that cannot be preprocessed.")


def _get_column_by_column_number(X: DataInputType, col_num: int) -> pd.Series:
    if isinstance(X, np.ndarray) and len(X.shape) == 1:
        return pd.Series(X)
    elif isinstance(X, np.ndarray):
        return pd.Series(X[:, col_num])
    else:
        return pd.Series(X.iloc[:, col_num])


def _validate_exp_timeout_for_data(X: DataInputType, automl_settings: AutoMLBaseSettings) -> None:
    error_msg = ("The ExperimentTimeout should be set more than 60 minutes with "
                 "an input data of rows*cols({}*{}={}) more than {:,}.")

    if X is not None and automl_settings is not None:
        if automl_settings.experiment_timeout_minutes is not None:
            if not scipy.sparse.issparse(X):
                n_rows = X.shape[0]
                n_cols = 1 if len(X.shape) < 2 else X.shape[1]
                # 1M is the timeout needs to be 60 min
                if n_rows * n_cols > constants.AutoMLValidation.TIMEOUT_DATA_BOUND \
                        and automl_settings.experiment_timeout_minutes < 60:
                    raise OutOfRangeException(
                        error_msg.format(
                            n_rows, n_cols, n_rows * n_cols, constants.AutoMLValidation.TIMEOUT_DATA_BOUND),
                        target="experiment_timeout_minutes",
                        reference_code=ReferenceCodes._VALIDATE_EXP_TIMEOUT_WITH_DATA, has_pii=False)


def _validate_all_column_not_ignored(
        X: DataInputType,
        x_raw_column_names: List[str],
        automl_settings: AutoMLBaseSettings
) -> None:
    """
    Validate whether all columns will be dropped by AutoML or not during featurization.

    :param X: The X input data.
    :param x_raw_column_names: A list of input x column names.
    :param automl_settings: The automl settings.
    """
    if isinstance(X, np.ndarray):
        df = pd.DataFrame(X, columns=x_raw_column_names)
    elif isinstance(X, pd.DataFrame):
        df = X
    else:
        # no check for the sparse scenario
        return

    featurization = automl_settings.featurization
    is_customized_featurization_enabled = isinstance(automl_settings.featurization, dict)

    # There is no data transformation when featurization is off.
    if featurization == FeaturizationConfigMode.Off:
        return

    # Featurization auto mode, all the related column set is empty.
    customized_columns = set()  # type: Set[str]
    transformer_params_column_set = set()  # type: Set[str]
    if is_customized_featurization_enabled:
        drop_columns_set = set(featurization.get("_drop_columns") or [])
        column_purpose_keep_column_dict = {}  # type: Dict[str, str]
        column_purpose_drop_column_dict = {}  # type: Dict[str, str]
        if featurization.get("_column_purposes") is not None:
            for column, purpose in featurization.get("_column_purposes").items():
                if purpose in _FeatureType.DROP_SET:
                    column_purpose_drop_column_dict[column] = purpose
                else:
                    column_purpose_keep_column_dict[column] = purpose

        transformer_params = featurization.get("_transformer_params") or {}
        for transfom_param in transformer_params.values():
            for cols, _ in transfom_param:
                transformer_params_column_set = transformer_params_column_set.union(cols)
        featurization_keep_column_set = set(column_purpose_keep_column_dict.keys())
        featurization_drop_column_set = drop_columns_set.union(column_purpose_drop_column_dict.keys())
        customized_columns = featurization_drop_column_set.union(featurization_keep_column_set)

    stats_and_column_purposes = ColumnPurposeDetector.get_raw_stats_and_column_purposes(df)

    not_auto_dropped_columns = set()  # type: Set[str]
    column_drop_reason_list = []  # type: List[str]
    dropped_transformer_params_column = []  # type: List[Tuple[str, str]]
    for _, feature_type_detected, column in stats_and_column_purposes:
        if feature_type_detected in _FeatureType.DROP_SET and column not in customized_columns:
            column_drop_reason_list.append(
                "Column {}, AutoML detected type {}.".format(column, feature_type_detected)
            )
            if column in transformer_params_column_set:
                dropped_transformer_params_column.append((column, feature_type_detected))
        else:
            not_auto_dropped_columns.add(column)
    # This should be logged via ConsoleInterface. Commenting this out until ConsoleInterface is available here.
    # if len(dropped_transformer_params_column) > 0:
    #     print("The following transformer_params in featurization config will be ignored as the these columns are"
    #           "automatically dropped by AutoML. If you still want to use these columns, please set correct value"
    #           "in column_purposes of featurizaiton config:")
    #     for col, purpose in dropped_transformer_params_column:
    #         print("Column {}, AutoML detected type {}.".format(col, purpose))

    if len(not_auto_dropped_columns) == 0:
        raise EmptyDataException(
            "All columns are automatically detected as ignored column by AutoML as no useful information "
            "can be inferred from the input data. The detected column purpose is as following,\n{}\n"
            "Please either inspect your input data or use featurization config to give hints about the desired "
            "data transformation.".format("\n".join(column_drop_reason_list)),
            target="X",
            reference_code=ReferenceCodes._VALIDATE_ALL_COLUMN_IGNORED,
            has_pii=True
        ).with_generic_msg('All columns are ignored by AutoML.')

    # Only check this part if featurization config is enabled.
    if is_customized_featurization_enabled:
        final_keep_column = set()  # type: Set[str]
        for column in sorted(not_auto_dropped_columns):
            if column not in featurization_drop_column_set:
                final_keep_column.add(column)
            if column in drop_columns_set:
                column_drop_reason_list.append(
                    "Column {}, included in featurization config's drop columns.".format(column))
            if column in column_purpose_drop_column_dict:
                column_drop_reason_list.append(
                    "Column {}, marked as {} in featurization config.".format(
                        column, column_purpose_drop_column_dict[column]))

        if len(final_keep_column) == 0:
            raise EmptyDataException(
                "All columns are automatically detected as ignored column by AutoML, ignored as drop columns or "
                "marked as ignored types({}) in featurization config. The detailed reason for ignoring column is as "
                "following,\n{}\nPlease either inspect your input data or modify your featurization config to give "
                "AutoML correct hints about data transformation.".format(
                    ", ".join(sorted(_FeatureType.DROP_SET)),
                    "\n".join(column_drop_reason_list)),
                target="featurization_config",
                reference_code=ReferenceCodes._VALIDATE_ALL_COLUMN_IGNORED_FEATURIZATION,
                has_pii=True
            ).with_generic_msg('All columns are as ignored by AutoML or featurization config.')
