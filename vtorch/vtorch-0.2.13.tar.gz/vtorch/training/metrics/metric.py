from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Union

import torch

if TYPE_CHECKING:
    from ...predictors.predictions_postprocessing.default import PredictionPostprocessor
    from ...data import Vocabulary


class Metric:
    """
    A very general abstract class representing a metric which can be
    accumulated.
    """

    NAMES: List[str] = []

    def __init__(self, predictions_postprocessor: Optional["PredictionPostprocessor"] = None,) -> None:
        self._predictions_postprocessor = predictions_postprocessor

    def index_with(self, vocab: "Vocabulary", label_namespace: str = "labels") -> None:
        if self._predictions_postprocessor is not None:
            self._predictions_postprocessor.index_with(vocab, label_namespace)

    def __call__(self, predictions: torch.Tensor, gold_labels: torch.Tensor) -> None:
        """
        Parameters
        ----------
        predictions : ``torch.Tensor``, required.
            A tensor of predictions.
        gold_labels : ``torch.Tensor``, required.
            A tensor corresponding to some gold label to evaluate against.
        """
        raise NotImplementedError

    def get_metric(self, reset: bool) -> Dict[str, Union[float, List[float]]]:
        """
        Compute and return the metric. Optionally also call :func:`self.reset`.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """
        Reset any accumulators or internal state.
        """
        raise NotImplementedError

    @staticmethod
    def unwrap_to_tensors(*tensors: torch.Tensor) -> Sequence[torch.Tensor]:
        """
        If you actually passed gradient-tracking Tensors to a Metric, there will be
        a huge memory leak, because it will prevent garbage collection for the computation
        graph. This method ensures that you're using tensors directly and that they are on
        the CPU.
        """
        return [x.detach().cpu() if isinstance(x, torch.Tensor) else x for x in tensors]
