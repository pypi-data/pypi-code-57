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
from loguru import logger





class HardendedClassifierModel(object):
    def __init__(self):
        self.model =  (
            preprocessing.StandardScaler() |
            sampling.HardSamplingClassifier(
                classifier = linear_model.LogisticRegression(),
                 p = 0.15,
                 size = 300,
            )
        )


    def fit_one(self, x: dict, y: typing.Union[float, int]):
        self.model.fit_one(x, y)

    def predict_one(self, x: dict):
        return self.model.predict_one(x)
    
    def predict_proba_one(self, x:dict):
        return self.model.predict_proba_one(x)