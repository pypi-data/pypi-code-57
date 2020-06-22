# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
from msrest.exceptions import HttpOperationError
from abc import ABC, abstractmethod
from typing import Any, cast, Dict, List, Optional, Tuple

import azureml.dataprep as dprep
from azureml.automl.runtime import dataprep_utilities as dataprep_runtime_utilities
from azureml.automl.runtime import training_utilities
from azureml.core import Run, Dataset, Datastore
from azureml.dataprep.api.dataflow import DataflowValidationError
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from ._data_characteristics_calculator import DataCharacteristicsCalculator, DataCharacteristics
from azureml.automl.core import dataprep_utilities
from azureml.train.automl.exceptions import AuthorizationException, ClientException, ConfigException, \
    DataException, DatasetServiceException, NotFoundException
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import AutoMLException, MemorylimitException
from azureml.automl.core.shared.reference_codes import ReferenceCodes

try:
    from azureml.dataprep import DataPrepException as DprepException
except ImportError:
    # TODO Task 748385. Clean up this branch once dataprep min version is updated to 1.6.0
    from azureml.dataprep import ExecutionError as DprepException

logger = logging.getLogger(__name__)


class DataPreparer(ABC):

    def __init__(self, dataprep_json_obj: Dict[str, Any]):
        """
        :param dataprep_json_obj: The JSON that represents the data location and metadata
        """
        self.data_characteristics = None     # type: Optional[DataCharacteristics]
        self._original_training_data = None  # type: Optional[dprep.Dataflow]
        with logging_utilities.log_activity(logger=logger, activity_name='ParsingDataprepJSON'):
            self._parse(dataprep_json_obj)

        with logging_utilities.log_activity(logger=logger, activity_name="BuildingDataCharacteristics"):
            self._buiid_data_characterstics()

    @abstractmethod
    def _parse(self, dataprep_json_obj: Dict[str, Any]) -> None:
        """
        Parse the JSON and cache the results for future use
        :param dataprep_json_obj:The JSON that represents the data location and metadata
        """
        raise NotImplementedError

    @abstractmethod
    def _get_fit_params(self, automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:
        """
        Return the fit data params
        :param automl_settings_obj: automl settings
        :return: dictionary containing fit data params
        """
        raise NotImplementedError

    def prepare(self, automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:
        """
        prepare data and return fit params
        :param automl_settings_obj: automl settings
        :return: dictionary containing fit data params
        """
        try:
            fit_params = self._get_fit_params(automl_settings_obj)
        except DprepException as e:
            logging_utilities.log_traceback(e, logger)
            dataprep_runtime_utilities.dataprep_error_handler(e)
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            reference_code_for_ex = 'prepare'
            if isinstance(e, DataflowValidationError):
                raise DataException.from_exception(e, reference_code=reference_code_for_ex).with_generic_msg(
                    'Dataflow validation error during data preparation.')
            elif isinstance(e, MemoryError):
                generic_msg = 'Failed to get data from DataPrep due to MemoryError'
                raise MemorylimitException.from_exception(e, reference_code=reference_code_for_ex,
                                                          msg=generic_msg, has_pii=False)
            elif not isinstance(e, AutoMLException):
                generic_msg = 'Failed to get data from DataPrep. Exception Type: {}'.format(type(e))
                logger.error(generic_msg)
                raise ClientException.from_exception(e, reference_code=reference_code_for_ex).with_generic_msg(
                    generic_msg)
            else:
                raise
        return fit_params

    def _buiid_data_characterstics(self):
        """
        Build data characteristics of the original training data and cache it for future use
        :return:
        """
        if self._original_training_data is not None:
            try:
                logger.info('Starting data characteristics calculation. This might take a while...')
                self.data_characteristics = DataCharacteristicsCalculator.calc_data_characteristics(
                    self._original_training_data)
            except Exception:
                # this is best effort based - hence log as info
                logger.info('data characteristics calculation failed')


class DataPreparerFromDataSet(DataPreparer):
    """
    Used to prepare the data when the input to training_data is a Dataset object.
    """

    def __init__(self, dataprep_json_obj: Dict[str, Any]):
        super().__init__(dataprep_json_obj)

    def _parse(self, dataprep_json_obj: Dict[str, Any]) -> None:
        logger.info('Creating dataflow from datasets for training_data and validation_data.')
        training_data = dataprep_json_obj['training_data']
        validation_data = dataprep_json_obj.get('validation_data', None)
        training_dataset_id = training_data['datasetId']  # mandatory

        ws = Run.get_context().experiment.workspace

        from azureml.data._dataset_deprecation import silent_deprecation_warning
        with silent_deprecation_warning():
            training_dataset = Dataset.get_by_id(ws, id=training_dataset_id)
            self.training_dataflow = training_dataset._dataflow

            self.validation_dataflow = None
            if validation_data is not None:
                validation_dataset_id = validation_data['datasetId']  # mandatory
                validation_data = Dataset.get_by_id(ws, id=validation_dataset_id)
                self.validation_dataflow = validation_data._dataflow

        self._original_training_data = self.training_dataflow

    def _get_fit_params(self, automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:
        if self.data_characteristics is None or not self.data_characteristics:
            training_data_row_count = 0
        else:
            training_data_row_count = self.data_characteristics.num_rows
        return DataPreparerUtils._get_dict_from_dataflows(self.training_dataflow,
                                                          self.validation_dataflow,
                                                          automl_settings_obj,
                                                          training_data_row_count)


class DataPreparerFromSerializedDataflows(DataPreparer):
    """
    Used to prepare the data when the input to training_data/X is a dataflow object.
    """

    def __init__(self, dataprep_json_obj: Dict[str, Any]):
        super().__init__(dataprep_json_obj)

    def _parse(self, dataprep_json_obj: Dict[str, Any]) -> None:
        logger.info('Deserializing dataflow.')
        self.dataflow_dict = dataprep_utilities.load_dataflows_from_json_dict(dataprep_json_obj)
        self._original_training_data = self.dataflow_dict.get('training_data')

    def _get_fit_params(self, automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:
        if self.data_characteristics is not None:
            training_data_row_count = self.data_characteristics.num_rows
        else:
            training_data_row_count = 0
        return DataPreparerUtils._helper_get_data_from_dict(self.dataflow_dict,
                                                            automl_settings_obj,
                                                            training_data_row_count)


class DataPreparerFromDatasetOptions(DataPreparer):
    """
    Used to prepare the data when the input comes from UI.
    """

    def __init__(self, dataprep_json_obj: Dict[str, Any]):
        super().__init__(dataprep_json_obj)

    def _parse(self, dataprep_json_obj: Dict[str, Any]) -> None:
        logger.info('Creating dataflow from dataset.')
        dataset_id = dataprep_json_obj['datasetId']  # mandatory
        self.label_column = dataprep_json_obj['label']  # mandatory
        self.feature_columns = dataprep_json_obj.get('features', [])

        ws = Run.get_context().experiment.workspace
        from azureml.data._dataset_deprecation import silent_deprecation_warning
        with silent_deprecation_warning():
            dataset = Dataset.get(ws, id=dataset_id)
        self._original_training_data = dataset.definition

    def _get_fit_params(self, automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:
        if self.data_characteristics is None or not self.data_characteristics:
            training_data_row_count = 0
        else:
            training_data_row_count = self.data_characteristics.num_rows
        return DataPreparerUtils._get_dict_from_dataflow(self._original_training_data,
                                                         automl_settings_obj,
                                                         self.feature_columns,
                                                         self.label_column,
                                                         training_data_row_count)


class DataPreparerFromDataprepOptions(DataPreparer):
    """
    Used to prepare the data when the input is dataset options parameter.
    """

    def __init__(self, dataprep_json_obj: Dict[str, Any]):
        super().__init__(dataprep_json_obj)

    def _parse(self, dataprep_json_obj: Dict[str, Any]) -> None:
        logger.info('Creating dataflow from options.')
        data_store_name = dataprep_json_obj['datastoreName']  # mandatory
        data_path = dataprep_json_obj['dataPath']  # mandatory
        self.label_column = dataprep_json_obj['label']  # mandatory
        separator = dataprep_json_obj.get('columnSeparator', ',')
        quoting = dataprep_json_obj.get('ignoreNewlineInQuotes', False)
        skip_rows = dataprep_json_obj.get('skipRows', 0)
        self.feature_columns = dataprep_json_obj.get('features', [])
        encoding = getattr(dprep.FileEncoding, cast(str, dataprep_json_obj.get('encoding')), dprep.FileEncoding.UTF8)
        if dataprep_json_obj.get('promoteHeader', True):
            header = dprep.PromoteHeadersMode.CONSTANTGROUPED
        else:
            header = dprep.PromoteHeadersMode.NONE
        ws = Run.get_context().experiment.workspace
        data_store = Datastore(ws, data_store_name)
        self._original_training_data = dprep.read_csv(path=data_store.path(data_path),
                                                      separator=separator,
                                                      header=header,
                                                      encoding=encoding,
                                                      quoting=quoting,
                                                      skip_rows=skip_rows)

    def _get_fit_params(self, automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:
        if self.data_characteristics is None or not self.data_characteristics:
            training_data_row_count = 0
        else:
            training_data_row_count = self.data_characteristics.num_rows
        return DataPreparerUtils._get_dict_from_dataflow(self._original_training_data,
                                                         automl_settings_obj,
                                                         self.feature_columns,
                                                         self.label_column,
                                                         training_data_row_count)


class DataPreparerFactory:
    """
    A factory class that can return the appropriate preparer based on JSON contents
    """

    @staticmethod
    def get_preparer(dataprep_json: str) -> DataPreparer:
        """
        Return a preparer based on JSON contents
        :param dataprep_json: JSON representing input data location and metadata
        :return: Datapreparer that can handle the data
        """
        try:
            logger.info('Resolving dataflows using dprep json.')
            logger.info('DataPrep version: {}'.format(dprep.__version__))
            try:
                from azureml._base_sdk_common import _ClientSessionId
                logger.info('DataPrep log client session id: {}'.format(_ClientSessionId))
            except Exception:
                logger.info('Cannot get DataPrep log client session id')

            dataprep_json_obj = json.loads(dataprep_json)

            if 'activities' in dataprep_json_obj:
                preparer = DataPreparerFromSerializedDataflows(dataprep_json_obj)  # type: DataPreparer
            elif 'datasetId' in dataprep_json_obj:
                preparer = DataPreparerFromDatasetOptions(dataprep_json_obj)
            elif 'datasets' in dataprep_json_obj:
                preparer = DataPreparerFromDataSet(dataprep_json_obj)
            else:
                preparer = DataPreparerFromDataprepOptions(dataprep_json_obj)

            logger.info('Successfully retrieved data using dataprep.')
            return preparer

        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            msg = str(e)
            reference_code_for_ex = '_get_data_from_dataprep'
            if "The provided path is not valid." in msg:
                raise ConfigException.from_exception(e, reference_code=reference_code_for_ex).with_generic_msg(
                    'The provided path is not valid.'
                )
            elif "Required secrets are missing. Please call use_secrets to register the missing secrets." in msg:
                raise ConfigException.from_exception(e, reference_code=reference_code_for_ex).with_generic_msg(
                    'Required secrets are missing. Please call use_secrets to register the missing secrets.'
                )
            elif "Cannot find dataset registered with name" in msg:
                raise NotFoundException.from_exception(e, 'Dataset not found.', reference_code=reference_code_for_ex)
            elif isinstance(e, HttpOperationError):
                if e.response.status_code == 404:
                    raise NotFoundException.from_exception(
                        e, 'Dataset not found.', reference_code=reference_code_for_ex)
                elif e.response.status_code == 401:
                    raise AuthorizationException.from_exception(
                        e, 'Error while trying to get Dataset.', reference_code=reference_code_for_ex)
                elif e.response.status_code >= 400 and e.response.status_code < 500:
                    raise ConfigException.from_exception(e, reference_code=reference_code_for_ex)
                else:
                    raise DatasetServiceException.from_exception(e, reference_code=reference_code_for_ex)
            elif isinstance(e, json.JSONDecodeError):
                raise ConfigException.from_exception(
                    e, 'Invalid dataprep JSON string passed.', reference_code=reference_code_for_ex)
            elif isinstance(e, DataflowValidationError):
                raise DataException.from_exception(e, reference_code=reference_code_for_ex).with_generic_msg(
                    'Error in dataflow validation while fetching data preparer.'
                )
            elif not isinstance(e, AutoMLException):
                generic_msg = 'Failed to get data from DataPrep. Exception Type: {}'.format(type(e))
                logger.error(generic_msg)
                raise ClientException.from_exception(e, reference_code=reference_code_for_ex).with_generic_msg(
                    generic_msg)
            else:
                raise


class DataPreparerUtils:
    """
    A set of utilities that can build fit data params given dataflow
    """
    @staticmethod
    def _get_dict_from_dataflows(training_dflow: Any,
                                 validation_dflow: Any,
                                 automl_settings_obj: AzureAutoMLSettings,
                                 train_data_row_count: int) -> Dict[str, Any]:
        training_data = DataPreparerUtils._get_inferred_types_dataflow(training_dflow)
        validation_data = None
        if validation_dflow is not None:
            validation_data = DataPreparerUtils._get_inferred_types_dataflow(validation_dflow)

        fit_iteration_parameters_dict = {}  # type: Dict[str, Any]
        fit_iteration_parameters_dict = DataPreparerUtils._set_dict_from_dataflow(training_data,
                                                                                  validation_data,
                                                                                  automl_settings_obj)

        return DataPreparerUtils._helper_get_data_from_dict(fit_iteration_parameters_dict,
                                                            automl_settings_obj,
                                                            train_data_row_count)

    @staticmethod
    def _get_dict_from_dataflow(dflow: Any,
                                automl_settings_obj: AzureAutoMLSettings,
                                feature_columns: List[str],
                                label_column: str,
                                train_data_row_count: int) -> Dict[str, Any]:
        fit_iteration_parameters_dict = {}  # type: Dict[str, Any]
        if not automl_settings_obj.enable_streaming:
            if len(feature_columns) == 0:
                X = dflow.drop_columns(label_column)
            else:
                X = dflow.keep_columns(feature_columns)

            X = DataPreparerUtils._get_inferred_types_dataflow(X)
            y = dflow.keep_columns(label_column)
            if automl_settings_obj.task_type == constants.Tasks.REGRESSION:
                y = y.to_number(label_column)

            _X = dataprep_runtime_utilities.retrieve_pandas_dataframe(X)
            _y = dataprep_runtime_utilities.retrieve_numpy_array(y)

            fit_iteration_parameters_dict = {
                "X": _X.values,
                "y": _y,
                "sample_weight": None,
                "x_raw_column_names": _X.columns.values,
                "X_valid": None,
                "y_valid": None,
                "sample_weight_valid": None,
                "X_test": None,
                "y_test": None,
                "cv_splits_indices": None,
            }
        else:
            if len(feature_columns) > 0:
                feature_columns_with_label = feature_columns + [label_column]
                dflow1 = dflow.keep_columns(feature_columns_with_label)
                training_data = dflow1
            else:
                training_data = dflow

            training_data = DataPreparerUtils._get_inferred_types_dataflow(training_data)
            validation_data, training_data = DataPreparerUtils._split_data_train_valid(
                training_data, train_data_row_count, automl_settings_obj.validation_size)

            fit_iteration_parameters_dict = DataPreparerUtils._set_dict_from_dataflow(
                training_data, validation_data, automl_settings_obj)
        return fit_iteration_parameters_dict

    @staticmethod
    def _helper_get_data_from_dict(dataflow_dict: Dict[str, Any],
                                   automl_settings_obj: AzureAutoMLSettings,
                                   train_data_row_count: int) -> Dict[str, Any]:
        if automl_settings_obj.enable_streaming:
            if 'training_data' not in dataflow_dict \
                    or automl_settings_obj.label_column_name is None:
                raise ConfigException("Streaming does not support X and y settings. "
                                      "Please provide 'training_data', 'validation_data' as DataFlow objects and "
                                      "'label_column_name' for target column name in AutoMLConfig.", has_pii=False)

            columns_list = [automl_settings_obj.label_column_name]
            if automl_settings_obj.weight_column_name is not None:
                columns_list.append(automl_settings_obj.weight_column_name)
            if automl_settings_obj.cv_split_column_names is not None:
                # CV Splits is not supported for streaming right now, these columns are dropped and not used
                columns_list.extend(automl_settings_obj.cv_split_column_names)

            fit_iteration_parameters_dict = dataflow_dict.copy()
            training_data = fit_iteration_parameters_dict.get('training_data')
            if training_data is None:
                raise DataflowValidationError("Training_data is not present in DataPrep JSON string", has_pii=False)
            validation_data = fit_iteration_parameters_dict.get('validation_data')

            if validation_data is not None:
                if train_data_row_count > 0:
                    # Attempt to calculate validation row count only if training row count has succeeded
                    # we're going to subsample the validation set to ensure we can compute the metrics in memory
                    data_profile = validation_data.get_profile()
                    validation_samples_count = data_profile.row_count
                    max_validation_size = training_utilities.LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE
                    if validation_samples_count > max_validation_size:
                        sample_probability = max_validation_size / validation_samples_count
                        logger.warning(
                            'Subsampling the validation from {} samples with a probability of {}.'
                            .format(validation_samples_count, sample_probability))
                        validation_data = validation_data.take_sample(probability=sample_probability, seed=42)

                # Some of the validation code downstream expects 'X_valid' and 'y_valid'. Hence populate that.
                fit_iteration_parameters_dict['X_valid'] = validation_data.drop_columns(columns_list)
                fit_iteration_parameters_dict['y_valid'] = validation_data.keep_columns(
                    automl_settings_obj.label_column_name)
            else:
                # since the validation data is not provided, we create one ourselves by splitting the training_data
                # Validations on this can be skipped (since it's a part of training data itself)
                validation_data, training_data = DataPreparerUtils._split_data_train_valid(
                    training_data, train_data_row_count, automl_settings_obj.validation_size)

            fit_iteration_parameters_dict['training_data'] = training_data
            fit_iteration_parameters_dict['validation_data'] = validation_data

            # Across SDK, we have a mixed use of ['X' or 'X_valid'] and 'training_data'.
            # Hence, fill in the other values so that other stuff works.
            fit_iteration_parameters_dict['X'] = training_data.drop_columns(columns_list)
            fit_iteration_parameters_dict['y'] = training_data.keep_columns(
                automl_settings_obj.label_column_name)

            fit_iteration_parameters_dict['x_raw_column_names'] = fit_iteration_parameters_dict['X'].head(
                1).columns.values

            if automl_settings_obj.weight_column_name is not None:
                fit_iteration_parameters_dict['sample_weight'] = training_data.keep_columns(
                    automl_settings_obj.weight_column_name)
                if automl_settings_obj.validation_size == 0:
                    # User provided a custom validation data
                    fit_iteration_parameters_dict['sample_weight_valid'] = validation_data.keep_columns(
                        automl_settings_obj.weight_column_name)

        else:
            cv_splits_indices = None
            if 'training_data' in dataflow_dict and automl_settings_obj.label_column_name is not None:
                df = dataflow_dict.get('training_data')  # type: dprep.Dataflow
                X, y, sample_weight, cv_splits_indices = training_utilities._extract_data_from_combined_dataflow(
                    df, automl_settings_obj.label_column_name, automl_settings_obj.weight_column_name,
                    automl_settings_obj.cv_split_column_names
                )
                dataflow_dict['X'] = X
                dataflow_dict['y'] = y
                dataflow_dict['sample_weight'] = sample_weight
                dataflow_dict.pop('training_data')

            if 'validation_data' in dataflow_dict and automl_settings_obj.label_column_name is not None:
                df = dataflow_dict.get('validation_data')
                X_valid, y_valid, sample_weight_valid, _ = training_utilities._extract_data_from_combined_dataflow(
                    df, automl_settings_obj.label_column_name,
                    sample_weight_column_name=automl_settings_obj.weight_column_name)
                dataflow_dict['X_valid'] = X_valid
                dataflow_dict['y_valid'] = y_valid
                dataflow_dict['sample_weight_valid'] = sample_weight_valid
                dataflow_dict.pop('validation_data')
            data_columns = ['X_valid', 'sample_weight', 'sample_weight_valid']
            label_columns = ['y', 'y_valid']

            fit_iteration_parameters_dict = {
                k: dataprep_runtime_utilities.retrieve_numpy_array(dataflow_dict.get(k))
                for k in data_columns
            }
            X = dataprep_runtime_utilities.retrieve_pandas_dataframe(dataflow_dict.get('X'))
            if X is None:
                raise DataException("Failed to retrieve feature columns, please make sure you set "
                                    "(training_data and label_column_name) or (X and Y) data correctly.",
                                    has_pii=False, target="_helper_get_data_from_dict",
                                    reference_code=ReferenceCodes._DATA_PREPARER_X_IS_NONE)

            fit_iteration_parameters_dict['x_raw_column_names'] = X.columns.values
            if X.shape[1] == 1:
                # if the DF is a single column ensure the resulting output is a 1 dim array by converting
                # to series first.
                fit_iteration_parameters_dict['X'] = X[X.columns[0]].values
            else:
                fit_iteration_parameters_dict['X'] = X.values

            for k in label_columns:
                fit_iteration_parameters_dict[k] = dataprep_runtime_utilities.retrieve_numpy_array(
                    dataflow_dict.get(k))

            if cv_splits_indices and automl_settings_obj.cv_split_column_names:
                # cv_splits_indices derived from cv_split_column_names
                fit_iteration_parameters_dict['cv_splits_indices'] = cv_splits_indices
            else:
                cv_splits_dataflows = []
                i = 0
                while 'cv_splits_indices_{0}'.format(i) in dataflow_dict:
                    cv_splits_dataflows.append(
                        dataflow_dict['cv_splits_indices_{0}'.format(i)])
                    i = i + 1

                fit_iteration_parameters_dict['cv_splits_indices'] = None if len(cv_splits_dataflows) == 0 \
                    else dataprep_runtime_utilities.resolve_cv_splits_indices(cv_splits_dataflows)

        return fit_iteration_parameters_dict

    @staticmethod
    def _get_inferred_types_dataflow(dflow: dprep.Dataflow) -> dprep.Dataflow:
        logger.info('Inferring type for feature columns.')
        set_column_type_dflow = dflow.builders.set_column_types()
        set_column_type_dflow.learn()
        set_column_type_dflow.ambiguous_date_conversions_drop()
        return set_column_type_dflow.to_dataflow()

    @staticmethod
    def _split_data_train_valid(
            train_data: dprep.Dataflow,
            train_data_row_count: int,
            validation_size: float = 0.0
    ) -> Tuple[dprep.Dataflow, dprep.Dataflow]:
        logger.info('Splitting input dataset into train & validation datasets')
        # sample_probability is a conservative estimate of what we think as a fair size of validation data
        # without running into memory errors, especially during metric calculation, which is currently
        # non-streaming
        sample_probability = 0.1   # type: float
        if train_data_row_count > 0:
            num_validation_rows = min(
                0.1 * train_data_row_count,
                training_utilities.LargeDatasetLimit.MAX_ROWS_TO_SUBSAMPLE)
            sample_probability = num_validation_rows / train_data_row_count

        if 0 < validation_size <= sample_probability:
            # User has provided a custom % for validation data, so pick the minimum of
            # 'validation_size' or 'sample_probability'
            ret = train_data.random_split(validation_size, seed=42)  # type: Tuple[dprep.Dataflow, dprep.Dataflow]
        else:
            if validation_size > 0 and validation_size > sample_probability:
                logger.warning(
                    "Overriding 'validation_size' to {} due to large data limits.".format(sample_probability))
            else:
                logger.info("'validation_size' was not specified. Using {}% of training data as validation data.".
                            format(sample_probability * 100))

            ret = train_data.random_split(sample_probability, seed=42)

        return ret

    @staticmethod
    def _set_dict_from_dataflow(training_data: Any,
                                validation_data: Any,
                                automl_settings_obj: AzureAutoMLSettings) -> Dict[str, Any]:

        fit_iteration_parameters_dict = {}  # type: Dict[str, Any]

        fit_iteration_parameters_dict['training_data'] = training_data
        if validation_data is not None:
            fit_iteration_parameters_dict['validation_data'] = validation_data

        columns_list = [automl_settings_obj.label_column_name]
        if automl_settings_obj.weight_column_name is not None:
            columns_list.append(automl_settings_obj.weight_column_name)

        # fill in x and y here so that other stuff works.
        fit_iteration_parameters_dict['X'] = training_data.drop_columns(columns_list)
        fit_iteration_parameters_dict['y'] = training_data.keep_columns(
            automl_settings_obj.label_column_name)

        # Some of the data validation code downstream expects 'X_valid' and 'y_valid'. Hence populate that.
        # If user provided a custom 'validation_size', the validation data is just a split of training data.
        # As such, no validations are needed in that case.
        if automl_settings_obj.validation_size == 0:
            fit_iteration_parameters_dict['X_valid'] = validation_data.drop_columns(columns_list) \
                if validation_data is not None else None

            fit_iteration_parameters_dict['y_valid'] = validation_data.keep_columns(
                automl_settings_obj.label_column_name) if validation_data is not None else None

        fit_iteration_parameters_dict['x_raw_column_names'] = fit_iteration_parameters_dict['X'].head(1).columns.values

        if automl_settings_obj.weight_column_name is not None:
            fit_iteration_parameters_dict['sample_weight'] = training_data.keep_columns(
                automl_settings_obj.weight_column_name)
            if automl_settings_obj.validation_size == 0:
                # User provided a custom validation data
                fit_iteration_parameters_dict['sample_weight_valid'] = validation_data.keep_columns(
                    automl_settings_obj.weight_column_name) if validation_data is not None else None

        return fit_iteration_parameters_dict
