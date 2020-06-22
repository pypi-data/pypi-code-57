# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""

import argparse
import logging
import os
import torch

from azureml.automl.core.shared.exceptions import ClientException
from azureml.contrib.automl.dnn.vision.common.utils import _safe_exception_logging, \
    _merge_settings_args_defaults, _make_arg, _save_image_df, _save_od_image_files, _set_random_seed

from azureml.train.automl import constants
from azureml.contrib.automl.dnn.vision.common.utils import _set_logging_parameters
from .data import datasets, loaders
from .models import detection
from .trainer import optimize, lrschedule, criterion, train
from .eval import cocotools, vocmap
from .writers import modelsaver
from .common.constants import TrainingParameters, LearningParameters, SchedulerParameters, \
    ArtifactLiterals, training_settings_defaults, TrainingLiterals, FasterRCNNLiterals, FasterRCNNParameters
from ..common.constants import SettingsLiterals

from azureml.core.run import Run

azureml_run = Run.get_context()

logger = logging.getLogger(__name__)


def read_aml_dataset(dataset_id, validation_dataset_id, ignore_data_errors, output_dir):
    """Read the training and validation datasets from AML datasets.

    :param dataset_id: Training dataset id
    :type dataset_id: str
    :param validation_dataset_id: Validation dataset id
    :type dataset_id: str
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (AmlDatasetObjectDetectionWrapper, AmlDatasetObjectDetectionWrapper)
    """
    ws = Run.get_context().experiment.workspace
    if validation_dataset_id is not None:
        training_dataset = datasets.AmlDatasetObjectDetectionWrapper(dataset_id, is_train=True,
                                                                     ignore_data_errors=ignore_data_errors,
                                                                     workspace=ws)
        validation_dataset = datasets.AmlDatasetObjectDetectionWrapper(validation_dataset_id, is_train=False,
                                                                       ignore_data_errors=ignore_data_errors,
                                                                       workspace=ws)
        _save_image_df(train_df=training_dataset.get_images_df(),
                       val_df=validation_dataset.get_images_df(),
                       output_dir=output_dir)

    else:
        dataset = datasets.AmlDatasetObjectDetectionWrapper(dataset_id, is_train=True,
                                                            ignore_data_errors=ignore_data_errors,
                                                            workspace=ws)
        training_dataset, validation_dataset = dataset.train_val_split()
        _save_image_df(train_df=dataset.get_images_df(), train_index=training_dataset._indices,
                       val_index=validation_dataset._indices, output_dir=output_dir)

    return training_dataset, validation_dataset


def read_file_dataset(image_folder, annotations_file, annotations_test_file, ignore_data_errors, output_dir):
    """Read the training and validation datasets from annotation files.

    :param image_folder: target image path
    :type image_folder: str
    :param annotations_file: Training annotations file
    :type annotations_file: str
    :param annotations_test_file: Validation annotations file
    :type annotations_test_file: str
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (FileObjectDetectionDatasetWrapper, FileObjectDetectionDatasetWrapper)
    """
    if image_folder is None:
        raise ClientException("images_folder or dataset_id needs to be specified", has_pii=False)

    if annotations_file is None:
        raise ClientException("labels_file needs to be specified", has_pii=False)

    if annotations_test_file:
        training_dataset = datasets.FileObjectDetectionDatasetWrapper(annotations_file, image_folder,
                                                                      is_train=True,
                                                                      ignore_data_errors=ignore_data_errors)
        validation_dataset = datasets.FileObjectDetectionDatasetWrapper(annotations_test_file,
                                                                        image_folder, is_train=False,
                                                                        ignore_data_errors=ignore_data_errors)
    else:
        dataset = datasets.FileObjectDetectionDatasetWrapper(annotations_file, image_folder, is_train=True,
                                                             ignore_data_errors=ignore_data_errors)
        training_dataset, validation_dataset = dataset.train_val_split()
        _save_od_image_files(train_ds=training_dataset, val_ds=validation_dataset, output_dir=output_dir)

    return training_dataset, validation_dataset


@_safe_exception_logging
def run(automl_settings):
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    """

    settings = _parse_argument_settings(automl_settings)

    task_type = constants.Tasks.IMAGE_OBJECT_DETECTION
    _set_logging_parameters(task_type, settings)

    # TODO JEDI
    # This is ok to log now because it can only be system metadata. When we expose the package to customers
    # we need to revisit.
    logger.debug("Final settings: \n {}".format(settings))

    model_name = settings[TrainingLiterals.MODEL_NAME]
    device = settings[SettingsLiterals.DEVICE]

    training_settings = {"number_of_epochs": settings[TrainingLiterals.NUMBER_OF_EPOCHS],
                         "lr": settings[TrainingLiterals.LEARNING_RATE],
                         "momentum": settings[TrainingLiterals.MOMENTUM],
                         "weight_decay": settings[TrainingLiterals.WEIGHT_DECAY],
                         "step_size": settings[TrainingLiterals.STEP_SIZE],
                         "gamma": settings[TrainingLiterals.GAMMA],
                         "max_patience_iterations": settings[TrainingLiterals.MAX_PATIENCE_ITERATIONS],
                         "primary_metric": settings[TrainingLiterals.PRIMARY_METRIC],
                         "enable_coco_validation": settings[TrainingLiterals.ENABLE_COCO_VALIDATION]}

    fasterrcnn_settings = {"min_size": settings[FasterRCNNLiterals.MIN_SIZE],
                           "box_score_thresh": settings[FasterRCNNLiterals.BOX_SCORE_THRESH],
                           "box_nms_thresh": settings[FasterRCNNLiterals.BOX_NMS_THRESH],
                           "box_detections_per_img": settings[FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG]}

    # Set dataloaders' num_workers
    num_workers = settings.get(SettingsLiterals.NUM_WORKERS, None)

    train_data_loader_settings = {"batch_size": settings[TrainingLiterals.TRAINING_BATCH_SIZE],
                                  "shuffle": True,
                                  "num_workers": num_workers}

    validation_data_loader_settings = {"batch_size": settings[TrainingLiterals.VALIDATION_BATCH_SIZE],
                                       "shuffle": False,
                                       "num_workers": num_workers}

    # Set randomization seed for deterministic training

    _set_random_seed(settings.get(SettingsLiterals.RANDOM_SEED, None))

    # Extract Automl Settings

    image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)

    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    annotations_file = settings.get(SettingsLiterals.LABELS_FILE, None)
    if annotations_file is not None:
        annotations_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], annotations_file)

    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    output_directory = ArtifactLiterals.OUTPUT_DIR
    annotations_test_file = None
    resume_file = settings.get(SettingsLiterals.RESUME, None)

    if SettingsLiterals.VALIDATION_LABELS_FILE in settings:
        annotations_test_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT],
                                             settings[SettingsLiterals.VALIDATION_LABELS_FILE])

    # Setup Dataset

    if dataset_id is not None:
        training_dataset, validation_dataset = read_aml_dataset(dataset_id,
                                                                validation_dataset_id,
                                                                ignore_data_errors,
                                                                output_directory)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        if image_folder is None:
            raise ClientException("Image folder path needs to be specified", has_pii=False)
        else:
            image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        training_dataset, validation_dataset = read_file_dataset(image_folder,
                                                                 annotations_file,
                                                                 annotations_test_file,
                                                                 ignore_data_errors,
                                                                 output_directory)

    if training_dataset.classes != validation_dataset.classes:
        all_classes = list(set(training_dataset.classes + validation_dataset.classes))
        training_dataset.reset_classes(all_classes)
        validation_dataset.reset_classes(all_classes)

    logger.info("# train images: {}, # validation images: {}, # labels: {}".format(
        len(training_dataset), len(validation_dataset), training_dataset.num_classes - 1))  # excluding "--bg--" class

    # Setup Model

    model = detection.setup_model(model_name=model_name, number_of_classes=training_dataset.num_classes,
                                  **fasterrcnn_settings)
    # TODO: Both classes and device should not be set here but in initialization
    model.classes = training_dataset.classes
    model.device = device

    num_params = sum([p.data.nelement() for p in model.parameters()])
    logger.info("[model: {}, #param: {}]".format(model_name, num_params))

    # Resume

    if resume_file:
        checkpoint = torch.load(resume_file, map_location="cpu")
        model.model.load_state_dict(checkpoint)

    # Setup Optimizer

    optimizer = optimize.setup_optimizer(model, **training_settings)
    lr_scheduler = lrschedule.setup_lr_scheduler(
        optimizer, **training_settings)
    loss_function = criterion.setup_criterion("FASTER_RCNN")

    # Setup Dataloaders

    train_loader = loaders.setup_dataloader(
        training_dataset, **train_data_loader_settings)
    validation_loader = loaders.setup_dataloader(
        validation_dataset, **validation_data_loader_settings)

    # Setup Evaluation Tools

    coco_index = None
    if training_settings["enable_coco_validation"]:
        coco_index = cocotools.create_coco_index(validation_dataset)
    val_vocmap = vocmap.VocMap(validation_dataset)

    # Train Model

    train_settings = train.TrainSettings(**training_settings)
    logger.info("[start training: train batch_size: {}, val batch_size: {}, train_settings {}]".format(
        train_data_loader_settings["batch_size"], validation_data_loader_settings["batch_size"], vars(train_settings)))

    train.train(model=model,
                optimizer=optimizer,
                scheduler=lr_scheduler,
                train_data_loader=train_loader,
                device=device,
                criterion=loss_function,
                train_settings=train_settings,
                val_data_loader=validation_loader,
                val_coco_index=coco_index,
                val_vocmap=val_vocmap,
                enable_coco_validation=training_settings["enable_coco_validation"],
                val_index_map=model.classes,
                run=azureml_run,
                ignore_data_errors=ignore_data_errors)

    # Save Model

    modelsaver.write_model(model, labels=training_dataset.classes, output_dir=output_directory, device=device,
                           train_datafile=annotations_file, val_datafile=annotations_test_file)

    folder_name = os.path.basename(output_directory)
    if azureml_run is not None:
        azureml_run.upload_folder(name=folder_name, path=output_directory)


def _parse_argument_settings(automl_settings):
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description="Object detection")

    # Model and Device Settings

    parser.add_argument(_make_arg(TrainingLiterals.MODEL_NAME), type=str,
                        help="model_name",
                        default=training_settings_defaults[TrainingLiterals.MODEL_NAME])

    parser.add_argument(_make_arg(SettingsLiterals.DEVICE), type=str,
                        help="Device to train on (cpu/cuda:0/cuda:1,...)",
                        default=training_settings_defaults[SettingsLiterals.DEVICE])

    # Training Related Settings

    parser.add_argument(_make_arg(TrainingLiterals.NUMBER_OF_EPOCHS), type=int,
                        help="number of training epochs",
                        default=TrainingParameters.DEFAULT_NUMBER_EPOCHS)
    parser.add_argument(_make_arg(TrainingLiterals.MAX_PATIENCE_ITERATIONS), type=int,
                        help="max number of epochs with no validation improvement",
                        default=TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
    parser.add_argument(_make_arg(TrainingLiterals.ENABLE_COCO_VALIDATION),
                        help="enable coco validation and evaluation", action="store_true")

    parser.add_argument(_make_arg(TrainingLiterals.LEARNING_RATE), type=float,
                        help="learning rate for optimizer",
                        default=LearningParameters.SGD_DEFAULT_LEARNING_RATE)
    parser.add_argument(_make_arg(TrainingLiterals.MOMENTUM), type=float,
                        help="momentum for optimizer",
                        default=LearningParameters.SGD_DEFAULT_MOMENTUM)
    parser.add_argument(_make_arg(TrainingLiterals.WEIGHT_DECAY), type=float,
                        help="optimizer weight decay",
                        default=LearningParameters.SGD_DEFAULT_WEIGHT_DECAY)

    parser.add_argument(_make_arg(TrainingLiterals.STEP_SIZE), type=int,
                        help="step size for learning rate scheduler",
                        default=SchedulerParameters.DEFAULT_STEP_LR_STEP_SIZE)
    parser.add_argument(_make_arg(TrainingLiterals.GAMMA), type=float,
                        help="decay rate for learning rate scheduler",
                        default=SchedulerParameters.DEFAULT_STEP_LR_GAMMA)

    # Faster-rcnn Settings

    parser.add_argument(_make_arg(FasterRCNNLiterals.MIN_SIZE), type=int,
                        help="minimum size of the image to be rescaled before feeding it to the backbone",
                        default=FasterRCNNParameters.DEFAULT_MIN_SIZE)
    parser.add_argument(_make_arg(FasterRCNNLiterals.BOX_SCORE_THRESH), type=float,
                        help="during inference, only return proposals with a classification score \
                        greater than box_score_thresh",
                        default=FasterRCNNParameters.DEFAULT_BOX_SCORE_THRESH)
    parser.add_argument(_make_arg(FasterRCNNLiterals.BOX_NMS_THRESH), type=float,
                        help="NMS threshold for the prediction head. Used during inference",
                        default=FasterRCNNParameters.DEFAULT_BOX_NMS_THRESH)
    parser.add_argument(_make_arg(FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG), type=int,
                        help="maximum number of detections per image, for all classes.",
                        default=FasterRCNNParameters.DEFAULT_BOX_DETECTIONS_PER_IMG)

    # Dataloader Settings

    parser.add_argument(_make_arg(TrainingLiterals.TRAINING_BATCH_SIZE), type=int,
                        help="training batch size",
                        default=TrainingParameters.DEFAULT_TRAINING_BATCH_SIZE)

    parser.add_argument(_make_arg(TrainingLiterals.VALIDATION_BATCH_SIZE), type=int,
                        help="validation batch size",
                        default=TrainingParameters.DEFAULT_VALIDATION_BATCH_SIZE)

    parser.add_argument(_make_arg(SettingsLiterals.DATA_FOLDER),
                        _make_arg(SettingsLiterals.DATA_FOLDER.replace("_", "-")),
                        type=str,
                        help="root of the blob store",
                        default="")

    parser.add_argument(_make_arg(SettingsLiterals.LABELS_FILE_ROOT),
                        _make_arg(SettingsLiterals.LABELS_FILE_ROOT.replace("_", "-")),
                        type=str,
                        help="root relative to which label file paths exist",
                        default="")

    # Extract Commandline Settings

    script_args = parser.parse_args()

    return _merge_settings_args_defaults(automl_settings, script_args, training_settings_defaults)
