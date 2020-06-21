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
"""Definition of the generic high level API for the library.

The rest of modules and packages will either inherit from these or use
them ignoring their implementations.
"""
from __future__ import annotations

import abc
import enum
import itertools
from typing import (
    Optional,
    Sequence,
    Callable,
    List,
    Iterable,
    Tuple,
    Any,
    Union,
    MutableSequence,
)

from . import callback
from .exception import FullPopulationError, NotInitialized


# ~~~~~~~~~~~~
# Pynetics API
# ~~~~~~~~~~~~
class EvolutiveAlgorithm(metaclass=abc.ABCMeta):
    """Base class which defines how a genetic algorithm works.

    More than one algorithm may exist so a base class is created to
    specify the required contract to be implemented by the other classes
    to work properly.
    """

    class EventType(enum.Enum):
        """The event type fired.

        It is used to differentiate which event should be called in the
        algorithm  listeners subscribed to the class.
        """
        ALGORITHM_BEGIN = 'on_algorithm_begin'
        STEP_BEGIN = 'on_step_begin'
        STEP_END = 'on_step_end'
        ALGORITHM_END = 'on_algorithm_end'

    def __init__(
            self,
            stop_condition: StopCondition,
            callbacks: Sequence[callback.Callback] = None,
    ):
        """Creates a new instance of this class.

        :param stop_condition: The condition to stop the algorithm.
        :param callbacks: An optional list of callbacks following the
            Callback contract.
        """
        self.stop_condition = stop_condition

        # We have to keep track of the generation while training, so
        # this is the variable
        self.__generation: int = 0

        # The list of callbacks to be notified each time an event is
        # fired. We maintain also a History callback, which will be
        # returned once run method finishes.
        self.__callbacks = set(c for c in callbacks or [] if c is not None)
        self.history = callback.History()

        # Control if a training stop has been requested
        self.__stop_requested = False

        # Control if the algorithm has been already initialized
        self.__initialized = False

    @property
    def callbacks(self):
        return [c for c in self.__callbacks]

    @property
    def generation(self) -> int:
        """The current generation in the algorithm."""
        return self.__generation

    def run(self):
        """Runs the algorithm."""
        # Initialize the algorithm.
        if not self.__initialized:
            self.initialize()
        # Start creating new generations until a solution is found
        self.__fire(self.EventType.ALGORITHM_BEGIN)

        while self.running():
            self.__fire(self.EventType.STEP_BEGIN)
            self.__generation += 1
            self.step()
            self.__fire(self.EventType.STEP_END)
        self.__fire(self.EventType.ALGORITHM_END)

        return self.history

    def running(self):
        """TODO TBD..."""
        if self.__stop_requested:
            return False
        else:
            return self.best() is None or not self.stop_condition(self)

    def stop(self):
        """TODO TBD..."""
        self.__stop_requested = True

    def initialize(self):
        """TODO: TBD..."""
        # Reset the generation; we'll start all over again
        self.__generation = 0

        # Call the delegated method in case the subclass implementation
        # requires specific configuration
        self.on_initialize()

        # Mark the algorithm as initialized
        self.__initialized = True

    @abc.abstractmethod
    def on_initialize(self):
        """Subclass specific initialization method"""

    def finalize(self):
        """Performs the finalization operations."""
        # Call the delegated method in case the subclass implementation
        # requires specific configuration
        self.on_finalize()

    @abc.abstractmethod
    def on_finalize(self):
        """Subclass specific finalization method"""

    @abc.abstractmethod
    def step(self):
        """Called on every iteration of the algorithm. """

    @abc.abstractmethod
    def best(self) -> Genotype:
        """Returns the best genotype in this current generation.

        :return: The best genotype.
        """

    def __fire(self, event_type: EventType):
        """Triggers the specified event in all the attached listeners.

        :param event_type: The event type to be fired in all the
            listeners.
        """
        for c in self.callbacks:
            getattr(c, event_type.value)(self)
        getattr(self.history, event_type.value)(self)


class Genotype(metaclass=abc.ABCMeta):
    """A possible codification of a solution to a problem."""

    def __init__(self):
        """Initializes this object."""
        self.fitness_function: Optional[Fitness] = None

    def fitness(self) -> float:
        """Returns the fitness of this particular genotype.

        It relies on the parameter fitness_function, which is filled
        by the Population object that manages each population inside
        a genetic algorithm.

        :return: The fitness of this particular genotype
        """
        if self.fitness_function is not None:
            return self.fitness_function(self)
        else:
            raise NotInitialized()

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        """Equality operator between two genotypes.

        Overriding is force to ensure the method differs from that
        provided by default in python.

        :param other: The other genotype to compare with.
        :return: True if the two genotypes differ or false otherwise.
        """

    def __ne__(self, other: object) -> bool:
        """Inequality operator (as the negation of the equality one).

        :param other: The other genotype to compare with.
        :return: True if the two genotypes differ or false otherwise.
        """
        return not (self == other)


class Initializer(metaclass=abc.ABCMeta):
    """Responsible for new genotypes generation.

    This class is used for both initialization phase (just before the
    first genetic algorithm step) and genotype creation when needed.
    """

    @abc.abstractmethod
    def create(self) -> Genotype:
        """Creates a new genotype.

        This method should be overwritten, as it depends completely on
        the problem codification.

        :return: A newly created genotype.
        """

    def fill(self, population: Population) -> Population:
        """Fills the population with newly created genotypes.

        The creation of those genotypes will be delegated to the create
        method.

        The population passed as argument will be modified. The returned
        population is nothing but a reference to the same population for
        fluent API purposes.

        :param population: The population to be filled. Cannot be None.
        :return: The same population, but with the new genotypes in it.
        """
        while not population.full():
            population.append(self.create())
        return population


class Population(MutableSequence[Genotype]):
    """Manages the pool of genotypes that are solutions of a G.A.

    It's a subclass of list, but with some additions.
    """

    def __init__(self, size: int, fitness: Fitness):
        """Initializes a new instance of this object.

        :param size: The maximum size of genotypes this population
            object hold. It should be greater than zero.
        :param fitness: The fitness functor to assign to the genotypes
            added to this population.
        """
        self.genotypes: List[Genotype] = []
        self.fitness = fitness
        self.max_size = size

        self.is_sorted = True

    def __add__(self, other: Population) -> Population:
        """Creates a new population adding the two specified.

        The new population will contain the genotypes of the two
        populations (even repeating genotypes) and its maximum size will
        be the sum of the maximum size of both populations.

        :param other: The population to add to this one.
        :return: A new population.
        """
        new_population = Population(
            size=self.max_size + other.max_size,
            fitness=self.fitness
        )

        for genotype in itertools.chain(self.genotypes, other.genotypes):
            new_population.append(genotype)

        return new_population

    def __getitem__(self, item: Union[int, slice]) -> Any:
        """To recover any item via bracket notation.

        :param item: The item to recover.
        """
        return self.genotypes.__getitem__(item)

    def __setitem__(self, key: int, genotype: Genotype) -> None:
        """Called to implement the assignment of self[key].

        The implementation is delegated to the super class (list) but
        the population is marked as not sorted.

        Notice that, after calling this method, the genotype object
        attribute fitness_function will be overridden by the one set
        in this population object.

        :param key: The position of the new value in the population.
        :param genotype: The value to occupy that position.
        :raise TypeError: if key is of an inappropriate type.
        :raise IndexError: if key is of a value outside the set of
            indexes for the sequence (after any special interpretation
            of negative values).
        """
        self.genotypes.__setitem__(key, genotype)
        genotype.fitness_function = self.fitness
        self.is_sorted = False

    def __delitem__(self, i: Union[int, slice]) -> None:
        """Removes the elements located in the position or slice i.

        :param i: The index to the elements to be deleted.
        """
        self.genotypes.__delitem__(i)

    def __len__(self) -> int:
        """Returns the number of genotypes contained in this population.

        :return: The number of genotypes. It could be less than the
            Population's max size, but never greater.
        """
        return len(self.genotypes)

    def full(self) -> bool:
        """Points out if the population is full or not.

        :return: True if the population is complete or false otherwise.
        """
        return len(self) >= self.max_size

    def empty(self) -> bool:
        """Points out if the population is empty or not.

        :return: True if the population is empty or false otherwise.
        """
        return len(self) == 0

    def append(self, genotype: Genotype) -> None:
        """Add a new genotype to this population.

        The implementation is delegated to the super class (list) but
        the population is marked as not sorted and it raises an error in
        case the maximum size (specified at initialization time) is
        reached.

        Notice that, after calling this method, the genotype object
        attribute fitness_function will be overriden by the one set
        in this population object.

        :param genotype: The genotype to add into this population.
        :raise FullError: in case the population has already reached its
            full size.
        """
        if self.full():
            raise FullPopulationError(self.max_size)
        else:
            self.genotypes.append(genotype)
            genotype.fitness_function = self.fitness
            self.is_sorted = False

    def extend(self, genotypes: Iterable[Genotype]) -> None:
        """Add a new bunch of genotypes to this population.

        The implementation is delegated to the super class (list) but
        the population is marked as not sorted and it raises an error in
        case the maximum size (specified at initialization time) is
        reached.

        Notice that, after calling this method, the genotype object
        attribute fitness_function will be overriden by the one set
        in this population object.

        :param genotypes: The genotypes to add into this population.
        :raise FullError: in case the population has already reached its
            full size.
        """
        for genotype in genotypes:
            genotype.fitness_function = self.fitness
            self.append(genotype)

    def insert(self, index: int, genotype: Genotype) -> None:
        """Add a new genotype to this population.

        The implementation is delegated to the super class (list) but
        the population is marked as not sorted and it raises an error in
        case the maximum size (specified at initialization time) is
        reached.

        Notice that, after calling this method, the genotype object
        attribute fitness_function will be overriden by the one set
        in this population object.

        :param index: The genotype to add into this population.
        :param genotype: The genotype to add into this population.
        :raise: FullError in case the population has already reached its
            full size.
        """
        if self.full():
            raise FullPopulationError(self.max_size)
        else:
            self.genotypes.insert(index, genotype)
            genotype.fitness_function = self.fitness
            self.is_sorted = False

    def pop(self, i: int = 0) -> Genotype:
        """Extracts the object in the specified position.

        :param i: The position. If not specified, it will be position 0.
        """
        return self.genotypes.pop(i)

    def reverse(self) -> None:
        """Reverse the elements of the list in place.

        The implementation is delegated to the super class (list) but
        the population is marked as not sorted.
        """
        self.genotypes.reverse()
        self.is_sorted = False

    def sort(self, **kwargs) -> None:
        """Sorts the genotypes of this population by a function.

        After calling this method, the order of the population will be
        in ascending order, i.e. from lower to higher fitness.
        """
        if not self.is_sorted:
            self.genotypes.sort(key=lambda genotype: genotype.fitness())
            self.is_sorted = True

    def clear(self):
        """Removes all the population genotypes."""
        self.genotypes.clear()
        self.is_sorted = True


# Definitions for typing purposes
Diversity = Callable[[Any], float]
Fitness = Callable[[Any], float]
Mutation = Callable[[float, Genotype], Genotype]
Recombination = Callable[[Genotype], Genotype]
Replacement = Callable[[Population, Population], Population]
Selection = Callable[[Population, int], Tuple[Genotype, ...]]
StopCondition = Callable[[EvolutiveAlgorithm], bool]
