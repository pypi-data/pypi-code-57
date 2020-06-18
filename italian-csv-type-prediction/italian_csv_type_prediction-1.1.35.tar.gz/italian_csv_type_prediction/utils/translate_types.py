import compress_json
import pandas as pd
from typing import Tuple, List, Union


class TranslateType:

    def __init__(self, language: str = "it"):
        """Create new object to translate types to given language."""
        self._translations = compress_json.local_load(
            "{}.json".format(language)
        )
        self._reverse_translations = {
            v: k
            for k, v in self._translations.items()
        }

    def translate(self, value_type: Union[List, Tuple]) -> str:
        """Return value type translated to given language."""
        if isinstance(value_type, (list, tuple)):
            return tuple([
                self.translate(v)
                for v in value_type
            ])
        return self._translations[value_type]

    def reverse_translate(self, value_type: Union[List, Tuple]) -> str:
        """Return value type translated back to english from given language."""
        if isinstance(value_type, (list, tuple)):
            return tuple([
                self._reverse_translations(v)
                for v in value_type
            ])
        return self._reverse_translations[value_type]

    def translate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Translate all dataframe."""
        return df.applymap(self.translate)
