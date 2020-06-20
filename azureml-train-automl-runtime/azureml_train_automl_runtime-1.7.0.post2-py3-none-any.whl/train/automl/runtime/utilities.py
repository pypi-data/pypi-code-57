# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains utility methods used in automated ML in Azure Machine Learning."""
from typing import Any, Dict, List, Optional, Tuple, Union
from types import ModuleType
from datetime import datetime
import importlib
import importlib.util
import importlib.abc
import json
import logging
import numbers
import os
import pytz

from azureml._restclient.constants import RunStatus
from azureml.core import Run
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.exceptions import RunStateChangeException
from azureml.automl.runtime import fit_pipeline
from azureml.automl.runtime._run_history.offline_automl_run import OfflineAutoMLRun
from azureml.automl.runtime.fit_output import FitOutput
from azureml.train.automl import constants
from azureml.train.automl.exceptions import ConfigException, FileNotFoundException
from azureml.train.automl.runtime._azureautomlruncontext import AzureAutoMLRunContext


logger = logging.getLogger(__name__)


def _load_user_script(script_path: str, calling_in_client_runtime: bool = True) -> ModuleType:
    #  Load user script to get access to GetData function
    logger.info('Loading data using user script.')

    module_name, module_ext = os.path.splitext(os.path.basename(script_path))
    if module_ext != '.py':
        raise ConfigException.create_without_pii('The provided user script was not a Python file.')
    spec = importlib.util.spec_from_file_location('get_data', script_path)
    if spec is None:
        if calling_in_client_runtime:
            raise ConfigException.create_without_pii('The provided user script path does not exist.')
        else:
            raise FileNotFoundException.create_without_pii('The provided user script path does not exist.',
                                                           target="LoadUserScript")

    module_obj = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ConfigException.create_without_pii('The provided user script is a namespace package, '
                                                 'which is not supported.')

    # exec_module exists on 3.4+, but it's marked optional so we have to assert
    assert isinstance(spec.loader, importlib.abc.Loader)
    assert spec.loader.exec_module is not None
    _execute_user_script_object(spec, calling_in_client_runtime, script_path, module_obj)
    return module_obj


def _execute_user_script_object(spec: Any, calling_in_client_runtime: bool, script_path: str, module_obj: Any) -> Any:
    """Execute the loaded user script to obtain the data."""
    try:
        spec.loader.exec_module(module_obj)
    except FileNotFoundError:
        if calling_in_client_runtime:
            raise ConfigException.create_without_pii('The provided user script path does not exist.')
        else:
            if not os.path.exists(script_path):
                raise FileNotFoundException.create_without_pii('The provided user script path does not exist.',
                                                               target="LoadUserScript")
            else:
                raise ConfigException.create_without_pii(
                    'The provided user script references files that are not in the project folder.')
    except Exception as e:
        raise ConfigException.from_exception(
            e,
            target="module_obj",
            reference_code="_execute_user_script_object.module_obj.exception").with_generic_msg(
            'Exception while executing user script.'
        )

    if not hasattr(module_obj, 'get_data'):
        raise ConfigException.with_generic_msg('The provided user script does not implement get_data().')

    return module_obj


def _get_run_createdtime_starttime_and_endtime(run: Optional[Run]) -> Tuple[Optional[datetime],
                                                                            Optional[datetime],
                                                                            Optional[datetime]]:
    if run is None:
        return None, None, None

    if isinstance(run, OfflineAutoMLRun):
        # Add timezone information.
        return (run.created_time.replace(tzinfo=pytz.UTC),
                run.start_time.replace(tzinfo=pytz.UTC) if run.start_time is not None else None,
                run.end_time.replace(tzinfo=pytz.UTC) if run.end_time is not None else None)

    def _get_utc_time(datetime_str: Optional[str]) -> Optional[datetime]:
        if datetime_str is not None and isinstance(datetime_str, str):
            try:
                return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=pytz.UTC)
            except Exception:
                pass

        return None

    if run._run_dto is None:
        return None, None, None

    created_time_utc = _get_utc_time(run._run_dto.get('created_utc'))
    start_time_utc = _get_utc_time(run._run_dto.get('start_time_utc'))
    end_time_utc = _get_utc_time(run._run_dto.get('end_time_utc'))

    return created_time_utc, start_time_utc, end_time_utc


def _calculate_start_end_times(start_time: datetime, end_time: datetime, run: Optional[Run]) -> Tuple[datetime,
                                                                                                      datetime]:
    _, run_start_time, run_end_time = _get_run_createdtime_starttime_and_endtime(run)
    start_time = run_start_time or start_time.replace(tzinfo=pytz.UTC)
    end_time = run_end_time or end_time.replace(tzinfo=pytz.UTC)
    return start_time, end_time


def _create_best_run(
    parent_run: Run,
    best_offline_run: OfflineAutoMLRun
) -> Run:
    """When not tracking all child run details, create a single child run in run history for the best child run."""
    best_run_id = '{}_{}'.format(parent_run.id, constants.BEST_RUN_ID_SUFFIX)
    best_run = parent_run.child_run(name="best child run", run_id=best_run_id)

    # upload metrics to best run
    best_metrics = best_offline_run.get_metrics()
    fit_pipeline._log_metrics(best_run, best_metrics)

    # upload tags
    best_tags = best_offline_run.get_tags()
    if best_tags:
        best_run.set_tags(best_tags)

    best_run_context = AzureAutoMLRunContext(best_run)

    # upload files
    file_names = best_offline_run.get_uploaded_file_names()
    file_paths = []
    for file_name in file_names:
        file_path = best_offline_run.get_file_path(file_name)
        file_paths.append(file_path)
    if file_names:
        best_run_context._batch_save_artifact_files(file_names, file_paths)

    # upload properties
    best_properties = best_offline_run.get_properties()
    best_properties.update(best_run_context._get_artifact_id_run_properties())
    if best_properties:
        best_run.add_properties(best_properties)

    # set terminal status
    run_status = best_offline_run.get_status()
    if run_status == constants.Status.Completed:
        best_run.complete()
    elif run_status == constants.Status.Terminated:
        best_run.fail(best_offline_run.error_details, best_offline_run.error_code)

    # Update the status of the run object (and ensure that it matches the status in RH).
    # (Calling Run.complete() or Run.fail() doesn't update the existing run object's status to the new value.)
    run_status = best_run.get_status()
    if run_status not in [RunStatus.COMPLETED, RunStatus.FAILED]:
        raise RunStateChangeException(
            "Summarized best child run was not updated to terminal state", target="CreateBestRun", has_pii=False)

    return best_run


def _upload_summary_of_iterations(
    parent_run_context: AzureAutoMLRunContext,
    fit_outputs: List[FitOutput]
) -> None:
    """Upload summary of child iterations to the parent run."""
    summary = []  # type: List[Optional[Dict[str, Any]]]
    for fit_output in fit_outputs:
        if fit_output:
            # Only upload numeric run scores.
            # (Run scores can leverage data structures that are not JSON serializble.)
            scores = {}
            if fit_output.scores:
                for name, score in fit_output.scores.items():
                    if isinstance(score, numbers.Number):
                        scores[name] = score

            summary.append({
                'pipeline_script': fit_output.pipeline_script,
                'run_preprocessor': fit_output.run_preprocessor,
                'run_algorithm': fit_output.run_algorithm,
                'scores': scores
            })
        else:
            summary.append(None)

    summary_str = json.dumps(summary)
    try:
        parent_run_context.save_str_output(
            input_str=summary_str,
            remote_path=constants.CHILD_RUNS_SUMMARY_PATH)
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning("Failed to upload summary of iterations to parent run.")
