import collections
import copy
import random
from datetime import datetime
import typing
from typing import Optional, Union, Iterable, List
from uuid import UUID, uuid4
import numpy as np
import pandas as pd
from creme import (anomaly, cluster, ensemble, linear_model, metrics,
                   naive_bayes, optim, preprocessing, proba, stats)
from creme.base import Estimator
from creme.base.anomaly import AnomalyDetector
from creme.compose import Pipeline
from creme.metrics.base import Metric
from creme.naive_bayes.base import BaseNB
from creme.stats import Bivariate, Univariate
from loguru import logger
from pydantic import BaseModel, Field

from darwin_ml.models import PriceResponse
from darwin_ml.models.creme_ml.pipelines import (HardendedClassifierModel,
                                                 PctHardRegressorModel)
from darwin_ml.models.creme_ml.transforms import PercentageChange, PredictionHistory
from darwin_ml.middleware import containers
from jamboree.utils.context import timecontext

def default_normal():
    return random.normalvariate(0, 0.3)


def default_log():
    return np.log(random.normalvariate(0.3, 0.3))


def default_uniform():
    return random.uniform(-1, 1)


def default_binary():
    return random.randint(0, 2)


def predictive_classifier() -> Pipeline:
    return Pipeline(preprocessing.StandardScaler(),
                    linear_model.PAClassifier())


def anomoly_detection_pipeline() -> anomaly.HalfSpaceTrees:
    return anomaly.HalfSpaceTrees(n_trees=6, height=4, window_size=5)


class ModelResponse(BaseModel):
    pred_class: int = 0
    pred_pct: float = 0.0
    mean_imbal_up: float = 0.0
    mean_imbal_down: float = 0.0
    var_imbal_up: float = 0.0
    var_imbal_down: float = 0.0
    m1: int = 0
    m2: int = 0
    m3: int = 0
    anomaly_score: float = 0.0
    weighted_recall:float = 0.0
    weighted_f1:float = 0.0
    accuracy:float = 0.0

    mae_regression:float=0.0
    smape_regression:float=0.0
    mse_regression:float=0.0

    def space(self):
        arr = [
            int(self.pred_class),
            self.pred_pct,
            self.mean_imbal_up,
            self.mean_imbal_down,
            self.var_imbal_up,
            self.var_imbal_down,
            self.m1,
            self.m2,
            self.m3,
            self.anomaly_score,
            self.weighted_recall,
            self.weighted_f1,
            self.accuracy,
            self.mae_regression,
            self.smape_regression,
            self.mse_regression
        ]
        return np.array(arr) 


class OnlineModels(BaseModel):
    class_pred_history: PredictionHistory = PredictionHistory()
    reg_pred_history: PredictionHistory = PredictionHistory()
    hard_regressor: HardendedClassifierModel = PctHardRegressorModel()
    hard_classifier: HardendedClassifierModel = HardendedClassifierModel()

    prior_hard_regressor: HardendedClassifierModel = PctHardRegressorModel()
    prior_hard_classifier: HardendedClassifierModel = HardendedClassifierModel()

    # Get rolling information of the incorrect imbalances.
    # Incorrect imbalances can only be fitted when the imbalances are incorrect.
    imbalance_up_score_rolling_mean: stats.EWMean = stats.EWMean()
    imbalance_up_score_rolling_var: stats.EWVar = stats.EWVar()

    # Get rolling information of the incorrect imbalances.
    # Incorrect imbalances can only be fitted when the imbalances are incorrect.
    imbalance_down_score_rolling_mean: stats.EWMean = stats.EWMean()
    imbalance_down_score_rolling_var: stats.EWVar = stats.EWVar()

    # Get the most common classifications over time
    roll_mod_1: stats.RollingMode = stats.RollingMode(window_size=3)
    roll_mod_3: stats.RollingMode = stats.RollingMode(window_size=5)
    roll_mod_4: stats.RollingMode = stats.RollingMode(window_size=7)

    # All Stats from Creme's ClassificationReport
    # This will be a base model as well
    # It'll extract all of the variables for the classification
    report: Metric = metrics.ClassificationReport()
    anon: AnomalyDetector = anomoly_detection_pipeline()

    # get the anomaly_score to detect when something is extremely off
    mae_reg: metrics.MAE = metrics.MAE()
    smape_reg: metrics.SMAPE = metrics.SMAPE()
    mse_reg: metrics.MSE = metrics.MSE()

    class Config:
        arbitrary_types_allowed = True

    def set_lag(self, lag=3):
        self.class_pred_history: PredictionHistory = PredictionHistory(lag=lag)
        self.reg_pred_history: PredictionHistory = PredictionHistory(lag=lag)

    def update_rolling_mode(self, change_delta: PriceResponse):
        self.roll_mod_1.update(change_delta.direction)
        self.roll_mod_3.update(change_delta.direction)
        self.roll_mod_4.update(change_delta.direction)
        m_1 = self.roll_mod_1.get()
        m_3 = self.roll_mod_3.get()
        m_4 = self.roll_mod_4.get()
        return m_1, m_3, m_4

    def update_anomaly_detection(self, X: dict):
        """Update Anomaly Detection

        Args:
            X (dict): The features from the enviornment for the ML algorithm.

        Returns:
            float: The anomaly score.
        """
        self.anon.fit_one(X)
        return self.anon.score_one(X)

    def fit_estimators(self, prior: dict, cdelta: PriceResponse) -> None:
        
        self.hard_regressor.fit_one(prior, cdelta.percentage)
        self.hard_classifier.fit_one(prior, cdelta.direction)

    def predict_estimators(self, current: dict):
        """
            # Predict Estimators

            Also store the prediction in history. This will likely be duplicated in Jamboree later.

        """
        pct_prediction = self.hard_regressor.predict_one(current)
        dir_prediction = self.hard_classifier.predict_one(current)
        dir_prediction = int(dir_prediction)
        self.reg_pred_history.update(pct_prediction)
        self.class_pred_history.update(dir_prediction)
        return pct_prediction, dir_prediction

    def evaluate_estimators(self, cdelta: PriceResponse, prior: dict):
        c_pred = self.class_pred_history.get()
        r_pred = self.reg_pred_history.get()
        # Add regression error metrics later
        c_res = cdelta.direction
        r_res = cdelta.percentage
        if c_pred is not None:
            if c_res != c_pred:
                # logger.success(self.class_pred_history.window)
                self.evaluate_incorrect_estimation(prior)
            self.report.update(c_pred, c_res)

        if r_pred is not None:
            self.mae_reg.update(r_res, r_pred)
            self.mse_reg.update(r_res, r_pred)
            self.smape_reg.update(r_res, r_pred)

    def evaluate_incorrect_estimation(self, prior: dict):
        """ Gets imbalance information on the variables that weren't correctly estimated."""
        prior_probabilities = self.prior_hard_classifier.predict_proba_one(
            prior)
        _up_prob = prior_probabilities[True]
        _down_prob = prior_probabilities[False]
        self.imbalance_up_score_rolling_mean.update(_up_prob)
        self.imbalance_up_score_rolling_var.update(_up_prob)

        self.imbalance_down_score_rolling_mean.update(_down_prob)
        self.imbalance_down_score_rolling_var.update(_down_prob)

    def transfer_estimator(self):
        self.prior_hard_regressor = copy.copy(self.hard_regressor)
        self.prior_hard_classifier = copy.copy(self.hard_classifier)

    def fit_predict_eval(self, current: dict, prior: dict,
                         cdelta: PriceResponse):
        self.transfer_estimator()
        self.fit_estimators(prior, cdelta)
        _pct, _direction = self.predict_estimators(current)
        self.evaluate_estimators(cdelta, prior)
        return self.report, _pct, _direction

    def step(self, feature_container:containers.FeaturesContainer, change_delta: PriceResponse) -> ModelResponse:
        """Given the features and the current delta information get the following:
        
        1. predictions
        2. stats on those predictions
        3. Get the metrics on each Estimator

        Args:
            current_features (dict): [description]
            prior_features (dict): [description]
            change_delta (PriceResponse): [description]
        """

        curr = feature_container.current
        prev = feature_container.previous
        # anon_score = self.update_anomaly_detection(curr)
        
        report, _pct, _class = self.fit_predict_eval(curr,
                                                    prev,
                                                    change_delta)

        weighted_recall = report.weighted_recall.get()
        weighted_f1     = report.weighted_f1.get()
        accuracy        = report.accuracy.get()
        mae_reg = self.mae_reg.get()
        mse_reg = self.mse_reg.get()
        smape_reg = self.smape_reg.get()

        _im_up = self.imbalance_up_score_rolling_mean.get()
        _im_upv = self.imbalance_up_score_rolling_var.get()

        _im_down = self.imbalance_down_score_rolling_mean.get()
        _im_downv = self.imbalance_down_score_rolling_var.get()

        mod_1, mod_2, mod_3 = self.update_rolling_mode(change_delta)
        response = ModelResponse(
            m1=mod_1,
            m2=mod_2,
            m3=mod_3,
            # anomaly_score=anon_score,
            pred_class = int(_class),
            pred_pct = float(_pct),
            mean_imbal_up=_im_up,
            mean_imbal_down=_im_down,
            var_imbal_down=_im_downv,
            var_imbal_up=_im_upv,
            weighted_recall=weighted_recall,
            weighted_f1=weighted_f1,
            accuracy=accuracy,
            mae_regression=mae_reg,
            smape_regression=mse_reg,
            mse_regression=smape_reg
        )
        return response


""" 
    Step though accessed information (should have accessed by now). 
    Get all of the predictions, statistical information on those predictions and train.
"""


def main():
    _online_models = OnlineModels()
    logger.critical(_online_models)


if __name__ == "__main__":
    main()
