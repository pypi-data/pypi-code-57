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

import time

import deap.gp
import deap.base
import deap.creator
import deap.algorithms

from .kernel_fitting_method import KernelFittingMethod

from ..gen_prog_tools import selection
from ..gen_prog_tools import mutation


class Greedy(KernelFittingMethod):
    """

    """

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        super(Greedy, self).__init__(
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

        start = time.time()
        fun_calls = 0
        restarts = 0
        population = []
        if isinstance(model.get_kernel_function(), deap.creator.Individual):
            individual = model.get_kernel_function()
        else:
            individual = self.toolbox.random_individual()

        base_id = int(individual.log.id * 1e5)

        while fun_calls < max_fun_call:
            individual.log.id = base_id  + restarts
            # run optimization
            model.set_kernel_function(individual)
            individual, ind_fun_calls = self.evaluate_model(
                model,
                folds,
                budget=max_fun_call - fun_calls,
                verbose=verbose
            )
            fun_calls += ind_fun_calls
            restarts += 1

            population.append(individual)
            best = self.toolbox.select(population, 1)[0]
            population = [best]
            individual = self.toolbox.mutate(best)[0]

        end = time.time()

        log = {
            'name': self.__class__.__name__,
            'fun_calls': fun_calls,
            'restarts': restarts,
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
