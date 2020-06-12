import uuid
import time

import maya
import pandas as pd
import pytest
import matplotlib.pyplot as plt
import typing
from stochastic.continuous import FractionalBrownianMotion
from loguru import logger
from jamboree import Jamboree

from darwin_ml.handlers import TAPredictionTransformer


class PriceSetupResponse:
    def __init__(self):
        self.__is_success: bool = False
        self.__metadata_id: typing.Optional[str] = None
        self.__microsoft_frame: Optional[pd.DataFrame] = None
        self.__apple_frame: Optional[pd.DataFrame] = None
    

    @property
    def success(self) -> bool:
        """success is_success property

        Were we able to successfully pull the price information.

        Returns:
            bool: Is_Success
        """
        is_success = self.__is_success and self.is_meta
        return is_success
    
    @success.setter
    def success(self, __success:bool):
        self.__is_success = __success

    @property
    def is_meta(self) -> bool:
        return self.metadata_id is not None


    @property
    def metadata_id(self):
        """metadata_id MetaData

        Metadata ID will be set if and only if the data was appropiately downloaded.

        Returns:
            str: The metadata id.
        """
        return self.__metadata_id
    
    @metadata_id.setter
    def metadata_id(self, _metadata_id:str):
        self.__metadata_id = _metadata_id
    

    @property
    def apple(self) -> pd.DataFrame:
        return self.__apple_frame
    

    @apple.setter
    def apple(self, value):
        self.__apple_frame = value

    @property
    def is_apple(self) -> bool:
        return self.apple is not None


    @property
    def microsoft(self):
        """The microsoft_dataframe property."""
        return self.__microsoft_frame

    @microsoft.setter
    def microsoft(self, value):
        self.__microsoft_frame = value

    @property
    def is_micro(self);
        return self.microsoft is not None




class DefaultPriceMetadataParameters:
    def __init__(self):
        self.category = "markets"
        self.subcategories = {
            "market": "stock",
            "country": "US",
            "sector": "techology",
        }
        self.submetatype = "price"