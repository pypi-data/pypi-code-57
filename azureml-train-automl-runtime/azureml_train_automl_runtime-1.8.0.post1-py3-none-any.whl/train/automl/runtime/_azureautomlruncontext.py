# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Context manager that wraps an AutoML run context."""
from typing import Any, Optional
import sys
import time

from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml._async import TaskQueue
from azureml.core import Run
from azureml.train.automl.run import AutoMLRun


class AzureAutoMLRunContext(AutoMLAbstractRunContext):

    def __init__(self, run: Optional[Run], is_adb_run: bool = False) -> None:
        """
        Create an AzureAutoMLRunContext object that wraps a run context.

        :param run: the run context to use
        :param is_adb_run: whether we are running in Azure DataBricks or not
        """
        super().__init__()
        self._run = run
        self._is_adb_run = is_adb_run

        # Refresh the run context after 15 minutes if running under adb
        self._timeout_interval = 900.0
        self._last_refresh = 0.0

        self._ident = 'AutoMLRunContextTasks'
        self._task_queue = TaskQueue(_ident=self._ident)

    def _get_run_internal(self) -> Run:
        """Retrieve a run context if needed and return it."""
        # In case we use get_run in nested with statements, only get the run context once
        if self._refresh_needed():
            self._last_refresh = time.time()
            self._run = Run.get_context()
        # `_OfflineRun`s aren't bound by experiment / workspace, so we can ignore those
        if isinstance(self._run, Run):
            return AutoMLRun(self._run.experiment, self._run.id)
        return self._run

    def _refresh_needed(self) -> bool:
        if self._run is None:
            return True

        if self._is_adb_run:
            return (time.time() - self._last_refresh) > self._timeout_interval

        return False

    def save_model_output(self, fitted_pipeline: Any, remote_path: str, working_dir: Optional[str]) -> None:
        """
        Save model output to provided path.

        :param fitted_pipeline:
        :param remote_path:
        :return:
        :raises azureml.exceptions.ServiceException
        """
        super().save_model_output(fitted_pipeline, remote_path, working_dir)

    def save_model_output_async(self, fitted_pipeline: Any, remote_path: str, working_dir: str) -> None:
        """
        Async save model function.

        # TODO: Move this function definition to common core

        :param fitted_pipeline:
        :param remote_path:
        :return:
        """
        self._task_queue.add(self.save_model_output, fitted_pipeline, remote_path, working_dir)

    def start_async_job(self, func, scores):
        """
        Start async job function.

        # TODO: Move this function definition to common core

        :param func:
        :param scores:
        :return:
        """
        self._task_queue.add(func, self, scores)

    def flush(self, timeout_seconds: int = sys.maxsize) -> None:
        """
        Flush the async task queue.

        # TODO: Move this function definition to common core

        :param timeout_seconds:
        :return:
        """
        timeout_seconds = timeout_seconds if timeout_seconds > 0 else sys.maxsize
        self._task_queue.flush(self._ident, timeout_seconds=timeout_seconds)
