from .simple_type import SimpleTypePredictor
from .set_type_predictor import SetTypePredictor
from ..datasets import load_boolean


class BooleanType(SimpleTypePredictor):

    def __init__(self):
        """Create new float type predictor based on regex."""
        super().__init__()
        self._predictor = SetTypePredictor(
            load_boolean(), normalize_values=True)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a valid region."""
        return self._predictor.validate(candidate)
