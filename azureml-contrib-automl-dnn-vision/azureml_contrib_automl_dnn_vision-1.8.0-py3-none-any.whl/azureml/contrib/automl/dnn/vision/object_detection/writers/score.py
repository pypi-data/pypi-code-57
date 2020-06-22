# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions for inference using a trained model"""

import logging
import os
import pickle
import json
import time
from torchvision.transforms import functional
import torch

from ..common.constants import ArtifactLiterals, ScoringParameters
from ...common.utils import AverageMeter
from ..data.loaders import _collate_function
from ..trainer.train import move_images_to_device
from azureml.contrib.automl.dnn.vision.common.utils import _data_exception_safe_iterator
from azureml.contrib.automl.dnn.vision.common.dataloaders import RobustDataLoader
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.prediction_dataset import PredictionDataset
from azureml.contrib.dataset.labeled_dataset import _LabeledDatasetFactory
from azureml.core.experiment import Experiment
from azureml.core.run import Run

logger = logging.getLogger(__name__)


def _load_model_wrapper(torch_model_file, model_wrapper_pkl, **model_settings):
    with open(model_wrapper_pkl, 'rb') as fp:
        model_wrapper = pickle.load(fp)

    model_weights = torch.load(torch_model_file)
    model_wrapper.restore_model(model_weights, **model_settings)

    return model_wrapper


def _fetch_model_from_artifacts(run_id, experiment_name=None, **model_settings):
    current_experiment = Run.get_context().experiment

    if experiment_name is None:
        experiment = current_experiment
    else:
        workspace = current_experiment.workspace
        experiment = Experiment(workspace, experiment_name)

    run = Run(experiment=experiment, run_id=run_id)

    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.MODEL_FILE_NAME),
                      ArtifactLiterals.MODEL_FILE_NAME)
    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.PICKLE_FILE_NAME),
                      ArtifactLiterals.PICKLE_FILE_NAME)

    return _load_model_wrapper(ArtifactLiterals.MODEL_FILE_NAME, ArtifactLiterals.PICKLE_FILE_NAME,
                               **model_settings)


def _test_fetch_model(model_file, model_wrapper_pkl):
    return _load_model_wrapper(model_file, model_wrapper_pkl)


def _get_box_dims(image, box):
    box_keys = ['topX', 'topY', 'bottomX', 'bottomY']
    _, height, width = image.shape

    box_dims = dict(zip(box_keys, [coordinate.item() for coordinate in box]))

    box_dims['topX'] = box_dims['topX'] * 1.0 / width
    box_dims['bottomX'] = box_dims['bottomX'] * 1.0 / width
    box_dims['topY'] = box_dims['topY'] * 1.0 / height
    box_dims['bottomY'] = box_dims['bottomY'] * 1.0 / height

    return box_dims


def _write_prediction_file_line(fw, filename, label, image, classes):
    bounding_boxes = []
    for box, label_index, score in zip(label['boxes'], label['labels'], label['scores']):

        box_dims = _get_box_dims(image, box)

        box_record = {'box': box_dims,
                      'label': classes[label_index],
                      'score': score.item()}

        bounding_boxes.append(box_record)

    annotation = {'filename': filename,
                  'boxes': bounding_boxes}

    fw.write('{}\n'.format(json.dumps(annotation)))


def _write_dataset_file_line(fw, filename, label, image, classes):
    labels = []
    scores = []
    for box, label_index, score in zip(label['boxes'], label['labels'], label['scores']):
        label_record = _get_box_dims(image, box)
        label_record['label'] = classes[label_index]

        labels.append(label_record)
        scores.append(score.item())

    AmlLabeledDatasetHelper.write_dataset_file_line(
        fw,
        filename,
        scores,
        labels)


def _score_with_model(model_wrapper, run, target_path, output_file, root_dir,
                      image_list_file, batch_size=1,
                      ignore_data_errors=True,
                      labeled_dataset_factory=_LabeledDatasetFactory,
                      labeled_dataset_file="labeled_dataset.json",
                      input_dataset_id=None, always_create_dataset=False,
                      num_workers=None):

    ws = run.experiment.workspace
    datastore = ws.get_default_datastore()

    model = model_wrapper.model
    classes = model_wrapper.classes
    model.eval()

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model.to(device)

    score_start = time.time()
    dataset = PredictionDataset(root_dir=root_dir, image_list_file=image_list_file,
                                transforms=functional.to_tensor,
                                ignore_data_errors=ignore_data_errors,
                                input_dataset_id=input_dataset_id, ws=ws)

    dataloader = RobustDataLoader(dataset, batch_size=batch_size, collate_fn=_collate_function,
                                  num_workers=num_workers)

    batch_time = AverageMeter()
    end = time.time()

    with torch.no_grad():
        try:
            with open(output_file, "w") as fw, open(labeled_dataset_file, "w") as ldsf:
                for i, (filenames, image_batch) in enumerate(_data_exception_safe_iterator(iter(dataloader))):
                    image_batch = move_images_to_device(image_batch, device)
                    labels = model(image_batch)

                    for filename, label, image in zip(filenames, labels, image_batch):
                        _write_prediction_file_line(fw, filename, label, image, classes)
                        _write_dataset_file_line(ldsf, filename,
                                                 label, image, classes)

                    batch_time.update(time.time() - end)
                    end = time.time()
                    if i % 100 == 0 or i == len(dataloader) - 1:
                        mesg = "Epoch: [{0}/{1}]\t" "Time {batch_time.value:.4f}" \
                               " ({batch_time.avg:.4f})\t".format(i, len(dataloader), batch_time=batch_time)
                        logger.info(mesg)

            if always_create_dataset or input_dataset_id is not None:
                AmlLabeledDatasetHelper.create(run, datastore, labeled_dataset_file, target_path,
                                               'ObjectDetection', labeled_dataset_factory)

        finally:
            os.remove(labeled_dataset_file)

    # measure total scoring time
    score_time = time.time() - score_start
    logger.info('Total scoring time {0:.4f}'.format(score_time))


def score(run_id, experiment_name=None, output_file=None, root_dir=None, image_list_file=None, batch_size=1,
          ignore_data_errors=True, output_dataset_target_path=None, input_dataset_id=None, **model_settings):
    """Load model and infer on new data.

    :param run_id: Name of the run to load model from
    :type run_id: String
    :param experiment_name: Name of experiment to load model from
    :type experiment_name: String
    :param output_file: Name of file to write results to
    :type output_file: String
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :batch_size: Inference batch size
    :type batch_size: Int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dataset_target_path: path on Datastore for the output dataset files.
    :type output_dataset_target_path: str
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    :param model_settings: Optional keyword arguments to define model specifications
    :type model_settings: Dictionary
    """
    logger.info("[start prediction: batch_size: {}]".format(batch_size))

    model_wrapper = _fetch_model_from_artifacts(run_id, experiment_name, **model_settings)

    run = Run.get_context()

    if output_dataset_target_path is None:
        output_dataset_target_path = AmlLabeledDatasetHelper.get_default_target_path()

    num_workers = ScoringParameters.DEFAULT_NUM_WORKERS

    _score_with_model(model_wrapper, run, output_dataset_target_path, output_file=output_file,
                      root_dir=root_dir, image_list_file=image_list_file,
                      batch_size=batch_size, ignore_data_errors=ignore_data_errors,
                      input_dataset_id=input_dataset_id, num_workers=num_workers)


def _score_from_files(weights_file, wrapper_file, output_file, root_dir, image_list_file, batch_size,
                      ignore_data_errors=True):

    model_wrapper = _test_fetch_model(weights_file, wrapper_file)
    _score_with_model(model_wrapper, output_file=output_file, root_dir=root_dir, image_list_file=image_list_file,
                      batch_size=batch_size, ignore_data_errors=ignore_data_errors)
