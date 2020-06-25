from typing import Dict, Optional

import torch
from overrides import overrides

from ...common.checks import ConfigurationError
from ...data import Vocabulary
from .default import PredictionPostprocessor


class MulticlassPostprocessor(PredictionPostprocessor):
    def __init__(
        self,
        named_thresholds: Optional[Dict[str, float]] = None,
        default_threshold: float = -1.0,
        default_label: Optional[str] = None,
    ):
        super().__init__(named_thresholds=named_thresholds, default_threshold=default_threshold)
        if (named_thresholds is not None or self._default_threshold > 0) and default_label is None:
            raise ConfigurationError(
                "If you set the default_threshold > 0 or any named_thresholds, "
                "you should provide a default_label to fallback to"
            )
        self._default_label: Optional[str] = default_label

    @overrides  # type: ignore
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        logits = torch.where(logits >= self.thresholds, logits, torch.tensor([0.0]))
        _, max_indexes = logits.max(dim=-1)  # type: ignore
        prediction = torch.zeros_like(logits)
        prediction[torch.arange(len(max_indexes)), max_indexes] = 1.0
        return prediction

    def index_with(self, vocab: Vocabulary, label_namespace: str = "labels") -> None:
        super().index_with(vocab, label_namespace)
        if self._default_label is not None:
            self.thresholds[0, self._label_to_index[self._default_label]] = -1
