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
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import logging

from .._logging import check_module

LOGGER = logging.getLogger(__name__)


def xgboost_train(experiment, original, return_value, *args, **kwargs):
    if experiment.auto_param_logging and not experiment.disabled_monkey_patching:
        # Log XGBoost parameters
        if not experiment._storage["xgboost"].get("parameter_set", False):
            params = {key: value for key, value in args[0].items() if value is not None}
            experiment._log_parameters(params)
            experiment._storage["xgboost"]["parameter_set"] = True

        # Log XGBoost eval metrics
        for key in kwargs["evals_result"]:
            with experiment.context_manager(key):
                for metric_name in kwargs["evals_result"][key]:
                    for step, value in enumerate(
                        kwargs["evals_result"][key][metric_name]
                    ):
                        experiment._log_metric(
                            metric_name, value, step=step, framework="xgboost"
                        )


def patch(module_finder):
    check_module("xgboost")
    module_finder.register_after("xgboost.training", "train", xgboost_train)


check_module("xgboost")
