from .italian_zip_code_type import ItalianZIPCodeType


class FuzzyItalianZIPCodeType(ItalianZIPCodeType):

    def convert(self, candidate) -> str:
        """Convert given candidate to CAP."""
        return super().convert(candidate).zfill(5)