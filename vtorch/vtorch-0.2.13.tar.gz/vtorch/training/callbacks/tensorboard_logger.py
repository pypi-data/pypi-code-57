import logging
import os
from typing import Dict, Iterable, Optional, Tuple

import torch
from torch.utils.tensorboard import SummaryWriter


class TfLogger:
    def __init__(self, path: str, experiment_name: str, save_grad_w: bool = False) -> None:
        if not os.path.isdir(path):
            os.mkdir(path)
        self._save_grad_w = save_grad_w
        self.summary_writer = SummaryWriter(os.path.join(path, experiment_name))  # type: ignore

    def logging(
        self,
        lr: float,
        train_metrics: Dict[str, float],
        val_metrics: Optional[Dict[str, float]],
        epoch: int,
        named_parameters: Iterable[Tuple[str, torch.nn.Parameter]],
    ) -> None:
        info = {"lr": lr}
        for data_name, metrics_value in [("train", train_metrics), ("val", val_metrics)]:
            if metrics_value is not None:
                for name, value in metrics_value.items():
                    info[f"{data_name}_{name}"] = value
        for tag, value in info.items():
            self.summary_writer.add_scalar(tag, value, epoch)
        if self._save_grad_w:
            for parameter_name, parameter_value in named_parameters:
                parameter_name = parameter_name.replace(".", "/")
                if parameter_value.grad is None:
                    logging.warning(f"{parameter_name} grad will not be saved to tensorboard, because it is None")
                else:
                    self.summary_writer.add_histogram(parameter_name, parameter_value.data.cpu().numpy(), epoch + 1)
                    self.summary_writer.add_histogram(
                        parameter_name + "/grad", parameter_value.grad.data.cpu().numpy(), epoch + 1
                    )

    def close(self) -> None:
        self.summary_writer.close()
