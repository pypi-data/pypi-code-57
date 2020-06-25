import torch
from torch import nn


class MaxPool(nn.Module):  # type: ignore
    zero_const: torch.Tensor
    big_const: torch.Tensor

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("zero_const", torch.tensor([0.0]))
        self.register_buffer("big_const", torch.tensor([1000.0]))

    def forward(self, x: torch.Tensor, batch_first: bool = False) -> torch.Tensor:  # type: ignore
        mask = torch.where(x != 0, self.zero_const, self.big_const)
        x = x - mask
        y = x.max(dim=int(batch_first))[0]
        return y


class MeanPool(nn.Module[torch.Tensor]):
    zero_const: torch.Tensor
    one_const: torch.Tensor

    def __init__(self) -> None:
        super().__init__()
        self.register_buffer("zero_const", torch.tensor([0.0]))
        self.register_buffer("one_const", torch.tensor([1.0]))

    def forward(self, x: torch.Tensor, batch_first: bool = False) -> torch.Tensor:  # type: ignore
        mask = torch.where(x != 0, self.one_const, self.zero_const)
        x = x * mask
        n_ = mask[:, :, 0].sum(dim=int(batch_first))[:, None]
        y = x.sum(dim=int(batch_first))[0]
        y = y / n_
        return y
