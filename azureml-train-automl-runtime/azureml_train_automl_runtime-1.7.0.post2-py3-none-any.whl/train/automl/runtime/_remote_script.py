# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import gc
import json
import logging
import os
import sys
import time
from typing import Any, cast, Dict, Optional, Tuple, Union, List

import numpy as np
import pandas as pd
from sklearn_pandas import DataFrameMapper

from azureml._history.utils.constants import LOGS_AZUREML_DIR
from azureml._restclient.constants import RUN_ORIGIN
from azureml._restclient.jasmine_client import JasmineClient
from azureml.automl.core._experiment_observer import ExperimentStatus, ExperimentObserver
from azureml.automl.core.constants import FeaturizationRunConstants, PreparationRunTypeConstants
from azureml.automl.core.onnx_convert import OnnxConvertConstants
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared import utilities
from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.constants import SupportedModelNames
from azureml.automl.core.shared.exceptions import CacheException, UserException
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.automl.runtime import data_transformation
from azureml.automl.runtime import fit_pipeline as fit_pipeline_helper
from azureml.automl.runtime import training_utilities
from azureml.automl.runtime._automl_settings_utilities import rule_based_validation
from azureml.automl.runtime._data_transformation_utilities import save_feature_config, save_engineered_feature_names
from azureml.automl.runtime._engineered_feature_names import _GenerateEngineeredFeatureNames
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.data_context import RawDataContext, TransformedDataContext
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurization import TransformerAndMapper
from azureml.automl.runtime.frequency_fixer import fix_data_set_regularity_may_be
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared import memory_utilities
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.core import Datastore, Experiment, Run
from azureml.data.azure_storage_datastore import AbstractAzureStorageDatastore
from azureml.data.constants import WORKSPACE_BLOB_DATASTORE
from azureml.train.automl import _logging  # type: ignore
from azureml.train.automl._automl_datamodel_utilities import CaclulatedExperimentInfo
from azureml.train.automl._automl_datamodel_utilities import MODEL_EXPLAINABILITY_ID
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager
from azureml.train.automl._azure_experiment_observer import AzureExperimentObserver
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.constants import ComputeTargets
from azureml.train.automl.exceptions import ClientException, DataException
from azureml.train.automl.run import AutoMLRun
from azureml.train.automl.runtime.automl_explain_utilities import _automl_auto_mode_explain_model, \
    _automl_perform_best_run_explain_model, ModelExplanationRunId
from azureml.train.automl.utilities import _get_package_version
from msrest.exceptions import HttpOperationError

from . import _automl
from ._azureautomlruncontext import AzureAutoMLRunContext
from ._cachestorefactory import CacheStoreFactory
from ._data_preparer import DataPreparerFactory, DataPreparer
from .utilities import _load_user_script

CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA = '_CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA_'

# The base dataset object can be cached in the setup iteration (to be later re-used during model training),
# with the following key
DATASET_BASE_CACHE_KEY = 'dataset_cached_object'


logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()


def _init_logger() -> None:
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    log_server.add_handler('stdout', handler)


def _parse_settings(current_run: Run, automl_settings: str) -> AzureAutoMLSettings:
    if not os.path.exists(LOGS_AZUREML_DIR):
        os.makedirs(LOGS_AZUREML_DIR, exist_ok=True)
    _init_logger()
    automl_settings_obj = AzureAutoMLSettings.from_string_or_dict(automl_settings, overrides={
        'debug_log': os.path.join(LOGS_AZUREML_DIR, "azureml_automl.log")
    })

    # enable traceback logging for remote runs
    os.environ['AUTOML_MANAGED_ENVIRONMENT'] = '1'

    _logging.set_run_custom_dimensions(
        automl_settings=automl_settings_obj,
        parent_run_id=_get_parent_run_id(current_run.id),
        child_run_id=current_run.id)

    # Don't reuse path from user's local machine for remote runs
    automl_settings_obj.path = os.getcwd()
    logger.info('Changing AutoML temporary path to current working directory.')

    return automl_settings_obj


def _init_directory(directory: Optional[str]) -> str:
    if directory is None:
        directory = os.getcwd()
        logger.info('Directory was None, using current working directory.')

    sys.path.append(directory)
    # create the outputs folder
    logger.info('Creating output folder.')
    os.makedirs('./outputs', exist_ok=True)
    return directory


def _get_parent_run_id(run_id: str) -> str:
    """
    Code for getting the AutoML parent run-id from the child run-id.
    :param run_id: This is in format AutoML_<GUID>_*
    :type run_id: str
    :return: str
    """
    parent_run_length = run_id.rfind("_")
    if parent_run_length == -1:
        raise ClientException.create_without_pii("Malformed AutoML child run-id passed")
    return run_id[0:parent_run_length]


def _prepare_data(data_preparer: Optional[DataPreparer],
                  automl_settings_obj: AzureAutoMLSettings,
                  script_directory: Optional[str],
                  entry_point: Optional[str],
                  verifier: Optional[VerifierManager] = None) -> Dict[str, Any]:
    if data_preparer:
        data_dict = data_preparer.prepare(automl_settings_obj)
    else:
        if script_directory is None:
            script_directory = ""
        if entry_point is None:
            entry_point = ""
        script_path = os.path.join(script_directory, entry_point)
        if script_path is None:
            script_path = '.'
        user_module = _load_user_script(script_path, False)
        data_dict = training_utilities._extract_user_data(user_module)

    # When data were read try to fix the frequency.
    if automl_settings_obj.is_timeseries and data_dict.get('X_valid') is None:
        training_utilities._check_dimensions(data_dict['X'], data_dict['y'], None, None, None, None)
        # If X and y are dataflow object, we need to deserialize it here.
        X = data_dict['X']
        if isinstance(X, np.ndarray) and data_dict.get('x_raw_column_names') is not None:
            X = pd.DataFrame(X, columns=data_dict.get('x_raw_column_names'))
        y = data_dict['y']
        X, data_dict['y'], failed, corrected = fix_data_set_regularity_may_be(
            X,
            y,
            automl_settings_obj.time_column_name,
            automl_settings_obj.grain_column_names)
        # We may have reordered data frame X reorder it back here.
        X = X[data_dict['x_raw_column_names']]
        # Do our best to clean up memory.
        del data_dict['X']
        gc.collect()
        # If we do not have enough memory, raise the exception.
        training_utilities.check_memory_limit(X, data_dict['y'])
        # and then copy the data to new location.
        data_dict['X'] = X.values
        if verifier:
            verifier.update_data_verifier_frequency_inference(failed, corrected)

    data_dict['X'], data_dict['y'], data_dict['sample_weight'], data_dict['X_valid'], data_dict['y_valid'], \
        data_dict['sample_weight_valid'] = rule_based_validation(automl_settings_obj,
                                                                 data_dict.get('X'),
                                                                 data_dict.get('y'),
                                                                 data_dict.get('sample_weight'),
                                                                 data_dict.get('X_valid'),
                                                                 data_dict.get('y_valid'),
                                                                 data_dict.get('sample_weight_valid'),
                                                                 data_dict.get('cv_splits_indices'),
                                                                 verifier=verifier)
    return data_dict


def _transform_and_validate_input_data(
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings_obj: AzureAutoMLSettings,
        cache_store: Optional[CacheStore],
        experiment_observer: Optional[ExperimentObserver] = None,
        verifier: Optional[VerifierManager] = None,
        feature_config_manager: Optional[AutoMLFeatureConfigManager] = None,
        preparation_type: str = PreparationRunTypeConstants.SETUP_ONLY
) -> Optional[Union[TransformedDataContext, StreamingTransformedDataContext]]:
    with logging_utilities.log_activity(logger=logger, activity_name="Getting transformed data context."):
        raw_data_context = RawDataContext(automl_settings_obj=automl_settings_obj,
                                          X=fit_iteration_parameters_dict.get('X'),
                                          y=fit_iteration_parameters_dict.get('y'),
                                          X_valid=fit_iteration_parameters_dict.get('X_valid'),
                                          y_valid=fit_iteration_parameters_dict.get('y_valid'),
                                          sample_weight=fit_iteration_parameters_dict.get('sample_weight'),
                                          sample_weight_valid=fit_iteration_parameters_dict.get('sample_weight_valid'),
                                          x_raw_column_names=fit_iteration_parameters_dict.get('x_raw_column_names'),
                                          cv_splits_indices=fit_iteration_parameters_dict.get('cv_splits_indices'),
                                          training_data=fit_iteration_parameters_dict.get('training_data'),
                                          validation_data=fit_iteration_parameters_dict.get('validation_data')
                                          )
        if cache_store is not None:
            logger.info('Using {} for caching transformed data.'.format(type(cache_store).__name__))

        experiment = None
        parent_run_id = None
        try:
            experiment, run_id = Run._load_scope()
            parent_run_id = _get_parent_run_id(run_id)
        except Exception:
            pass  # No environment variable found, so must be running from unit test.

        feature_sweeping_config = {}  # type: Dict[str, Any]
        if experiment is not None and parent_run_id is not None:
            if feature_config_manager is None:
                feature_config_manager = _build_feature_config_manager(experiment)
            feature_sweeping_config = feature_config_manager.get_feature_sweeping_config(
                enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
                parent_run_id=parent_run_id,
                task_type=automl_settings_obj.task_type)

        transformed_data_context = None
        if preparation_type == PreparationRunTypeConstants.SETUP_BEFORE_FEATURIZATION:
            logger.info("Checking if feature sweeping is necessary.")
            feature_sweeped_state_container = data_transformation.get_transformers_for_full_featurization(
                raw_data_context,
                cache_store=cache_store,
                is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
                experiment_observer=experiment_observer,
                enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
                verifier=verifier,
                enable_streaming=automl_settings_obj.enable_streaming,
                feature_sweeping_config=feature_sweeping_config,
                enable_dnn=automl_settings_obj.enable_dnn,
                force_text_dnn=automl_settings_obj.force_text_dnn
            )
            if feature_sweeped_state_container is None:
                # we do not kick off a separate featurization run
                with logging_utilities.log_activity(logger=logger,
                                                    activity_name="Skipping setup/featurization run split. "
                                                                  "Beginning full featurization logic."):
                    transformed_data_context = data_transformation.complete_featurization(
                        raw_data_context,
                        cache_store=cache_store,
                        is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
                        experiment_observer=experiment_observer,
                        enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
                        verifier=verifier,
                        enable_streaming=automl_settings_obj.enable_streaming,
                        feature_sweeping_config=feature_sweeping_config,
                        enable_dnn=automl_settings_obj.enable_dnn,
                        force_text_dnn=automl_settings_obj.force_text_dnn,
                        feature_sweeped_state_container=feature_sweeped_state_container
                    )
            else:
                # we do kick off a separate feature sweeping run, so we must upload
                # the artifacts necessary for that to succeed
                logger.info("Uploading artifacts required for separate featurization run.")
                # cast getter functions to remove NoneType that checker sees would
                # result on code paths that raise an error
                save_feature_config(cast(Union[List[TransformerAndMapper], DataFrameMapper],
                                         feature_sweeped_state_container.get_feature_config()))
                save_engineered_feature_names(cast(_GenerateEngineeredFeatureNames,
                                                   feature_sweeped_state_container.get_engineered_feature_names()))
                setup_run = Run.get_context()
                setup_run.add_properties({FeaturizationRunConstants.CONFIG_PROP: FeaturizationRunConstants.CONFIG_PATH,
                                          FeaturizationRunConstants.NAMES_PROP: FeaturizationRunConstants.NAMES_PATH})
        elif preparation_type == PreparationRunTypeConstants.FEATURIZATION_ONLY:
            with logging_utilities.log_activity(logger=logger, activity_name="Beginning full featurization logic."):
                transformed_data_context = data_transformation.complete_featurization(
                    raw_data_context,
                    cache_store=cache_store,
                    is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
                    experiment_observer=experiment_observer,
                    enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
                    verifier=verifier,
                    enable_streaming=automl_settings_obj.enable_streaming,
                    feature_sweeping_config=feature_sweeping_config,
                    enable_dnn=automl_settings_obj.enable_dnn,
                    force_text_dnn=automl_settings_obj.force_text_dnn
                )
        else:
            # likely equal to PreparationRunTypeConstants.SETUP_ONLY,
            # in which we want to default to legacy setup behavior.
            with logging_utilities.log_activity(logger=logger,
                                                activity_name="Invoking default data transformation behavior."):
                transformed_data_context = data_transformation.transform_data(
                    raw_data_context,
                    cache_store=cache_store,
                    is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
                    enable_feature_sweeping=automl_settings_obj.enable_feature_sweeping,
                    enable_dnn=automl_settings_obj.enable_dnn,
                    force_text_dnn=automl_settings_obj.force_text_dnn,
                    experiment_observer=experiment_observer,
                    verifier=verifier,
                    enable_streaming=automl_settings_obj.enable_streaming,
                    feature_sweeping_config=feature_sweeping_config)
    return transformed_data_context


def _set_problem_info_for_featurized_data(
        run: Run,
        fit_iteration_parameters_dict: Dict[str, Any],
        automl_settings_obj: AzureAutoMLSettings,
        cache_store: Optional[CacheStore],
        experiment_observer: ExperimentObserver,
        verifier: Optional[VerifierManager] = None,
        feature_config_manager: Optional[AutoMLFeatureConfigManager] = None,
        preparation_type: str = PreparationRunTypeConstants.SETUP_ONLY) \
        -> Optional[Union[TransformedDataContext, StreamingTransformedDataContext]]:
    """
    Sets problem info in the run that generates it, which will either be the setup or featurization run,
    depending on the code path/scenario.

    :param run: The current run.
    :param fit_iteration_parameters_dict: Dictionary of parameters for fit iteration.
    :param automl_settings_obj: Object containing AutoML settings as specified by user.
    :param cache_store: The cache store.
    :param experiment_observer: The experiment observer.
    :param verifier: The fault verifier manager.
    :param feature_config_manager: The config manager for AutoML features.
    :param preparation_type: The type of preparation run currently being performed.
    :return: The transformed data context, after the problem info has been set.
    """
    if cache_store is not None:
        try:
            transformed_data_context = _transform_and_validate_input_data(
                fit_iteration_parameters_dict,
                automl_settings_obj,
                cache_store,
                experiment_observer,
                verifier=verifier,
                feature_config_manager=feature_config_manager,
                preparation_type=preparation_type)
            if is_transformation_finished(transformed_data_context):
                transformed_data_context = cast(Union[TransformedDataContext, StreamingTransformedDataContext],
                                                transformed_data_context)  # drop NoneType checked in conditional
                logger.info('Setting problem info.')
                _automl._set_problem_info(
                    transformed_data_context.X,
                    transformed_data_context.y,
                    automl_settings=automl_settings_obj,
                    current_run=run,
                    transformed_data_context=transformed_data_context,
                    cache_store=cache_store
                )
            return transformed_data_context
        except CacheException as e:
            # Log warning and retry without caching.
            logging_utilities.log_traceback(e, logger)
            logger.warning('Setup failed, falling back to alternative method.')

    logger.info('Start setting problem info using old model.')
    transformed_data_context = _transform_and_validate_input_data(
        fit_iteration_parameters_dict,
        automl_settings_obj,
        cache_store=None,
        experiment_observer=experiment_observer,
        verifier=verifier,
        preparation_type=preparation_type)
    if is_transformation_finished(transformed_data_context):
        _automl._set_problem_info(
            X=fit_iteration_parameters_dict.get('X'),
            y=fit_iteration_parameters_dict.get('y'),
            automl_settings=automl_settings_obj,
            current_run=run,
            transformed_data_context=transformed_data_context
        )
    return transformed_data_context


def _get_cache_data_store(current_run: Run) -> Optional[Datastore]:
    data_store = None   # type: Optional[Datastore]
    start = time.time()
    try:
        data_store = Datastore.get(current_run.experiment.workspace, WORKSPACE_BLOB_DATASTORE)
        logger.info('Successfully got the cache data store, caching enabled.')
    except HttpOperationError as response_exception:
        logging_utilities.log_traceback(response_exception, logger)
        if response_exception.response.status_code >= 500:
            raise
        else:
            raise UserException.from_exception(response_exception).with_generic_msg(
                'Failed to get default datastore from Datastore Service. HTTP Status code: {}'.format(
                    response_exception.response.status_code)
            )
    end = time.time()
    logger.info('Took {} seconds to retrieve cache data store'.format(end - start))
    return data_store


def _initialize_onnx_converter_with_cache_store(automl_settings_obj: AzureAutoMLSettings,
                                                onnx_cvt: OnnxConverter,
                                                fit_iteration_parameters_dict: Dict[str, Any],
                                                parent_run_id: str,
                                                cache_store: Optional[CacheStore]) -> None:
    if automl_settings_obj.enable_onnx_compatible_models:
        # Initialize the ONNX converter, get the converter metadata.
        onnx_mdl_name = '{}[{}]'.format(OnnxConvertConstants.OnnxModelNamePrefix, parent_run_id)
        onnx_mdl_desc = {'ParentRunId': parent_run_id}
        logger.info('Initialize ONNX converter for run {}.'.format(parent_run_id))
        onnx_cvt.initialize_input(X=fit_iteration_parameters_dict.get('X'),
                                  x_raw_column_names=fit_iteration_parameters_dict.get("x_raw_column_names"),
                                  model_name=onnx_mdl_name,
                                  model_desc=onnx_mdl_desc)
        onnx_cvt_init_metadata_dict = onnx_cvt.get_init_metadata_dict()
        # If the cache store and the onnx converter init metadata are valid, save it into cache store.
        if (cache_store is not None and
                onnx_cvt_init_metadata_dict is not None and
                onnx_cvt_init_metadata_dict):
            logger.info('Successfully initialized ONNX converter for run {}.'.format(parent_run_id))
            logger.info('Begin saving onnx initialization metadata for run {}.'.format(parent_run_id))
            cache_store.add([CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA], [onnx_cvt_init_metadata_dict])
            logger.info('Successfully Saved onnx initialization metadata for run {}.'.format(parent_run_id))
        else:
            logger.info('Failed to initialize ONNX converter for run {}.'.format(parent_run_id))


def _load_data_from_cache(cache_store: CacheStore) -> Optional[DatasetBase]:
    try:
        cache_store.load()
        dataset_dict = cache_store.get([DATASET_BASE_CACHE_KEY])
        if dataset_dict is not None:
            result = dataset_dict.get(DATASET_BASE_CACHE_KEY, None)  # type: Optional[DatasetBase]
            if result:
                logger.info('Successfully loaded the AutoML Dataset from cache.')
                return result
        logger.warning("Failed to find {} in cache_store.".format(DATASET_BASE_CACHE_KEY))
        return None
    except CacheException as e:
        logging_utilities.log_traceback(e, logger, is_critical=False)
        logger.warning("Failed to initialize Datasets from the cache, proceeding with re-transforming the "
                       "input data.")
        return None
    except Exception as e:
        logging_utilities.log_traceback(e, logger, is_critical=False)
        logger.warning('Fatal exception encountered while trying to load data from cache')
        raise


def _recover_dataset(
        script_directory: str,
        automl_settings_obj: AzureAutoMLSettings,
        run_id: str,
        dataprep_json: str,
        entry_point: str,
        onnx_cvt: Optional[Any] = None,
        **kwargs: Any
) -> Any:
    automl_run = get_automl_run_from_context(run_id)
    script_directory = _init_directory(directory=script_directory)
    data_store = _get_cache_data_store(automl_run)
    parent_run_id = _get_parent_run_id(run_id)

    cache_store = _get_cache_store(data_store=data_store, run_id=parent_run_id)
    dataset = _load_data_from_cache(cache_store)

    if dataset is None:
        logger.warning('Could not load data from cache, preparing to pull data from dataprep or user script.')
        dataset = _recover_dataset_internal(automl_settings_obj, cache_store, dataprep_json, entry_point,
                                            onnx_cvt, parent_run_id, script_directory)
    else:
        logger.info("Recovered dataset using datastore")

    return dataset


def _recover_dataset_internal(automl_settings_obj: AzureAutoMLSettings,
                              cache_store: CacheStore,
                              dataprep_json: str,
                              entry_point: str,
                              onnx_cvt: Optional[Any],
                              parent_run_id: str,
                              script_directory: str) -> DatasetBase:
    data_preparer = None
    if dataprep_json:
        data_preparer = DataPreparerFactory.get_preparer(dataprep_json)
    fit_iteration_parameters_dict = _prepare_data(
        data_preparer=data_preparer,
        automl_settings_obj=automl_settings_obj,
        script_directory=script_directory,
        entry_point=entry_point
    )  # type: Dict[str, Any]
    if fit_iteration_parameters_dict is None:
        raise DataException('Invalid raw data returned from _prepare_data().', has_pii=False)
    # Initialize the ONNX converter with raw data and cache the metadata.
    if automl_settings_obj.enable_onnx_compatible_models and onnx_cvt is not None:
        _initialize_onnx_converter_with_cache_store(
            automl_settings_obj=automl_settings_obj,
            onnx_cvt=onnx_cvt,
            fit_iteration_parameters_dict=fit_iteration_parameters_dict,
            parent_run_id=parent_run_id,
            cache_store=cache_store)

    # _transform_and_validate_input_data can only return None when preparation_type is specified
    transformed_data_context = cast(Union[TransformedDataContext, StreamingTransformedDataContext],
                                    _transform_and_validate_input_data(fit_iteration_parameters_dict,
                                                                       automl_settings_obj=automl_settings_obj,
                                                                       cache_store=cache_store))

    dataset = training_utilities.init_dataset(
        transformed_data_context=transformed_data_context,
        cache_store=cache_store,
        automl_settings=automl_settings_obj,
        remote=True,
        init_all_stats=False,
        keep_in_memory=False)
    logger.info("Initialized AutoML Dataset from transformed_data_context.")
    logger.info("Deleting transformed_data_context.")
    del transformed_data_context
    logger.info("Deleting input data")
    del fit_iteration_parameters_dict
    return dataset


def _get_feature_configs(parent_run_id: str, automl_settings_obj: Any) -> Dict[str, Any]:
    feature_configs = {}  # type: Dict[str, Any]
    try:
        experiment, _ = Run._load_scope()
        jasmine_client = JasmineClient(experiment.workspace.service_context, experiment.name,
                                       user_agent=type(JasmineClient).__name__)
        feature_config_manager = AutoMLFeatureConfigManager(jasmine_client=jasmine_client)
        # Get the community or premium config
        feature_configs = feature_config_manager.get_feature_configurations(
            parent_run_id,
            model_explainability=automl_settings_obj.model_explainability,
            is_remote=True)
    except Exception:
        logger.info("Unable to get model explanation community/premium config")

    return feature_configs


def model_exp_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        child_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """
    Compute best run model or on-demand explanations in remote runs.

    :param script_directory:
    :param automl_settings:
    :param run_id: The run id for model explanations run. This is AutoML_<GUID>_ModelExplain in case
                   of best run model explanations and <GUID> in case of on-demand explanations.
    :param child_run_id: The AutoML child run id for which to compute on-demand explanations for.
                         This is 'None' for best run model explanations and an AutoMl child run-id
                         for on-demand model explanation run.
    :param dataprep_json:
    :param entry_point:
    :param kwargs:
    :return:
    """
    model_exp_output = {}  # type: Dict[str, Any]
    current_run = get_automl_run_from_context()
    if child_run_id:
        automl_run_obj = AutoMLRun(current_run.experiment, child_run_id)
    else:
        automl_run_obj = current_run
    automl_settings_obj = _parse_settings(automl_run_obj, automl_settings)
    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))
    try:
        if not child_run_id:
            parent_run_id = _get_parent_run_id(run_id)
            dataset = _recover_dataset(script_directory, automl_settings_obj, run_id,
                                       dataprep_json, entry_point, activity_logger)
        else:
            parent_run_id = _get_parent_run_id(child_run_id)
            dataset = _recover_dataset(script_directory, automl_settings_obj, child_run_id,
                                       dataprep_json, entry_point, activity_logger)

        feature_configs = _get_feature_configs(parent_run_id, automl_settings_obj)

        if not child_run_id:
            logger.info('Beginning best run remote model explanations for run {}.'.format(parent_run_id))
            print('Beginning best run remote model explanations for run {}.'.format(parent_run_id))

            # Get the best run model explanation
            parent_run = AutoMLRun(current_run.experiment, parent_run_id)
            experiment_observer = AzureExperimentObserver(parent_run, console_logger=sys.stdout, file_logger=logger)
            _automl_perform_best_run_explain_model(
                parent_run, dataset, automl_settings_obj,
                logger, compute_target=ComputeTargets.AMLCOMPUTE,
                current_run=current_run,
                experiment_observer=experiment_observer,
                model_exp_feature_config=feature_configs.get(MODEL_EXPLAINABILITY_ID))
        else:
            logger.info('Beginning on-demand remote model explanations for run {}.'.format(child_run_id))
            print('Beginning on-demand remote model explanations for run {}.'.format(child_run_id))

            child_run = AutoMLRun(current_run.experiment, child_run_id)
            if current_run is not None:
                child_run.set_tags({ModelExplanationRunId: str(current_run.id)})

            # Get the model explanation for the child run
            with dataset.open_dataset():
                _automl_auto_mode_explain_model(child_run, dataset,
                                                automl_settings_obj,
                                                logger,
                                                model_exp_feature_config=feature_configs.get(
                                                    MODEL_EXPLAINABILITY_ID))
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        if not child_run_id:
            logger.info("Error in best run model explanations computation.")
        else:
            logger.info("Error in on-demand model explanations computation.")
        current_run._fail_with_error(e)
    return model_exp_output


def driver_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_percent: int,
        iteration: int,
        pipeline_spec: str,
        pipeline_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """
    Code for iterations in remote runs.
    """
    from datetime import datetime
    print("{} - INFO - Beginning driver wrapper.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
    current_run = get_automl_run_from_context()  # this is the child run
    automl_settings_obj = _parse_settings(current_run, automl_settings)
    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))

    result = {}  # type: Dict[str, Any]

    try:
        logger.info('Beginning AutoML remote driver for run {}.'.format(run_id))

        script_directory = _init_directory(directory=script_directory)
        data_store = _get_cache_data_store(current_run)
        parent_run_id = _get_parent_run_id(run_id)
        cache_store = _get_cache_store(data_store=data_store, run_id=parent_run_id)

        if automl_settings_obj.enable_streaming:
            _modify_settings_for_streaming(automl_settings_obj, dataprep_json)

        onnx_cvt = None
        if automl_settings_obj.enable_onnx_compatible_models:
            enable_split_onnx_models = automl_settings_obj.enable_split_onnx_featurizer_estimator_models
            onnx_cvt = OnnxConverter(logger=logger,
                                     version=pkg_ver,
                                     is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
                                     enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)

        dataset = _recover_dataset(script_directory, automl_settings_obj, run_id,
                                   dataprep_json, entry_point, onnx_cvt)

        if automl_settings_obj.enable_onnx_compatible_models and onnx_cvt is not None:
            if cache_store is not None and not onnx_cvt.is_initialized():
                # Try to initialize the ONNX converter with cached converter metadata if it wasn't initialized
                # in the previous step.
                logger.info('Get ONNX converter init metadata for run {}.'.format(run_id))
                cache_store.load()
                cached_data_dict = cache_store.get([CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA])
                if cached_data_dict is not None and cached_data_dict:
                    onnx_cvt_init_metadata_dict = cached_data_dict.get(
                        CACHE_STORE_KEY_ONNX_CONVERTER_INIT_METADATA, None)  # type: Optional[Dict[str, Any]]
                    if onnx_cvt_init_metadata_dict is not None:
                        logger.info('Initialize ONNX converter with cached metadata run {}.'.format(run_id))
                        onnx_mdl_name = 'AutoML_ONNX_Model_[{}]'.format(parent_run_id)
                        onnx_mdl_desc = {'ParentRunId': parent_run_id}
                        onnx_cvt.initialize_with_metadata(metadata_dict=onnx_cvt_init_metadata_dict,
                                                          model_name=onnx_mdl_name,
                                                          model_desc=onnx_mdl_desc)

            if onnx_cvt.is_initialized():
                logger.info('Successfully initialized ONNX converter for run {}.'.format(run_id))
            else:
                logger.info('Failed to initialize ONNX converter for run {}.'.format(run_id))

        logger.info('Starting the run.')
        child_run = Run.get_context()
        automl_run_context = AzureAutoMLRunContext(child_run)
        automl_pipeline = AutoMLPipeline(automl_run_context, pipeline_spec, pipeline_id, training_percent / 100)

        # Dataset will have a valid value for # of CV splits if we were to do auto CV.
        # Set the value of n_cross_validations in AutoML settings if that were the case
        if automl_settings_obj.n_cross_validations is None and dataset.get_num_auto_cv_splits() is not None:
            n_cv = dataset.get_num_auto_cv_splits()
            logger.info("Number of cross-validations in Dataset is {}.".format(n_cv))
            automl_settings_obj.n_cross_validations = None if n_cv == 0 else n_cv
    except Exception as e:
        logger.info("Error in preparing part of driver_wrapper.")
        logging_utilities.log_traceback(e, logger)
        current_run._fail_with_error(e)
    else:
        try:
            feature_configs = _get_feature_configs(parent_run_id, automl_settings_obj)
            parent_run = get_automl_run_from_context(parent_run_id)
            # exception if fit_pipeline should already been logged and saved to rundto.error.
            fit_output = fit_pipeline_helper.fit_pipeline(
                automl_pipeline=automl_pipeline,
                automl_settings=automl_settings_obj,
                automl_run_context=automl_run_context,
                remote=True,
                dataset=dataset,
                onnx_cvt=onnx_cvt,
                bypassing_model_explain=parent_run.get_tags().get('model_explain_run'),
                feature_configs=feature_configs,
                working_dir=os.getcwd())
            result = fit_output.get_output_dict()
            if fit_output.errors:
                for fit_exception in fit_output.errors.values():
                    if fit_exception.get("is_critical"):
                        exception = cast(BaseException, fit_exception.get("exception"))
                        raise exception.with_traceback(exception.__traceback__)
            primary_metric = fit_output.primary_metric
            score = fit_output.score
            duration = fit_output.actual_time
            logger.info('Child run completed with {}={} after {} seconds.'.format(primary_metric, score, duration))
        except Exception as e:
            logger.info("Error in fit_pipeline part of driver_wrapper.")
            current_run._fail_with_error(e)
    return result


def _get_cache_store(
        data_store: Optional[AbstractAzureStorageDatastore],
        run_id: str
) -> CacheStore:
    cache_location = '{0}/{1}'.format('_remote_cache_directory_', run_id)

    os.makedirs(cache_location, exist_ok=True)
    return CacheStoreFactory.get_cache_store(enable_cache=True,
                                             temp_location=cache_location,
                                             run_target=ComputeTargets.AMLCOMPUTE,
                                             run_id=run_id,
                                             data_store=data_store)


def _build_feature_config_manager(experiment: Experiment) -> AutoMLFeatureConfigManager:
    """Build an AutoML feature config manager for the run."""
    jasmine_client = JasmineClient(
        experiment.workspace.service_context,
        experiment.name,
        user_agent=type(JasmineClient).__name__)
    return AutoMLFeatureConfigManager(jasmine_client=jasmine_client)


def _modify_settings_for_streaming(
        automl_settings_obj: AzureAutoMLSettings,
        dataprep_json: str
) -> None:
    automl_settings_obj.enable_streaming = True
    # check if UX and update the settings appropriately
    dataprep_json_obj = json.loads(dataprep_json)
    if 'activities' not in dataprep_json_obj:
        # for UI we need to set the label_column_name
        if automl_settings_obj.label_column_name is None:
            automl_settings_obj.label_column_name = dataprep_json_obj.get('label', None)
            logger.info('Set label_column_name')

    if automl_settings_obj.enable_stack_ensembling is True or automl_settings_obj.enable_ensembling is True:
        logger.warning('The training data is large. Ensembling is not available for this run.')
        automl_settings_obj.enable_stack_ensembling = False
        automl_settings_obj.enable_ensembling = False


def _are_inputs_conducive_for_streaming(
        automl_settings: AzureAutoMLSettings,
        data_preparer: DataPreparer
) -> bool:
    if automl_settings.force_streaming:
        return True

    # List storing all the reasons due to which streaming could not be enabled
    incompatibility_reasons = []    # type: List[str]

    if data_preparer._original_training_data is None:
        incompatibility_reasons.append("'training_data' is not provided")

    if automl_settings.spark_context is not None:
        incompatibility_reasons.append("Spark runs are not supported")

    if automl_settings.is_timeseries:
        incompatibility_reasons.append("Forecasting is not supported")

    if automl_settings.n_cross_validations is not None:
        incompatibility_reasons.append("'n_cross_validations' was non-empty")

    if automl_settings.enable_onnx_compatible_models:
        incompatibility_reasons.append("ONNX compatibility is not supported")

    if automl_settings.enable_dnn:
        incompatibility_reasons.append("DNN is not supported")

    if automl_settings.enable_subsampling:
        incompatibility_reasons.append("Subsampling is enabled")

    if automl_settings.whitelist_models is not None:
        supported_set = set([model.customer_model_name for model in SupportedModelNames.SupportedStreamingModelList])
        if not set(automl_settings.whitelist_models).issubset(supported_set):
            incompatibility_reasons.append("Whitelisted models are unsupported. "
                                           "Supported models: [{}]".format(','.join(supported_set)))

    if incompatibility_reasons:
        logger.info("Streaming is not conducive due to incompatible settings. "
                    "Reason[s]: [{}]".format(', '.join(incompatibility_reasons)))
        return False

    return True


def setup_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        preparation_type: str = PreparationRunTypeConstants.SETUP_ONLY,
        **kwargs: Any
) -> None:
    """
    Code for setup iterations for AutoML remote runs.
    """

    verifier = VerifierManager()
    setup_run = get_automl_run_from_context()
    automl_settings_obj = _parse_settings(setup_run, automl_settings)
    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))
    try:
        fit_iteration_parameters_dict, cache_store, experiment_observer, feature_config_manager, parent_run = \
            _prep_and_validate_input_data(setup_run, "setup", automl_settings_obj, pkg_ver,
                                          script_directory, dataprep_json, entry_point, verifier)
        # Transform raw input, validate and save to cache store.
        logger.info('Set problem info. AutoML remote setup iteration for run {}.'.format(setup_run.id))
        transformed_data_context = \
            _set_problem_info_for_featurized_data(setup_run,
                                                  fit_iteration_parameters_dict,
                                                  automl_settings_obj,
                                                  cache_store,
                                                  experiment_observer,
                                                  verifier=verifier,
                                                  feature_config_manager=feature_config_manager,
                                                  preparation_type=preparation_type)
        if is_transformation_finished(transformed_data_context):
            # transformation is finished, so transformed_data_context cannot be None
            cache_dataset(cast(Union[TransformedDataContext, StreamingTransformedDataContext],
                               transformed_data_context),
                          cache_store,
                          automl_settings_obj,
                          experiment_observer,
                          parent_run)

        parent_run_context = AzureAutoMLRunContext(parent_run)
        verifier.write_result_file(parent_run_context)

    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.info("Error in setup_wrapper.")
        setup_run._fail_with_error(e)


def featurization_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        **kwargs: Any) -> None:
    """
    Code for featurization part of setup iterations for AutoML remote runs.
    """
    featurization_run = get_automl_run_from_context()
    property_dict = featurization_run.get_properties()
    transfer_files_from_setup(featurization_run, setup_container_id,
                              property_dict.get(FeaturizationRunConstants.CONFIG_PROP,
                                                FeaturizationRunConstants.CONFIG_PATH),
                              property_dict.get(FeaturizationRunConstants.NAMES_PROP,
                                                FeaturizationRunConstants.NAMES_PATH))
    automl_settings_obj = _parse_settings(featurization_run, automl_settings)
    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))
    try:
        fit_iteration_parameters_dict, cache_store, experiment_observer, feature_config_manager, parent_run = \
            _prep_and_validate_input_data(featurization_run, "featurization", automl_settings_obj,
                                          pkg_ver, script_directory, dataprep_json, entry_point)

        # Transform raw input, validate and save to cache store.
        logger.info('Set problem info. AutoML remote featurization iteration for run {}.'.format(featurization_run.id))
        transformed_data_context = \
            _set_problem_info_for_featurized_data(featurization_run,
                                                  fit_iteration_parameters_dict,
                                                  automl_settings_obj,
                                                  cache_store,
                                                  experiment_observer,
                                                  feature_config_manager=feature_config_manager,
                                                  preparation_type=PreparationRunTypeConstants.FEATURIZATION_ONLY)
        cache_dataset(cast(Union[TransformedDataContext, StreamingTransformedDataContext], transformed_data_context),
                      cache_store,
                      automl_settings_obj,
                      experiment_observer,
                      parent_run)
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.info("Error in featurization_wrapper.")
        featurization_run._fail_with_error(e)


def _prep_and_validate_input_data(run: Run,
                                  iteration_name: str,
                                  automl_settings_obj: AzureAutoMLSettings,
                                  pkg_ver: str,
                                  script_directory: Optional[str],
                                  dataprep_json: str,
                                  entry_point: str,
                                  verifier: Optional[VerifierManager] = None,
                                  ) \
        -> Tuple[Dict[str, Any], CacheStore, ExperimentObserver, AutoMLFeatureConfigManager, Run]:
    parent_run_id = _get_parent_run_id(run.id)
    # get the parent run instance to be able to report preprocessing progress on it and set error.
    parent_run = get_automl_run_from_context(parent_run_id)

    logger.info('Beginning AutoML remote {} iteration for run {}.'.format(iteration_name, run.id))

    script_directory = _init_directory(directory=script_directory)
    cache_data_store = _get_cache_data_store(run)

    calculated_experiment_info = None
    data_preparer = None
    if dataprep_json:
        data_preparer = DataPreparerFactory.get_preparer(dataprep_json)
        conducive_for_streaming = _are_inputs_conducive_for_streaming(automl_settings_obj, data_preparer)
        if conducive_for_streaming and data_preparer.data_characteristics is not None:
            calculated_experiment_info = \
                CaclulatedExperimentInfo(data_preparer.data_characteristics.num_rows,
                                         data_preparer.data_characteristics.num_numerical_columns,
                                         data_preparer.data_characteristics.num_categorical_columns,
                                         data_preparer.data_characteristics.num_text_columns,
                                         memory_utilities.get_available_physical_memory())

    feature_config_manager = _build_feature_config_manager(run.experiment)
    feature_config_manager.fetch_all_feature_profiles_for_run(
        parent_run_id=parent_run_id,
        automl_settings=automl_settings_obj,
        caclulated_experiment_info=calculated_experiment_info
    )

    if feature_config_manager.is_streaming_enabled():
        logger.info('Service responded with streaming enabled')
        _modify_settings_for_streaming(
            automl_settings_obj,
            dataprep_json)
    else:
        logger.info('Service responded with streaming disabled')

    fit_iteration_parameters_dict = _prepare_data(
        data_preparer=data_preparer,
        automl_settings_obj=automl_settings_obj,
        script_directory=script_directory,
        entry_point=entry_point,
        verifier=verifier
    )

    experiment_observer = AzureExperimentObserver(parent_run, file_logger=logger)

    # Get the cache store.
    cache_store = _get_cache_store(data_store=cache_data_store, run_id=parent_run_id)

    if automl_settings_obj.enable_streaming:
        logger.info("Streaming enabled")

    if automl_settings_obj.enable_onnx_compatible_models:
        # Initialize the ONNX converter and save metadata in the cache store.
        enable_split_onnx_models = automl_settings_obj.enable_split_onnx_featurizer_estimator_models
        onnx_cvt = OnnxConverter(logger=logger,
                                 version=pkg_ver,
                                 is_onnx_compatible=automl_settings_obj.enable_onnx_compatible_models,
                                 enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)
        _initialize_onnx_converter_with_cache_store(automl_settings_obj=automl_settings_obj,
                                                    onnx_cvt=onnx_cvt,
                                                    fit_iteration_parameters_dict=fit_iteration_parameters_dict,
                                                    parent_run_id=parent_run_id,
                                                    cache_store=cache_store)

    logger.info('Validating training data.')
    training_utilities.validate_training_data_dict(fit_iteration_parameters_dict, automl_settings_obj, logger)
    logger.info('Input data successfully validated.')
    return fit_iteration_parameters_dict, cache_store, experiment_observer, feature_config_manager, parent_run


def cache_dataset(transformed_data_context: Union[TransformedDataContext, StreamingTransformedDataContext],
                  cache_store: CacheStore,
                  automl_settings_obj: AzureAutoMLSettings,
                  experiment_observer: ExperimentObserver,
                  parent_run: Run) -> None:
    try:
        dataset = training_utilities.init_dataset(
            transformed_data_context=transformed_data_context,
            cache_store=cache_store,
            automl_settings=automl_settings_obj,
            remote=True,
            init_all_stats=False,
            keep_in_memory=False)
        cache_store.set(DATASET_BASE_CACHE_KEY, dataset)
        logger.info("Initialized Datasets from transformed_data_context during setup.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger, is_critical=False)
        logger.warning("Failed to initialize Datasets object from transformed_data_context. We will need to "
                       "re-transform the input data for every individual iteration moving forward.")

    logger.info('Preparation for run id {} finished successfully.'.format(parent_run.id))

    experiment_observer.report_status(ExperimentStatus.ModelSelection, "Beginning model selection.")


def is_transformation_finished(
        transformed_data_context: Optional[Union[TransformedDataContext, StreamingTransformedDataContext]]) -> bool:
    """
    Helper function that encapsulates the logic for detecting whether this SDK
    has finished transforming the data context or not.

    :param transformed_data_context: the transformed data context, as returned
     by _set_problem_info_for_featurized_data.
    """
    return transformed_data_context is not None


def transfer_files_from_setup(run: Run, setup_container_id: str,
                              feature_config_path: str, engineered_names_path: str) -> None:
    """
    Helper function that transfers essential files from the setup run's data container to the featurization run.

    :param run: the run object to which we are downloading the files.
    :param setup_container_id: the id string of the setup run's data container.
    :param feature_config_path: the path to the feature_config object in the setup run's data container.
    :param engineered_names_path: the path to the engineered_feature_names object in the setup run's data container.
    :return: None
    """
    run._client.artifacts.download_artifact(RUN_ORIGIN, setup_container_id,
                                            feature_config_path, feature_config_path)
    run._client.artifacts.download_artifact(RUN_ORIGIN, setup_container_id,
                                            engineered_names_path, engineered_names_path)


def get_automl_run_from_context(run_id: Optional[str] = None) -> AutoMLRun:
    run = Run.get_context()
    return AutoMLRun(run.experiment, run_id or run.id)
