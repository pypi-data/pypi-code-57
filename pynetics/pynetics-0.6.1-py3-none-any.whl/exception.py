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
"""Definition of library specific errors.
"""


# ~~~~~~~~~~~~~~
# Base exception
# ~~~~~~~~~~~~~~
class PyneticsError(Exception):
    """Generic class for the errors raised from inside the library. """


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Unclassified (yet) exceptions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BoundsCannotBeTheSame(PyneticsError):
    """The lower and upper bounds are equal and cannot be."""

    def __init__(self, value):
        super().__init__(f'Bounds cannot have the same value: {value}')


class ElementNotFound(PyneticsError):
    """The element was not found where it was supposed to be."""
    pass


class GeneticAlgorithmError(PyneticsError):
    pass


class NotInitialized(GeneticAlgorithmError):
    """The algorithm hasn't been initialized before start."""

    def __init__(self):
        super().__init__('The algorithm has not been initialized')


class PopulationError(PyneticsError):
    pass


class EmptyPopulation(PopulationError):
    """The population has no individuals."""

    def __init__(self, population_name: str = None):
        super().__init__('Empty population')


class FullPopulationError(PopulationError):
    """We are trying to add more genotypes than the allowed."""

    def __init__(self, size: int):
        """Initializes this object.

        :param size: The size of the population.
        """
        msg = f'The population has reached its limit ({size})'
        super().__init__(msg)


class AllelesError(PyneticsError):
    pass


class MoreGenesRequiredThanExisting(AllelesError):
    def __init__(self, req_size: int, pool_size: int):
        msg = f'Requested {req_size} genes but there exist only {pool_size}'
        super().__init__(msg)


# ~~~~~~~~~~~~~~~~~~~~
# Recombination errors
# ~~~~~~~~~~~~~~~~~~~~
class RecombinationError(PyneticsError):
    """Errors related to mating issues."""
    pass


# ~~~~~~~~~~~~~~~~~~
# Replacement errors
# ~~~~~~~~~~~~~~~~~~
class ReplacementError(PyneticsError):
    """Errors related to replacement issues."""
    pass


class OffspringSizeBiggerThanPopulationSize(ReplacementError):
    """The offspring size cannot be bigger than the population size."""

    def __init__(self, *, population_size, offspring_size):
        """Initializes this object.

        :param population_size: The population size.
        :param offspring_size: The offspring size.
        """
        msg = f'Offspring size {offspring_size} is bigger than population ' \
              f'size ({population_size})'
        super().__init__(msg)


class PopulationSizesDoNotMatchAfterReplacement(ReplacementError):
    """Population sizes dont match after the replacement operation."""

    def __init__(self, *, old_size, new_size):
        """Initializes this object.

        :param old_size: The size of the population before the
            replacement operation.
        :param new_size: The size of the population after the
            replacement operation.
        """
        msg = f"Sizes don't match after replacement ({old_size} != {new_size})"
        super().__init__(msg)


# ~~~~~~~~~~~~~~~~
# Selection errors
# ~~~~~~~~~~~~~~~~
class SelectionError(PyneticsError):
    """Errors related with selection algorithms"""


class WrongSelectionSize(SelectionError):
    """Tried to extract zero or negative genotypes."""

    def __init__(self, n: int):
        """Initializes this object.

        :param n: The (wrong) amount of genotypes to extract.
        """
        msg = f'The amount of genotypes must be positive (tried {n})'
        super().__init__(msg)


class CannotSelectThatMany(SelectionError):
    """The population has fewer chromosomes than the required."""

    def __init__(self, size: int, n: int):
        """Initializes this object.

        :param size: The maximum size allowed by the population.
        :param n: The amount of genotypes to extract.
        """
        msg = f'Tried to extract {n} genotypes from a population of {size}'
        super().__init__(msg)


# ~~~~~~~~~~~~~~~~~~~~~~
# Stop conditions errors
# ~~~~~~~~~~~~~~~~~~~~~~
class StopConditionError(PyneticsError):
    """Any error related to stop conditions"""
