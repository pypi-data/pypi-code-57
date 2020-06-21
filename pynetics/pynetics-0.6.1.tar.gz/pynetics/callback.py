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
"""General behaviour of the callbacks called while training.
"""
from __future__ import annotations

import abc
from typing import Dict

from . import api


# ~~~~~~~~~~~~~~~~~~~~~~~
# Abstract callback class
# ~~~~~~~~~~~~~~~~~~~~~~~
class Callback(metaclass=abc.ABCMeta):
    """Base class to listen Genetic Algorithm events during training.

    It is useful not only to monitor how the whole genetic algorithm is
    evolving during training, but also to modify it in real time (i.e.
    the problem constraints change in real time).
    """

    def on_algorithm_begin(self, ga: api.EvolutiveAlgorithm):
        """The method to be called when the genetic algorithm starts.

        It will be called AFTER initialization but BEFORE the first
        iteration, including the check against the stop condition.

        :param ga: The genetic algorithm that caused the event.
        """

    def on_algorithm_end(self, ga: api.EvolutiveAlgorithm):
        """The method to be called when the genetic algorithm ends.

        It will be called AFTER the stop condition has been met.

        :param ga: The genetic algorithm that caused the event.
        """
        pass

    def on_step_begin(self, ga: api.EvolutiveAlgorithm):
        """The method to be called when an iteration step starts.

        It will be called AFTER the stop condition has been checked and
        proved to be false) and BEFORE the new step is computed.

        :param ga: The genetic algorithm that caused the event.
        """
        pass

    def on_step_end(self, ga: api.EvolutiveAlgorithm):
        """The method to be called when an iteration step ends.

        It will be called AFTER an step of the algorithm has been
        computed and BEFORE a new check against the stop condition is
        going to be made.

        :param ga: The genetic algorithm that caused the event.
        """
        pass


# ~~~~~~~~~
# Callbacks
# ~~~~~~~~~
class History(Callback):
    """Keep track of some of the indicators of the algorithm.

    This callback is automatically added by the GeneticAlgorithm base
    class and is returned by its `run` method.
    """

    def __init__(self):
        """Initializes this object."""
        self.generation: int = 0
        self.data: Dict = {}

    def on_algorithm_begin(self, ga: api.EvolutiveAlgorithm):
        """When the algorithm starts, the parameters are reset.

        :param ga: The genetic algorithm that caused the event.
        """
        self.generation = 0
        self.data.clear()

    def on_step_end(self, ga: api.EvolutiveAlgorithm):
        """Once a step is finished, some indicators are recorded.

        Those indicators include the best genotype instance and the best
        fitness achieved.

        :param ga: The genetic algorithm that caused the event.
        """
        self.generation = ga.generation

        best_genotype = ga.best()
        best_fitness = best_genotype.fitness()
        self.data.setdefault('Best genotype', []).append(best_genotype)
        self.data.setdefault('Best fitness', []).append(best_fitness)
