import logging
from typing import Dict, Optional

import torch
from overrides import overrides

from ...common.checks import ConfigurationError
from ..vocabulary import Vocabulary
from .field import Field

logger = logging.getLogger(__name__)


class CategoricalField(Field):
    """
    A ``CategoricalField`` is a categorical label of some kind, where the categories are either strings of
    text or 0-indexed integers (if you wish to skip indexing by passing skip_indexing=True).
    If the categories need indexing, we will use a :class:`Vocabulary` to convert the string categories
    into integers.
    This field will get converted into an integer index representing the class category.
    Parameters
    ----------
    category : ``Union[str, int]``
    category_namespace : ``str``, optional (default="category")
        The namespace to use for converting category strings into integers.  We map category strings to
        integers for you (e.g., "entailment" and "contradiction" get converted to 0, 1, ...),
        and this namespace tells the ``Vocabulary`` object which mapping from strings to integers
        to use (so "entailment" as a label doesn't get the same integer id as "entailment" as a
        word).  If you have multiple different category fields in your data, you should make sure you
        use different namespaces for each one, always using the suffix "category" (e.g.,
        "passage_category" and "question_category").
    """

    def __init__(
        self,
        category: str,
        category_namespace: str = "category",
        one_hot_encoding: bool = True,
        category_to_id: Optional[Dict[str, int]] = None,
    ) -> None:
        self.category = category
        self._one_hot_encoding = one_hot_encoding
        self._category_namespace = category_namespace
        self._category_id: Optional[int] = None
        self._category_to_id = category_to_id
        self._n_categories: Optional[int] = None

        if not isinstance(category, str):
            raise ValueError(f"LabelFields expects string label. Found label: {self.category}")

    @overrides  # type: ignore
    def get_padding_lengths(self) -> Dict[str, int]:  # pylint: disable=no-self-use
        return {}

    @overrides  # type: ignore
    def count_vocab_items(self, counter: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
        if self._category_id is None:
            counter[self._category_namespace][self.category] += 1
        return counter

    @overrides  # type: ignore
    def index(self, vocab: Vocabulary, use_pretrained_tokenizer: bool = False) -> None:
        if self._category_id is None:
            if self._category_to_id is None:
                self._category_id = vocab.get_token_index(self.category, self._category_namespace)
            else:
                self._category_id = self._category_to_id[self.category]

        if not self._n_categories:
            self._n_categories = vocab.get_vocab_size(self._category_namespace)

    @overrides  # type: ignore
    def as_tensor(self, padding_lengths: Dict[str, int]) -> torch.Tensor:
        if self._n_categories is None or self._category_id is None:
            raise ConfigurationError("You can get tensor, need to index field before.")
        if self._one_hot_encoding:
            tensor = torch.zeros(self._n_categories, dtype=torch.float32)
            if self._category_id:
                tensor.scatter_(0, torch.tensor(self._category_id, dtype=torch.long), 1.0)
        else:
            tensor = torch.tensor(self._category_id, dtype=torch.float32)
        return tensor

    @overrides  # type: ignore
    def __str__(self) -> str:
        return f"LabelField with label: {self.category} in namespace: '{self._category_namespace}'.'"
