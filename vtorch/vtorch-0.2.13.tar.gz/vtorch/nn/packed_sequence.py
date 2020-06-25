import torch


def get_last_rnn_state(padded_seq: torch.Tensor, length: torch.Tensor) -> torch.Tensor:
    masks = (length - 1).view(1, -1, 1).expand(int(torch.max(length).item()), padded_seq.size(1), padded_seq.size(2))
    return padded_seq.gather(0, masks)[0]
