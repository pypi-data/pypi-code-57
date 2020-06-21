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
"""Replacement algorithms.
"""
import abc

from . import api
from .exception import (
    PopulationSizesDoNotMatchAfterReplacement,
    OffspringSizeBiggerThanPopulationSize,
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Abstract replacement schemas
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ReplacementSchema(metaclass=abc.ABCMeta):
    """Groups common behavior across all the replacement schemas.

    The replacement schema is defined as a class. However, it is enough
    to implement it a replacement method, i.e. a function that receives
    two populations (original and offspring) and returns a population
    resulting from the combination of the previous two.
    """

    def __init__(self, *, maintain: bool = True):
        """Initializes this object.

        :param maintain: If the returned population must have the same
            population size than the original one. Defaults to True.
        """
        self.maintain = maintain

    def __call__(
            self, *,
            population: api.Population,
            offspring: api.Population,
    ) -> api.Population:
        """Executes the replacement method.

        This method performs some checks to the arguments and delegates
        the implementation to the abstract method
        :func:`~replacement.ReplacementSchema.do`.

        :param population: The original population.
        :param offspring: The population to replace the original one.
        :return: A new Population instance.
        :raise OffspringSizeBiggerThanPopulationSize: If the offspring
            size is bigger than the population size.
        :raise PopulationSizesDontMatchAfterReplacement: If the new
            population size is bigger after the call of the method.
        """
        if len(offspring) > len(population):
            raise OffspringSizeBiggerThanPopulationSize(
                population_size=len(population),
                offspring_size=len(offspring),
            )

        new_population = self.do(population=population, offspring=offspring)

        if self.maintain and len(population) != len(new_population):
            raise PopulationSizesDoNotMatchAfterReplacement(
                old_size=len(population),
                new_size=len(new_population),
            )
        else:
            return new_population

    @abc.abstractmethod
    def do(
            self, *,
            population: api.Population,
            offspring: api.Population,
    ) -> api.Population:
        """Executes this particular implementation of selection.

        This method is not called by the base algorithms implemented,
        but from :func:`~selection.SelectionSchema.__call__` instead.
        It should contain the logic of the specific selection schema.

        :param population: The original population.
        :param offspring: The population to replace the original one.
        :return: A new Population instance.
        """


# ~~~~~~~~~~~~~~~~~~~
# Replacement schemas
# ~~~~~~~~~~~~~~~~~~~
# TODO Actually the high and low elitism schemas can be parametrised
#  resulting in even more different replacement schemes.
class HighElitism(ReplacementSchema):
    """Replacement with the fittest among both population and offspring.

    Only those best genotypes among both populations will be selected,
    thus discarding those less fit. This makes this operator extremely
    elitist.
    """

    def do(
            self, *,
            population: api.Population,
            offspring: api.Population,
    ) -> api.Population:
        """Executes this replacement.

        :param population: The original population.
        :param offspring: The population to replace the original one.
        :return: A new Population instance.
        """
        # Concat both populations
        new_population = population + offspring

        # Sort it by fitness to have the best ones at the beginning
        new_population.sort()

        # Just delete the works ones until population has the expected
        # size and set it as the maximum size of the new population
        del new_population[:-population.max_size]
        new_population.max_size = population.max_size

        # Return the newly created population
        return new_population


high_elitism = HighElitism()


class LowElitism(ReplacementSchema):
    """Replaces the less fit of the population with the fittest of the
    offspring.

    The method will replace the less fit genotypes by the best ones of
    the offspring. This makes this operator elitist, but at least not
    much. Moreover, if the offspring size equals to the population
    size then it's a full replacement (i.e. a generational scheme).
    """

    def do(
            self, *,
            population: api.Population,
            offspring: api.Population,
    ) -> api.Population:
        """Executes this replacement.

        :param population: The original population.
        :param offspring: The population to replace the original one.
        :return: A new Population instance.
        """
        # Create the new population to fill with the genotypes
        new_population = api.Population(
            size=population.max_size,
            fitness=population.fitness
        )

        # Fill the best n genotypes of the first population, being n the
        # max_length of the populations minus the number of genotypes in
        # the second population
        population.sort()
        new_population.extend(population[len(offspring):])

        # Fill with the genotypes of the second population
        new_population.extend(offspring)

        # Return the newly created population
        return new_population


low_elitism = LowElitism()
