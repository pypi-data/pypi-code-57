# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that wrap training steps"""

import torch
import copy
import logging
import time

from ..eval import cocotools
from ..eval.utils import prepare_bounding_boxes_for_eval
from ..common import boundingbox
from ..common.constants import TrainingParameters
from ...common.utils import _add_run_properties, _data_exception_safe_iterator, _get_gpu_usage
from ...common.utils import AverageMeter

logger = logging.getLogger(__name__)


class TrainSettings:
    """Settings for training."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional training parameters. Currently supports
          -number_of_epochs: Number of epochs to train for (int)
          -max_patience_iterations: Number of epochs with no validation
          improvement before stopping.
          -primary_metric: Metric that is evaluated and logged by AzureML run object.
        :type kwargs: dict
        """

        self._number_of_epochs = kwargs.get(
            "number_of_epochs", TrainingParameters.DEFAULT_NUMBER_EPOCHS)
        self._max_patience_iterations = kwargs.get(
            "max_patience_iterations", TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
        self.primary_metric = kwargs.get(
            "primary_metric", TrainingParameters.DEFAULT_PRIMARY_METRIC)

    @property
    def number_of_epochs(self):
        """Get number of epochs

        :return: number_of_epochs
        :rtype: int
        """
        return self._number_of_epochs

    @property
    def max_patience_iterations(self):
        """Get number of patience iterations

        :return: max_patience_iterations
        :rtype: int
        """
        return self._max_patience_iterations


def move_images_to_device(images, device):
    """Convenience function to move images to device (gpu/cpu).

    :param images: Batch of images
    :type images: Pytorch tensor
    :param device: Target device
    :type device: Pytorch device
    """

    return [image.to(device) for image in images]


def move_targets_to_device(targets, device):
    """Convenience function to move training targets to device (gpu/cpu)

    :param targets: Batch Training targets (bounding boxes and classes)
    :type targets: Dictionary
    :param device: Target device
    :type device: Pytorch device
    """

    return [{k: v.to(device) for k, v in target.items()} for
            target in targets]


def train_one_epoch(model, optimizer, scheduler, train_data_loader,
                    device, criterion, epoch, print_freq):
    """Train a model for one epoch

    :param model: Model to be trained
    :type model: Pytorch nn.Module
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler
    :type scheduler: Pytorch Learning Rate Scheduler
    :param train_data_loader: Data loader for training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device
    :type device: Pytorch device
    :param criterion: Loss function wrapper
    :type criterion: Object derived from BaseCriterionWrapper (see object_detection.train.criterion)
    :param epoch: Current training epoch
    :type epoch: int
    :param print_freq: How often you want to print the output
    :type print_freq: int
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    model.train()

    end = time.time()
    avg_gpu_usage = {}
    avg_gpu_mem_use = {}
    for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(train_data_loader))):
        # measure data loading time
        data_time.update(time.time() - end)

        images = move_images_to_device(images, device)
        targets = move_targets_to_device(targets, device)

        loss_dict = criterion.evaluate(model, images, targets)
        loss = sum(loss_dict.values())
        loss_value = loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # record loss and measure elapsed time
        losses.update(loss_value, len(images))
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0 or i == len(train_data_loader) - 1:
            mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                   "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                   "({loss.avg:.4f})\t".format(epoch, i, len(train_data_loader), optimizer.param_groups[0]["lr"],
                                               batch_time=batch_time, data_time=data_time, loss=losses)
            if torch.cuda.is_available():
                mesg += _get_gpu_usage(avg_gpu_mem_use, avg_gpu_usage)
            logger.info(mesg)

    scheduler.step()


def validate(model, val_data_loader, device, val_index_map):
    """Gets model results on validation set.

    :param model: Model to score
    :type mode: Pytorch nn.Module
    :param val_data_loader: Data loader for validation data
    :type val_data_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param val_index_map: Map from numerical indices to class names
    :type val_index_map: List of strings
    :returns: List of detections
    :rtype: List of ImageBoxes (see object_detection.common.boundingbox)
    """

    batch_time = AverageMeter()

    model.eval()

    bounding_boxes = []
    end = time.time()
    avg_gpu_usage = {}
    avg_gpu_mem_use = {}
    with torch.no_grad():
        for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(val_data_loader))):
            images = move_images_to_device(images, device)

            labels = model(images)

            for info, label in zip(info, labels):
                image_boxes = boundingbox.ImageBoxes(
                    info["filename"], val_index_map)

                image_boxes.add_boxes(label["boxes"],
                                      label["labels"],
                                      label["scores"])

                bounding_boxes.append(image_boxes)

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % 100 == 0 or i == len(val_data_loader) - 1:
                mesg = "Test: [{0}/{1}]\t"\
                       "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, len(val_data_loader),
                                                                                     batch_time=batch_time)
                if torch.cuda.is_available():
                    mesg += _get_gpu_usage(avg_gpu_mem_use, avg_gpu_usage)
                logger.info(mesg)

    return bounding_boxes


def train(model, optimizer, scheduler,
          train_data_loader, device, criterion,
          train_settings, val_data_loader, val_coco_index=None, val_vocmap=None,
          enable_coco_validation=False, val_index_map=None, run=None, ignore_data_errors=True):
    """Train a model

    :param model: Model to train
    :type model: Object derived from CommonObjectDetectionModelWrapper (see object_detection.models.base_model_wrapper)
    :param optimizer: Model Optimizer
    :type optimizer: Pytorch Optimizer
    :param scheduler: Learning Rate Scheduler
    :type scheduler: Pytorch Learning Rate Scheduler
    :param train_data_loader: Data loader with training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device (gpu/cpu)
    :type device: Pytorch Device
    :param criterion: Loss function
    :type criterion: Object dervied from CommonCriterionWrapper (see object_detection.train.criterion)
    :param train_settings: Settings for training.
    :type train_settings: TrainSettings object
    :param val_data_loader: Data loader with validation data.
    :type val_data_loader: Pytorch data loader
    :param val_coco_index (optional): Cocoindex created from validation data
    :type val_coco_index (optional): Pycocotool Cocoindex object
    :param val_vocmap (optional): VocMap created from validation data
    :type val_vocmap (optional): VocMap object
    :param enable_coco_validation (optional): enable validation and evaluation for every epoch using Pycocotools.
    :type enable_coco_validation (optional): bool
    :param val_index_map (optional): Map from class indices to class names
    :type val_index_map (optional): List of strings
    :param run: azureml run object
    :type run: azureml.core.run.Run
    :param ignore_data_errors: boolean flag to turn on or off errors due to missing or malformed input data
    :type ignore_data_errors: bool
    :returns: Trained model
    :rtype: Object derived from CommonObjectDetectionModelWrapper
    """
    epoch_time = AverageMeter()

    base_model = model.model
    base_model.to(device)

    best_score = 0.0
    best_model = copy.deepcopy(base_model.state_dict())

    patience_iterations = 0

    epoch_end = time.time()
    train_start = time.time()
    coco_metric_time = AverageMeter()
    voc_metric_time = AverageMeter()
    for epoch in range(train_settings.number_of_epochs):

        train_one_epoch(base_model, optimizer, scheduler,
                        train_data_loader, device, criterion, epoch, print_freq=100)

        bounding_boxes = validate(base_model, val_data_loader, device, val_index_map)
        eval_bounding_boxes = prepare_bounding_boxes_for_eval(bounding_boxes)
        if not eval_bounding_boxes:
            logger.info("no detected bboxes for evaluation")

        if val_coco_index and enable_coco_validation:
            coco_metric_start = time.time()
            cocotools.score_from_index(val_coco_index, eval_bounding_boxes)
            coco_metric_time.update(time.time() - coco_metric_start)
            logger.info("Coco Time {coco_time.value:.4f} ({coco_time.avg:.4f})".format(coco_time=coco_metric_time))

        if val_vocmap:
            voc_metric_start = time.time()
            vocmap_score, vocmap_label_scores = val_vocmap.compute(eval_bounding_boxes)
            voc_metric_time.update(time.time() - voc_metric_start)
            logger.info("Per label voc map scores: {}".format(vocmap_label_scores))
            logger.info("Voc map score: {}".format(round(vocmap_score, 3)))
            logger.info("Voc Time {voc_time.value:.4f} ({voc_time.avg:.4f})".format(voc_time=voc_metric_time))

            patience_iterations += 1

            if vocmap_score > best_score:
                best_model = copy.deepcopy(base_model.state_dict())
                patience_iterations = 0
                best_score = vocmap_score

            if run is not None:
                run.log("average_precision_score_macro", round(vocmap_score, 3))  # for backwards compatibility
                run.log(train_settings.primary_metric, round(vocmap_score, 3))
        else:
            best_model = copy.deepcopy(base_model.state_dict())

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        if patience_iterations > train_settings.max_patience_iterations:
            break

    # measure total training time
    train_time = time.time() - train_start
    logger.info("Total training time {0:.4f}".format(train_time))

    base_model.load_state_dict(best_model)
    if run is not None:
        _add_run_properties(run, best_score)
