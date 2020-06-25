import torch
from overrides import overrides

from .default import PredictionPostprocessor


class MultilabelPostprocessor(PredictionPostprocessor):
    @overrides  # type: ignore
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        thresholds_with_logits_shape = torch.ones_like(logits) * self.thresholds
        predictions: torch.Tensor = torch.where(
            logits >= thresholds_with_logits_shape, torch.tensor([1.0]), torch.tensor([0.0])
        )
        return predictions
