# -*- coding: utf-8 -*-
#
#    Copyright 2020 Ibai Roman
#
#    This file is part of EvoCov.
#
#    EvoCov is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    EvoCov is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with EvoCov. If not, see <http://www.gnu.org/licenses/>.

import numpy as np

import time

import deap.algorithms

from .kernel_fitting_method import KernelFittingMethod
from ..gen_prog_tools import selection
from ..gen_prog_tools import mutation
from ..gen_prog_tools import crossover


class EvoCov(KernelFittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None,
                 cxpb=0.4, mutpb=0.6, beta=1e-4):

        super(EvoCov, self).__init__(
            obj_fun,
            max_fun_call=max_fun_call,
            dims=dims,
            nested_fit_method=nested_fit_method
        )

        selection.add_selection(
            toolbox=self.toolbox,
            selection_method='best'
        )

        mutation.add_mutation(
            toolbox=self.toolbox,
            pset=self.pset,
            mutation_method='all'
        )

        crossover.add_crossover(
            toolbox=self.toolbox,
            pset=self.pset
        )

        self.cxpb = cxpb
        self.mutpb = mutpb
        self.beta = beta

    def fit(self, model, folds, budget=None, verbose=False):
        """

        :param model:
        :type model:
        :param folds:
        :type folds:
        :param budget:
        :type budget:
        :param verbose:
        :type verbose:
        :return:
        :rtype:
        """
        if budget is None or self.max_fun_call < budget:
            max_fun_call = self.max_fun_call
        else:
            max_fun_call = budget

        max_eval = int(max_fun_call / self.nested_fit_method.max_fun_call)
        ngen = int(np.power(max_eval, 0.535))
        npop = int(float(max_eval)/ngen)
        mu = max(3, int(npop * 0.25))

        start = time.time()
        fun_calls = 0
        population = self.toolbox.random_population(n=npop)
        id_i = 0
        for ind in population:
            ind.log.id = id_i
            id_i += 1
        best_fitness_m1 = np.inf
        all_population = population

        # Begin the generational process
        for gen in range(0, ngen-1):

            # Evaluate the individuals with an invalid fitness
            population, pop_fun_calls = self.evaluate_population(
                model, population, folds, verbose
            )
            fun_calls += pop_fun_calls

            # Measure improvement
            best_fitness = np.min(np.array([
                best.fitness.getValues()
                for best in population
            ]), axis=0)

            relative_improvement = (best_fitness_m1 - best_fitness) / \
                np.abs(best_fitness)

            if verbose:
                print("\nrelative improvement: {}\n".format(
                    relative_improvement
                ))

            # Restart condition
            if self.beta < np.max(relative_improvement):
                # Select the next generation population
                selection = self.toolbox.select(population, mu)
                # Vary the population
                offspring = deap.algorithms.varOr(
                    selection,
                    self.toolbox,
                    npop-mu,
                    self.cxpb,
                    self.mutpb
                )
            else:
                if verbose:
                    print("\nRestart...\n")
                selection = []
                offspring = self.toolbox.random_population(n=npop)
                best_fitness = np.inf

            for ind in offspring:
                ind.log.creation = gen + 1
                ind.log.id = id_i
                id_i += 1

            population = offspring + selection
            all_population += population
            best_fitness_m1 = best_fitness

        # Evaluate the individuals with an invalid fitness
        population, pop_fun_calls = self.evaluate_population(
            model, population, folds, verbose
        )
        fun_calls += pop_fun_calls

        best = self.toolbox.select(all_population, 1)[0]

        end = time.time()

        log = {
            'name': self.__class__.__name__,
            'fun_calls': fun_calls,
            'restarts': ngen,
            'time': end - start,
            'best': {
                'params': str(best),
                'value': best.fitness.values[0],
                'creation': best.log.creation,
                'evals': best.log.evals,
                'id': best.log.id,
                'origin': best.log.origin,
                'hp_count': best.log.hp_count,
                'prim_count': best.log.prim_count,
                'nested': best.log.nested
            }
        }

        assert best, "No kernel found"

        model.set_kernel_function(best)

        return log
