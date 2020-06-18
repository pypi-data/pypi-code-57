import random
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


def default_normal():
    return random.normalvariate(0, 0.3)


def default_log():
    return np.log(random.normalvariate(0.3, 0.3)) 


def default_uniform():
    return random.uniform(-1, 1)

def default_binary():
    return random.randint(0, 2)

class PredictionModel(BaseModel):
    log_pct_up_prediction: float = Field(default_factory=default_normal)
    percentage_up_prediction: float = Field(default_factory=default_normal)
    classification: int = Field(default_factory=default_binary)
    classification_proba: float = Field(default_factory=default_uniform)
    # the imbalance of incorrect predictions. Some datasets skew to one end or another
    imbalance_up: float = Field(default_factory=default_uniform)
    imbalance_down: float = Field(default_factory=default_uniform)

    # Get the most common classifications over time
    rolling_class_mode_1: int = Field(default_factory=default_binary)
    rolling_class_mode_3: int = Field(default_factory=default_binary)
    rolling_class_mode_4: int = Field(default_factory=default_binary)

    # All Stats from Creme's ClassificationReport
    # This will be a base model as well
    # It'll extract all of the variables for the classification
    py_classification_report: int = Field(default_factory=default_binary)
    joint_log_likelihood_2: float = Field(default_factory=default_uniform)
    joint_log_likelihood_3: float = Field(default_factory=default_uniform)
    anomaly_score: float = Field(default_factory=default_uniform)
    rolling_pct_change_mean: float = Field(default_factory=default_uniform)
    rolling_pct_change_var: float = Field(default_factory=default_uniform)
    rolling_pct_change_sem: float = Field(default_factory=default_uniform)
    rolling_pct_change_skew: float = Field(default_factory=default_uniform)
    # get the anomaly_score to detect when something is extremely off


    def prediction_array(self) -> np.ndarray:
        arr = [
            self.log_pct_up_prediction,
            self.percentage_up_prediction,
            self.classification,
            self.classification_proba,
            self.imbalance_up,
            self.imbalance_down,
            self.rolling_class_mode_1,
            self.rolling_class_mode_3,
            self.rolling_class_mode_4,
            self.joint_log_likelihood_2,
            self.joint_log_likelihood_3,
            self.anomaly_score,
            self.rolling_pct_change_mean,
            self.rolling_pct_change_var,
            self.rolling_pct_change_sem,
            self.rolling_pct_change_skew
        ]
        return np.array(arr)