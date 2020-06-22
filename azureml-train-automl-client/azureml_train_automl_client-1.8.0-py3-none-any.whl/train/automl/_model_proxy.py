# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Proxy for models produced by AutoML."""
import datetime
import logging
import os
import pickle
import shutil
import tempfile

from azureml.core import Dataset, Run, RunConfiguration, ScriptRunConfig
from azureml.core.compute import ComputeTarget
from azureml.data.abstract_dataset import AbstractDataset
from azureml.automl.core.shared.exceptions import ConfigException
from ._constants_azureml import MODEL_PATH
from .constants import LOCAL_PREDICT_NAME, PREDICT_INPUT_FILE, SCRIPT_RUN_ID_PROPERTY

PREDICT = "predict"
PREDICT_PROBA = "predict_proba"
FORECAST = "forecast"

logger = logging.getLogger(__name__)


class _ModelProxy:
    """Proxy object for AutoML models that enables inference on remote compute."""

    def __init__(self, child_run, compute_target=None):
        """
        Create an AutoML ModelProxy object.
        """
        if not isinstance(child_run, Run):
            raise ConfigException("Child run needs to be an azureml.core.Run object.", has_pii=False)
        self.run = child_run
        if compute_target is not None:
            if isinstance(compute_target, ComputeTarget):
                self.compute_target = compute_target.name
            elif isinstance(compute_target, str):
                self.compute_target = compute_target
            else:
                raise ConfigException("Compute_target needs to either be the str name of the compute target, or "
                                      "a ComputeTarget object.")
        else:
            self.compute_target = child_run._run_dto.get('target')

    def _inference(self, function_name, values, y_values=None):
        logger.info("Submitting inference job.")

        if not isinstance(values, AbstractDataset):
            raise ConfigException("Input for remote inferencing needs to be a Dataset.")

        with tempfile.TemporaryDirectory() as project_folder:
            with open(os.path.join(project_folder, PREDICT_INPUT_FILE), "wb+") as file:
                pickle.dump((values, y_values), file)

            run_configuration = RunConfiguration()

            script_run_id = self.run.parent.get_properties().get(SCRIPT_RUN_ID_PROPERTY)
            if script_run_id is None:
                env = self.run.get_environment()
            else:
                script_run = Run(self.run.experiment, script_run_id)
                env = script_run.get_environment()

            run_configuration.environment = env
            run_configuration.target = self.run._run_dto.get('target', 'local')

            # TODO, how to enable docker for local inference?
            # run_configuration.environment.docker.enabled = docker

            if self.compute_target is not None:
                run_configuration.target = self.compute_target

            package_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(package_dir, LOCAL_PREDICT_NAME)
            shutil.copy(script_path, os.path.join(project_folder, LOCAL_PREDICT_NAME))

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            inference_results_path = "{}_{}".format(self.run.id, timestamp)

            src = ScriptRunConfig(source_directory=project_folder,
                                  script=LOCAL_PREDICT_NAME,
                                  run_config=run_configuration,
                                  arguments=["--child_run_id", self.run.id,
                                             "--function_name", function_name,
                                             "--inference_results_path", inference_results_path])

            logger.info("Submitting script run for inferencing.")
            script_run = self.run.submit_child(src)

            logger.info("Waiting for script run for inferencing to complete.")
            script_run.wait_for_completion(show_output=False, wait_post_processing=True)

            logger.info("Inferencing complete.")
            datastore = self.run.experiment.workspace.get_default_datastore()
            returned_values = Dataset.Tabular.from_delimited_files(path=[(datastore, inference_results_path)])
            return returned_values

    def predict(self, values):
        """
        Submit a job to run predict on the model for the given values.

        :param values: Input test data to run predict on.
        :type values: AbstractDataset
        :return: The predicted values.
        """
        return self._inference(PREDICT, values)

    def predict_proba(self, values):
        """
        Submit a job to run predict_proba on the model for the given values.

        :param values: Input test data to run predict on.
        :type values: AbstractDataset
        :return: The predicted values.
        """
        return self._inference(PREDICT_PROBA, values)

    def forecast(self, X_values, y_values):
        """
        Submit a job to run forecast on the model for the given values.

        :param X_values: Input test data to run forecast on.
        :type X_values: AbstractDataset
        :param y_values: Input y values to run the forecast on.
        :type y_values: AbstractDataset
        :return: The forecast values.
        """
        return self._inference(FORECAST, X_values, y_values)
