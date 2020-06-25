import json
import logging
import os
from typing import List, Optional, Tuple

from ...common.checks import ConfigurationError
from ...data.dataset import Batch
from ...data.instance import Instance
from ...data.iterators import BucketIterator

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BucketIteratorOptimized(BucketIterator):
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

    MAX_BATCH_SIZE = 150

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
        batch_optimization_step_size: int = 10,
        batch_reverse_sort: bool = False,
    ) -> None:
        if not sorting_keys:
            raise ConfigurationError("BucketIterator requires sorting_keys to be specified")

        super().__init__(
            sorting_keys=sorting_keys,
            biggest_batch_first=biggest_batch_first,
            batch_size=batch_size,
            batch_first=batch_first,
            use_sampling=use_sampling,
            instances_per_epoch=instances_per_epoch,
            max_instances_in_memory=max_instances_in_memory,
            cache_instances=cache_instances,
            track_epoch=track_epoch,
            maximum_samples_per_batch=maximum_samples_per_batch,
            fields_with_pretrained_tokenizers=fields_with_pretrained_tokenizers,
        )

        self._batch_optimization_step_size = batch_optimization_step_size
        self._batch_reverse_sort = batch_reverse_sort
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "length_bs_time.json")), "r") as fp:
            self._length_bs_time = json.load(fp)

    @staticmethod
    def _get_max_sequence_length(instances: List[Instance]) -> int:
        return max([instance["sequence_length"].metadata[0] for instance in instances])  # type: ignore

    def _get_new_batch(
        self, current_batch: List[Instance], left_data: List[Instance]
    ) -> Tuple[List[Instance], List[Instance], List[Instance]]:
        # batch could not be bigger then maximum batch size
        if len(current_batch) >= self.MAX_BATCH_SIZE - self._batch_optimization_step_size:
            return (
                current_batch,
                left_data[: self._batch_optimization_step_size],
                left_data[self._batch_optimization_step_size :],
            )
        # add to current batch left data, if its size smaller then _batch_optimization_step_size
        if len(left_data) < self._batch_optimization_step_size + 1:
            return current_batch + left_data, [], []
        batch_max_length = self._get_max_sequence_length(current_batch)
        contender_max_length = self._get_max_sequence_length(left_data[: self._batch_optimization_step_size])
        if (
            self._length_bs_time[f"{contender_max_length}"][
                f"{len(current_batch) + self._batch_optimization_step_size}"
            ]
            > self._length_bs_time[f"{batch_max_length}"][f"{len(current_batch)}"]
            + self._length_bs_time[f"{contender_max_length}"][f"{self._batch_optimization_step_size}"]
        ):
            return (
                current_batch,
                left_data[: self._batch_optimization_step_size],
                left_data[self._batch_optimization_step_size :],
            )
        return self._get_new_batch(
            current_batch + left_data[: self._batch_optimization_step_size],
            left_data[self._batch_optimization_step_size :],
        )

    def _form_batches(self, sampled_instances: List[Instance]) -> List[Batch]:
        batches = []
        if len(sampled_instances) <= self._batch_optimization_step_size:
            return [Batch(sampled_instances)]
        sampled_instances.sort(
            key=lambda x: x["sequence_length"].metadata,  # type: ignore
            reverse=self._batch_reverse_sort,
        )
        current_batch = sampled_instances[: self._batch_optimization_step_size]
        left_data = sampled_instances[self._batch_optimization_step_size :]
        while len(current_batch) > 0:
            final_batch, current_batch, left_data = self._get_new_batch(current_batch, left_data)
            batches.append(Batch(final_batch))

        return batches
