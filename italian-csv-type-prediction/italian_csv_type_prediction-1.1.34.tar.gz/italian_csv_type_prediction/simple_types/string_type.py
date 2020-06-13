from .simple_type import SimpleTypePredictor
from .float_type import FloatType

class StringType(SimpleTypePredictor):

    def __init__(self):
        self._float_predictor = FloatType()

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a string"""
        return not self._float_predictor.validate(candidate) and isinstance(candidate, str)