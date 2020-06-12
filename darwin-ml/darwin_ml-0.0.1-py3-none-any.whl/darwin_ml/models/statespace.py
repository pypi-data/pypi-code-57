import numpy as np
import pandas as pd
from loguru import logger
from typing import Optional
from pydantic import BaseModel
from darwin_ml.models.prediction import PredictionModel
from darwin_ml.models import AllocationStepSystem
from darwin_ml.models import OnlineModels
from darwin_ml.models import PriceDeltaModel
from darwin_ml.models.creme_ml.transforms import FeatureWindow
from darwin_ml.middleware import containers
from jamboree.utils.context import timecontext
class StateSpaceModel(object):
    """Blob Storage State Space Model

        This is the directly stored model for the state space. 
        The goal is to store all of the relavent variables and gradients.
    """
    def __init__(self, prediction_lag=3):
        # Get the change of price over the given lag period
        self.price_delta_calc: PriceDeltaModel = PriceDeltaModel()
        # Get the statistical change for the allocations over time.
        self.allo_step: AllocationStepSystem = AllocationStepSystem()
        # Predict and get a stacked version of the predictions over time.
        self.prediction_step: OnlineModels = OnlineModels()
        # Use this to locally store features and determine features relavent to the predictions.
        self.feature_window: FeatureWindow = FeatureWindow(lag=prediction_lag)
        
        self.prediction_step.set_lag(lag=prediction_lag)
        self.price_delta_calc.set_lag(lag=prediction_lag)

        self.current_prev_feature = None
    
    @property
    def is_previous_feature(self) -> bool:
        self.current_prev_feature = self.feature_window.get()
        return bool(self.current_prev_feature)

    @logger.catch(reraise=True)
    def step(self, all_c:containers.AllocationContainer,
             feature_container: containers.FeaturesContainer, price_container: containers.PriceContainer):
        
        curr = feature_container.current

        self.feature_window.update(curr)
        if not self.is_previous_feature:
            return None


        delta = self.price_delta_calc.step(price_container)
        pred_model = self.prediction_step.step(feature_container, delta)
        allo_model = self.allo_step.step(all_c.percentage, all_c.filling)
        joined_space = np.concatenate([pred_model.space(), allo_model.space()])
        return joined_space

    def step_complete(self, 
                        current_allocation: float,
                        current_fill_percentage: float, 
                        current_features: dict, 
                        prior_features: dict,
                        prior_price: dict,
                        current_price: dict):
        """Run the step with the prior features and price in the parameters. 
        
        Used to make real life predictions and changes.

        Args:
            current_allocation (float): The current allocation cap of the current asset.
            current_fill_percentage (float): How much of the allocation limit is filled.
            current_features (dict): The features at the current timestamp. Used to make prediction of future.
            current_price (dict): The current price of the asset.

        Returns:
            [type]: [description]
        """
        delta = self.price_delta_calc.step(current_price)
        return None
    
    def reset():
        """reset Reset function

        Reset core functions.
        """
        pass