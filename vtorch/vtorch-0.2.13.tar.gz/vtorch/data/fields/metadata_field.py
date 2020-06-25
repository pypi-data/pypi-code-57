from typing import Any, Dict, Iterable, List

import torch
from overrides import overrides

from .field import Field


class MetadataField(Field):
    """
    A ``MetadataField`` is a ``Field`` that does not get converted into tensors.  It just carries
    side information that might be needed later on, for computing some third-party metric, or
    outputting debugging information, or whatever else you need.  We use this in the BiDAF model,
    for instance, to keep track of question IDs and passage token offsets, so we can more easily
    use the official evaluation script to compute metrics.
    We don't try to do any kind of smart combination of this field for batched input - when you use
    this ``Field`` in a model, you'll get a list of metadata objects, one for each instance in the
    batch.
    Parameters
    ----------
    metadata : ``Any``
        Some object containing the metadata that you want to store.  It's likely that you'll want
        this to be a dictionary, but it could be anything you want.
    """

    def __init__(self, metadata: Any) -> None:
        self.metadata = metadata

    def __getitem__(self, key: str) -> Any:
        try:
            return self.metadata[key]
        except TypeError:
            raise TypeError("your metadata is not a dict")

    def __setitem__(self, key: str, value: Any) -> None:
        try:
            self.metadata[key] = value
        except TypeError:
            raise TypeError("your metadata is not a dict")

    def __iter__(self) -> Iterable[Any]:
        try:
            return iter(self.metadata)
        except TypeError:
            raise TypeError("your metadata is not iterable")

    def __len__(self) -> int:
        try:
            return len(self.metadata)
        except TypeError:
            raise TypeError("your metadata has no length")

    @overrides  # type: ignore
    def get_padding_lengths(self) -> Dict[str, int]:
        return {}

    @overrides  # type: ignore
    def as_tensor(self, padding_lengths: Dict[str, int]) -> torch.Tensor:
        if isinstance(self.metadata, int):
            return torch.tensor(self.metadata, dtype=torch.int64)
        elif isinstance(self.metadata, list):
            return torch.tensor(self.metadata, dtype=torch.long)
        else:
            return torch.tensor([], dtype=torch.long)

    @overrides  # type: ignore
    def batch_tensors(self, tensor_list: List[torch.Tensor], batch_first: bool = False) -> torch.Tensor:
        return torch.stack(tensor_list).view(-1)

    def __str__(self) -> str:
        return f"MetadataField (print field.metadata to see specific information)."

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MetadataField):
            return NotImplemented
        return self.metadata == other.metadata
