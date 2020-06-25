import logging
from typing import Dict, Optional

import torch
from overrides import overrides

from ...common.checks import ConfigurationError
from ..vocabulary import Vocabulary
from .field import Field

logger = logging.getLogger(__name__)


class LabelField(Field):
    """
    A ``LabelField`` is a categorical label of some kind, where the labels are either strings of
    text or 0-indexed integers (if you wish to skip indexing by passing skip_indexing=True).
    If the labels need indexing, we will use a :class:`Vocabulary` to convert the string labels
    into integers.
    This field will get converted into an integer index representing the class label.
    Parameters
    ----------
    label : ``str``
    label_namespace : ``str``, optional (default="labels")
        The namespace to use for converting label strings into integers.  We map label strings to
        integers for you (e.g., "entailment" and "contradiction" get converted to 0, 1, ...),
        and this namespace tells the ``Vocabulary`` object which mapping from strings to integers
        to use (so "entailment" as a label doesn't get the same integer id as "entailment" as a
        word).  If you have multiple different label fields in your data, you should make sure you
        use different namespaces for each one, always using the suffix "labels" (e.g.,
        "passage_labels" and "question_labels").
    """

    def __init__(self, label: str, label_namespace: str = "labels") -> None:
        self.label = label
        self._label_namespace = label_namespace
        self._label_id: Optional[int] = None

        if not isinstance(label, str):
            raise ValueError(f"LabelFields expects string label. Found label: {self.label} of type {type(self.label)}")

    @overrides  # type: ignore
    def get_padding_lengths(self) -> Dict[str, int]:  # pylint: disable=no-self-use
        return {}

    @overrides  # type: ignore
    def count_vocab_items(self, counter: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
        if self._label_id is None:
            counter[self._label_namespace][self.label] += 1
        return counter

    @overrides  # type: ignore
    def index(self, vocab: Vocabulary, use_pretrained_tokenizer: bool = False) -> None:
        if self._label_id is None:
            self._label_id = vocab.get_token_index(self.label, self._label_namespace)

    @overrides  # type: ignore
    def as_tensor(self, padding_lengths: Dict[str, int]) -> torch.Tensor:
        if self._label_id is None:
            raise ConfigurationError("You can't get tensor, you should .index field before.")
        tensor = torch.tensor(self._label_id, dtype=torch.long)
        return tensor

    @overrides  # type: ignore
    def __str__(self) -> str:
        return f"LabelField with label: {self.label} in namespace: '{self._label_namespace}'.'"
