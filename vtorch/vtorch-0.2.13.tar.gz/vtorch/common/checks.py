"""
Functions and exceptions for checking that
Vtorch and its models are configured correctly.
"""
import logging
from typing import List, Union

from torch import cuda

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """
    The exception raised by any Vtorch object when it's misconfigured
    (e.g. missing properties, invalid properties, unknown properties).
    """

    def __init__(self, message: str) -> None:
        super(ConfigurationError, self).__init__()
        self.message = message

    def __str__(self) -> str:
        return repr(self.message)


def check_for_gpu(device_id: Union[int, List[int]]) -> None:
    if isinstance(device_id, list):
        for did in device_id:
            check_for_gpu(did)
    elif device_id is not None and device_id >= 0:
        num_devices_available = cuda.device_count()
        if num_devices_available == 0:
            raise ConfigurationError(
                "Experiment specified a GPU but none is available;"
                " if you want to run on CPU use the override"
                " 'trainer.cuda_device=-1' in the json config file."
            )
        elif device_id >= num_devices_available:
            raise ConfigurationError(
                f"Experiment specified GPU device {device_id}"
                f" but there are only {num_devices_available} devices "
                f" available."
            )
