import pprint
import time
import uuid
import warnings
from typing import List

import maya
from jamboree import Jamboree
from jamboree.handlers.default import DataHandler
from jamboree.utils.support.search import querying
from loguru import logger

from darwin_ml.handlers import PriceStateTransformer
from darwin_ml.technical import fiboacci_general, fibonacci

warnings.simplefilter(action='ignore', category=FutureWarning)


class TAPriceData(DataHandler):
    """
        # TAPriceData

        A way to store ta_features for the.
    """
    def __init__(self):
        super().__init__()
        self['category'] = "markets"
        self['submetatype'] = "technical"

"""
def pick(self, _id: str):
self.clear()
current_search = self.search
item = current_search.pick(_id)
if item is None:
    raise AttributeError("File Metadata doesn't exist")

item = Dict(**item)
reloaded = self.file_from_dict(item)
reloaded.reset()
return reloaded
"""


class TAPredictionTransformer(PriceStateTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ta_price = TAPriceData()

    @property
    def features(self) -> TAPriceData:
        """TAPrice Data

        Raises:
            AttributeError: If there's not metadata loaded in just yet.

        Returns:
            DataHandler -- All of the processed TAInformation.
        """
        
        current_model = self.meta_model
        if current_model.name is None:
            raise AttributeError("No price metadata was set yet.")

        
        if self.is_same_meta_model():
            self.__ta_price.time = self.time
            self.__ta_price.episode = self.episode
            self.__ta_price.live = self.live
            return self.__ta_price
        # Uses the default price submetadata
        self.__ta_price.processor = self.processor
        self.__ta_price.time = self.time
        self.__ta_price.episode = self.episode
        self.__ta_price.live = self.live
        
        self.__ta_price['name'] = current_model.name
        self.__ta_price['category'] = current_model.category
        self.__ta_price['subcategories'] = current_model.subcategories
        self.__ta_price['metatype'] = current_model.metatype
        self.__ta_price['abbreviation'] = current_model.abbreviation
        self.__ta_price.reset()
        self.previous_meta_model = current_model
        return self.__ta_price
    
    @property
    def tcount(self) -> int:
        """Get a count of the number of TA Features.

        Returns:
            int -- The number of TA Features
        """
        return self.features.count()
    
    @property
    def feature_num(self) -> int:
        """Get a count of the number of TA Features.

        Returns:
            int -- The number of TA Features
        """
        return self.features.count()

    def preprocess_existing_price_info(self):
        curr_time = self.current_time
        self.time.head = time.time()
        df = self.price.dataframe_from_dynamic_peak(1, 100000)
        ta_features = fiboacci_general(df, target="close", high="high", _open="open", low="low", volume="volume", adj_close="adj_close")
        self.features.store_time_df(ta_features)
        self.time.head = curr_time

    def _reset_big_ta_preprocessing(self):
        """Preprocesses all price data
        """
        if not self.live:
            # check to see if we've already created all of the ta features for the given asset.
            logger.warning("This episode is not live")
            logger.success("We are running ta featurization.")
            logger.error(f"Number of features={self.feature_num}")
            if self.price.count() != 0:
                logger.critical("Creating technical analysis information")
                self.preprocess_existing_price_info()

    def _reset_price(self):
        """Resets the price information as a
        """
        if self.meta.name is None:
            # Load information here
            self.meta_model
            self.features
            
    def reset(self):
        self._reset_price()
        self._reset_big_ta_preprocessing()


if __name__ == "__main__":
    episode = uuid.uuid4().hex
    state_trans = TAPredictionTransformer()
    state_trans.asset = "80de790b2d024654b76de0e76a623bcf"
    state_trans.processor = Jamboree()
    state_trans.episode = episode
    state_trans.live = False
    # logger.success(state_trans.current_time)
    # logger.info(state_trans.meta_model)
    state_trans.reset()
    # logger.success(state_transformer.everything)
    # logger.warning(state_trans.step().prediction_array())
