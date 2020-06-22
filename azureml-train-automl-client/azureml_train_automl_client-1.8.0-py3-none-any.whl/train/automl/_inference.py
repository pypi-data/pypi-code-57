# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import io
import logging
import os
import pickle as pkl
import sys
import tempfile

import azureml.train.automl
from azureml.core import Run
from azureml.core.dataset import Dataset
from azureml.train.automl._constants_azureml import MODEL_PATH
from azureml.automl.core.shared.exceptions import MemorylimitException

try:
    from azureml.train.automl.constants import LOCAL_MODEL_PATH, INFERENCE_OUTPUT, PREDICT_INPUT_FILE
except ImportError:
    PREDICT_INPUT_FILE = "predict.pkl"
    LOCAL_MODEL_PATH = "model.pkl"
    INFERENCE_OUTPUT = "inference.csv"

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("Starting inference run.")
    # pandas is only available on the remote compute, we don't want this imported in azureml-train-automl-client
    import pandas as pd

    run = Run.get_context()

    parser = argparse.ArgumentParser()

    # the run id of he child run we want to inference
    parser.add_argument('--child_run_id', type=str, dest='child_run_id')
    # Which function we want to use for inferencing, "predict", "forecast", or "predict_proba"
    parser.add_argument('--function_name', type=str, dest='function_name')
    # The Dataset path to upload the inference results to.
    parser.add_argument('--inference_results_path', type=str, dest='inference_results_path')

    args = parser.parse_args()

    logger.info("Running {} for run {}.".format(args.child_run_id, args.function_name))

    logger.info("Fetching model.")

    child_run = Run(run.experiment, args.child_run_id)

    child_run.download_file(name=MODEL_PATH, output_file_path=LOCAL_MODEL_PATH)

    logger.info("Loading model.")
    with open(LOCAL_MODEL_PATH, "rb") as model_file:
        fitted_model = pkl.load(model_file)

    try:
        logger.info("Fetching data.")
        with open(PREDICT_INPUT_FILE, "rb+") as file:
            (X_inputs, y_inputs) = pkl.load(file)

        X_inputs = X_inputs.to_pandas_dataframe()
        if y_inputs is not None:
            y_inputs = y_inputs.to_pandas_dataframe()
    except MemoryError as e:
        generic_msg = 'Failed to retrieve the data from the dataflow due to MemoryError'
        raise MemorylimitException.from_exception(e, msg=generic_msg, has_pii=False)

    logger.info("Inferencing.")
    inference_func = getattr(fitted_model, args.function_name)
    try:
        if y_inputs is None:
            results = inference_func(X_inputs)
        else:
            results = inference_func(X_inputs, y_inputs)
        results = pd.DataFrame(data=results)
    except MemoryError as e:
        generic_msg = 'Failed to {} due to MemoryError'.format(args.function_name)
        raise MemorylimitException.from_exception(e, msg=generic_msg, has_pii=False)
    except Exception as e:
        logger.info("Failed to inference the model.")
        raise

    with tempfile.TemporaryDirectory() as project_folder:
        target_path = "inference_results"
        results_data_fname = os.path.join(project_folder, INFERENCE_OUTPUT)

        results.to_csv(results_data_fname, index=False)

        logger.info("Uploading results to {}".format(args.inference_results_path))
        datastore = run.experiment.workspace.get_default_datastore()
        datastore.upload(src_dir=project_folder, target_path=args.inference_results_path, overwrite=True)
