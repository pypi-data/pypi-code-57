from typing import Dict, List, Optional, TypeVar

import torch
from overrides import overrides
from transformers import PreTrainedTokenizer

from ..preprocessors import Preprocessor
from ..vocabulary import Vocabulary
from .field import Field

T = TypeVar("T", bound="TextField")


class TextField(Field):
    """
    A ``TextField`` is a field for text storage. Moreover, the text is preprocessed and tokenized here.
    Available other methods as for base class ``Field``

    Parameters:
    ------------
    text: ``str``
        Raw text
    preprocessor:
        An object for text preprocessing. Should have ``preprocess`` method which returns ``str``
    tokenizer: ``Tokenizer``
        An object for text tokenization. Should have ``tokenize`` method which returns ``List[str]``
    max_padding_length: ``int`` (default = None)
        Maximum length for the padded sequence
    text_namespace: ``str`` (default = "text")
        The namespace to use for converting tokens into integers. We map tokens to
        integers for you (e.g., "I" and "am" get converted to 0, 1, ...),
        and this namespace tells the ``Vocabulary`` object which mapping from strings to integers
        to use.
    """

    def __init__(
        self,
        text: str,
        preprocessor: Preprocessor,
        tokenizer: PreTrainedTokenizer,
        max_padding_length: Optional[int] = None,
        text_namespace: str = "text",
    ) -> None:
        self.text: Optional[str] = text
        self._text_namespace = text_namespace
        self._preprocessor = preprocessor
        self._tokenizer = tokenizer
        self._max_padding_length = max_padding_length

        self._tokenized_text: Optional[List[str]] = None
        self._indexed_tokens: Optional[List[int]] = None

    def _preprocess(self, text: str) -> str:
        return self._preprocessor.preprocess(text)

    def _tokenize(self, text: str) -> List[str]:
        return self._tokenizer.tokenize(text=text)

    def _prepare(self, use_pretrained_tokenizer: bool = False) -> None:
        if self.text is None:
            raise RuntimeError("After tokenization text is deleted for memory efficiency.")
        preprocessed_text = self._preprocess(self.text)
        self._tokenized_text = self._tokenize(preprocessed_text)
        if use_pretrained_tokenizer:
            self._indexed_tokens = self._tokenizer.convert_tokens_to_ids(self._tokenized_text)

    @overrides  # type: ignore
    def count_vocab_items(self, counter: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
        if self._tokenized_text is None:
            self._prepare()
        if self._tokenized_text is None:
            raise RuntimeError("You must tokenize text before count_vocab_items")
        for token in self._tokenized_text:
            counter[self._text_namespace][token] += 1
        return counter

    @overrides  # type: ignore
    def index(self, vocab: Vocabulary, use_pretrained_tokenizer: bool = False) -> None:
        if self._indexed_tokens is None:
            self._prepare(use_pretrained_tokenizer)

        if self._tokenized_text is None:
            raise RuntimeError("You must tokenize text before token indexing")
        if not use_pretrained_tokenizer:
            self._indexed_tokens = [
                vocab.get_token_index(token, self._text_namespace) for token in self._tokenized_text
            ]

        self._tokenized_text = None
        self.text = None

    @overrides  # type: ignore
    def get_padding_lengths(self) -> Dict[str, int]:
        if self._indexed_tokens is None:
            raise RuntimeError("You must call .index(vocabulary) on a field before determining padding lengths.")
        if self._max_padding_length is not None:
            return {"num_tokens": min(len(self._indexed_tokens), self._max_padding_length)}
        return {"num_tokens": len(self._indexed_tokens)}

    def sequence_length(self) -> int:
        if self._indexed_tokens is None:
            raise RuntimeError("You must call .index(vocabulary) on a field before determining padding lengths.")
        return len(self._indexed_tokens)

    @overrides  # type: ignore
    def as_tensor(self, padding_length: Dict[str, int]) -> torch.Tensor:
        if self._indexed_tokens is None:
            raise RuntimeError("You must index fields before 'as_tensor' applying")
        if self.sequence_length() >= padding_length["num_tokens"]:
            return torch.tensor(self._indexed_tokens[: padding_length["num_tokens"]], dtype=torch.long)
        n_padded_elements = padding_length["num_tokens"] - self.sequence_length()
        return torch.cat(
            [torch.tensor(self._indexed_tokens, dtype=torch.long), torch.zeros([n_padded_elements], dtype=torch.long)]
        )

    @overrides  # type: ignore
    def batch_tensors(self, tensor_list: List[torch.Tensor], batch_first: bool = False) -> torch.Tensor:
        if batch_first:
            return torch.stack(tensor_list)
        return torch.stack(tensor_list).transpose(0, 1)

    def __len__(self) -> int:
        if self._indexed_tokens is None:
            raise RuntimeError("You can't get `len` without indexing field. Returns number of tokens.")
        return len(self._indexed_tokens)

    def __str__(self) -> str:
        if self.text is None:
            raise RuntimeError("You can't get `str` after indexing field. Original text was deleted.")
        return self.text
