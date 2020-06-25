import logging
import random
from collections import deque
from typing import Deque, Iterable, List, Optional, Tuple

from overrides import overrides

from vtorch.common.checks import ConfigurationError
from vtorch.common.utils import lazy_groups_of
from vtorch.data.dataset import Batch
from vtorch.data.fields import MetadataField
from vtorch.data.instance import Instance
from vtorch.data.iterators.data_iterator import DataIterator
from vtorch.data.vocabulary import Vocabulary

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def sort_by_padding_reverse(
    instances: List[Instance],
    fields_with_pretrained_tokenizers: List[str],
    sorting_keys: List[Tuple[str, str]],
    vocab: Vocabulary,
) -> List[Instance]:
    """
    Sorts the instances by their padding lengths, using the keys in
    ``sorting_keys`` (in the order in which they are provided).  ``sorting_keys`` is a list of
    ``(field_name, padding_key)`` tuples.
    """
    instances_with_lengths = []
    for serial_index, instance in enumerate(instances):
        instance.index_fields(vocab, fields_with_pretrained_tokenizers, serial_index)
        padding_lengths = instance.get_padding_lengths()
        instance.add_field(
            "sequence_length",
            MetadataField([padding_lengths[field_name][padding_key] for (field_name, padding_key) in sorting_keys]),
            vocab=vocab,
        )
        instances_with_lengths.append(instance)
    instances_with_lengths.sort(key=lambda x: x["sequence_length"].metadata, reverse=True)  # type: ignore
    return instances_with_lengths


class BucketIterator(DataIterator):
    """
    An iterators which by default, pads batches with respect to the maximum input lengths `per
    batch`. Additionally, you can provide a list of field names and padding keys which the dataset
    will be sorted by before doing this batching, causing inputs with similar length to be batched
    together, making computation more efficient (as less time is wasted on padded elements of the
    batch).
    Parameters
    ----------
    sorting_keys : List[Tuple[str, str]]
        To bucket inputs into batches, we want to group the instances by padding length, so that we
        minimize the amount of padding necessary per batch. In order to do this, we need to know
        which fields need what type of padding, and in what order.
        For example, ``[("sentence1", "num_tokens"), ("sentence2", "num_tokens"), ("sentence1",
        "num_token_characters")]`` would sort a dataset first by the "num_tokens" of the
        "sentence1" field, then by the "num_tokens" of the "sentence2" field, and finally by the
        "num_token_characters" of the "sentence1" field.
        documentation somewhere that gives the standard padding keys used by different fields.
    biggest_batch_first : bool, optional (default=False)
        This is largely for testing, to see how large of a batch you can safely use with your GPU.
        This will let you try out the largest batch that you have in the data `first`, so that if
        you're going to run out of memory, you know it early, instead of waiting through the whole
        epoch to find out at the end that you're going to crash.
        Note that if you specify ``max_instances_in_memory``, the first batch will only be the
        biggest from among the first "max instances in memory" instances.
    batch_size : int, optional, (default = 32)
        The size of each batch of instances yielded when calling the iterators.
    batch_first : ``bool`` (default = ``False``)
            For many pytorch implementation batch_first=``False`` is default setting.
            Change it if you need.
    instances_per_epoch : int, optional, (default = None)
        See :class:`BasicIterator`.
    max_instances_in_memory : int, optional, (default = None)
        See :class:`BasicIterator`.
    maximum_samples_per_batch : ``Tuple[str, int]``, (default = None)
        See :class:`BasicIterator`.
    """

    def __init__(
        self,
        sorting_keys: List[Tuple[str, str]],
        biggest_batch_first: bool = False,
        batch_size: int = 32,
        batch_first: bool = False,
        use_sampling: bool = False,
        instances_per_epoch: Optional[int] = None,
        max_instances_in_memory: Optional[int] = None,
        cache_instances: bool = False,
        track_epoch: bool = False,
        maximum_samples_per_batch: Optional[Tuple[str, int]] = None,
        fields_with_pretrained_tokenizers: Optional[List[str]] = None,
    ) -> None:
        if not sorting_keys:
            raise ConfigurationError("BucketIterator requires sorting_keys to be specified")

        super().__init__(
            cache_instances=cache_instances,
            track_epoch=track_epoch,
            batch_first=batch_first,
            batch_size=batch_size,
            instances_per_epoch=instances_per_epoch,
            max_instances_in_memory=max_instances_in_memory,
            maximum_samples_per_batch=maximum_samples_per_batch,
            fields_with_pretrained_tokenizers=fields_with_pretrained_tokenizers,
        )
        self._sorting_keys = sorting_keys
        self._biggest_batch_first = biggest_batch_first
        self._use_sampling = use_sampling

    @overrides  # type: ignore
    def _create_batches(self, instances: Iterable[Instance], shuffle: bool) -> Iterable[Batch]:
        for instance_list in self._memory_sized_lists(instances):
            sampled_instances = []
            if self._use_sampling:
                for instance in instance_list:
                    if isinstance(instance.get("sampling_rate"), MetadataField) and isinstance(
                        instance["sampling_rate"].metadata,  # type: ignore
                        float,
                    ):
                        if random.random() < instance["sampling_rate"].metadata:  # type: ignore
                            sampled_instances.append(instance)
            else:
                sampled_instances = instance_list

            if self.vocab is not None:
                sampled_instances = sort_by_padding_reverse(
                    sampled_instances, self._fields_with_pretrained_tokenizers, self._sorting_keys, self.vocab
                )
            else:
                raise ConfigurationError("You should set vocab before creating batches.")
            batches = self._form_batches(sampled_instances)
            batches = self._biggest_batch_first_and_shuffle(batches, shuffle)

            yield from batches

    def _form_batches(self, sampled_instances: List[Instance]) -> List[Batch]:
        batches = []
        excess: Deque[Instance] = deque()
        for batch_instances in lazy_groups_of(iter(sampled_instances), self._batch_size):
            for possibly_smaller_batches in self._ensure_batch_is_sufficiently_small(batch_instances, excess):
                batches.append(Batch(possibly_smaller_batches))
        if excess:
            batches.append(Batch(excess))
        return batches

    def _biggest_batch_first_and_shuffle(self, batches: List[Batch], shuffle: bool) -> List[Batch]:
        move_to_front = self._biggest_batch_first and len(batches) > 1
        if move_to_front:
            # We'll actually pop the last _two_ batches, because the last one might not be full.
            batches.reverse()
            last_batch = batches.pop()
            penultimate_batch = batches.pop()
        if shuffle:
            # NOTE: if shuffle is false, the data will still be in a different order
            # because of the bucket sorting.
            random.shuffle(batches)
        if move_to_front:
            batches.insert(0, penultimate_batch)  # type: ignore
            batches.insert(0, last_batch)  # type: ignore
        return batches
