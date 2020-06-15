# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Manages settings for AutoML experiments."""
from typing import Any, cast, Dict, List, Optional, Union
import logging
import math
import os
import pkg_resources
import sys

from azureml.automl.core.constants import (FeaturizationConfigMode,
                                           TransformerParams,
                                           SupportedTransformers,
                                           FeatureType)
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.constants import ModelNameMappings, SupportedModelNames
from azureml.automl.core.shared.exceptions import (ClientException,
                                                   ConfigException,
                                                   OutOfRangeException,
                                                   InvalidValueException,
                                                   ScenarioNotSupportedException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import ColumnTransformerParamType
from azureml.automl.core.shared.utilities import get_primary_metrics, minimize_or_maximize
from .onnx_convert import OnnxConvertConstants


logger = logging.getLogger(__name__)


class AutoMLBaseSettings:
    """Persist and validate settings for an AutoML experiment."""

    MAXIMUM_DEFAULT_ENSEMBLE_SELECTION_ITERATIONS = 15
    MINIMUM_REQUIRED_ITERATIONS_ENSEMBLE = 2

    # 525600 minutes = 1 year
    MAXIMUM_EXPERIMENT_TIMEOUT_MINUTES = 525600

    # 43200 minutes = 1 month
    MAXIMUM_ITERATION_TIMEOUT_MINUTES = 43200

    # 1073741824 MB = 1 PB
    MAXIMUM_MEM_IN_MB = 1073741824

    MAX_LAG_LENGTH = 2000
    MAX_N_CROSS_VALIDATIONS = 1000
    MAX_CORES_PER_ITERATION = 16384

    MIN_EXPTIMEOUT_MINUTES = 15

    """
    TODO: Add the following bits back to AzureML SDK:
    - experiment
    - compute target
    - spark context
    """

    def __init__(self,
                 path: Optional[str] = None,
                 iterations: int = 100,
                 data_script: Optional[str] = None,
                 primary_metric: Optional[str] = None,
                 task_type: Optional[str] = None,
                 validation_size: Optional[float] = None,
                 n_cross_validations: Optional[int] = None,
                 y_min: Optional[float] = None,
                 y_max: Optional[float] = None,
                 num_classes: Optional[int] = None,
                 featurization: Union[str, FeaturizationConfig] = FeaturizationConfigMode.Auto,
                 max_cores_per_iteration: int = 1,
                 max_concurrent_iterations: int = 1,
                 iteration_timeout_minutes: Optional[int] = None,
                 mem_in_mb: Optional[int] = None,
                 enforce_time_on_windows: bool = os.name == 'nt',
                 experiment_timeout_minutes: Optional[int] = None,
                 experiment_exit_score: Optional[float] = None,
                 blacklist_models: Optional[List[str]] = None,
                 whitelist_models: Optional[List[str]] = None,
                 exclude_nan_labels: bool = True,
                 verbosity: int = log_server.DEFAULT_VERBOSITY,
                 debug_log: str = 'automl.log',
                 debug_flag: Optional[Dict[str, Any]] = None,
                 enable_voting_ensemble: bool = True,
                 enable_stack_ensemble: bool = False,
                 ensemble_iterations: Optional[int] = None,
                 model_explainability: bool = True,
                 enable_tf: bool = True,
                 enable_cache: bool = True,
                 enable_subsampling: Optional[bool] = None,
                 subsample_seed: Optional[int] = None,
                 cost_mode: int = constants.PipelineCost.COST_NONE,
                 is_timeseries: bool = False,
                 enable_early_stopping: bool = False,
                 early_stopping_n_iters: int = 10,
                 enable_onnx_compatible_models: bool = False,
                 enable_feature_sweeping: bool = False,
                 enable_nimbusml: Optional[bool] = None,
                 enable_streaming: Optional[bool] = None,
                 force_streaming: Optional[bool] = None,
                 label_column_name: Optional[str] = None,
                 weight_column_name: Optional[str] = None,
                 cv_split_column_names: Optional[List[str]] = None,
                 enable_local_managed: bool = False,
                 vm_type: Optional[str] = None,
                 track_child_runs: bool = True,
                 **kwargs: Any):
        """
        Manage settings used by AutoML components.

        :param path: Full path to the project folder
        :param iterations: Number of different pipelines to test
        :param data_script: File path to the script containing get_data()
        :param primary_metric: The metric that you want to optimize.
        :param task_type: Field describing whether this will be a classification or regression experiment
        :param validation_size: What percent of the data to hold out for validation
        :param n_cross_validations: How many cross validations to perform
        :param y_min: Minimum value of y for a regression experiment
        :param y_max: Maximum value of y for a regression experiment
        :param num_classes: Number of classes in the label data
        :param featurization: Indicator for whether featurization step should be done automatically or not,
            or whether customized featurization should be used.
        :param max_cores_per_iteration: Maximum number of threads to use for a given iteration
        :param max_concurrent_iterations:
            Maximum number of iterations that would be executed in parallel.
            This should be less than the number of cores on the AzureML compute. Formerly concurrent_iterations.
        :param iteration_timeout_minutes: Maximum time in seconds that each iteration before it terminates
        :param mem_in_mb: Maximum memory usage of each iteration before it terminates
        :param enforce_time_on_windows: flag to enforce time limit on model training at each iteration under windows.
        :param experiment_timeout_minutes: Maximum amount of time that all iterations combined can take
        :param experiment_exit_score:
            Target score for experiment. Experiment will terminate after this score is reached.
        :param blacklist_models: List of algorithms to ignore for AutoML experiment
        :param whitelist_models: List of model names to search for AutoML experiment
        :param exclude_nan_labels: Flag whether to exclude rows with NaN values in the label
        :param verbosity: Verbosity level for AutoML log file
        :param debug_log: File path to AutoML logs
        :param enable_voting_ensemble: Flag to enable/disable an extra iteration for Voting ensemble.
        :param enable_stack_ensemble: Flag to enable/disable an extra iteration for Stack ensemble.
        :param ensemble_iterations: Number of models to consider for the ensemble generation
        :param model_explainability: Flag whether to explain best AutoML model at the end of training iterations.
        :param enable_tf: Flag to enable/disable Tensorflow algorithms
        :param enable_cache: Flag to enable/disable disk cache for transformed, featurized data.
        :param enable_subsampling: Flag to enable/disable subsampling.
        :param subsample_seed: random_state used to sample the data.
        :param cost_mode: Flag to set cost prediction modes. COST_NONE stands for none cost prediction,
            COST_FILTER stands for cost prediction per iteration.
        :type cost_mode: int or azureml.automl.core.shared.constants.PipelineCost
        :param is_timeseries: Flag whether AutoML should process your data as time series data.
        :type is_timeseries: bool
        :param enable_early_stopping: Flag whether the experiment should stop early if the score is not improving.
        :type enable_early_stopping: bool
        :param early_stopping_n_iters: The number of iterations to run in addition to landmark pipelines before
            early stopping kicks in.
        :type early_stopping_n_iters: int
        :param enable_onnx_compatible_models: Flag to enable/disable enforcing the onnx compatible models.
        :param enable_feature_sweeping: Flag to enable/disable feature sweeping.
        :param enable_nimbusml: Flag to enable/disable NimbusML transformers / learners.
        :param enable_streaming: Flag to enable/disable streaming.
        :param force_streaming: Flag to force streaming to kick in.
        :param label_column_name: The name of the label column.
        :param weight_column_name: Name of the column corresponding to the sample weights.
        :param cv_split_column_names: List of names for columns that contain custom cross validation split.
        :param enable_local_managed: flag whether to allow local managed runs
        :type enable_local_managed: bool
        :param track_child_runs: Flag whether to upload all child run details to Run History. If false, only the
            best child run and other summary details will be uploaded.
        :param target_lags: The number of past periods to lag from the target column.

            When forecasting, this parameter represents the number of rows to lag the target values based
            on the frequency of the data. This is represented as a list or single integer. Lag should be used
            when the relationship between the independent variables and dependant variable do not match up or
            correlate by default. For example, when trying to forecast demand for a product, the demand in any
            month may depend on the price of specific commodities 3 months prior. In this example, you may want
            to lag the target (demand) negatively by 3 months so that the model is training on the correct
            relationship.
        :type target_lags: List(int)
        :param feature_lags: Flag for generating lags for the numeric features
        :type feature_lags: str
        :param kwargs:
        """
        self._init_logging(debug_log, verbosity)
        self.path = path

        self.iterations = iterations

        if primary_metric is None and task_type is None:
            raise ConfigException.create_without_pii('One or both of primary metric and '
                                                     'task type must be provided.')
        elif primary_metric is None and task_type is not None:
            self.task_type = task_type
            if task_type == constants.Tasks.CLASSIFICATION:
                self.primary_metric = constants.Metric.Accuracy
            elif task_type == constants.Tasks.REGRESSION:
                self.primary_metric = constants.Metric.Spearman
        elif primary_metric is not None and task_type is None:
            self.primary_metric = primary_metric
            if self.primary_metric in constants.Metric.REGRESSION_PRIMARY_SET:
                self.task_type = constants.Tasks.REGRESSION
            elif self.primary_metric in constants.Metric.CLASSIFICATION_PRIMARY_SET:
                self.task_type = constants.Tasks.CLASSIFICATION
            else:
                msg = 'Invalid primary metric specified. Please use one of {0} for classification '\
                      'or {1} for regression.'
                msg = msg.format(constants.Metric.CLASSIFICATION_PRIMARY_SET,
                                 constants.Metric.REGRESSION_PRIMARY_SET)
                raise ConfigException.create_without_pii(msg)
        else:
            self.primary_metric = cast(str, primary_metric)
            self.task_type = cast(str, task_type)
            if self.primary_metric not in get_primary_metrics(self.task_type):
                msg = "Invalid primary metric specified for {0}. Please use one of: {1}"
                msg = msg.format(self.task_type, get_primary_metrics(self.task_type))
                raise ConfigException.create_without_pii(msg)

        self.data_script = data_script

        # TODO remove this once Miro/AutoML common code can handle None
        if validation_size is None:
            self.validation_size = 0.0
        else:
            self.validation_size = validation_size
        self.n_cross_validations = n_cross_validations

        self.y_min = y_min
        self.y_max = y_max

        self.num_classes = num_classes

        if isinstance(featurization, FeaturizationConfig):
            self.featurization = featurization.__dict__  # type: Union[str, Dict[str, Any]]
        else:
            self.featurization = featurization

        # Empty featurization config setting, run in auto featurization mode
        if isinstance(self.featurization, Dict) and \
                FeaturizationConfig._is_featurization_dict_empty(self.featurization):
            self.featurization = FeaturizationConfigMode.Auto

        # Flag whether to ensure or ignore package version
        # incompatibilities of Automated Machine learning's dependent packages.
        self._ignore_package_version_incompatibilities = 'AUTOML_IGNORE_PACKAGE_VERSION_INCOMPATIBILITIES'.lower() in\
                                                         os.environ

        # Deprecation of preprocess
        try:
            preprocess = kwargs.pop('preprocess')
            # TODO: Enable logging
            # logging.warning("Parameter `preprocess` will be deprecated. Use `featurization`")
            if self.featurization == FeaturizationConfigMode.Auto and preprocess is False:
                self.featurization = FeaturizationConfigMode.Off
            # TODO: Enable logging
            # else:
            #     logging.warning("Detected both `preprocess` and `featurization`. `preprocess` is being deprecated "
            #                     "and will be overridden by `featurization` setting.")
        except KeyError:
            pass

        self.is_timeseries = is_timeseries

        self.max_cores_per_iteration = max_cores_per_iteration
        self.max_concurrent_iterations = max_concurrent_iterations
        self.iteration_timeout_minutes = iteration_timeout_minutes
        self.mem_in_mb = mem_in_mb
        self.enforce_time_on_windows = enforce_time_on_windows
        self.experiment_timeout_minutes = experiment_timeout_minutes
        self.experiment_exit_score = experiment_exit_score

        self.whitelist_models = self._filter_model_names_to_customer_facing_only(whitelist_models)
        self.blacklist_algos = self._filter_model_names_to_customer_facing_only(blacklist_models)
        self.supported_models = self._get_supported_model_names()

        self.auto_blacklist = True
        self.blacklist_samples_reached = False
        self.exclude_nan_labels = exclude_nan_labels

        self.verbosity = verbosity
        self._debug_log = debug_log
        self.show_warnings = False
        self.model_explainability = model_explainability
        self.service_url = None
        self.sdk_url = None
        self.sdk_packages = None

        self.enable_onnx_compatible_models = enable_onnx_compatible_models
        if self.enable_onnx_compatible_models:
            # Read the config of spliting the onnx models of the featurizer and estimator parts.
            enable_split_onnx_featurizer_estimator_models = kwargs.get(
                "enable_split_onnx_featurizer_estimator_models", False)
            self.enable_split_onnx_featurizer_estimator_models = enable_split_onnx_featurizer_estimator_models
        else:
            self.enable_split_onnx_featurizer_estimator_models = False

        self.vm_type = vm_type

        # telemetry settings
        self.telemetry_verbosity = verbosity
        self.send_telemetry = True

        # enable/ disable neural networks for forecasting and natural language processing
        self.enable_dnn = kwargs.pop('enable_dnn', False)

        # Throw configuration exception if dataset language is specified to a non english code
        # but enable_dnn is not enabled.
        if not isinstance(self.featurization, dict) or self.featurization.get("_dataset_language", None) is None:
            # isinstance(self.featurization, dict) checks for whether featurization customization is used.
            language = "eng"
        else:
            language = self.featurization.get("_dataset_language", "eng")
        if language != "eng" and self.task_type == constants.Tasks.CLASSIFICATION and not self.enable_dnn:
            lang_msg = """For non-English support for text data, please set enable_dnn=True
                and be sure you are using GPU compute."""
            raise ConfigException.create_without_pii(lang_msg)

        self.force_text_dnn = kwargs.pop('force_text_dnn', False)
        if self.task_type == constants.Tasks.CLASSIFICATION and self.enable_dnn and \
                self.featurization == FeaturizationConfigMode.Off:
            self.featurization = FeaturizationConfigMode.Auto
            logger.info("Resetting AutoMLBaseSettings param featurization='auto' "
                        "required by DNNs for classification.")

        is_feature_sweeping_possible = (not is_timeseries) and (not self.enable_onnx_compatible_models)
        self.enable_feature_sweeping = is_feature_sweeping_possible and enable_feature_sweeping

        # Force enable feature sweeping so enable_dnn flag can be honored for text DNNs.
        if is_feature_sweeping_possible and self.enable_dnn and self.task_type == constants.Tasks.CLASSIFICATION \
                and not self.enable_feature_sweeping:
            self.enable_feature_sweeping = True
            logger.info(
                "Resetting AutoMLBaseSettings param enable_feature_sweeping=True required by DNNs for classification."
            )

        # time series settings
        if is_timeseries:
            self.time_column_name = kwargs.pop(constants.TimeSeries.TIME_COLUMN_NAME, None)
            grains = kwargs.pop(constants.TimeSeries.GRAIN_COLUMN_NAMES, None)
            wrong_grains_msg = "Wrong grain type: expected string, list of strings or None."
            if isinstance(grains, str):
                self.grain_column_names = [grains]  # type: Optional[List[str]]
            elif grains is None or isinstance(grains, list):
                if grains is not None:
                    for grain in grains:
                        if not isinstance(grain, str):
                            raise ConfigException.create_without_pii(wrong_grains_msg)
                    if len(grains) == 0:
                        grains = None
                self.grain_column_names = grains
            else:
                raise ConfigException.create_without_pii(wrong_grains_msg)
            drop_columns = kwargs.pop(constants.TimeSeries.DROP_COLUMN_NAMES, None)
            if drop_columns is None:
                self.drop_column_names = []  # type: List[Any]
            elif not isinstance(drop_columns, list):
                self.drop_column_names = [drop_columns]
            else:
                self.drop_column_names = drop_columns
            self.max_horizon = kwargs.pop(constants.TimeSeries.MAX_HORIZON,
                                          constants.TimeSeriesInternal.MAX_HORIZON_DEFAULT)
            AutoMLBaseSettings._is_int_or_auto(self.max_horizon, constants.TimeSeries.MAX_HORIZON, False)
            self.dropna = False
            self.overwrite_columns = constants.TimeSeriesInternal.OVERWRITE_COLUMNS_DEFAULT
            self.transform_dictionary = constants.TimeSeriesInternal.TRANSFORM_DICT_DEFAULT
            self.window_size = kwargs.pop(constants.TimeSeries.TARGET_ROLLING_WINDOW_SIZE,
                                          constants.TimeSeriesInternal.WINDOW_SIZE_DEFDAULT)
            AutoMLBaseSettings._is_int_or_auto(self.window_size, constants.TimeSeries.TARGET_ROLLING_WINDOW_SIZE)
            if isinstance(self.window_size, int) and self.window_size < 2:
                raise ConfigException.create_without_pii(
                    "Target rolling window size should be greater than or equal to 2.",
                    reference_code=ReferenceCodes._TARGET_ROLLING_WINDOW_SMALL,
                    target=constants.TimeSeries.TARGET_ROLLING_WINDOW_SIZE)
            self.country_or_region = kwargs.pop(constants.TimeSeries.COUNTRY_OR_REGION, None)
            # For backward compatibility, keep country for a while
            # TODO: remove support for country parameter
            _country = kwargs.pop("country", None)
            if _country is not None:
                msg = "Parameter 'country' will be deprecated. Use 'country_or_region'"
                logging.warning(msg)  # print warning to console
                logger.warning(msg)  # print warning to logs
                self.country_or_region = _country

            lags = kwargs.pop(
                constants.TimeSeries.TARGET_LAGS,
                constants.TimeSeriesInternal.TARGET_LAGS_DEFAULT)  # type: Optional[Union[List[int], int]]
            type_error = (
                'Unsupported value of target_lags. target_lags must be integer, list of integers or \'{}\'.'
                .format(constants.TimeSeries.AUTO))
            if isinstance(lags, int) or isinstance(lags, list):
                if isinstance(lags, int):
                    target_lags = [lags]  # type: Optional[List[Union[int, str]]]
                else:
                    # Get unique values.
                    target_lags = list(set(lags))
                if target_lags == []:
                    target_lags = None
                elif target_lags is not None:  # This condition is required for mypy.
                    for lag in target_lags:
                        if not isinstance(lag, int):
                            raise ConfigException.create_without_pii(type_error)
                        if lag < 1 or lag > AutoMLBaseSettings.MAX_LAG_LENGTH:
                            raise ConfigException.create_without_pii(
                                "The {} must be between 1 and {} inclusive.".format(
                                    constants.TimeSeries.TARGET_LAGS,
                                    AutoMLBaseSettings.MAX_LAG_LENGTH))
            elif lags == constants.TimeSeries.AUTO:
                target_lags = [constants.TimeSeries.AUTO]
            elif lags is None:
                target_lags = None
            else:
                raise ConfigException.create_without_pii(type_error)

            # Convert target lags to dictionary or None.
            if target_lags is not None:
                self.lags =\
                    {constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN:
                     target_lags}  # type: Optional[Dict[str, List[Union[int, str]]]]
            else:
                self.lags = None
            # add feature lags
            feature_lags = kwargs.pop(
                constants.TimeSeries.FEATURE_LAGS,
                constants.TimeSeriesInternal.FEATURE_LAGS_DEFAULT)
            permitted_feature_lags_options = [constants.TimeSeries.AUTO,
                                              constants.TimeSeriesInternal.FEATURE_LAGS_DEFAULT]
            type_error_feature_lags = (
                'Unsupported value of feature_lags, which must be \'{}\' or \'{}\'.'
                .format(*permitted_feature_lags_options))
            if feature_lags in permitted_feature_lags_options:
                setattr(self, constants.TimeSeries.FEATURE_LAGS, feature_lags)
            else:
                raise ConfigException.create_without_pii(type_error_feature_lags)
            # seasonality
            seasonality_input = kwargs.pop(constants.TimeSeries.SEASONALITY,
                                           constants.TimeSeriesInternal.SEASONALITY_VALUE_DEFAULT)
            setattr(self, constants.TimeSeries.SEASONALITY, seasonality_input)
            stl_input = kwargs.pop(constants.TimeSeries.USE_STL,
                                   constants.TimeSeriesInternal.USE_STL_DEFAULT)
            setattr(self, constants.TimeSeries.USE_STL, stl_input)
            rm_insufficient = kwargs.pop(
                constants.TimeSeries.SHORT_SERIES_HANDLING,
                constants.TimeSeriesInternal.SHORT_SERIES_HANDLING_DEFAULT)
            setattr(self, constants.TimeSeries.SHORT_SERIES_HANDLING, rm_insufficient)

        # Early stopping settings
        self.enable_early_stopping = enable_early_stopping
        self.early_stopping_n_iters = early_stopping_n_iters

        if debug_flag:
            if 'service_url' in debug_flag:
                self.service_url = debug_flag['service_url']
            if 'show_warnings' in debug_flag:
                self.show_warnings = debug_flag['show_warnings']
            if 'sdk_url' in debug_flag:
                self.sdk_url = debug_flag['sdk_url']
            if 'sdk_packages' in debug_flag:
                self.sdk_packages = debug_flag['sdk_packages']

        # Deprecated param
        self.metrics = None

        # backward compatible settings
        old_voting_ensemble_flag = kwargs.pop("enable_ensembling", None)
        old_stack_ensemble_flag = kwargs.pop("enable_stack_ensembling", None)
        enable_voting_ensemble = \
            old_voting_ensemble_flag if old_voting_ensemble_flag is not None else enable_voting_ensemble
        enable_stack_ensemble = \
            old_stack_ensemble_flag if old_stack_ensemble_flag is not None else enable_stack_ensemble

        if self.enable_onnx_compatible_models:
            # disable Stack Ensemble until support for ONNX comes in
            enable_stack_ensemble = False

        total_ensembles = 0
        if enable_voting_ensemble:
            total_ensembles += 1
        if enable_stack_ensemble:
            total_ensembles += 1

        if self.iterations >= AutoMLBaseSettings.MINIMUM_REQUIRED_ITERATIONS_ENSEMBLE + total_ensembles:
            self.enable_ensembling = enable_voting_ensemble
            self.enable_stack_ensembling = enable_stack_ensemble
            if ensemble_iterations is not None:
                self.ensemble_iterations = ensemble_iterations  # type: Optional[int]
            else:
                self.ensemble_iterations = min(AutoMLBaseSettings.MAXIMUM_DEFAULT_ENSEMBLE_SELECTION_ITERATIONS,
                                               self.iterations)
        else:
            self.enable_ensembling = False
            self.enable_stack_ensembling = False
            self.ensemble_iterations = None

        self.enable_tf = enable_tf
        self.enable_cache = enable_cache
        # Deprecation warning for enable_cache, if set to False
        if not enable_cache:
            msg = (
                "Parameter 'enable_cache' will be deprecated. Azure blob store / local disk based "
                "caches for pre-processed and/or transformed data will always be preferred."
            )
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
        self.enable_subsampling = enable_subsampling
        self.subsample_seed = subsample_seed
        self.enable_nimbusml = False if enable_nimbusml is None else enable_nimbusml
        self.enable_streaming = False if enable_streaming is None else enable_streaming
        self.force_streaming = False if force_streaming is None else force_streaming
        # backward compatible settings
        old_streaming_flag = kwargs.pop("use_incremental_learning", None)
        self.enable_streaming = \
            old_streaming_flag if old_streaming_flag is not None else self.enable_streaming

        self.track_child_runs = track_child_runs

        self.label_column_name = label_column_name
        self.weight_column_name = weight_column_name
        self.cv_split_column_names = cv_split_column_names
        self.enable_local_managed = enable_local_managed

        self.cost_mode = cost_mode
        # Show warnings for deprecating lag_length

        lags = kwargs.pop('lag_length', 0)
        if lags is None:
            lags = 0
        if lags != 0:
            msg = "Parameter 'lag_length' will be deprecated. Please use "\
                  "target_lags parameter in forecasting task to set it."
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
        setattr(self, 'lag_length', lags)

        self._verify_settings()

        # Settings that need to be set after verification
        if self.task_type is not None and self.primary_metric is not None:
            self.metric_operation = minimize_or_maximize(
                task=self.task_type, metric=self.primary_metric)
        else:
            self.metric_operation = None

        # Deprecation of concurrent_iterations
        try:
            concurrent_iterations = kwargs.pop('concurrent_iterations')  # type: int
            msg = "Parameter 'concurrent_iterations' will be deprecated. Use 'max_concurrent_iterations'"
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
            self.max_concurrent_iterations = concurrent_iterations
        except KeyError:
            pass

        # Deprecation of max_time_sec
        try:
            max_time_sec = kwargs.pop('max_time_sec')  # type: int
            msg = "Parameter 'max_time_sec' will be deprecated. Use 'iteration_timeout_minutes'"
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
            if max_time_sec:
                self.iteration_timeout_minutes = math.ceil(max_time_sec / 60)
        except KeyError:
            pass

        # Deprecation of exit_time_sec
        try:
            exit_time_sec = kwargs.pop('exit_time_sec')  # type: int
            msg = "Parameter 'exit_time_sec' will be deprecated. Use 'experiment_timeout_minutes'"
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
            if exit_time_sec:
                self.experiment_timeout_minutes = math.ceil(exit_time_sec / 60)
        except KeyError:
            pass

        # Deprecation of exit_score
        try:
            exit_score = kwargs.pop('exit_score')
            msg = "Parameter 'exit_score' will be deprecated. Use 'experiment_exit_score'"
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
            self.experiment_exit_score = exit_score
        except KeyError:
            pass

        # Deprecation of blacklist_algos
        try:
            old_algos_param = kwargs.pop('blacklist_algos')
            # TODO: Re-enable this warning once we change everything to use blacklist_models
            # logging.warning("Parameter 'blacklist_algos' will be deprecated. Use 'blacklist_models.'")
            if self.blacklist_algos and old_algos_param is not None:
                self.blacklist_algos = self.blacklist_algos + \
                    self._filter_model_names_to_customer_facing_only(
                        list(set(old_algos_param) - set(self.blacklist_algos))
                    )
            else:
                self.blacklist_algos = self._filter_model_names_to_customer_facing_only(old_algos_param)
        except KeyError:
            pass

        # Deprecation of preprocess
        # preprocess flag is preserved in here only to be accessible from JOS validation service.
        self.preprocess = False if self.featurization == FeaturizationConfigMode.Off else True

        # Update custom dimensions
        automl_core_sdk_version = pkg_resources.get_distribution("azureml-automl-core").version
        if self.is_timeseries:
            task_type = "forecasting"
        else:
            task_type = self.task_type
        custom_dimensions = {
            "task_type": task_type,
            "automl_core_sdk_version": automl_core_sdk_version
        }
        log_server.update_custom_dimensions(custom_dimensions)

        for key, value in kwargs.items():
            if key not in self.__dict__.keys():
                msg = "Received unrecognized parameter {}".format(key)
                logging.warning(msg)  # print warning to console
            setattr(self, key, value)

    @property
    def debug_log(self) -> str:
        return self._debug_log

    @debug_log.setter
    def debug_log(self, debug_log: str) -> None:
        """
        Set the new log file path. Setting this will also update the log server with the new path.

        :param debug_log:
        :return:
        """
        self._debug_log = debug_log
        log_server.set_log_file(debug_log)

    @property
    def _instrumentation_key(self) -> str:
        return ''

    def _init_logging(self, debug_log: str, verbosity: int) -> None:
        """

        :return:
        """
        log_server.set_log_file(debug_log)
        log_server.enable_telemetry(self._instrumentation_key)
        log_server.set_verbosity(verbosity)

    def _verify_settings(self):
        """
        Verify that input automl_settings are sensible.

        TODO (#357763): Reorganize the checks here and in AutoMLConfig and see what's redundant/can be reworked.

        :return:
        :rtype: None
        """
        if self.validation_size is not None:
            if self.validation_size > 1.0 or self.validation_size < 0.0:
                raise OutOfRangeException.create_without_pii(
                    "validation_size parameter must be between 0 and 1 when specified.")

        if self.n_cross_validations is not None:
            if not isinstance(self.n_cross_validations, int):
                raise ConfigException.create_without_pii('n_cross_validations must be an integer.')
            if self.n_cross_validations < 2 or self.n_cross_validations > AutoMLBaseSettings.MAX_N_CROSS_VALIDATIONS:
                raise OutOfRangeException.create_without_pii(
                    'n_cross_validations must be between 2 to {} inclusive when specified.'.format(
                        AutoMLBaseSettings.MAX_N_CROSS_VALIDATIONS))
            if self.enable_dnn and self.task_type == constants.Tasks.CLASSIFICATION:
                msg = 'Deep neural networks (DNN) do not support cross-validation '\
                      'for classification task, please provide validation data or disable DNNs.'
                raise ConfigException.create_without_pii(msg)

        if self.cv_split_column_names is not None and self.enable_streaming:
            raise ConfigException.create_without_pii("Streaming does not support custom cv splits.")

        if self.iterations < 1 or self.iterations > constants.MAX_ITERATIONS:
            raise OutOfRangeException.create_without_pii(
                'Number of iterations must be between 1 and {} inclusive.'.format(constants.MAX_ITERATIONS))

        ensemble_enabled = self.enable_ensembling or self.enable_stack_ensembling
        if ensemble_enabled and cast(int, self.ensemble_iterations) < 1:
            raise OutOfRangeException.create_without_pii(
                "When ensembling is enabled, the ensemble_iterations setting can't be less than 1")

        if ensemble_enabled and cast(int, self.ensemble_iterations) > self.iterations:
            raise OutOfRangeException.create_without_pii(
                "When ensembling is enabled, the ensemble_iterations setting can't be greater than \
                the total number of iterations.")

        if self.path is not None and not isinstance(self.path, str):
            raise ConfigException.create_without_pii('Input parameter \"path\" needs to be a string.')

        if self.max_cores_per_iteration is not None and self.max_cores_per_iteration != -1 and \
                (self.max_cores_per_iteration < 1 or
                 self.max_cores_per_iteration > AutoMLBaseSettings.MAX_CORES_PER_ITERATION):
            raise OutOfRangeException.create_without_pii(
                'Input parameter \"max_cores_per_iteration\" needs to be -1 or between 1 and {} inclusive.'.format(
                    AutoMLBaseSettings.MAX_CORES_PER_ITERATION))
        if self.max_concurrent_iterations is not None and self.max_concurrent_iterations < 1:
            raise OutOfRangeException.create_without_pii(
                'Input parameter \"max_concurrent_iterations\" needs to be greater or equal to 1, if set.')
        if self.iteration_timeout_minutes is not None and \
                (self.iteration_timeout_minutes < 1 or self.iteration_timeout_minutes >
                 AutoMLBaseSettings.MAXIMUM_ITERATION_TIMEOUT_MINUTES):
            raise OutOfRangeException.create_without_pii(
                'Input parameter \"iteration_timeout_minutes\" needs to be between 1 and {} inclusive if set.'.format(
                    AutoMLBaseSettings.MAXIMUM_ITERATION_TIMEOUT_MINUTES))
        if self.mem_in_mb is not None and \
                (self.mem_in_mb < 1 or self.mem_in_mb > AutoMLBaseSettings.MAXIMUM_MEM_IN_MB):
            raise OutOfRangeException.create_without_pii(
                'Input parameter \"mem_in_mb\" needs to be between 1 and {} if set.'.format(
                    AutoMLBaseSettings.MAXIMUM_MEM_IN_MB))
        if self.enforce_time_on_windows is not None and not isinstance(self.enforce_time_on_windows, bool):
            raise ConfigException.create_without_pii('Input parameter \"enforce_time_on_windows\" needs to be a '
                                                     'boolean if set.')
        if self.experiment_timeout_minutes is not None and \
                (self.experiment_timeout_minutes < AutoMLBaseSettings.MIN_EXPTIMEOUT_MINUTES or
                 self.experiment_timeout_minutes > AutoMLBaseSettings.MAXIMUM_EXPERIMENT_TIMEOUT_MINUTES):
            raise OutOfRangeException.create_without_pii(
                msg='Input parameter \"experiment_timeout_minutes\" '
                'needs to be between {} and {} or parameter \"experiment_timeout_hours\" '
                'needs to be between {} and {} if set.'
                .format(AutoMLBaseSettings.MIN_EXPTIMEOUT_MINUTES,
                        AutoMLBaseSettings.MAXIMUM_EXPERIMENT_TIMEOUT_MINUTES,
                        AutoMLBaseSettings.MIN_EXPTIMEOUT_MINUTES / 60,
                        AutoMLBaseSettings.MAXIMUM_EXPERIMENT_TIMEOUT_MINUTES / 60),
                target="experiment_timeout_minutes")
        if self.blacklist_algos is not None and not isinstance(self.blacklist_algos, list):
            raise ConfigException.create_without_pii(
                'Input parameter \"blacklist_algos\" needs to be a list of strings.')
        if not isinstance(self.exclude_nan_labels, bool):
            raise ConfigException.create_without_pii('Input parameter \"exclude_nan_labels\" needs to be a boolean.')
        if self.debug_log is not None and not isinstance(self.debug_log, str):
            raise ConfigException.create_without_pii('Input parameter \"debug_log\" needs to be a string filepath.')
        if self.is_timeseries:
            if isinstance(self.featurization, dict):
                self._validate_timeseries_featurization_settings(self.featurization)
            if self.task_type == constants.Tasks.CLASSIFICATION:
                raise ConfigException.create_without_pii('Timeseries do not support classification yet.')
            if self.time_column_name is None:
                raise ConfigException.create_without_pii('Timeseries need to set time column. ')
            if getattr(self, 'lag_length', 0) < 0 or\
                    getattr(self, 'lag_length', 0) > AutoMLBaseSettings.MAX_LAG_LENGTH:
                raise OutOfRangeException.create_without_pii(
                    'Lag length must be between 0 and {} inclusive.'.format(AutoMLBaseSettings.MAX_LAG_LENGTH))

        if self.enable_onnx_compatible_models:
            if sys.version_info >= OnnxConvertConstants.OnnxIncompatiblePythonVersion:
                raise ConfigException.create_without_pii('The ONNX package does not support Python 3.8, please use '
                                                         'lower version of Python to get the ONNX model.')
            if self.is_timeseries:
                raise ConfigException.create_without_pii('Timeseries is not ONNX compatible, disable '
                                                         'enable_onnx_compatible_models to run.')
            if self.enable_tf:
                raise ConfigException.create_without_pii(
                    'Tensorflow models are not ONNX compatible, disable enable_onnx_compatible_models to run.')

        if self.enable_subsampling and not isinstance(self.enable_subsampling, bool):
            raise ConfigException.create_without_pii('Input parameter \"enable_subsampling\" needs to be a boolean. ')
        if not self.enable_subsampling and self.subsample_seed:
            msg = 'Input parameter \"enable_subsampling\" is set to False but \"subsample_seed\" was specified.'
            logging.warning(msg)  # print warning to console
            logger.warning(msg)  # print warning to logs
        if self.enable_subsampling and self.subsample_seed and not \
                isinstance(self.subsample_seed, int):
            raise ConfigException.create_without_pii('Input parameter \"subsample_seed\" needs to be an integer.')

        self._validate_whitelist_blacklist()

        if self.early_stopping_n_iters < 0:
            raise OutOfRangeException.create_without_pii('The number of additional iterations for early stopping '
                                                         'cannot be negative.')

    def _validate_whitelist_blacklist(self):
        """
        Validate that whitelist and blacklist are correct.

        Assumes that blacklist_algos and whitelist_models have been filtered to contain only
        valid model names.
        """

        bla = set()
        wlm = set()

        # check blacklist
        if self.blacklist_algos is not None:
            bla = set(self.blacklist_algos)
            enabled_algos = set(self._get_supported_model_names()) - bla
            if len(enabled_algos) == 0:
                msg = 'All models are blacklisted, please make sure at least one model is allowed.'
                raise ConfigException(
                    msg,
                    target='blacklist_models',
                    has_pii=False,
                    reference_code=ReferenceCodes._AUTOML_CONFIG_BLACKLIST_ALL_MODELS
                )

            # If everything but arima and/or prophet are blacklisted (equivalent to whitelist arima/prophet) but
            # lags/rolling windows enabled, we should raise scenario not supported.
            if self.is_timeseries and (self.lags is not None or self.window_size is not None):
                for algo in [constants.SupportedModels.Forecasting.Prophet,
                             constants.SupportedModels.Forecasting.AutoArima]:
                    enabled_algos.discard(algo)
                if len(enabled_algos) == 0:
                    raise ScenarioNotSupportedException(
                        "AutoArima and Prophet are not supported when lags or rolling window is enabled for "
                        "forecasting tasks. Please either enable more algorithms or disable lags and rolling window.",
                        target='blacklist_models',
                        has_pii=False,
                        reference_code=ReferenceCodes._SETTINGS_AUTOARIMA_PROPHET_NOT_SUPPORTED_BLACKLIST
                    )

        # check whitelist
        if self.whitelist_models is not None:
            # check whitelist not empty
            if len(self.whitelist_models) == 0:
                msg = 'Input values for whitelist_models not recognized.'\
                      'Please use one of {}'.format(self._get_supported_model_names())
                raise ConfigException(
                    msg,
                    target="whitelist_models",
                    has_pii=False,
                    reference_code=ReferenceCodes._AUTOML_CONFIG_WHITELIST_EMPTY
                )
            wlm = set(self.whitelist_models)

            actual_wlm = wlm - bla
            shared = bla.intersection(wlm)

            if len(actual_wlm) == 0:
                raise ConfigException(
                    'blacklisted and whitelisted models are exactly the same.'
                    'Please remove models from the blacklist or add models to the whitelist.',
                    target='whitelist_models',
                    has_pii=False,
                    reference_code=ReferenceCodes._AUTOML_CONFIG_BLACKLIST_EQUAL_WHITELIST
                )
            if len(shared) > 0:
                logging.warning('blacklist and whitelist contain shared models.')

            # If only arima and/or prophet are blacklisted (equivalent to blacklist all but arima/prophet) but
            # lags/rolling windows enabled, we should raise scenario not supported.
            if self.is_timeseries and (self.lags is not None or self.window_size is not None):
                for algo in [constants.SupportedModels.Forecasting.Prophet,
                             constants.SupportedModels.Forecasting.AutoArima]:
                    actual_wlm.discard(algo)
                if len(actual_wlm) == 0:
                    raise ScenarioNotSupportedException(
                        "AutoArima and Prophet are not supported when lags or rolling window is enabled for "
                        "forecasting tasks. Please either enable more algorithms or disable lags and rolling window.",
                        target='whitelist_models',
                        has_pii=False,
                        reference_code=ReferenceCodes._SETTINGS_AUTOARIMA_PROPHET_NOT_SUPPORTED_WHITELIST
                    )

    def _filter_model_names_to_customer_facing_only(self, model_names):
        if model_names is None:
            return None
        supported_model_names = self._get_supported_model_names()
        return [model for model in model_names if model
                in supported_model_names]

    def _get_supported_model_names(self):
        supported_model_names = []  # type: List[str]
        if self.task_type == constants.Tasks.CLASSIFICATION:
            supported_model_names = list(set([m.customer_model_name for m in
                                              SupportedModelNames.SupportedClassificationModelList]))
        elif self.task_type == constants.Tasks.REGRESSION:
            supported_model_names = list(set([model.customer_model_name for model in
                                              SupportedModelNames.SupportedRegressionModelList]))
        if self.is_timeseries:
            supported_model_names = list(set([model.customer_model_name for model in
                                              SupportedModelNames.SupportedForecastingModelList]))
        return supported_model_names

    @staticmethod
    def from_string_or_dict(val: Union[Dict[str, Any], str, 'AutoMLBaseSettings']) -> 'AutoMLBaseSettings':
        """
        Convert a string or dictionary containing settings to an AutoMLBaseSettings object.

        If the provided value is already an AutoMLBaseSettings object, it is simply passed through.

        :param val: the input data to convert
        :return: an AutoMLBaseSettings object
        """
        if isinstance(val, str):
            val = eval(val)
        if isinstance(val, dict):
            val = AutoMLBaseSettings(**val)

        if isinstance(val, AutoMLBaseSettings):
            return val
        else:
            raise ValueError("`input` parameter is not of type string or dict")

    def __str__(self):
        """
        Convert this settings object into human readable form.

        :return: a human readable representation of this object
        """
        output = [' - {0}: {1}'.format(k, v) for k, v in self.__dict__.items()]
        return '\n'.join(output)

    def _format_selective(self, black_list_keys):
        """
        Format selective items for logging.

        Returned string will look as follows below
        Example:
            - key1: value1
            - key2: value2

        :param black_list_keys: List of keys to ignore.
        :type black_list_keys: list(str)
        :return: Filterd settings as string
        :rtype: str
        """
        dict_copy = self._filter(black_list_keys=black_list_keys)
        output = [' - {0}: {1}'.format(k, v) for k, v in dict_copy.items()]
        return '\n'.join(output)

    def as_serializable_dict(self) -> Dict[str, Any]:
        return self._filter(['spark_context'])

    def _filter(self, black_list_keys: Optional[List[str]]) -> Dict[str, Any]:
        return dict([(k, v) for k, v in self.__dict__.items()
                     if black_list_keys is None or k not in black_list_keys])

    def _get_featurization_config_mode(self) -> str:
        featurization = self.__dict__.get('featurization')
        if featurization:
            if isinstance(featurization, str):
                if (featurization == FeaturizationConfigMode.Auto or featurization == FeaturizationConfigMode.Off):
                    return featurization
            return FeaturizationConfigMode.Customized
        return ""

    def _validate_timeseries_featurization_settings(
            self, featurization: Dict[str, Any]) -> None:
        """
        Validate whether the custom featurization is supported.

        :param featurization: The customized featurization config dict.
        """
        warning_msg_template = ("Custom {0} is currently not supported by forecasting task. "
                                "All the settings related will be ignored by AutoML.")

        blocked_transformers = featurization.get("_blocked_transformers")
        if blocked_transformers is not None and len(blocked_transformers) > 0:
            logging.warning(warning_msg_template.format("blocked_transformers"))
            logger.warning(warning_msg_template.format("blocked_transformers"))

        self._validate_ts_column_purposes(featurization)

        self._validate_ts_featurization_drop_columns(featurization)

        self._validate_ts_featurization_transform_params(featurization)

    def _validate_ts_featurization_drop_columns(self,
                                                featurization: Dict[str, Any]) -> None:
        """
        Validate the custom featurization's drop columns.

        :param featurization: The customized featurization config dict.
        """
        drop_columns_error_msg = "The following columns: [{}] cannot be dropped as part of Featurization " \
                                 "configuration as they are part of {}."
        drop_columns = set(featurization.get("_drop_columns") or [])

        if self.time_column_name in drop_columns:
            raise InvalidValueException(
                drop_columns_error_msg.format(self.time_column_name, "time column"),
                target="drop_columns",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_DROP_TIME_COLUMN).with_generic_msg(
                    "Time column name has been specified in Featurization's drop column configuration.")

        shared_grain_columns = drop_columns.intersection(self.grain_column_names or [])
        if len(shared_grain_columns) > 0:
            raise InvalidValueException(
                drop_columns_error_msg.format(",".join(shared_grain_columns), "grain columns"),
                target="drop_columns",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_DROP_GRAIN_COLUMNS).with_generic_msg(
                    "Grain columns have been specified in Featurization's drop column configuration.")

        shared_reserve_columns = drop_columns.intersection(constants.TimeSeriesInternal.RESERVED_COLUMN_NAMES)
        if len(shared_reserve_columns) > 0:
            raise InvalidValueException(
                drop_columns_error_msg.format(",".join(shared_reserve_columns), "reserved columns"),
                target="drop_columns",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_DROP_RESERVED_COLUMNS,
                has_pii=False)

        shared_drop_columns = drop_columns.intersection(self.drop_column_names or [])
        if len(shared_drop_columns) > 0:
            warning_msg = "Featurization's drop column configuration and automl settings' drop column configuration " \
                          "have columns specified in common."
            logging.warning(warning_msg)
            logger.warning(warning_msg)

    def _validate_ts_featurization_strategies(
            self,
            transformer_params: Dict[str, List[ColumnTransformerParamType]]
    ) -> None:
        """
        Validate the custom featurization's transform params strategies.

        :param transformer_params: The customized featurization config params.
        """
        wrong_featurization_msg = "Forecasting task only supports simple imputation with following strategies: {}. " \
                                  "All other imputation settings will be ignored.".format(
                                      ", ".join(sorted(TransformerParams.Imputer.ForecastingEnabledStrategies)))
        target_columns = {self.label_column_name, constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN}
        for cols, params in transformer_params[SupportedTransformers.Imputer]:
            strategy = params.get(TransformerParams.Imputer.Strategy)
            if strategy not in TransformerParams.Imputer.ForecastingEnabledStrategies:
                logging.warning(wrong_featurization_msg)
                logger.warning(wrong_featurization_msg)
            if strategy not in TransformerParams.Imputer.ForecastingTargetEnabledStrategies:
                for col in cols:
                    if col in target_columns:
                        raise InvalidValueException(
                            "Only the following strategies({}) are enabled for a forecasting task's target column. "
                            "Please fix your featurization_config and try again.".format(
                                ",".join(sorted(TransformerParams.Imputer.ForecastingTargetEnabledStrategies))),
                            target="featurization_config",
                            reference_code=ReferenceCodes._SETTINGS_CONFIG_IMPUTE_TARGET_UNSUPPORT,
                            has_pii=False
                        )

    def _validate_ts_featurization_transform_params(
            self,
            featurization: Dict[str, Any]
    ) -> None:
        """
        Validate the custom featurization's transform params.

        :param featurization: The customized featurization config dict.
        """
        transformer_params = featurization.get("_transformer_params")
        if transformer_params is not None and len(transformer_params) > 0:
            if transformer_params.get(SupportedTransformers.Imputer) is not None:
                self._validate_ts_featurization_strategies(transformer_params)
                self._validate_ts_featurization_strategies_columns(transformer_params)
                self._validate_ts_featurization_multi_strategies_columns(transformer_params)

    def _validate_ts_featurization_strategies_columns(
            self,
            transformer_params: Dict[str, List[ColumnTransformerParamType]]
    ) -> None:
        """
        Validate the custom featurization's transform params column not in reserve or drop columns.

        :param transformer_params: The customized featurization config params.
        """
        drop_columns = set(self.drop_column_names or [])

        # the DUMMY_TARGET_COLUMN is used as target column for if user is using X and y as input.
        cannot_customized_reserved_columns = set(
            [col for col in constants.TimeSeriesInternal.RESERVED_COLUMN_NAMES
                if col != constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN])

        config_dropped_columns = list()
        config_reserved_columns = list()
        for cols, params in transformer_params[SupportedTransformers.Imputer]:
            strategy = params.get(TransformerParams.Imputer.Strategy)
            if strategy in TransformerParams.Imputer.ForecastingEnabledStrategies:
                for col in cols:
                    if col in drop_columns:
                        config_dropped_columns.append(col)
                    if col in cannot_customized_reserved_columns:
                        config_reserved_columns.append(col)

        if len(config_dropped_columns) > 0:
            raise InvalidValueException(
                "Featurization customization contains {} which {} in drop column names.".format(
                    ",".join(config_dropped_columns),
                    "is" if len(config_dropped_columns) == 1 else "are"
                ),
                target="featurization_config",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_IMPUTE_COLUMN_DROPPED).with_generic_msg(
                    "Imputation configuration was provided for a column configured to be dropped.")
        if len(config_reserved_columns) > 0:
            raise InvalidValueException(
                "Featurization customization contains {} which {} in reserved column names.".format(
                    ",".join(config_reserved_columns),
                    "is" if len(config_reserved_columns) == 1 else "are"
                ),
                target="featurization_config",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_IMPUTE_COLUMN_RESERVED,
                has_pii=False)

    def _validate_ts_featurization_multi_strategies_columns(
            self,
            transformer_params: Dict[str, List[ColumnTransformerParamType]]
    ) -> None:
        """
        Validate the custom featurization's transform params column not have different stategies.

        :param transformer_params: The customized featurization config params.
        """
        col_strategies = dict()  # type: Dict[str, List[str]]
        for cols, params in transformer_params[SupportedTransformers.Imputer]:
            strategy = params.get(TransformerParams.Imputer.Strategy)
            if strategy in TransformerParams.Imputer.ForecastingEnabledStrategies:
                for col in cols:
                    if col in col_strategies:
                        col_strategies[col].append(strategy)
                    else:
                        col_strategies[col] = [strategy]

        error_msg_list = []
        for col, imputers in col_strategies.items():
            if len(imputers) > 1:
                error_msg_list.append("{}: {}".format(col, ", ".join(imputers)))
        if len(error_msg_list) > 0:
            raise InvalidValueException(
                "Only one imputation method may be defined for each column. In the provided configuration "
                "multiple imputers are assigned to the following columns {}\n. Please remove non needed imputers so "
                "that only one imputer will correspond to the column.".format("\n".join(error_msg_list)),
                target="featurization_config",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_IMPUTE_COLUMN_CONFLICT).with_generic_msg(
                    "Columns are in different customized imputation methods.")

    def _validate_ts_column_purposes(self, featurization: Dict[str, Any]) -> None:
        """
        Validate the column purposes in featurization config for forecasting tasks.

        :param featurization: The featurizaiton config dict.
        :raises: Column purpose column in settings.drop_column_names.
        """
        column_purposes = featurization.get("_column_purposes")
        if column_purposes is None:
            return None

        ts_enabled_column_purposes = {FeatureType.DateTime, FeatureType.Numeric, FeatureType.Categorical}

        drop_columns = set(self.drop_column_names or [])

        unsupported_cols = set()
        dropped_cols = list()
        for col, purpose in column_purposes.items():
            if purpose not in ts_enabled_column_purposes:
                unsupported_cols.add(col)
            if col in drop_columns:
                dropped_cols.append(col)

        unsupported_warning_msg = ("Forecasting supports the following column purposes only: {}. "
                                   "All other inputs will be ignored".format(", ".join(ts_enabled_column_purposes)))
        if len(unsupported_cols) > 0:
            logging.warning(unsupported_warning_msg)
            logger.warning(unsupported_warning_msg)

        if len(dropped_cols) > 0:
            raise InvalidValueException(
                "Column purpose customization contains the following columns {}; out of which {} specified "
                "to be dropped in featurization customization configuration.".format(
                    ",".join(dropped_cols),
                    "is" if len(dropped_cols) == 1 else "are"
                ),
                target="featurization_config",
                reference_code=ReferenceCodes._SETTINGS_CONFIG_DROP_COLUMN_PURPOSE).with_generic_msg(
                "Column purpose customization has the column to be dropped.")

    @staticmethod
    def _is_int_or_auto(val: Optional[Any], val_name: str, allow_none: bool = True) -> None:
        """
        Raise a ConfigException if value is not 'auto' or integer.

        :param val: The value to test.
        :param val_name: the name of a value to be displayed in the error message.
        :param allow_none: if true, the None value is allowed for val.
        :raises: ConfigException
        """
        if allow_none and val is None:
            return
        if not isinstance(val, int) and val != constants.TimeSeries.AUTO:
            raise ConfigException(
                exception_message='Unsupported value of {}. {} must be integer or \'{}\'.'.format(
                    val_name, val_name, constants.TimeSeries.AUTO),
                target=val_name)
