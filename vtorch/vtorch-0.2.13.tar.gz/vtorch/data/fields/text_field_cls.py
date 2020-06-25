from typing import Dict, List, Optional, Tuple

import torch
from overrides import overrides
from transformers.tokenization_utils import PreTrainedTokenizer

from ...common.checks import ConfigurationError
from ..preprocessors import Preprocessor
from .text_field import TextField


class TextFieldCLS(TextField):
    """
    A ``TextFieldCLS`` is a field for text storage, used for prepare text for a classification task.
    Moreover, the text is preprocessed and tokenized here.
    Available other methods as for base class ``TextField``

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
    cls_token_at_end: ``bool`` (default = False)
        If `False` place CLS token at start, ``True`` – at end (only for XLNet)
    pad_on_left: ``bool`` (default = False)
        Padding left only for XLNet
    """

    MASK_PADDING_WITH_ZERO = True
    DEFAULT_TEXT_TOKEN_TYPE_ID = 0

    def __init__(
        self,
        text: str,
        preprocessor: Preprocessor,
        tokenizer: PreTrainedTokenizer,
        max_padding_length: Optional[int] = None,
        text_namespace: str = "text",
        object_highlight_token: str = "[",
        cls_token_at_end: bool = False,
        pad_on_left: bool = False,
    ) -> None:
        super().__init__(text, preprocessor, tokenizer, max_padding_length, text_namespace)
        self._obj_token_start_index = self._tokenizer.convert_tokens_to_ids(object_highlight_token)
        self._sep_token_index = self._tokenizer.convert_tokens_to_ids(self._tokenizer.sep_token)
        self._cls_token_index = self._tokenizer.convert_tokens_to_ids(self._tokenizer.cls_token)
        self._pad_token_index = self._tokenizer.convert_tokens_to_ids(self._tokenizer.pad_token)
        self._n_additional_special_tokens = len([self._cls_token_index] + [self._sep_token_index])

        self._cls_token_at_end = cls_token_at_end
        self._pad_on_left = pad_on_left

    @overrides  # type: ignore
    def as_tensor(self, padding_length: Dict[str, int]) -> torch.Tensor:
        indexed_tokens, token_type_ids, attention_mask = self._generate_tokens_for_training(
            padding_length["num_tokens"]
        )

        # token_type x length
        return torch.stack(
            (
                torch.tensor(indexed_tokens, dtype=torch.long),
                torch.tensor(token_type_ids, dtype=torch.long),
                torch.tensor(attention_mask, dtype=torch.long),
            )
        )

    def _generate_tokens_for_training(self, required_length: int) -> Tuple[List[int], List[int], List[int]]:
        if self._indexed_tokens is None:
            raise ConfigurationError("You must index tokens before getting tensor.")
        indexed_tokens_main = self._crop_based_on_object(
            self._indexed_tokens, required_length - self._n_additional_special_tokens
        )

        if self._cls_token_at_end:
            updated_indexed_tokens = indexed_tokens_main + [self._sep_token_index] + [self._cls_token_index]
        else:
            updated_indexed_tokens = [self._cls_token_index] + indexed_tokens_main + [self._sep_token_index]

        attention_mask = [1 if self.MASK_PADDING_WITH_ZERO else 0] * len(updated_indexed_tokens)

        if len(updated_indexed_tokens) < required_length:
            padding_length = required_length - len(updated_indexed_tokens)
            if self._pad_on_left:
                updated_indexed_tokens = [self._pad_token_index] * padding_length + updated_indexed_tokens
                attention_mask = [0 if self.MASK_PADDING_WITH_ZERO else 1] * padding_length + attention_mask
            else:
                updated_indexed_tokens.extend([self._pad_token_index] * padding_length)
                attention_mask.extend([0 if self.MASK_PADDING_WITH_ZERO else 1] * padding_length)

        token_type_ids = [self.DEFAULT_TEXT_TOKEN_TYPE_ID] * len(updated_indexed_tokens)
        return updated_indexed_tokens, token_type_ids, attention_mask

    @overrides  # type: ignore
    def get_padding_lengths(self) -> Dict[str, int]:
        if self._indexed_tokens is None:
            raise ConfigurationError("You must call .index(vocabulary) on a field before determining padding lengths.")
        if self._max_padding_length is not None:
            return {"num_tokens": min(self.sequence_length, self._max_padding_length)}
        return {"num_tokens": self.sequence_length}

    def _crop_based_on_object(self, tokens: List[int], max_length: int) -> List[int]:
        if self._obj_token_start_index in tokens[-max_length:]:
            return tokens[-max_length:]
        return tokens[:max_length]

    @property
    def sequence_length(self) -> int:
        if self._indexed_tokens is None:
            raise ConfigurationError("You must call .index(vocabulary) on a field before determining padding lengths.")

        return len(self._indexed_tokens) + self._n_additional_special_tokens

    @overrides  # type: ignore
    def batch_tensors(self, tensor_list: List[torch.Tensor], batch_first: bool = False) -> torch.Tensor:
        if batch_first:
            # batch x token_type x length
            batch = torch.stack(tensor_list)
        else:
            batch = torch.stack(tensor_list).transpose(1, 2)

        # token_type x batch x length
        return batch.transpose(0, 1)
