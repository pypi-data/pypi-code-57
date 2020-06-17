""" Inheriting from this class means that this member can be converted into a DataFrame. """

from dataclasses import dataclass
from abc import abstractmethod
import pandas as pd


@dataclass
class MapObjectDf:

    @abstractmethod
    def df(self) -> pd.DataFrame:
        """ """
        raise NotImplementedError
