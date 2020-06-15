"""Implements several general-purpose sampling algorithms."""

from bisect import bisect
from typing import Sequence, List, Callable

__all__ = [
    'sample_discrete_roulette',
    'AliasTable'
]


def sample_discrete_roulette(
        randfloat: Callable[[], float],
        cum_weights: Sequence[float]) -> int:
    """Sample from a given discrete distribution given its cumulative
    weights, using binary search / the roulette wheel
    selection algorithm.

    Args:
        randfloat (Callable[[], float]): A function returning a random
            float in [0.0, 1.0), e.g. ``random.random()``.
            Will only be called once.
        cum_weights (Sequence[float]): The list of cumulative weights.
            These do not need to be normalized, so `cum_weights[-1]`
            does not necessarily have to be 1.0.

    Returns:
        An index into the population from 0 to ``len(cum_weights) - 1``.
    """
    total = cum_weights[-1]
    high = len(cum_weights) - 1
    return bisect(cum_weights, randfloat() * total, 0, high)


class AliasTable(object):
    """Sample from a given discrete distribution given its relative
    weights, using the alias table algorithm.

    Alias tables are slow to construct, but offer increased sampling
    speed compared to the roulette wheel algorithm.

    Construct a table using :meth:`from_weights`.

    Attributes:
        probability (List[float]): The probability row of the table
        alias (List[int]): The alias row of the table
    """

    def __init__(self, probability: Sequence[float], alias: Sequence[int]):
        self.probability: List[float] = probability
        self.alias: List[int] = alias

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.probability == other.probability) and \
                   (self.alias == other.alias)
        return NotImplemented

    def sample(self,
               randbelow: Callable[[int], int],
               randchance: Callable[[float], bool]) -> int:
        """Sample from the alias table.

        Args:
            randbelow (Callable[[int], int]): A function returning a
                random int in [0, `arg`), e.g. ``random.randrange()``.
                Will only be called once per sample.
            randchance (Callable[[float], bool): A function returning
                ``True`` with chance `arg` and ``False`` otherwise,
                e.g. ``lambda arg: random.random() < arg``. Will only
                be called once per sample.

        Returns:
            An index into the population from 0 to ``len(weights) - 1``.
        """
        column = randbelow(len(self.probability))
        return column if randchance(self.probability[column]) else self.alias[column]

    @classmethod
    def from_weights(cls, weights: Sequence[float]):
        """Construct an alias table using a list of relative weights.

        The provided weights need not sum to 1.0."""
        result = cls([], [])

        length = len(weights)
        weights_sum = sum(weights)
        weights = [x / weights_sum for x in weights]
        average = 1.0 / length

        result.probability = [0.0] * length
        result.alias = [0] * length
        small = []
        large = []
        for i, chance in enumerate(weights):
            if chance >= average:
                large.append(i)
            else:
                small.append(i)

        while small and large:
            less = small.pop()
            more = large.pop()

            result.probability[less] = weights[less] * length
            result.alias[less] = more
            new_prob = weights[more] + weights[less] - average
            weights[more] = new_prob
            if new_prob >= average:
                large.append(more)
            else:
                small.append(more)

        while small:
            result.probability[small.pop()] = 1.0

        while large:
            result.probability[large.pop()] = 1.0

        return result
