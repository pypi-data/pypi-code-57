# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import pickle as pkl
from typing import Optional

import azureml.train.automl
from azureml.train.automl.constants import AUTOML_SETTINGS_PATH, AUTOML_FIT_PARAMS_PATH
from azureml.train.automl._azureautomlclient import AzureAutoMLClient
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.core import Run, Dataset, Workspace
from azureml.data.abstract_dataset import AbstractDataset


# Remove this once everything uses curated envs >= 1.6.0
# from azureml.train.automl.constants import _DataArgNames
class _DataArgNames:
    X = "X"
    y = "y"
    sample_weight = "sample_weight"
    X_valid = "X_valid"
    y_valid = "y_valid"
    sample_weight_valid = "sample_weight_valid"
    training_data = "training_data"
    validation_data = "validation_data"


def _get_dataset(workspace: Workspace, id: str) -> Optional[AbstractDataset]:
    try:
        return Dataset.get_by_id(workspace=workspace, id=id)
    except Exception:
        return None


if __name__ == '__main__':
    run = Run.get_context()

    parser = argparse.ArgumentParser()

    # the run id of he child run we want to inference
    parser.add_argument('--{}'.format(_DataArgNames.X), type=str,
                        dest=_DataArgNames.X)
    parser.add_argument('--{}'.format(_DataArgNames.y), type=str,
                        dest=_DataArgNames.y)
    parser.add_argument('--{}'.format(_DataArgNames.sample_weight), type=str,
                        dest=_DataArgNames.sample_weight)
    parser.add_argument('--{}'.format(_DataArgNames.X_valid), type=str,
                        dest=_DataArgNames.X_valid)
    parser.add_argument('--{}'.format(_DataArgNames.y_valid), type=str,
                        dest=_DataArgNames.y_valid)
    parser.add_argument('--{}'.format(_DataArgNames.sample_weight_valid), type=str,
                        dest=_DataArgNames.sample_weight_valid)
    parser.add_argument('--{}'.format(_DataArgNames.training_data), type=str,
                        dest=_DataArgNames.training_data)
    parser.add_argument('--{}'.format(_DataArgNames.validation_data), type=str,
                        dest=_DataArgNames.validation_data)

    args = parser.parse_args()

    with open(AUTOML_SETTINGS_PATH, 'rb+') as f:
        automl_setting = pkl.load(f)
    with open(AUTOML_FIT_PARAMS_PATH, 'rb+') as f:
        fit_params = pkl.load(f)

    experiment = run.experiment
    ws = experiment.workspace
    if "show_output" in automl_setting:
        del automl_setting["show_output"]
    if "show_output" in fit_params:
        del fit_params["show_output"]
    fit_params["_script_run"] = run

    fit_params[_DataArgNames.X] = _get_dataset(workspace=ws, id=args.X)
    fit_params[_DataArgNames.y] = _get_dataset(workspace=ws, id=args.y)
    fit_params[_DataArgNames.sample_weight] = _get_dataset(workspace=ws, id=args.sample_weight)
    fit_params[_DataArgNames.X_valid] = _get_dataset(workspace=ws, id=args.X_valid)
    fit_params[_DataArgNames.y_valid] = _get_dataset(workspace=ws, id=args.y_valid)
    fit_params[_DataArgNames.sample_weight_valid] = _get_dataset(workspace=ws, id=args.sample_weight_valid)
    fit_params[_DataArgNames.training_data] = _get_dataset(workspace=ws, id=args.training_data)
    fit_params[_DataArgNames.validation_data] = _get_dataset(workspace=ws, id=args.validation_data)

    settings = AzureAutoMLSettings(experiment, **automl_setting)
    automl_estimator = AzureAutoMLClient(experiment, settings)

    local_run = automl_estimator.fit(**fit_params)
