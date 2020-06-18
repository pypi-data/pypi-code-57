from .string_type import StringType
from .set_type_predictor import SetTypePredictor
from ..datasets import load_surnames
from codicefiscale import codicefiscale


class SurnameType(StringType):

    def __init__(self, **kwargs):
        """Create new surname type predictor."""
        super().__init__()
        self._predictor = SetTypePredictor(
            load_surnames(), normalize_values=True, **kwargs)

    @property
    def fuzzy(self):
        return True

    def validate(self, candidate, fiscal_code: str = None, **kwargs) -> bool:
        """Return boolean representing if given candidate is a valid italian surname."""
        if not super().validate(candidate, **kwargs):
            return False
        if fiscal_code is None:
            return self._predictor.validate(candidate)

        characters = codicefiscale.decode(
            fiscal_code
        )["raw"]["surname"]

        code = codicefiscale.decode(
            codicefiscale.encode(surname=candidate, name="XXXXXXXXXXX", sex='M', birthdate='01/01/1990', birthplace='Roma')
        )["raw"]["surname"]

        return code == characters