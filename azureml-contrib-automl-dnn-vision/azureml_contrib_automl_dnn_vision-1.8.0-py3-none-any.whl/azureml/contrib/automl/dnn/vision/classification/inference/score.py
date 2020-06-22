# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""

import logging
import os
import json
import time
import torch
from azureml.contrib.automl.dnn.vision.common.dataloaders import RobustDataLoader
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.prediction_dataset import PredictionDataset
from azureml.contrib.dataset.labeled_dataset import _LabeledDatasetFactory
from azureml.core.experiment import Experiment
from azureml.core.run import Run
from ..common.constants import ArtifactsLiterals, PredictionLiterals, scoring_settings_defaults, \
    featurization_settings_defaults
from ...common.constants import SettingsLiterals
from ...common.utils import AverageMeter
from . import InferenceModelWrapper

logger = logging.getLogger(__name__)


def _get_labels_as_array(num_to_labels):
    num_labels = max(num_to_labels.keys()) + 1
    labels = [0] * num_labels
    for i in range(num_labels):
        labels[i] = num_to_labels[i]

    return labels


def _get_run(run_id, experiment_name=None):
    """Get a Run object

    :param run_id: run id of the run that produced the model
    :type run_id: str
    :param experiment_name: name of experiment that contained the run id
    :type experiment_name: str
    :return: Run object
    :rtype: Run
    """

    current_experiment = Run.get_context().experiment
    if experiment_name is None:
        experiment = current_experiment
    else:
        ws = current_experiment.workspace
        experiment = Experiment(ws, experiment_name)

    return Run(experiment=experiment, run_id=run_id)


def load_model_from_artifacts(run_id, experiment_name=None, artifacts_dir=None):
    """
    :param run_id: run id of the run that produced the model
    :type run_id: str
    :param experiment_name: name of experiment that contained the run id
    :type experiment_name: str
    :param artifacts_dir: artifacts directory
    :type artifacts_dir: str
    :return: InferenceModelWrapper object
    :rtype: inference.InferenceModelWrapper
    """
    if artifacts_dir is None:
        artifacts_dir = ArtifactsLiterals.OUTPUT_DIRECTORY

    run = _get_run(run_id, experiment_name)

    run.download_file(os.path.join(artifacts_dir, ArtifactsLiterals.MODEL_WRAPPER_PKL),
                      output_file_path=ArtifactsLiterals.MODEL_WRAPPER_PKL)

    return InferenceModelWrapper.load_serialized_inference_model_wrapper(ArtifactsLiterals.MODEL_WRAPPER_PKL)


def _write_prediction_file_line(fw, filename, prob, inference_model_wrapper):
    fw.write(
        json.dumps(
            {
                PredictionLiterals.FILENAME: filename,
                PredictionLiterals.PROBS: prob.cpu().numpy().tolist(),
                PredictionLiterals.LABELS: inference_model_wrapper.labels
            }
        )
    )
    fw.write('\n')


def _write_dataset_file_line(fw, file_name, prob, inference_model_wrapper):
    AmlLabeledDatasetHelper.write_dataset_file_line(
        fw,
        file_name,
        prob.cpu().numpy().tolist(),
        inference_model_wrapper.labels)


def _score_with_model(inference_model_wrapper, run, target_path, output_file=None,
                      root_dir=None, image_list_file=None, batch_size=80,
                      ignore_data_errors=True, labeled_dataset_factory=_LabeledDatasetFactory,
                      labeled_dataset_file="labeled_dataset.json",
                      input_dataset_id=None, always_create_dataset=False,
                      num_workers=None):
    if output_file is None:
        output_file = os.path.join(ArtifactsLiterals.OUTPUT_DIRECTORY, PredictionLiterals.PREDICTION_FILE_NAME)

    ws = run.experiment.workspace
    datastore = ws.get_default_datastore()

    model_wrapper = inference_model_wrapper.model_wrapper
    model_wrapper.model.eval()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_wrapper.model = model_wrapper.model.to(device)

    try:
        with open(output_file, 'w') as fw, open(labeled_dataset_file, "w") as ldsf:
            score_start = time.time()
            dataset = PredictionDataset(root_dir=root_dir, image_list_file=image_list_file,
                                        transforms=model_wrapper.transforms,
                                        ignore_data_errors=ignore_data_errors,
                                        input_dataset_id=input_dataset_id, ws=ws)
            dataloader = RobustDataLoader(dataset, batch_size=batch_size, drop_last=False,
                                          num_workers=num_workers)

            batch_time = AverageMeter()
            end = time.time()

            with torch.no_grad():
                for i, (filenames, batch) in enumerate(dataloader):
                    batch = batch.to(device)
                    outputs = model_wrapper.model(batch)
                    probs = model_wrapper.predict_proba_from_outputs(outputs)
                    for filename, prob in zip(filenames, probs):
                        _write_prediction_file_line(fw, filename, prob, inference_model_wrapper)
                        _write_dataset_file_line(ldsf, filename,
                                                 prob, inference_model_wrapper)

                    batch_time.update(time.time() - end)
                    end = time.time()
                    if i % 100 == 0 or i == len(dataloader) - 1:
                        mesg = "Epoch: [{0}/{1}]\t" "Time {batch_time.value:.4f}" \
                               " ({batch_time.avg:.4f})\t".format(i, len(dataloader), batch_time=batch_time)
                        logger.info(mesg)

            # measure total scoring time
            score_time = time.time() - score_start
            logger.info('Total scoring time {0:.4f}'.format(score_time))

        if always_create_dataset or input_dataset_id is not None:
            AmlLabeledDatasetHelper.create(run, datastore, labeled_dataset_file, target_path,
                                           'ImageClassification', labeled_dataset_factory)

    finally:
        os.remove(labeled_dataset_file)


def _featurize_with_model(inference_model_wrapper, run, output_file=None,
                          root_dir=None, image_list_file=None, batch_size=80,
                          ignore_data_errors=True, num_workers=None,
                          input_dataset_id=None):
    if output_file is None:
        output_file = os.path.join(ArtifactsLiterals.OUTPUT_DIRECTORY, PredictionLiterals.FEATURE_FILE_NAME)

    ws = run.experiment.workspace

    model_wrapper = inference_model_wrapper.model_wrapper
    model_wrapper.featurizer.eval()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_wrapper.model = model_wrapper.featurizer.to(device)

    with open(output_file, 'w') as fw:
        featurize_start = time.time()
        dataset = PredictionDataset(root_dir=root_dir, image_list_file=image_list_file,
                                    transforms=model_wrapper.transforms,
                                    ignore_data_errors=ignore_data_errors,
                                    input_dataset_id=input_dataset_id, ws=ws)

        dataloader = RobustDataLoader(dataset, batch_size=batch_size, drop_last=False,
                                      num_workers=num_workers)

        batch_time = AverageMeter()
        end = time.time()

        with torch.no_grad():
            for i, (filenames, batch) in enumerate(dataloader):
                batch = batch.to(device)
                features = model_wrapper.featurizer(batch).squeeze()
                # make sure we don't squeeze the batch dimension
                if len(features.shape) == 1:
                    features = features.unsqueeze(0)
                features = features.cpu().numpy()
                for filename, feat in zip(filenames, features):
                    fw.write(
                        json.dumps(
                            {
                                PredictionLiterals.FILENAME: filename,
                                PredictionLiterals.FEATURE_VECTOR: feat.tolist(),
                            }
                        )
                    )
                    fw.write('\n')

                batch_time.update(time.time() - end)
                end = time.time()
                if i % 100 == 0 or i == len(dataloader) - 1:
                    mesg = "Epoch: [{0}/{1}]\t" "Time {batch_time.value:.4f}" \
                           " ({batch_time.avg:.4f})\t".format(i, len(dataloader), batch_time=batch_time)
                    logger.info(mesg)

        # measure total scoring time
        featurize_time = time.time() - featurize_start
        logger.info('Total featurization time {0:.4f}'.format(featurize_time))


def featurize(run_id, experiment_name=None, output_file=None, root_dir=None, image_list_file=None, batch_size=80,
              ignore_data_errors=True, input_dataset_id=None):
    """Generate predictions from input files.

    :param run_id: azureml run id
    :type run_id: str
    :param experiment_name: name of experiment
    :type experiment_name: str
    :param output_file: path to output file
    :type output_file: str
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :param batch_size: batch size for prediction
    :type batch_size: int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    """
    logger.info("[start featurization: batch_size: {}]".format(batch_size))

    inference_model_wrapper = load_model_from_artifacts(run_id, experiment_name=experiment_name)
    run = Run.get_context()

    num_workers = scoring_settings_defaults[SettingsLiterals.NUM_WORKERS]

    _featurize_with_model(inference_model_wrapper, run, output_file=output_file, root_dir=root_dir,
                          image_list_file=image_list_file, batch_size=batch_size,
                          ignore_data_errors=ignore_data_errors, input_dataset_id=input_dataset_id,
                          num_workers=num_workers)


def score(run_id, experiment_name=None, output_file=None, root_dir=None, image_list_file=None, batch_size=80,
          ignore_data_errors=True, output_dataset_target_path=None, input_dataset_id=None):
    """Generate predictions from input files.

    :param run_id: azureml run id
    :type run_id: str
    :param experiment_name: name of experiment
    :type experiment_name: str
    :param output_file: path to output file
    :type output_file: str
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :param batch_size: batch size for prediction
    :type batch_size: int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dataset_target_path: path on Datastore for the output dataset files.
    :type output_dataset_target_path: str
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    """
    logger.info("[start inference: batch_size: {}]".format(batch_size))

    inference_model_wrapper = load_model_from_artifacts(run_id, experiment_name=experiment_name)
    run = Run.get_context()

    if output_dataset_target_path is None:
        output_dataset_target_path = AmlLabeledDatasetHelper.get_default_target_path()

    num_workers = featurization_settings_defaults[SettingsLiterals.NUM_WORKERS]

    _score_with_model(inference_model_wrapper, run, output_dataset_target_path, output_file=output_file,
                      root_dir=root_dir, image_list_file=image_list_file, batch_size=batch_size,
                      ignore_data_errors=ignore_data_errors, input_dataset_id=input_dataset_id,
                      num_workers=num_workers)
