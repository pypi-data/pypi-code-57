from typing import Dict
from ..utils import TranslateType


class Extractor:

    def __init__(self, translator: TranslateType = None):
        self._translator = translator

    def extract(self, candidate: str, candidate_type: str, **kwargs) -> Dict:
        raise NotImplementedError(
            "This method must be implemented in the child classes.")

    @property
    def name(self):
        """Return type identified by this predictor."""
        return self.__class__.__name__[:-9]

    def _build_placeholder(self, candidate: str, values: Dict) -> str:
        if len(values)==1:
            return "{{{0}}}".format(list(values.keys())[0])
        for key, values in values.items():
            for value in values:
                candidate = candidate.replace(value, "{{{0}}}".format(key), 1)
        return candidate

    def build_dictionary(self, candidate: str, values: Dict) -> str:
        values = {
            (self._translator.translate(key) if self._translator is not None else key): value
            for key, value in values.items()
        }
        return {
            "placeholder": self._build_placeholder(candidate, values),
            "values": values
        }
