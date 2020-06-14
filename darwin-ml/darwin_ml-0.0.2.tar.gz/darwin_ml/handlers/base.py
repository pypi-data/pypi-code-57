import uuid
from typing import Optional

import pandas as pd
from jamboree import Jamboree, TimeHandler
from jamboree.handlers.abstracted.datasets import PriceData
from loguru import logger
from pydantic import BaseModel

from darwin_ml.handlers import StateTransformerAbstract
from darwin_ml.models.metadata import MetadataModel
from darwin_ml.models.prediction import PredictionModel


class PriceStateTransformer(StateTransformerAbstract):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__price = PriceData()
        self.__meta = MetadataModel()
        self.__assetid:Optional[str] = None
        self.previous_meta_model: Optional[MetadataModel] = None
        self.previous_asset: Optional[str] = None

    @property
    def price(self):
        if self.previous_asset == self.asset:
            return self.__price
        self.__price.processor = self.processor
        self.__price.episode = self.episode
        self.__price.live = self.live
        self.__price.pick(self.asset)
        self.previous_asset = self.asset
        return self.__price

    @property
    def asset(self) -> str:
        if self.__assetid is None or not isinstance(self.__assetid, str):
            raise ValueError("Assetid isn't set correctly")
        return self.__assetid

    @asset.setter
    def asset(self, _asset: str):
        self.__assetid = _asset

    @property
    def everything(self) -> pd.DataFrame:
        return self.price.everything

    @property
    def meta(self):
        return self.__meta

    @property
    def meta_model(self) -> MetadataModel:
        """Metadata Model

        Returns:
            MetadataModel -- The metadata model.
        """
        price_obj = self.price
        self.__meta.name = price_obj['name']
        self.__meta.category = price_obj['category']
        self.__meta.subcategories = price_obj['subcategories']
        self.__meta.metatype = price_obj['metatype']
        self.__meta.submetatype = price_obj['submetatype']
        self.__meta.abbreviation = price_obj['abbreviation']
        return self.__meta
    
    
    def is_same_meta_model(self):
        if self.previous_meta_model == self.meta_model:
            return True
        return False

    @property
    def is_next(self) -> bool:
        return self.price.is_next

    @property
    def state_model(self):
        """The BaseModel used to return a desired state. Use to provide type constraints.

        Returns:
            BaseModel -- The data we return back.
        """
        return None

    @property
    def param_model(self):
        """Supposed to be a pydantic model to state which parameters are to be there. Will delete soon.

        Returns:
            [type] -- [description]
        """
        return None

    @property
    def step_model(self):
        return None

    @property
    def state(self):
        return None

    def set_params(self,
                   asset_id: Optional[str] = None,
                   episode: Optional[str] = None,
                   live: Optional[bool] = None,
                   **kwargs):
        if asset_id is not None:
            self.asset = asset_id
        if episode is not None:
            self.episode = episode
        if live is not None:
            self.live = live

    def reset(self):
        # I don't know what's supposed to be here
        pass

    def step(self) -> PredictionModel:
        """Take a single step necessary to create a state space.

        Raises:
            NotImplementedError: If the abstract method wasn't overwritten

        Returns:
            BaseModel -- A type constrained model to return all of the variables
        """
        # logger.error(self.current_time)
        return PredictionModel()


if __name__ == "__main__":
    episode = uuid.uuid4().hex
    state_trans = PriceStateTransformer()
    state_trans.asset = "80de790b2d024654b76de0e76a623bcf"
    state_trans.processor = Jamboree()
    state_trans.episode = episode
    state_trans.live = False
    logger.success(state_trans.current_time)
    logger.info(state_trans.meta_model)
    # logger.success(state_transformer.everything)
    logger.warning(state_trans.step().prediction_array())
