from .integer_type import IntegerType
from .set_type_predictor import SetTypePredictor
from ..datasets import load_caps


class ItalianZIPCodeType(SetTypePredictor):

    def __init__(self):
        """Create new Italian ZIP Code type predictor based on regex."""
        self._integer = IntegerType()
        super().__init__([
            self.convert(e)
            for e in load_caps()
        ])

    def convert(self, candidate) -> str:
        """Convert given candidate to CAP."""
        if self._integer.validate(candidate):
            candidate = self._integer.convert(candidate)
        return str(candidate)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for CAP values."""
        return super().validate(self.convert(candidate))