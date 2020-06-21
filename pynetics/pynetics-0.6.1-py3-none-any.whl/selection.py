# ======================================================================
# pynetics: a simple yet powerful evolutionary computation library
# Copyright (C) 2020 Alberto Díaz-Álvarez
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# “Software”), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ======================================================================
"""Different implementations for some well known selection schemas.
"""
import abc
import math
import random
from typing import Tuple, Iterable, List

from . import api
from .api import Genotype
from .exception import (
    EmptyPopulation,
    CannotSelectThatMany,
    WrongSelectionSize,
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Abstract selection schemas
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
class SelectionSchema(metaclass=abc.ABCMeta):
    """Groups common behavior across all the selection schemas.

    The selection schema is defined as a class. However, it is enough to
    implement it as a selection method, i.e. a function that receives a
    sequence and a number of individuals, and returns a sample of
    individuals of that size from the given population.
    """

    def __init__(self, replacement: bool = False):
        """Creates a new instance of this object.

        :param replacement: If it is allowed to select the same genotype
            more than once. Defaults to False (i.e. selection without
            replacement).
        """
        self.__replacement = replacement

    @property
    def replacement(self):
        """If selection schema is with or without replacement.

        :return: True if is a selection with replacement or False
            otherwise.
        """
        return self.__replacement

    def __call__(
            self,
            population: api.Population,
            n: int
    ) -> Tuple[api.Genotype, ...]:
        """Executes the selection method.

        This method performs some checks to the arguments and delegates
        the implementation to the abstract method
        :func:`~selection.SelectionSchema.do`.

        :param population: The population where genotypes are extracted.
        :param n: The number of genotypes to return.
        :return: A sequence of genotypes.
        :raise: WrongSelectionSize if the number of genotypes to extract
            is zero or negative.
        :raise: EmptyPopulation if the population is empty.
        :raise: CannotSelectThatMany if the number of genotypes to
            extract is bigger than the population size and the selection
            is configures without replacement.
        """
        # The population is not empty
        if len(population) <= 0:
            raise EmptyPopulation()
        # The amount of genotypes to extract is positive
        if n <= 0:
            raise WrongSelectionSize(n)
        # The population isn't smaller than the genotypes to select
        if not self.replacement and len(population) < n:
            raise CannotSelectThatMany(len(population), n)

        # Everything is ok, so perform the selection
        return tuple(self.do(population, n))

    @abc.abstractmethod
    def do(
            self,
            population: api.Population,
            n: int
    ) -> Iterable[api.Genotype]:
        """Executes this particular implementation of selection.

        This method is not called by the base algorithms implemented,
        but from :func:`~selection.SelectionSchema.__call__` instead.
        It should contain the logic of the specific selection schema.

        :param population: The population where genotypes are extracted.
        :param n: The number of genotypes to return.
        :return: A sequence of genotypes.
        """


class WeightedSelectionSchema(SelectionSchema, metaclass=abc.ABCMeta):
    """Generic behaviour to all the weight based schemas."""

    def do(
            self,
            population: api.Population,
            n: int
    ) -> Iterable[api.Genotype]:
        """Implementation of the selection schema.

        :param population: The population where genotypes are extracted.
        :param n: The number of genotypes to return.
        :return: A sequence of genotypes.
        """
        available_genotypes = population[:]
        weights = None
        selected_genotypes: List[Genotype] = []
        while len(selected_genotypes) < n:
            # Recalculate the weights in case no replacement is allowed
            # (because the available genotypes list has changed)
            if weights is None or not self.replacement:
                weights = self.get_weights(genotypes=available_genotypes)

            # Get a random genotype, but weighted by the specific schema
            # implementation
            best = random.choices(available_genotypes, weights=weights, k=1)[0]

            # Add it to the list
            selected_genotypes.append(best)

            # If no replacement is allowed, remove the genotype from the
            # pool of available genotypes.
            if not self.replacement:
                del available_genotypes[available_genotypes.index(best)]

        return selected_genotypes

    @abc.abstractmethod
    def get_weights(
            self, *,
            genotypes: Iterable[api.Genotype],
    ) -> Tuple[float, ...]:
        """Computes as many probabilities as genotypes.

        The probabilities depend completely of the implementing class.

        :param genotypes: The genotypes to select from.
        :return: A tuple with as many frequencies as genotypes in the
            population.
        """


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Selection schemas
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
class ExponentialRank(WeightedSelectionSchema):
    """Selection based on the fitness rank exponentially.

    It's somewhat similar to the roulette wheel method but instead of
    assigning the probability to be selected proportionally to their
    fitness, their probability to be selected is exponentially to their
    position in a rank where the genotypes are ordered accordingly to
    their fitnesses.

    If the beta parameter is 0, the schema is equivalent to the monte
    carlo one, i.e. every chromosome has the same probability to be
    chosen.
    """

    def __init__(self, *, alpha: float = 1, replacement: bool = False):
        """Initializes this object.

        :param alpha: The exponential factor. The weight of a genotype
            will be its position to the alpha, so the bigger the alpha,
            biggest the gap between genotypes.
        :param replacement: If this selection schema is with or without
            replacement.
        """
        super().__init__(replacement=replacement)
        self.alpha = alpha

    def get_weights(
            self, *,
            genotypes: Iterable[api.Genotype]
    ) -> Tuple[float, ...]:
        """Weights will be arranged according to the genotypes position.

        Because the fittest genotype is the last one, the weights will
        be in ascending order.

        :param genotypes: The genotypes (only used to get the number of
            them).
        :return: A tuple with as many frequencies as genotypes in the
            population.
        """
        return tuple(
            math.pow(i, self.alpha) for i, _ in enumerate(genotypes, 1)
        )


class LinearRank(WeightedSelectionSchema):
    """Selection based on the fitness rank proportionally.

    It's somewhat similar to the roulette wheel method but instead of
    assigning the probability to be selected proportionally to their
    fitness, their probability to be selected is proportional to their
    position in a rank where the genotypes are ordered accordingly to
    their fitnesses.

    If the alpha parameter is 0, the schema is equivalent to the monte
    carlo one, i.e. every chromosome has the same probability to be
    chosen.
    """

    def __init__(self, *, alpha: float = 1, replacement: bool = False):
        """Initializes this object.

        :param alpha: The proportional factor. The weight of a genotype
            will be its position times alpha, so the bigger the alpha,
            biggest the gap between genotypes. Cannot be negative.
            Defaults to 1.
        :param replacement: If this selection schema is with or without
            replacement.
        """
        super().__init__(replacement=replacement)
        self.alpha = alpha

    def get_weights(
            self, *,
            genotypes: Iterable[api.Genotype]
    ) -> Tuple[float, ...]:
        """Weights will be arranged according to the genotypes position.

        Because the fittest genotype is the last one, the weights will
        be in ascending order.

        :param genotypes: The genotypes (only used to get the number of
            them).
        :return: A tuple with as many frequencies as genotypes in the
            population.
        """
        if self.alpha == 0:
            return tuple(1 for _ in genotypes)
        else:
            return tuple(self.alpha * i for i, _ in enumerate(genotypes, 1))


class MonteCarlo(SelectionSchema):
    """Selects the genotypes uniformly of the whole population.

    It doesn't provide any means to increase the selective pressure
    across the generations. It's rather a way of measuring how well
    other selection schemes behave
    """

    def do(
            self,
            population: api.Population,
            n: int
    ) -> Iterable[api.Genotype]:
        """Implementation of the selection schema.

        :param population: The population where genotypes are extracted.
        :param n: The number of genotypes to return.
        :return: A sequence of genotypes.
        """
        if self.replacement:
            return random.choices(population, k=n)
        else:
            return random.sample(population, k=n)


class RouletteWheel(WeightedSelectionSchema):
    """Selection by associating the fitness to a probabilities.

    Also called "fitness proportionate selection", the function selects
    the genotypes weighting proportionally their fitness.
    """

    def get_weights(
            self, *,
            genotypes: Iterable[api.Genotype],
    ) -> Tuple[float, ...]:
        """The frequency is directly each fitness.

        :param genotypes: The genotypes to select from.
        :return: A tuple with as many frequencies as genotypes in the
            population.
        """
        return tuple(genotype.fitness() for genotype in genotypes)


class Tournament(SelectionSchema):
    """Selects the best genotypes after random tournaments of genotypes.

    The idea is as follows: If n genotypes are required, then n rounds
    (tournaments) of the following process are executed:

    1. Select m genotypes uniformly across the whole population.
    2. Select the best genotypes of those m genotypes.

    After those n rounds are executed, the n resulting genotypes are
    returned.

    As m is a meta-parameter of the genetic algorithm, it is necessary
    to create a new object with the desired value. For example, if a
    selection schema with m=3 is needed, the selection functor should be
    created as follows:

    >>> tournament_m3 = Tournament(m=3)

    After that, tournamet_m3 will be a tournament selection functor with
    an m of 3.
    """

    def __init__(self, m: int, replacement: bool = False):
        """Initializes this instance.

        :param m: The size of the random sample of genotypes to pick
            prior to make the selection of the fittest. Must be greater
            than z
        """
        super().__init__(replacement=replacement)
        self.m = m

    def do(
            self,
            population: api.Population,
            n: int
    ) -> Iterable[api.Genotype]:
        """Implementation of the selection schema.

        :param population: The population where genotypes are extracted.
        :param n: The number of genotypes to return.
        :return: A sequence of genotypes.
        """
        available_genotypes = population[:]
        selected_genotypes: List[Genotype] = []
        while len(selected_genotypes) < n:
            # Extract a random sample of genotypes
            sample = random.choices(available_genotypes, k=self.m)

            # Select the best among them
            best = max(sample, key=lambda g: g.fitness())

            # Add it to the list
            selected_genotypes.append(best)

            # If no replacement is allowed, remove the genotype from the
            # pool of available genotypes.
            if not self.replacement:
                del available_genotypes[available_genotypes.index(best)]

        return tuple(selected_genotypes)


class Truncation(SelectionSchema):
    """Selects the best genotypes after sorting the population.

    This selector simply selects the best n individuals from the
    population.
    """

    def do(
            self,
            population: api.Population,
            n: int
    ) -> Iterable[api.Genotype]:
        """Implementation of the selection schema.

        :param population: The population where genotypes are extracted.
        :param n: The number of genotypes to return.
        :return: A sequence of genotypes.
        """
        population.sort()
        if self.replacement:
            return [population[-1] for _ in range(n)]
        else:
            return list(reversed(population[-n:]))
