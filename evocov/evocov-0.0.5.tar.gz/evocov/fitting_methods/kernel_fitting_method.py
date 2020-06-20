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

import deap.base

from gplib.fitting_methods.fitting_method import FittingMethod
from ..gen_prog_tools import primitive_set, creation, selection


class KernelFittingMethod(FittingMethod):
    """

    """
    MAX_SIGMA = 10.0 ** 20

    def __init__(self, obj_fun, max_fun_call=500, dims=1,
                 nested_fit_method=None):

        self.max_fun_call = max_fun_call

        self.nested_fit_method = nested_fit_method
        self.obj_fun = obj_fun

        self.toolbox = deap.base.Toolbox()

        self.pset = primitive_set.get_primitive_set(
            arg_num=20
        )

        creation.add_creation(
            toolbox=self.toolbox,
            pset=self.pset,
            max_depth=30,
            dims=dims
        )

    def evaluate_model(self, model, folds, budget, verbose=False):
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
        nested_log = {
            'fun_calls': 1
        }

        if verbose:
            print(model.get_kernel_function())

        try:
            if self.nested_fit_method is not None:
                nested_log = self.nested_fit_method.fit(
                    model,
                    folds,
                    budget=budget-1,
                    verbose=verbose
                )
            fitness = self.obj_fun(
                model=model,
                folds=folds,
                grad_needed=False
            )
            if not hasattr(fitness, "__len__"):
                fitness = [fitness]
            if verbose:
                print(fitness)
        except (AssertionError, np.linalg.linalg.LinAlgError) as ex:
            fitness = [KernelFittingMethod.MAX_SIGMA]
            if verbose:
                print(ex)

        kernel = model.get_kernel_function()
        kernel.log.nested = nested_log
        kernel.log.evals += 1
        kernel.fitness.setValues(fitness)
        fun_calls = kernel.log.nested['fun_calls'] + 1

        return kernel, fun_calls

    def evaluate_population(self, model, population, folds, verbose=False):
        """

        :param model:
        :type model:
        :param population:
        :type population:
        :param folds:
        :type folds:
        :param budget:
        :type budget:
        :param verbose:
        :type verbose:
        :return:
        :rtype:
        """
        evaluated = []
        fun_calls = 0
        for individual in population:
            model.set_kernel_function(individual)
            mod_individual, ind_fun_calls = self.evaluate_model(
                model,
                folds,
                budget=self.nested_fit_method.max_fun_call,
                verbose=verbose
            )
            fun_calls += ind_fun_calls
            evaluated.append(mod_individual)

        return evaluated, fun_calls

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

        raise NotImplementedError("Not Implemented. This is an interface.")
