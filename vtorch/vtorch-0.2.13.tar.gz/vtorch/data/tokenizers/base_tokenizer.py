from typing import List

from .tokenizer import Tokenizer


class BaseTokenizer(Tokenizer):
    @staticmethod
    def tokenize(text: str) -> List[str]:
        return text.split()
