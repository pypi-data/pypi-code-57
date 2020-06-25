"""
Helper functions for Trainers
"""
import datetime
import logging
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Tuple, Union

import torch

from ..nn import utils as nn_util

if TYPE_CHECKING:
    from ..models.model import Model

logger = logging.getLogger(__name__)


def move_optimizer_to_cuda(optimizer: torch.optim.Optimizer) -> None:  # type: ignore
    """
    Move the optimizer state to GPU, if necessary.
    After calling, any parameter specific state in the optimizer
    will be located on the same device as the parameter.
    """
    for param_group in optimizer.param_groups:
        for param in param_group["params"]:
            if param.is_cuda:
                param_state = optimizer.state[param]
                for k in param_state.keys():
                    if isinstance(param_state[k], torch.Tensor):
                        param_state[k] = param_state[k].cuda(device=param.get_device())


def get_batch_size(batch: Union[Dict[str, Any], torch.Tensor]) -> int:
    """
    Returns the size of the batch dimension. Assumes a well-formed batch,
    returns 0 otherwise.
    """
    if isinstance(batch, torch.Tensor):
        return batch.size(0)  # type: ignore
    elif isinstance(batch, Dict):
        return get_batch_size(next(iter(batch.values())))
    return 0


def time_to_str(timestamp: int) -> str:
    """
    Convert seconds past Epoch to human readable string.
    """
    datetimestamp = datetime.datetime.fromtimestamp(timestamp)
    return "{:04d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}".format(
        datetimestamp.year,
        datetimestamp.month,
        datetimestamp.day,
        datetimestamp.hour,
        datetimestamp.minute,
        datetimestamp.second,
    )


def str_to_time(time_str: str) -> datetime.datetime:
    """
    Convert human readable string to datetime.datetime.
    """
    pieces: Any = [int(piece) for piece in time_str.split("-")]
    return datetime.datetime(*pieces)


def enable_gradient_clipping(model: "Model", grad_clipping: float) -> None:
    for parameter in model.parameters():
        if parameter.requires_grad:
            parameter.register_hook(
                lambda grad: nn_util.clamp_tensor(grad, minimum=-grad_clipping, maximum=grad_clipping)
            )


def get_metrics(model: "Model", total_loss: float, num_batches: int, reset: bool = False) -> Dict[str, float]:
    """
    Gets the metrics but sets ``"loss"`` to
    the total loss divided by the ``num_batches`` so that
    the ``"loss"`` metric is "average loss per batch".
    """
    metrics = model.get_metrics(reset=reset)
    metrics["loss"] = float(total_loss / num_batches) if num_batches > 0 else 0.0
    return metrics


def prepare_parameters_group(
    named_model_parameters: Iterator[Tuple[str, torch.nn.Parameter]],
    base_lr: float,
    additional_lr: float,
    additional_lr_sub_strings: List[str],
    no_decay_layers_sub_strings: List[str],
    weight_decay: float,
) -> List[Dict[str, Union[float, torch.nn.Parameter]]]:
    parameters_with_lr_and_wd: List[Dict[str, Union[float, torch.nn.Parameter]]] = []
    for parameter_name, parameter_value in named_model_parameters:
        if any(sub_string in parameter_name for sub_string in additional_lr_sub_strings):
            lr = additional_lr
        else:
            lr = base_lr
        if any(sub_string in parameter_name for sub_string in no_decay_layers_sub_strings):
            wd = 0.0
        else:
            wd = weight_decay
        parameters_with_lr_and_wd.append({"params": parameter_value, "lr": lr, "weight_decay": wd})
    return parameters_with_lr_and_wd
