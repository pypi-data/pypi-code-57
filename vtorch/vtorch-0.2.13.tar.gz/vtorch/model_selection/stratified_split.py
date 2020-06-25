import collections
from typing import Any, Sequence, Tuple

from sklearn.model_selection import StratifiedShuffleSplit

from ..common.checks import ConfigurationError


class StratifiedSplit:
    def __init__(self, test_share: float, random_state: int = 13, min_class_representatives: int = 5) -> None:
        if not 0 < test_share < 1:
            raise ConfigurationError("test_size should be greater than 0 and lower than 1")
        self._test_share = test_share
        self._random_state = random_state
        self._min_class_representatives = min_class_representatives

    def split(self, data: Sequence[Any], target: Sequence[Any]) -> Tuple[Sequence[Any], Sequence[Any]]:
        unified_classes = [
            tuple(sorted(set(classes))) if self._is_sequence(classes) else tuple([classes]) for classes in target
        ]
        unified_counter = collections.Counter(unified_classes)

        if any(samples_with_tag < self._min_class_representatives for samples_with_tag in unified_counter.values()):
            for i, unified_class in enumerate(unified_classes):
                if unified_counter[unified_class] < self._min_class_representatives:
                    tag_frequencies = [
                        (tag, unified_counter[(tag,)])
                        for tag in unified_class
                        if unified_counter[tag] >= self._min_class_representatives
                    ]
                    if tag_frequencies:
                        unified_classes[i] = (min(tag_frequencies, key=lambda x: x[1])[0],)
                    else:
                        unified_classes[i] = unified_counter.most_common(1)[0][0]
        test_size = int(len(data) * self._test_share)

        # test size could not be less than a number of classes
        test_size = test_size if test_size > len(set(unified_classes)) else len(set(unified_classes))
        splitter = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=self._random_state)
        train_ids, test_ids = next(splitter.split(data, unified_classes))

        train_data = [data[train_id] for train_id in train_ids]
        test_data = [data[test_id] for test_id in test_ids]
        return train_data, test_data

    @staticmethod
    def _is_sequence(object_item: Any) -> bool:
        return isinstance(object_item, collections.Sequence) and not isinstance(object_item, str)
