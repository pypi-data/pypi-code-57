from typing import Sequence, Tuple

import torch
from torch import nn


class SelfAttention(nn.Module):  # type: ignore
    one_const: torch.Tensor

    def __init__(self, hidden_size: int, batch_first: bool = False) -> None:
        super(SelfAttention, self).__init__()

        self.hidden_size = hidden_size
        self.batch_first = batch_first

        self.att_weights = nn.Parameter(torch.zeros((1, hidden_size)), requires_grad=True)
        nn.init.xavier_uniform_(self.att_weights.data)
        self.register_buffer("one_const", torch.tensor([[1.0]]))

    def get_mask(self) -> None:
        pass

    def forward(  # type: ignore
        self, inputs: torch.Tensor, lengths: Sequence[int]
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.batch_first:
            batch_size, max_len = inputs.size()[:2]
        else:
            max_len, batch_size = inputs.size()[:2]
            inputs = inputs.permute(1, 0, 2)

        # apply attention layer
        weights = torch.bmm(
            inputs,
            self.att_weights.permute(1, 0)  # (1, hidden_size)  # (hidden_size, 1)
            .unsqueeze(0)  # (1, hidden_size, 1)
            .repeat(batch_size, 1, 1),  # (batch_size, hidden_size, 1)
        )

        attentions = torch.softmax(torch.relu(weights.squeeze()), dim=-1)

        # create mask based on the sentence lengths
        mask = self.one_const.repeat(attentions.size())
        for i, l in enumerate(lengths):  # skip the first sentence
            if l < max_len:
                mask[i, l:] = 0

        # apply mask and renormalize attention scores (weights)
        masked = attentions * mask
        _sums = masked.sum(-1).unsqueeze(-1)  # sums per row

        attentions = torch.div(masked, _sums)

        # apply attention weights
        weighted = torch.mul(inputs, attentions.unsqueeze(-1).expand_as(inputs))

        # get the final fixed vector representations of the sentences
        representations = weighted.sum(1).squeeze().view(batch_size, self.hidden_size)

        return representations, attentions
