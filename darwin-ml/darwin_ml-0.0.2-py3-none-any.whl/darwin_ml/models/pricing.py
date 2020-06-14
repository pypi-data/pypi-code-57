import numpy as np
import pandas as pd
from creme import stats
from pydantic import BaseModel
import collections
from darwin_ml.utils import Injectable
from darwin_ml.models.creme_ml.transforms import PercentageChange
from darwin_ml.models.creme_ml.transforms import FeatureWindow
from darwin_ml.middleware import containers


class PriceResponse(BaseModel):
    """A return model for the price delta

    Args:
        BaseModel (None): This is the model we're getting returned.
    """
    direction: int = 0
    percentage: float = 0.0


class PriceDeltaModel(BaseModel, Injectable):
    # Get the average percentage change of the allocation
    pct_model: PercentageChange = PercentageChange(lag=3)

    class Config:
        arbitrary_types_allowed = True

    def set_lag(self, lag=3):
        self.pct_model = PercentageChange(lag=lag)

    def stored_model(self, price_container: containers.PriceContainer):
        price: float = price_container.current_price
        self.pct_model.update(price)

        pct_window = self.pct_model.get()
        direction = self.pct_model.get_class()

        res = PriceResponse(direction=direction, percentage=pct_window)
        return res

    def step(self,
             price_container: containers.PriceContainer,
             is_stored: bool = False) -> PriceResponse:
        """Add price information to get target change information.

        Args:
            price_dict (dict): OHLCV Price Information.

        Returns:
            PriceResponse: The direction classification of the price change over a gievn lag.
        """
        
        if is_stored:
            return self.stored_model(price_container)

        direction = price_container.direction
        percentage = price_container.percentage

        res = PriceResponse(direction=direction, percentage=percentage)
        return res