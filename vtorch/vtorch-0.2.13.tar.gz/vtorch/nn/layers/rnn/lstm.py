from typing import Any

import torch.nn as nn
from overrides import overrides

from .rnn_layer import RNNLayer


class LSTM(RNNLayer, nn.LSTM):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @overrides  # type: ignore
    def get_output_dim(self) -> int:
        return self.hidden_size * (int(self.bidirectional) + 1)
