# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""

import argparse
import logging
import os

from ..common.utils import _safe_exception_logging, _make_arg, \
    _merge_settings_args_defaults, _set_logging_parameters, \
    _set_random_seed
from .common.constants import TrainingLiterals, base_training_settings_defaults, \
    multiclass_training_settings_defaults, multilabel_training_settings_defaults
from .trainer.trainer import train_model
from .io.read.dataset_wrappers import AmlDatasetWrapper, \
    ImageFolderLabelFileDatasetWrapper
from .io.write.write_model import _write_model
from ..common.constants import SettingsLiterals
from ..common.exceptions import AutoMLVisionValidationException
from .common.utils import _gen_validfile_from_trainfile
from ..common.utils import _save_image_df

from azureml.train.automl import constants

from azureml.core.run import Run

azureml_run = Run.get_context()

logger = logging.getLogger(__name__)


def _get_train_valid_dataset_wrappers(root_dir, train_file=None, valid_file=None, multilabel=False,
                                      ignore_data_errors=True, settings=None):
    """
    :param root_dir: root directory that will be used as prefix for paths in train_file and valid_file
    :type root_dir: str
    :param train_file: labels file for training with filenames and labels
    :type train_file: str
    :param valid_file: labels file for validation with filenames and labels
    :type valid_file: str
    :param multilabel: boolean flag for whether its multilabel or not
    :type multilabel: bool
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param settings: dictionary containing settings for training
    :type settings: dict
    :return: tuple of train and validation dataset wrappers
    :rtype: tuple[BaseDatasetWrapper, BaseDatasetWrapper]
    """
    if valid_file is None:
        train_file, valid_file = _gen_validfile_from_trainfile(train_file,
                                                               val_size=settings[TrainingLiterals.TEST_RATIO],
                                                               output_dir=settings[SettingsLiterals.OUTPUT_DIR])

    train_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(root_dir=root_dir, input_file=train_file,
                                                               multilabel=multilabel,
                                                               ignore_data_errors=ignore_data_errors)
    valid_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(root_dir=root_dir, input_file=valid_file,
                                                               multilabel=multilabel,
                                                               all_labels=train_dataset_wrapper.labels,
                                                               ignore_data_errors=ignore_data_errors)

    return train_dataset_wrapper, valid_dataset_wrapper


@_safe_exception_logging
def run(automl_settings, multilabel=False):
    """Invoke training by passing settings and write the output model.

    :param automl_settings: dictionary with automl settings
    :type automl_settings: dict
    :param multilabel: boolean flag for multilabel
    :type multilabel: bool
    """

    settings = _parse_argument_settings(automl_settings, multilabel)

    task_type = constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION if multilabel \
        else constants.Tasks.IMAGE_CLASSIFICATION
    _set_logging_parameters(task_type, settings)

    # TODO JEDI
    # This is ok to log now because it can only be system metadata. When we expose the package to customers
    # we need to revisit.
    logger.debug("Final settings: \n {}".format(settings))

    # set multilabel flag in settings
    settings[SettingsLiterals.MULTILABEL] = multilabel
    labels_file = settings.get(SettingsLiterals.LABELS_FILE, None)
    validation_labels_file = settings.get(SettingsLiterals.VALIDATION_LABELS_FILE, None)
    image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)
    output_dir = settings[SettingsLiterals.OUTPUT_DIR]
    device = settings[SettingsLiterals.DEVICE]
    ignore_data_errors = settings[SettingsLiterals.IGNORE_DATA_ERRORS]
    labels_path = None
    validation_labels_path = None

    # set randomization seed for deterministic training
    _set_random_seed(settings.get(SettingsLiterals.RANDOM_SEED, None))

    if dataset_id is not None:
        ws = Run.get_context().experiment.workspace
        train_dataset_wrapper = AmlDatasetWrapper(dataset_id, multilabel=multilabel, workspace=ws)
        if validation_dataset_id is None:
            train_dataset_wrapper, valid_dataset_wrapper = train_dataset_wrapper.train_val_split()
        else:
            valid_dataset_wrapper = AmlDatasetWrapper(validation_dataset_id, multilabel=multilabel, workspace=ws)

        _save_image_df(train_df=train_dataset_wrapper._images_df, val_df=valid_dataset_wrapper._images_df,
                       output_dir=output_dir)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        if labels_file is None and image_folder is None:
            raise AutoMLVisionValidationException("Neither images_folder or labels_file found in automl settings",
                                                  has_pii=False)

        if labels_file is not None:
            labels_path = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], labels_file)
        if validation_labels_file is not None:
            validation_labels_path = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], validation_labels_file)

        image_folder_path = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        train_dataset_wrapper, valid_dataset_wrapper = _get_train_valid_dataset_wrappers(
            root_dir=image_folder_path, train_file=labels_path, valid_file=validation_labels_path,
            multilabel=multilabel, ignore_data_errors=ignore_data_errors, settings=settings
        )

    if valid_dataset_wrapper.labels != train_dataset_wrapper.labels:
        all_labels = list(set(valid_dataset_wrapper.labels + train_dataset_wrapper.labels))
        train_dataset_wrapper.reset_labels(all_labels)
        valid_dataset_wrapper.reset_labels(all_labels)

    logger.info("# train images: {}, # validation images: {}, # labels: {}".format(
        len(train_dataset_wrapper), len(valid_dataset_wrapper), train_dataset_wrapper.num_classes))

    best_model = train_model(settings[TrainingLiterals.MODEL_NAME], strategy=settings[TrainingLiterals.STRATEGY],
                             dataset_wrapper=train_dataset_wrapper, settings=settings,
                             valid_dataset=valid_dataset_wrapper, device=device, azureml_run=azureml_run)

    _write_model(best_model, labels=train_dataset_wrapper.labels, output_dir=output_dir, device=device,
                 train_datafile=labels_path, val_datafile=validation_labels_path)

    folder_name = os.path.basename(output_dir)
    azureml_run.upload_folder(name=folder_name, path=output_dir)


def _parse_argument_settings(automl_settings, multilabel):
    """Parse all arguments and merge settings

    :param automl_settings: dictionary with automl settings
    :type automl_settings: dict
    :param multilabel: boolean flag for multilabel
    :type multilabel: bool
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """

    training_settings_defaults = base_training_settings_defaults
    if multilabel:
        training_settings_defaults.update(multilabel_training_settings_defaults)
    else:
        training_settings_defaults.update(multiclass_training_settings_defaults)

    parser = argparse.ArgumentParser(description="cluster images")
    parser.add_argument(_make_arg(TrainingLiterals.MODEL_NAME), type=str,
                        default=training_settings_defaults[TrainingLiterals.MODEL_NAME],
                        help="model name.")
    parser.add_argument(_make_arg(TrainingLiterals.STRATEGY), type=str,
                        default=training_settings_defaults[TrainingLiterals.STRATEGY])
    parser.add_argument(_make_arg(TrainingLiterals.BATCH_SIZE), type=int,
                        default=training_settings_defaults[TrainingLiterals.BATCH_SIZE],
                        help="batch size to use")
    # Data args
    parser.add_argument(_make_arg(SettingsLiterals.DATA_FOLDER),
                        _make_arg(SettingsLiterals.DATA_FOLDER.replace("_", "-")),
                        type=str,
                        default=training_settings_defaults[SettingsLiterals.DATA_FOLDER],
                        help="root of the blob store")
    parser.add_argument(_make_arg(SettingsLiterals.LABELS_FILE_ROOT),
                        _make_arg(SettingsLiterals.LABELS_FILE_ROOT.replace("_", "-")), type=str,
                        default=training_settings_defaults[SettingsLiterals.LABELS_FILE_ROOT],
                        help="root relative to which label file paths exist")

    args = parser.parse_args()

    return _merge_settings_args_defaults(automl_settings, args, training_settings_defaults)
