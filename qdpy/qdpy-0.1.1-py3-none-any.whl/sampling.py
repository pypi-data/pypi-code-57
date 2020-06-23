#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""TODO""" # TODO


#__all__ = ["SamplingDecorator", "FixedSamplingDecorator"]

from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, Mapping, MutableMapping, overload
import numpy as np
import random


from qdpy.utils import *
from qdpy.base import *
from qdpy.containers import *
from qdpy import tools



class Sampling(CreatableFromConfig, Summarisable):
    deepcopy_inds: bool

    def __init__(self, deepcopy_inds: bool = True, **kwargs):
        self.deepcopy_inds = deepcopy_inds

    def __call__(self, eval_fn: Callable, ind_or_inds: Any, *args, **kwargs):
        if isinstance(ind_or_inds, Sequence) and isinstance(ind_or_inds[0], IndividualLike):
            res = []
            for ind in ind_or_inds:
                res.append(self._commit_sampling_info(ind, *self._sample_ind(eval_fn, ind, *args, **kwargs)))
            return res
        else:
            return self._commit_sampling_info(ind_or_inds, *self._sample_ind(eval_fn, ind_or_inds, *args, **kwargs))

    def _commit_sampling_info(self, ind: Any,
            avg_fit: Any, avg_ft: Any,
            sampled_fit: Sequence[Any], sampled_ft: Sequence[Any]):
        ind.fitness.values = avg_fit
        ind.features = avg_ft
        ind.sampled_fitnesses = sampled_fit
        ind.sampled_features = sampled_ft
        #print(f"DEBUG _commit_sampling_info {ind.fitness} {ind.features}")
        return ind

    def _fn_call(self, fn, ind, *args, **kwargs):
        ind2 = copy.deepcopy(ind) if self.deepcopy_inds else ind
        res = fn(ind2, *args, **kwargs)
        if isinstance(res, IndividualLike):
            return res.fitness, res.features
        else:
            ind_fitness_val, ind_features = res
            if isinstance(ind_fitness_val, FitnessLike):
                ind_fitness_val = ind_fitness_val.values
            return ind_fitness_val, ind_features

    def _sample_ind(self, fn: Callable, ind: IndividualLike,  *args, **kwargs):
        ind_fitness_val, ind_features = self._fn_call(fn, ind, *args, **kwargs)
        return ind_fitness_val, ind_features, [ind_fitness_val], [ind_features]

    def _explicit_averaging(self, coll):
        return list(np.mean(np.array(coll), axis=0))



@registry.register
class FixedSampling(Sampling):
    nb_samples: int

    def __init__(self, nb_samples: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.nb_samples = nb_samples
        assert(self.nb_samples > 0)

    def _sample_ind(self, fn: Callable, ind: IndividualLike, *args, **kwargs):
        fits = []
        fts = []
        for _ in range(self.nb_samples):
            ind_fitness_val, ind_features = self._fn_call(fn, ind, *args, **kwargs)
            fits.append(ind_fitness_val)
            fts.append(ind_features)
        avg_fit = self._explicit_averaging(fits)
        avg_ft = self._explicit_averaging(fts)
        return avg_fit, avg_ft, fits, fts





#
## TODO refactor
#class SamplingDecorator(QDAlgorithm):
#    """TODO"""
#
#    def __init__(self, base_alg: QDAlgorithm, **kwargs):
#        self.base_alg = base_alg
#        self.base_alg_batch_start = 0.
#        self.inds_to_ask = []
#        self.staging_inds = []
#
#        #kwargs['batch_size'] = kwargs.get('batch_size') or min(base_alg.batch_size // 10, 10) # XXX HACK
#        kwargs['batch_size'] = kwargs.get('batch_size') or base_alg.batch_size
#        kwargs['dimension'] = kwargs.get('dimension') or base_alg.dimension
#        kwargs['optimisation_task'] = kwargs.get('optimisation_task') or base_alg.optimisation_task
#        kwargs['ind_domain'] = kwargs.get('ind_domain') or base_alg.ind_domain
#        kwargs['name'] = kwargs.get('name') or base_alg.name
#        kwargs['base_ind_gen'] = kwargs.get('base_ind_gen') or base_alg._base_ind_gen
#        if kwargs['base_ind_gen'] is None:
#            kwargs['base_ind_gen'] = gen_sampled_individuals()
#        kwargs['budget'] = kwargs.get('budget') or base_alg.budget
#        kwargs['container'] = base_alg.container
#        super().__init__(**kwargs)
#
#    def _internal_ask(self, base_ind: IndividualLike) -> IndividualLike:
#        if len(self.inds_to_ask) > 0:
#            base_ind[:] = self.inds_to_ask.pop()[:] # XXX dirty
#            base_ind.optim_flags['reeval'] = True # XXX dirty
#            return base_ind
#        else:
##            return self.base_alg.ask()
#            tmp = self.base_alg.ask()
#            #print("DEBUG _internal_ask2:", tmp)
#            base_ind[:] = tmp[:] # XXX dirty
#            return base_ind
#
#
#    def _tell_sampling(self, ind: IndividualLike) -> bool:
#        added = self.base_alg.tell(ind)
#        self._tell_after_container_update(ind, added)
#        return added
#
#
#    def tell(self, individual: IndividualLike, fitness: Optional[Any] = None,
#            features: Optional[FeaturesLike] = None, elapsed: Optional[float] = None) -> bool:
#        """Give the algorithm an evaluated `individual` (with a valid fitness function)
#        and store it into the container.
#
#        Parameters
#        ----------
#        :param individual: IndividualLike
#            The `individual` provided to the algorithm.
#        :param fitness: Optional[FitnessLike]
#            If provided, set `individual.fitness` to `fitness`.
#        :param features: Optional[FeaturesLike]
#            If provided, set `individual.features` to `features`.
#        :param elapsed: Optional[float]
#            If provided, set `individual.elapsed` to `elapsed`.
#            It corresponds to the time (in seconds) elapsed during evaluation.
#        """
#        ind = copy.deepcopy(individual)
#        if fitness is not None:
#            if isinstance(fitness, FitnessLike):
#                ind.fitness = fitness
#            else:
#                ind.fitness.values = fitness
#        if len(ind.fitness.values) != self.base_alg._nb_objectives:
#            raise ValueError(f"`individual` must possess a `fitness` attribute of dimension {self.base_alg._nb_objectives} (specified through parameter `nb_objectives` when creating a QDAlgorithm sub-class), instead of {len(individual.fitness.values)}.")
#        if features is not None:
#            ind.features[:] = features
#        if elapsed is not None:
#            ind.elapsed = elapsed
#        #print("TELL: ", ind, ind.fitness, ind.fitness.nb_samples, ind.features, ind.features.nb_samples)
#
#        if ind.nb_samples == 0:
#            ind.nb_samples = 1 # XXX HACK
#
#        try:
#            if ind in self.container:
#                index = self.container.index(ind)
#                ind_in_grid = self.container[index]
#                self.container.discard(ind_in_grid)
#                ind.merge(ind_in_grid)
#                added: bool = self.container.update([ind]) == 1
#                if ind.optim_flags.get('reeval', False):
#                    self._tell_after_container_update(ind, added)
#                    #self._nb_updated_self += 1
#                    #self._nb_evaluations_self += 1
#                else:
#                    added = self._tell_sampling(ind)
#            else:
#                added = self._tell_sampling(ind)
#        except Exception as e:
#            print(f"Exception during _tell_sampling: {e}")
#            raise e
#
##        # XXX HACK
##        remaining_suggestions = self.budget - self.nb_suggestions
##        if len(self.inds_to_ask) > remaining_suggestions:
##            self.budget += len(self.inds_to_ask) - remaining_suggestions
##        #print("DEBUG tell: ", self.budget, self.nb_evaluations, self.base_alg.nb_evaluations, self.nb_suggestions, self.base_alg.nb_suggestions, len(self.staging_inds), len(self.inds_to_ask))
#        return added
#
#
#
##    def optimise(self, evaluate: Callable, budget: Optional[int] = None,
##            batch_mode: bool = True, executor: Optional[ExecutorLike] = None,
##            send_several_suggestions_to_fn: bool = False) -> IndividualLike:
##        optimisation_start_time: float = timer()
##        self.base_alg_batch_start = optimisation_start_time
##        # Call base_alg callback functions
##        for fn in self.base_alg._callbacks.get("started_optimisation"):
##            fn(self.base_alg)
##        res = super().optimise(evaluate, budget, batch_mode, executor, send_several_suggestions_to_fn)
##        # Call base_alg callback functions
##        optimisation_elapsed: float = timer() - optimisation_start_time
##        for fn in self.base_alg._callbacks.get("finished_optimisation"):
##            fn(self.base_alg, optimisation_elapsed)
##        return res
#
#
#    def _verify_if_finished_iteration(self, batch_start_time: float) -> bool:
#        res = super()._verify_if_finished_iteration(batch_start_time)
#        if self.base_alg._nb_evaluations_in_iteration != 0:
#            base_alg_res = self.base_alg._verify_if_finished_iteration(self.base_alg_batch_start) # XXX batch_start_time
#            if base_alg_res:
#                self.base_alg_batch_start = timer()
#        return res
#
#
#
#@registry.register
#class FixedSamplingDecorator(SamplingDecorator):
#    """TODO"""
#
#    def __init__(self, base_alg: QDAlgorithm, nb_samples = 1, **kwargs):
#        self.nb_samples = nb_samples
#        super().__init__(base_alg, **kwargs)
#        #self.budget = base_alg.budget # * nb_samples
#
#
#    def _tell_sampling(self, ind: IndividualLike) -> bool:
#        if self.nb_samples == 1:
#            added = self.base_alg.tell(ind)
#            self._tell_after_container_update(ind, added)
#            return added
#
#        if ind in self.staging_inds:
#            idx = self.staging_inds.index(ind)
#            #tmp_nb_samples = self.staging_inds[idx].nb_samples # XXX
#            self.staging_inds[idx].merge(ind)
#            ind = self.staging_inds[idx]
#            #print("DEBUG staging: ", ind.nb_samples, tmp_nb_samples)
#            if ind.nb_samples >= self.nb_samples:
#                added = self.base_alg.tell(ind)
#                self._tell_after_container_update(ind, added)
#                self.staging_inds.remove(ind)
#                return added
#
#        else:
#            self.staging_inds.append(ind)
#            for _ in range(self.nb_samples - ind.nb_samples):
#                self.inds_to_ask.append(ind)
#            #self.budget += self.nb_samples - ind.nb_samples # XXX
#        self._tell_after_container_update(ind, False)
#        return False
#



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
