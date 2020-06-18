from codicefiscale import codicefiscale
from .string_type import StringType


class ItalianFiscalCodeType(StringType):

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches rules for Codice Fiscale values."""
        return super().validate(candidate, **kwargs) and codicefiscale.is_valid(candidate)