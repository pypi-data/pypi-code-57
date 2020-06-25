from typing import TYPE_CHECKING, Dict, Iterable, Optional, Tuple

import torch

if TYPE_CHECKING:
    from .early_stopping import EarlyStopping  # noqa: F401
    from .tensorboard_logger import TfLogger  # noqa: F401


class Callbacks:
    def __init__(
        self, tf_logging: Optional["TfLogger"] = None, early_stopping: Optional["EarlyStopping"] = None
    ) -> None:
        self.tf_logging = tf_logging
        self.early_stopping = early_stopping

    def write_tensorboard_logs(
        self,
        train_metrics: Dict[str, float],
        val_metrics: Optional[Dict[str, float]],
        lr: float,
        epoch: int,
        named_parameters: Iterable[Tuple[str, torch.nn.Parameter]],
    ) -> None:
        if self.tf_logging is not None:
            self.tf_logging.logging(lr, train_metrics, val_metrics, epoch, named_parameters)

    def add_metric(self, val_metrics: Dict[str, float]) -> None:
        if self.early_stopping is not None:
            self.early_stopping.add_metric(val_metrics[self.early_stopping.metric_name])

    def should_stop_early(self) -> bool:
        if self.early_stopping is not None:
            return self.early_stopping.should_stop_early()
        return False

    def is_best_so_far(self) -> bool:
        if self.early_stopping is not None:
            return self.early_stopping.is_best_so_far()
        return True
