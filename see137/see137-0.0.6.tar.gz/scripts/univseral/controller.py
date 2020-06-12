import uuid
from typing import Any, Dict, List

import maya
import pandas as pd
import yfinance as yf
from addict import Dict as ADDict
from anycache import anycache
from jamboree import Jamboree
from jamboree.handlers import DataHandler, MultiDataManagement
from jamboree.handlers.abstracted.datasets.price import PriceData
from loguru import logger


@anycache(cachedir='/tmp/anycache.my')
def get_dataset_info(ds_str: str):
    # ds_str = " ".join(ds_list)
    ticker = yf.Ticker(ds_str)

    return ticker.info


@anycache(cachedir='/tmp/anyticker.my')
def get_ticker_data(ds_str: str):
    data = yf.download(ds_str, group_by='ticker').dropna()
    return data


class CallablePriceData(PriceData):
    def __init__(self):
        super().__init__()
        self.forced_subcategories = ['market', 'country', 'sector', 'exchange']
        self.specs = [
            'market', 'country', 'sector', 'exchange', 'abbreviation', 'name'
        ]

    def __call__(self,
                 name: str,
                 abbv: str,
                 market: str = "crypto",
                 country: str = "US",
                 sector: str = "technology",
                 exchange: str = "coinbase",
                 **kwargs):
        self['name'] = name
        self['abbreviation'] = abbv
        self['subcategories'] = {
            "market": market,
            "country": country,
            "sector": sector,
            "exchange": exchange,
        }

        # TODO: Figure out how to add random search fields.

        # for k, v in kwargs.items():
        #     if k not in self.specs:
        #         self[k] = v
        return self

    def dataframe_from_last(self):
        """ Get a dataframe between a head and tail. Resample according to our settings"""

        values = self.many(ar="relative")
        frame = pd.DataFrame(values)
        frame = self._timestamp_resample_and_drop(frame)
        return frame


class DatasetCommander:
    """ 
        Use this to manage individual datasets. 
        * Create 
    """
    def __init__(self, *args, **kwargs):
        self.processor = Jamboree()
        self.pricedata_management = CallablePriceData()
        self.multi_data = MultiDataManagement()
        self.pricedata_management.processor = self.processor
        self.multi_data.processor = self.processor

    def AllMeta(self) -> List[Dict[str, Any]]:
        """ Get all metadata for datasets """
        return []

    def AllPrice(self) -> List[Dict[str, Any]]:
        """ Get all price metadata out there. """
        _current_search = self.pricedata_management.search
        res = _current_search.find()
        return res

    def AllUniverses(self):
        """
            All Universes

            Get all universes available.
        """
        current_search = self.multi_data.search
        return current_search.find()

    def AttachMetaParams(self, meta_params):
        """ 
            Attach time information and other parameters we need for operations to metadata.

            Use to know when to pull information for a given piece of metadata.

            * Find all metadata IDs that are over current time.
            * Lock current position inside of database
            * Set operation that they're being worked on
            * On pull, update the last time we operated on such data.
        """
        pass

    def RemoveAllPrice(self):
        """Removes all of the price information.

        Finds all of the price information given the supplied information general fields then removes the metadata.

        """
        _current_search = self.pricedata_management.search
        _current_search.remove()

    def GetPriceHandler(self, _id: str):
        """Get Price Handler

        Get a price handler by id. 

        Parameters
        ----------
        _id : str
            metadata id for the price handler. 
        """
        _current_search = self.pricedata_management.search
        full_metadata = _current_search.FindById(_id)
        if not bool(full_metadata):
            return None
        gen = ADDict(**full_metadata)

        self.pricedata_management(name=gen.name,
                                  abbv=gen.abbreviation,
                                  market=gen.subcategories.market,
                                  country=gen.subcategories.country,
                                  sector=gen.subcategories.sector,
                                  exchange=gen.subcategories.exchange)
        self.pricedata_management.reset()
        return self.pricedata_management.copy()
        # print(self.pricedata_management.dataframe_from_last())


def run_dataset_commandments():
    callable_price = CallablePriceData()
    callable_price(name="Blank",
                   abbv="BLK",
                   market="stocks",
                   country="US",
                   sector="technology",
                   exchage="dow jones")
    callable_price.live = False
    callable_price.episode = uuid.uuid4().hex

    # Download assets


if __name__ == "__main__":
    run_dataset_commandments()
