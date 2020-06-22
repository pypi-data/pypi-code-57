# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines a common interface for learning rate schedulers."""

from abc import ABC
from ..common import constants
import torch.optim
from . import learning_parameters
from azureml.automl.core.shared.exceptions import ClientException


class BaseLRSchedulerWrapper(ABC):
    """Class that provides a common interface for all learning
    rate schedulers"""

    def __init__(self, learning_parameters, optimizer):
        """
        :param learning_parameters: Parameters that define learning
        rate sechduler
        :type learning_parameters: SchedulerParameters object (see
        object_detection.train.learning_parameters
        :param optimizer: Optimizer the scheduler will operate on
        :type optimizer: Pytorch optimizer
        """
        self._lr_scheduler = None

    @property
    def lrScheduler(self):
        """Get the learning rate scheduler.

        :return: learning rate scheduler
        :rtype: pytoch learning rate scheduler
        """
        return self._lr_scheduler


class StepLRWrapper(BaseLRSchedulerWrapper):
    """Wrapper for Step Learning Rate Scheduler."""

    def __init__(self, learning_parameters, optimizer):
        """
        :param learning_parameters: Parameters that define learning rate scheduler. StepLR Supports:
                                        - step_size
                                        - gamma
        :type learning_parameters: SchedulerParameters object (see
        object_detection.train.learning_parameters
        :param optimizer: Optimizer the scheduler will operate on
        :type optimizer: Pytorch optimizer
        """

        self._step_size = (learning_parameters.step_size if
                           learning_parameters.step_size is not None else
                           constants.SchedulerParameters.DEFAULT_STEP_LR_STEP_SIZE)

        self._gamma = (learning_parameters.gamma if
                       learning_parameters.gamma is not None else
                       constants.SchedulerParameters.DEFAULT_STEP_LR_GAMMA)

        self._lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                             step_size=self._step_size,
                                                             gamma=self._gamma)


class LRSchedulerFactory:
    """Factory class that produces different learning rate scheduler algorithms."""
    _scheduler_dict = {
        constants.LRSchedulerNames.STEP: StepLRWrapper
    }

    def get_lr_scheduler(self, lr_scheduler_name, optimizer, learning_parameters):
        """Construct and return a learning rate scheduler wrapper.

        :param lr_scheduler_name: Name of the learning rate scheduler
        :type lr_scheduler_name: String
        :param optimizer: Optimizer that scheduler will change learning rate for
        :type optimizer: Pytorch optimizer
        :param learning_parameters: Parameters that define scheduler
        :type learning_parameters: SchedulerParameters object (see object_detection.train.learning_parameters
        :returns: Learning rate scheduler
        :rtype: Pytorch Learning Rate Scheduler
        """

        if lr_scheduler_name is None:
            lr_scheduler_name = constants.LRSchedulerNames.DEFAULT_LR_SCHEDULER

        if lr_scheduler_name not in LRSchedulerFactory._scheduler_dict:
            raise ClientException('{} not supported'.format(lr_scheduler_name))\
                .with_generic_msg("Scheduler name not supported.")

        return LRSchedulerFactory._scheduler_dict[lr_scheduler_name](learning_parameters,
                                                                     optimizer).lrScheduler


def setup_lr_scheduler(optimizer, scheduler=None, **kwargs):
    """Creates learning rate scheduler.

    :param optimizer: Optimizer that scheduler will operate on
    :type optimizer: Pytorch optimizer
    :param scheduler: (optional) Name of scheduler to use. Defaults to StepLR.
    :type scheduler: str
    :param kwargs: Optional scheduler parameters
    :type kwargs: dict
    :returns: Learning rate scheduler
    :rtype: Pytorch Learning Rate Scheduler
    """

    scheduler_parameters = learning_parameters.SchedulerParameters(**kwargs)

    scheduler_factory = LRSchedulerFactory()

    return scheduler_factory.get_lr_scheduler(scheduler, optimizer, scheduler_parameters)
