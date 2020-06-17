# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2020 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************

import logging

import six

from .._typing import Any, Optional
from ..experiment import BaseExperiment
from ..predictor import Predictor
from ..utils import get_time_monotonic

LOGGER = logging.getLogger(__name__)


def build_base_callback(base):
    class BaseCallback(base):  # type: ignore
        """
        Base Keras callback.
        """

        def __init__(self):
            super(BaseCallback, self).__init__()

        def on_epoch_begin(self, epoch, logs=None):
            pass

        def on_epoch_end(self, epoch, logs=None):
            pass

        def on_batch_begin(self, batch, logs=None):
            pass

        def on_batch_end(self, batch, logs=None):
            pass

        def on_train_begin(self, logs=None):
            pass

        def on_train_end(self, logs=None):
            pass

        def on_train_batch_begin(self, batch, logs=None):
            pass

        def on_train_batch_end(self, batch, logs=None):
            pass

        def on_test_batch_begin(self, batch, logs=None):
            pass

        def on_test_batch_end(self, batch, logs=None):
            pass

        def on_test_begin(self, logs=None):
            pass

        def on_test_end(self, logs=None):
            pass

        def on_predict_begin(self, logs=None):
            pass

        def on_predict_end(self, logs=None):
            pass

        def on_predict_batch_begin(self, batch, logs=None):
            pass

        def on_predict_batch_end(self, batch, logs=None):
            pass

    return BaseCallback


def build_predictive_early_stopping_keras_callback(base):
    class PredictiveEarlyStoppingKerasCallback(base):  # type: ignore
        def __init__(self, predictor, predict_epoch_rate=1):
            # type: (Predictor, int) -> None
            super(PredictiveEarlyStoppingKerasCallback, self).__init__()
            self.predictor = predictor
            self.predict_epoch_rate = predict_epoch_rate

        def on_epoch_end(self, epoch, logs={}):
            if epoch % self.predict_epoch_rate == 0:
                loss = logs.get(self.predictor.loss_name)
                self.predictor.report_loss(loss)

                if self.predictor.stop_early(epoch=epoch):
                    self.model.stop_training = True

    return PredictiveEarlyStoppingKerasCallback


def build_empty_keras_callback(base):
    class EmptyKerasCallback(base):  # type: ignore
        """
        Empty Keras callback.
        """

    return EmptyKerasCallback


def build_keras_callback(base):
    class KerasCallback(base):  # type: ignore
        """ Keras callback to report params, metrics to Comet.ml Experiment()"""

        def __init__(
            self,
            experiment,  # type: BaseExperiment
            log_params=True,  # type: bool
            log_metrics=True,  # type: bool
            log_graph=True,  # type: bool
        ):
            # type: (...) -> None
            """
            Create a new experiment and submit source code.
            :param api_key: User's API key. Required.
            """
            super(KerasCallback, self).__init__()

            # Inits the experiment with reference to the name of this class. Required for loading the correct
            # script file
            self.experiment = experiment
            self.log_params = log_params
            self.log_metrics = log_metrics
            self.log_graph = log_graph
            self.epoch_start_time = None  # type: Optional[float]
            self.our_step = 0

        def on_epoch_begin(self, epoch, logs=None):
            try:
                # This function should only be called during train mode.
                LOGGER.debug("On epoch begin %s %s", epoch, logs)
                self.experiment.set_epoch(epoch)
                self.epoch_start_time = get_time_monotonic()
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_epoch_begin; ignoring",
                    exc_info=True,
                )

        def on_epoch_end(self, epoch, logs=None):
            try:
                # This function should only be called during train mode.
                LOGGER.debug("On epoch end %s %s", epoch, logs)
                if self.log_metrics:
                    if self.epoch_start_time is not None:
                        self.experiment._log_metric(
                            "epoch_duration",
                            get_time_monotonic() - self.epoch_start_time,
                            step=self.our_step,
                            framework="keras",
                        )
                        self.epoch_start_time = None
                    self.experiment.log_epoch_end(epoch, step=self.our_step)
                    if logs:
                        for name, val in logs.items():
                            self.experiment._log_metric(
                                name, val, step=self.our_step, framework="keras"
                            )
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_epoch_end; ignoring",
                    exc_info=True,
                )

        def on_batch_begin(self, batch, logs=None):
            try:
                # This function called directly when in train mode.
                LOGGER.debug("On batch begin %s %s", batch, logs)
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_batch_begin; ignoring",
                    exc_info=True,
                )

        def on_batch_end(self, batch, logs=None):
            """
            Logs training metrics.
            """
            try:
                # This function called directly when in train mode.
                LOGGER.debug("On batch end %s %s", batch, logs)

                self.our_step += 1

                if self.experiment.batch_report_rate > 0:
                    if batch is not None and isinstance(batch, six.integer_types):
                        if batch % self.experiment.batch_report_rate == 0:
                            self._send_batch_messages(logs)
                    else:
                        self._send_batch_messages(logs)
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_batch_end; ignoring",
                    exc_info=True,
                )

        def on_train_batch_end(self, batch, logs=None):
            try:
                # No context added here, to match previous behavior:
                self.on_batch_end(batch, logs)
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_train_batch_end; ignoring",
                    exc_info=True,
                )

        def on_test_batch_end(self, batch, logs=None):
            try:
                with self.experiment.validate():
                    self.on_batch_end(batch, logs)
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_test_batch_end; ignoring",
                    exc_info=True,
                )

        def _send_batch_messages(self, logs):
            if logs and self.log_metrics:
                for name, val in logs.items():
                    self.experiment._log_metric(
                        "batch_" + name, val, step=self.our_step, framework="keras"
                    )

        def on_train_begin(self, logs=None):
            """
            Sets model graph.
            """
            try:
                LOGGER.debug("On train begin %s", logs)

                if self.log_graph:
                    model_graph = get_keras_json_model(self.experiment, self.model)

                    if model_graph:
                        self.experiment._set_model_graph(model_graph, framework="keras")
                    else:
                        LOGGER.debug("Empty graph model, skipping")

                try:
                    trainable_params = self.model.count_params()
                    self.experiment._log_other(
                        "trainable_params", trainable_params, framework="keras"
                    )
                except Exception:
                    LOGGER.debug("Failed to count params in model", exc_info=True)

                if self.log_params:
                    if logs:
                        for k, v in logs.items():
                            self.experiment._log_parameter(k, v, framework="keras")

                    # Keras Callback doesn't set this parameter at creation by default
                    if hasattr(self, "params") and self.params:
                        for k, v in self.params.items():
                            if k != "metrics":
                                self.experiment._log_parameter(k, v, framework="keras")

                    try:
                        optimizer_name = self.model.optimizer.__class__.__name__
                        config = self.model.optimizer.get_config()
                        for key, value in config.items():
                            self.experiment._log_parameter(
                                optimizer_name + "_" + key, value, framework="keras"
                            )
                    except Exception:
                        LOGGER.debug(
                            "Failed to extract optimizer information", exc_info=True
                        )
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_train_begin; ignoring",
                    exc_info=True,
                )

        def on_train_end(self, *args, **kwargs):
            try:
                LOGGER.debug("On train end %r", locals())
            except Exception:
                LOGGER.warning(
                    "An unknown exception happened in Keras callback on_train_end; ignoring",
                    exc_info=True,
                )

    return KerasCallback


def get_keras_json_model(experiment, model):
    # type: (BaseExperiment, Any) -> Any

    # With multi-gpu models we save the original model in the experiment
    # storage
    storage_key = "gpu_model_%s" % id(model)
    json_model = experiment._storage["keras"].get(storage_key, None)

    if json_model is not None:
        return json_model
    else:
        try:
            return model.to_json(sort_keys=True)
        except Exception:
            experiment._log_once_at_level(
                logging.WARNING, "Failed to save keras graph model", exc_info=True
            )
            return None
