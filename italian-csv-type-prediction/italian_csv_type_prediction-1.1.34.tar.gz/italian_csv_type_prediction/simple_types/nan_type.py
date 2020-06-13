from .string_type import StringType
from .set_type_predictor import SetTypePredictor
from ..datasets import load_nan
import pandas as pd


class NaNType(StringType):

    def __init__(self):
        super().__init__()
        self._predictor = SetTypePredictor(load_nan())

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a NaN."""
        return self._predictor.validate(candidate) or pd.isna(candidate) or super().validate(candidate) and all(
            self._predictor.validate(element)
            for element in set(candidate)
        )
