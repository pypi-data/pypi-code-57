import math
import random
import typing
from datetime import datetime
from typing import Optional, Union
from uuid import UUID, uuid4

import numpy as np
import pandas as pd
from creme import (anomaly, cluster, compose, datasets, ensemble,
                   feature_extraction, feature_selection, linear_model, meta,
                   metrics, model_selection, naive_bayes, optim, preprocessing,
                   proba, sampling, stats)
from creme.meta import BoxCoxRegressor
from loguru import logger

from darwin_ml.models.creme_ml.transforms import PercentageChange

# logger.disable("jamboree")


class PctHardRegressorModel(object):
    def __init__(self):
        lin_reg = linear_model.LinearRegression()
        # boxcot_reg = meta.TransformedTargetRegressor(regressor=lin_reg, func=math.log, inverse_func=math.exp)
        self.model = compose.Pipeline(
            ('scale', preprocessing.StandardScaler()),
            ('lin_reg',
             sampling.HardSamplingRegressor(
                 size=400,
                 p=0.2,
                 regressor=lin_reg
                )
            )
        )

    def fit_one(self, x: dict, y: typing.Union[float, int]):
        self.model.fit_one(x, y)

    def predict_one(self, x: dict):
        return self.model.predict_one(x)
