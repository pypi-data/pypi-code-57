# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common utilities across classification and object detection."""
import functools
import logging
import os
import statistics
import sys
import json
from argparse import Namespace
from typing import Optional
import random

import numpy as np
import torch
import pynvml

from typing import Dict
from PIL import Image

from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.logging_fields import TELEMETRY_AUTOML_COMPONENT_KEY
from azureml.automl.core.shared.exceptions import ClientException

from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException

from azureml.telemetry import get_diagnostics_collection_info, INSTRUMENTATION_KEY
from azureml.train.automl._logging import set_run_custom_dimensions
from azureml.train.automl.constants import ComputeTargets
from azureml.train.automl import constants

from azureml.core.run import Run, _OfflineRun

from .constants import RunPropertyLiterals, SystemSettings
from ..classification.common.constants import LoggingLiterals


logger = logging.getLogger(__name__)


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        """reset self params to zero"""
        self.val = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        """Update total sum and count for the meter

        :param val: current value
        :type val: Float
        :param n: Count
        :type n: Int
        """
        self.val = val
        self.sum += val * n
        self.count += n

    @property
    def avg(self):
        """Get average values

        :return: Average Value
        :rtype: Float
        """
        return self.sum / self.count

    @property
    def value(self):
        """Get current values

        :return: Current Value
        :rtype: Float
        """
        return self.val


def _accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def _add_run_properties(run, best_metric):
    if run is None:
        raise ClientException('run is None', has_pii=False)
    properties_to_add = {RunPropertyLiterals.PIPELINE_SCORE: best_metric}
    run.add_properties(properties_to_add)


class AzureAutoMLSettingsStub:
    """Stub for AzureAutoMLSettings class to configure logging."""

    is_timeseries = False
    task_type = None
    compute_target = None
    name = None
    subscription_id = None
    region = None
    verbosity = None
    telemetry_verbosity = None
    send_telemetry = None
    azure_service = None


def _set_logging_parameters(task_type: constants.Tasks,
                            settings: Dict,
                            output_dir: Optional[str] = None,
                            azureml_run: Optional[Run] = None):
    """ Sets the logging parameters so that we can track all the training runs from
    a given project.

    :param task_type: The task type for the run.
    :type task_type: constants.Tasks
    :param settings: All the settings for this run.
    :type settings: Dict
    :output_dir: The output directory.
    :type Optional[str]
    :azureml_run: The run object.
    :type Optional[Run]
    """

    log_server.update_custom_dimensions({LoggingLiterals.TASK_TYPE: task_type})

    if LoggingLiterals.PROJECT_ID in settings:
        project_id = settings[LoggingLiterals.PROJECT_ID]
        log_server.update_custom_dimensions({LoggingLiterals.PROJECT_ID: project_id})

    if LoggingLiterals.VERSION_NUMBER in settings:
        version_number = settings[LoggingLiterals.VERSION_NUMBER]
        log_server.update_custom_dimensions({LoggingLiterals.VERSION_NUMBER: version_number})

    _set_automl_run_custom_dimensions(output_dir, azureml_run)


def _set_automl_run_custom_dimensions(output_dir: Optional[str] = None, azureml_run: Optional[Run] = None):
    if output_dir is None:
        output_dir = SystemSettings.LOG_FOLDER
    os.makedirs(output_dir, exist_ok=True)

    if azureml_run is None:
        azureml_run = Run.get_context()

    name = "not_available_offline"
    subscription_id = "not_available_offline"
    region = "not_available_offline"
    parent_run_id = "not_available_offline"
    child_run_id = "not_available_offline"
    if not isinstance(azureml_run, _OfflineRun):
        # If needed in the future, we can replace with a uuid5 based off the experiment name
        # name = azureml_run.experiment.name
        name = "online_scrubbed_for_compliance"
        subscription_id = azureml_run.experiment.workspace.subscription_id
        region = azureml_run.experiment.workspace.location
        parent_run_id = azureml_run.parent.id if azureml_run.parent is not None else None
        child_run_id = azureml_run.id

    # Build the automl settings expected by the logger
    send_telemetry, level = get_diagnostics_collection_info(component_name=TELEMETRY_AUTOML_COMPONENT_KEY)
    automl_settings = AzureAutoMLSettingsStub
    automl_settings.is_timeseries = False
    automl_settings.task_type = constants.Tasks.ALL_IMAGE  # This will be overwritten by each task's runner
    automl_settings.compute_target = ComputeTargets.AMLCOMPUTE
    automl_settings.name = name
    automl_settings.subscription_id = subscription_id
    automl_settings.region = region
    automl_settings.verbosity = logging.DEBUG
    automl_settings.telemetry_verbosity = level
    automl_settings.send_telemetry = send_telemetry

    log_server.set_log_file(os.path.join(output_dir, SystemSettings.LOG_FILENAME))
    if send_telemetry:
        log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity(level)

    set_run_custom_dimensions(
        automl_settings=automl_settings,
        parent_run_id=parent_run_id,
        child_run_id=child_run_id)

    # Add console handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    log_server.add_handler('stdout', stdout_handler)


def _get_gpu_usage(mem_usage_accumulator=None, gpu_usage_accumulator=None):
    """Returns a string with GPU usage.

    :param mem_usage_accumulator: if not None, use it to accumulate mem usage values over time.
    :type mem_usage_accumulator: Dict
    :param gpu_usage_accumulator: if not None, use it to accumulate gpu usage values over time.
    :type gpu_usage_accumulator: Dict
    :return:
    """
    _megabyte = 1024.0 * 1024.0
    pynvml.nvmlInit()
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        usage_str = "GPU info:"
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            utilization_rates = pynvml.nvmlDeviceGetUtilizationRates(handle)

            mem_total = "{0:.2f}".format(mem_info.total / _megabyte)
            mem_free = "{0:.2f}".format(mem_info.free / _megabyte)
            mem_used = "{0:.2f}".format(mem_info.used / _megabyte)
            usage_str += "{}:  Mem (MB): mem_info_total={}, mem_info_free={}, mem_info_used={}, " \
                         "gpu_utilization={}%".format(pynvml.nvmlDeviceGetName(handle),
                                                      mem_total, mem_free, mem_used,
                                                      utilization_rates.gpu)
            if mem_usage_accumulator is not None:
                mem_usage_accumulator[i] = mem_usage_accumulator.get(i, {})
                mem_info_key = "mem_info_used"
                mem_usage_accumulator[i][mem_info_key] = mem_usage_accumulator[i].get(
                    mem_info_key, []) + [mem_info.used]
                usage_str += ", avg_mem_info_used={0:.2f}. ".format(statistics.mean(
                    mem_usage_accumulator[i][mem_info_key]) / _megabyte)
            if gpu_usage_accumulator is not None:
                gpu_usage_accumulator[i] = gpu_usage_accumulator.get(i, {})
                gpu_usage_key = "gpu_utilization"
                gpu_usage_accumulator[i][gpu_usage_key] = gpu_usage_accumulator[i].get(
                    gpu_usage_key, []) + [utilization_rates.gpu]
                usage_str += ", avg_gpu_utilization={}%. ".format(statistics.mean(
                    gpu_usage_accumulator[i][gpu_usage_key]))
        return usage_str + "\n"
    except pynvml.NVMLError as error:
        return str(error)
    finally:
        pynvml.nvmlShutdown()


def _data_exception_safe_iterator(iterator):
    while True:
        try:
            yield next(iterator)
        except AutoMLVisionDataException:
            mesg = "Got AutoMLVisionDataException as all images in the current batch are invalid. Skipping the batch."
            logger.warning(mesg)
            pass
        except StopIteration:
            break


def _read_image(ignore_data_errors, image_url):
    try:
        return Image.open(image_url).convert('RGB')
    except IOError as ex:
        if ignore_data_errors:
            msg = '{}: since ignore_data_errors is True, file will be ignored.'.format(__file__)
            logger.warning(msg)
        else:
            raise AutoMLVisionDataException(str(ex), has_pii=True)
        return None


def _safe_exception_logging(func):
    """Decorates a function to compliantly log uncaught exceptions."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, FileExistsError) and not isinstance(e, FileNotFoundError):
                # This doesn't contain any user data, so it is safe to log.
                logger.error(e)
            # These might contain user data, they'll be scrubbed by the logging module.
            logging_utilities.log_traceback(e, logger)
            raise

    return wrapper


def _make_arg(arg_name: str) -> str:
    return "--{}".format(arg_name)


def _merge_settings_args_defaults(automl_settings: Dict, args: Namespace, defaults: Dict) -> Dict:
    """Creates a dictionary that is a superset of the automl_settings, args and defaults.
    The priority is  automl_settings > args > defaults

    :param automl_settings: automl settings object to fill
    :type automl_settings: dict
    :param args: command line arguments
    :type args: Namespace
    :param defaults: default values
    :type defaults: dict
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """

    merged_settings = {}
    merged_settings.update(defaults)
    merged_settings.update(vars(args))
    merged_settings.update(automl_settings)

    return merged_settings


def _save_image_df(train_df=None, val_df=None, train_index=None, val_index=None, output_dir=None):
    """Save train and validation label info from AMLdataset dataframe in output_dir

    :param train_df: training dataframe
    :type train_df: pandas.core.frame.DataFrame class
    :param val_df: validation dataframe
    :type val_df: pandas.core.frame.DataFrame class
    :param train_index: subset indices of train_df for training after train_val_split()
    :type train_index: <class 'numpy.ndarray'>
    :param val_index: subset indices of train_df for validation after train_val_split()
    :type val_index: <class 'numpy.ndarray'>
    :param output_dir: where to save
    :type output_dir: str
    """
    os.makedirs(output_dir, exist_ok=True)

    train_file = os.path.join(output_dir, 'train_df.csv')
    val_file = os.path.join(output_dir, 'val_df.csv')

    if train_df is not None:
        if train_index is not None and val_index is not None:
            train_df[train_df.index.isin(train_index)].to_csv(train_file, columns=['image_url', 'label'],
                                                              header=False, sep='\t', index=False)
            train_df[train_df.index.isin(val_index)].to_csv(val_file, columns=['image_url', 'label'],
                                                            header=False, sep='\t', index=False)
        elif val_df is not None:
            train_df.to_csv(train_file, columns=['image_url', 'label'], header=False, sep='\t', index=False)
            val_df.to_csv(val_file, columns=['image_url', 'label'], header=False, sep='\t', index=False)


def _extract_od_label(dataset=None, output_file=None):
    """Extract label info from a target dataset from label-file for object detection

    :param dataset: target dataset to extract label info
    :type dataset: <class 'object_detection.data.datasets.CommonObjectDetectionSubsetWrapper'>
    :param output_file: output filename
    :type output_file: str
     """
    if dataset is not None:
        image_infos = []
        for idx in dataset._indices:
            fname = dataset._image_urls[idx]
            annotations = dataset._annotations[fname]
            for annotation in annotations:
                ishard = True if annotation.iscrowd else False
                image_dict = {"imageUrl": fname,
                              "label": {"label": annotation.label,
                                        "topX": annotation._x0_percentage,
                                        "topY": annotation._y0_percentage,
                                        "bottomX": annotation._x1_percentage,
                                        "bottomY": annotation._y1_percentage,
                                        "isCrowd": str(ishard)}}
                image_infos.append(image_dict)

        with open(output_file, 'w') as of:
            for info in image_infos:
                json.dump(info, of)
                of.write("\n")


def _save_od_image_files(train_ds=None, val_ds=None, output_dir=None):
    """Save train and validation label info from dataset from label-file for object detection

    :param train_ds: training dataset
    :type train_ds: <class 'object_detection.data.datasets.CommonObjectDetectionSubsetWrapper'>
    :param val_ds: validation dataset
    :type val_ds: <class 'object_detection.data.datasets.CommonObjectDetectionSubsetWrapper'>
    :param output_dir: where to save
    :type output_dir: str
    """
    os.makedirs(output_dir, exist_ok=True)

    train_file = os.path.join(output_dir, 'train_sub.json')
    val_file = os.path.join(output_dir, 'val_sub.json')

    _extract_od_label(dataset=train_ds, output_file=train_file)
    _extract_od_label(dataset=val_ds, output_file=val_file)


def _set_random_seed(seed):
    """Set randomization seed and cuDNN settings for deterministic training

    :param seed: randomization seed
    :type seed: int
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        logger.info('Random number generator initialized with seed={}'.format(seed))

        if torch.cuda.is_available():
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
            logger.warning('You have chosen to seed training. This will '
                           'turn on the CUDNN deterministic setting, which can '
                           'slow down your training considerably! You may see '
                           'unexpected behavior when restarting from checkpoints.')
