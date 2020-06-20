from abc import ABC, abstractmethod
from queue import Queue
import numpy as np
from scipy import stats
from sklearn.model_selection import ParameterGrid, ParameterSampler
import skopt


__all__ = ["ListSearcher", "GridSearcher", "RandomSearcher", "SkoptSearcher"]


class _Searcher(ABC):
    def __init__(self, space, n_experiments=None):
        """
        Base structure to Labs Searcher.
        :param space: hyperparameters search space. The dictionary structure is a Searcher implementation dependant.
        :param n_experiments: (int) number of experiments to create. Not any Searcher implementation required the param.
        """
        self._internal_optimizer = None

        self.space = space

        self.n_experiments = n_experiments

        self.experiments_queue = Queue()

    @abstractmethod
    def _init_experiments(self, **kwargs):
        """
        initial the experiments by loading elements to experiments_queue.
        """

    @abstractmethod
    def get_next_experiments(self, n=None):
        """
        Return a list of the next experiments. If n is None, return all the next experiments.
        :param n: number of experiment to return
        :return: (list) the n length experiments list.
        """

    @abstractmethod
    def update_search(self, *kwargs):
        """
        Get values extracted from previous experiments and update obj. The next experiment will be created using the
        update_search operation. The method will be implemented when searcher using bayesian search optimizations.
        """

    @abstractmethod
    def is_finished(self):
        """
        Check if the searcher work is done.
        :return: (bool) True if the search process is finished, otherwise False.
        """


class ListSearcher(_Searcher):
    def __init__(self, space):
        """
        This searcher provide user defined hyperparameters combinations.
        :param space: (list) hyperparameters search space. The list contains the explicit hyperparameters dictionaries.
        """
        super().__init__(space)

        self._init_experiments()

    def _init_experiments(self):
        """
        Populate the experiments queue and experiments count.
        """
        [self.experiments_queue.put({'ix': ix, 'hyperparams': item}) for ix, item in enumerate(self.space)]

        self.n_experiments = self.experiments_queue.qsize()

    def get_next_experiments(self, n=None):
        """
        Return a list of the next experiments. If n is None, return all the next experiments.
        :param n: number of experiment to return
        :return: (list) the n length experiments list (or all when n is None).
        """
        if n is None:
            n = self.experiments_queue.qsize()

        next_experiments = [self.experiments_queue.get() for _ in range(n)]

        return next_experiments

    def update_search(self, *kwargs):
        """
        Method is not implemented (no need to update search).
        """
        pass

    def is_finished(self):
        """
        Check if the searcher work is done.
        :return: (bool) True if the experiments_queue is empty, otherwise False.
        """
        return self.experiments_queue.empty()


class GridSearcher(_Searcher):
    def __init__(self, space):
        """
        This searcher create from user defined space a grid search of hyperparameters. It's using sklearn ParameterGrid.
        :param space: (dict) hyperparameters search space. There 6 types of hyperparams space:
        hyperparams space examples:
        "space": {
          "hyperparam1": { # list space example
            "search_vals": [val1, val2, val3],
            "type": "list"
          },
          "hyperparam2": { # static space example
            "search_vals": val1,
            "type": "static"
          },
          "hyperparam3": { # linear space example
            "search_vals": [val1, val2],
            "type": "linear-space",
            "count": n
          },
          "hyperparam4": { # linear integers space example
            "search_vals": [val1, val2],
            "type": "linear-space-int",
            "count": n
          },
          "hyperparam5": { # log space space example
            "search_vals": [val1, val2],
            "type": "log-space",
            "count": n
          },
          "hyperparam3": { # log space integer example
            "search_vals": [val1, val2],
            "type": "log-space-int",
            "count": n
          }
        }
        """
        super().__init__(space)

        self._init_experiments()

    def _init_experiments(self):
        """
        Populate the experiments queue and experiments count.
        """
        prepared_space = self._prepare_grid_space(self.space)

        [self.experiments_queue.put(item) for item in prepared_space]

        self.n_experiments = self.experiments_queue.qsize()

    def get_next_experiments(self, n=None):
        """
        Return a list of the next experiments. If n is None, return all the next experiments.
        :param n: number of experiment to return
        :return: (list) the n length experiments list (or all when n is None).
        """
        if n is None:
            n = self.experiments_queue.qsize()

        # if experiments count left is lower than n return the remainder experiments
        if self.experiments_queue.qsize() % n != 0:
            n = self.experiments_queue.qsize() % n

        next_experiments = [self.experiments_queue.get() for _ in range(n)]

        return next_experiments

    def update_search(self, *kwargs):
        """
        Method is not implemented (no need to update search).
        """
        pass

    def is_finished(self):
        """
        Check if the searcher work is done.
        :return: (bool) True if the experiments_queue is empty, otherwise False.
        """
        return self.experiments_queue.empty()

    def _prepare_grid_space(self, hyperparams_space):
        """
        Iterate user defined hyperparams dict space modify it to fit sklearn ParameterGrid and create grid space
        using sklearn ParameterGrid
        :param hyperparams_space: (dict) user defined hyperparams
        :return: (list) enumerated list of the grid space -> [{'ix': 1, 'hyperparams': {'param1': value, ..}}, ...]
        """
        prepared_space = {}

        # iterate space dict
        for param_name in hyperparams_space.keys():
            # modify param to fit ParameterGrid structure
            prepared_space[param_name] = self._get_grid_space_vals(hyperparams_space[param_name])

        grid = ParameterGrid(prepared_space)

        # enumerate grid
        enumerated_grid = [{'ix': ix + 1, 'hyperparams': comb} for ix, comb in enumerate(grid)]

        return enumerated_grid

    @staticmethod
    def _get_grid_space_vals(param_space):
        """
        Get user defined single hyperparameter and modify it to fit sklearn ParameterGrid input
        :param param_space: (dict) user defined hyperparams space
        :return: (list/np.array) transformed user space definition to list of values
        """
        space = None

        if param_space['type'] == "list":
            space = param_space['search_vals']
        elif param_space['type'] == "static":
            space = [param_space['search_vals']]
        elif param_space['type'] == "linear-space":
            space = np.linspace(param_space['search_vals'][0], param_space['search_vals'][1], param_space['count'])
        elif param_space['type'] == "linear-space-int":
            space = np.linspace(param_space['search_vals'][0], param_space['search_vals'][1],
                                param_space['count']).astype(np.int)
        elif param_space['type'] == "log-space":
            space = np.logspace(param_space['search_vals'][0], param_space['search_vals'][1], param_space['count'])
        elif param_space['type'] == "log-space-int":
            space = np.logspace(param_space['search_vals'][0], param_space['search_vals'][1],
                                param_space['count']).astype(np.int)

        return space


class RandomSearcher(_Searcher):
    def __init__(self, space, n_experiments, search_params):
        """
        This searcher use the user defined hyperparameters distribution to sample experiments hyperparameters.
        It's using sklearn ParameterSampler.
        :param space: (dict) hyperparameters search space. There 8 types of hyperparams space:
        hyperparams space examples:
        "space": {
          "hyperparam2": { # static space example
            "search_vals": val1,
            "type": "static"
          },
          "hyperparam1": { # categorical space example
            "search_vals": [val1, val2, val3],
            "type": "categorical"
          },
          "hyperparam3": { # normal distribution space example
            "search_vals": [mean, variance],
            "type": "normal"
          },
          "hyperparam4": { # exp distribution space example
            "search_vals": [lambda],
            "type": "exp"
          },
          "hyperparam5": { # poisson distribution space example
            "search_vals": [lambda],
            "type": "poisson"
          },
          "hyperparam3": { # log-uniform/reciprocal distribution example
            "search_vals": [a, b],
            "type": "log-uniform"
          },
          "hyperparam3": { # uniform distribution example
            "search_vals": [a, b],
            "type": "uniform"
          },
          "hyperparam3": { # int-uniform distribution example
            "search_vals": [a, b],
            "type": "int-uniform"
          }
        }
        :param n_experiments: number of experiments to sample
        :param search_params: ParameterSampler params:
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ParameterSampler.html
        """
        super().__init__(space, n_experiments)

        self.search_params = search_params

        self._init_experiments()

    def _init_experiments(self):
        """
        Populate the experiments queue and experiments count.
        """
        prepared_space = self._prepare_random_space(self.space)

        [self.experiments_queue.put(item) for item in prepared_space]

    def get_next_experiments(self, n=None):
        """
        Return a list of the next experiments. If n is None, return all the next experiments.
        :param n: number of experiment to return
        :return: (list) the n length experiments list (or all when n is None).
        """
        if n is None:
            n = self.experiments_queue.qsize()

        # if experiments count left is lower than n return the remainder experiments
        if self.experiments_queue.qsize() % n != 0:
            n = self.experiments_queue.qsize() % n

        next_experiments = [self.experiments_queue.get() for _ in range(n)]

        return next_experiments

    def update_search(self, *kwargs):
        """
        Method is not implemented (no need to update search).
        """
        pass

    def is_finished(self):
        """
       Check if the searcher work is done.
       :return: (bool) True if the experiments_queue is empty, otherwise False.
       """
        return self.experiments_queue.empty()

    @staticmethod
    def _get_rand_space_vals(param_space):
        """
        Get user defined single hyperparameter and modify it to fit sklearn ParameterSampler input.
        :param param_space: (dict) user defined hyperparams space
        :return: (list/np.array) transformed user space definition to Distribution (scipy) or a list for categorical
        space
        """

        space = None

        if param_space['type'] == "static":
            space = [param_space['search_vals']]
        elif param_space['type'] == "categorical":
            space = param_space['search_vals']
        elif param_space['type'] == "normal":
            space = stats.norm(param_space['search_vals'][0], param_space['search_vals'][1])
        elif param_space['type'] == "exp":
            space = stats.expon(param_space['search_vals'][0])
        elif param_space['type'] == "poisson":
            space = stats.poisson(param_space['search_vals'][0])
        elif param_space['type'] == "log-uniform":
            space = stats.reciprocal(param_space['search_vals'][0], param_space['search_vals'][1])
        elif param_space['type'] == "uniform":
            space = stats.uniform(param_space['search_vals'][0], param_space['search_vals'][1])
        elif param_space['type'] == "int-uniform":
            space = stats.randint(param_space['search_vals'][0], param_space['search_vals'][1])

        return space

    def _prepare_random_space(self, hyperparams_space):
        """
        Iterate user defined hyperparams dict space, modify it to fit sklearn ParameterSampler and create random space
        using sklearn ParameterSampler.
        :param hyperparams_space: (dict) user defined hyperparams
        :return: (list) enumerated list of the grid space -> [{'ix': 1, 'hyperparams': {'param1': value, ..}}, ...]
        """
        prepared_space = {}

        # iterate space dict
        for param_name in hyperparams_space.keys():
            # modify param to fit ParameterGrid structure
            prepared_space[param_name] = self._get_rand_space_vals(hyperparams_space[param_name])

        grid = ParameterSampler(prepared_space, self.n_experiments, **self.search_params)

        # enumerate experiments
        enumerated_experiments = [{'ix': ix + 1, 'hyperparams': comb} for ix, comb in enumerate(grid)]

        return enumerated_experiments


class SkoptSearcher(_Searcher):
    def __init__(self, space, n_experiments, search_params):
        """
                This searcher use the user defined hyperparameters distribution to sample experiments hyperparameters.
                It's using sklearn ParameterSampler.
                :param space: (dict) hyperparameters search space. There 8 types of hyperparams space:
                hyperparams space examples:
                "space": {
                  "hyperparam2": { # static space example
                    "search_vals": val1,
                    "type": "static"
                  },
                  "hyperparam1": { # categorical space example
                    "search_vals": [val1, val2, val3],
                    "type": "categorical"
                  },
                  "hyperparam3": { # integer numeric space example
                    "search_vals": [low, high],
                    "type": "integer"
                  },
                  "hyperparam4": { # real numeric space example
                    "search_vals": [low, high],
                    "type": "real"
                  }
                }
                :param n_experiments: number of experiments to sample
                :param search_params: skopt Optimizer params:
                https://scikit-optimize.github.io/stable/modules/generated/skopt.Optimizer.html
                """
        super().__init__(space, n_experiments)

        self.search_params = search_params

        self._init_experiments(space, self.search_params)

        self._ix = 0

    def _init_optimizer(self, hyperparams_space, search_params):
        """
        Init skopt Optimizer. It will be used to perform bayesian search.
        :param hyperparams_space: user define space
        :param search_params: skopt Optimizer params
        """
        prepared_space = []

        for param_name in hyperparams_space.keys():
            prepared_space.append(self._get_skopt_space_vals(hyperparams_space[param_name], param_name=param_name))

        optimizer = skopt.Optimizer(prepared_space, **search_params)

        self._internal_optimizer = optimizer

    def _init_experiments(self, hyperparams_space, search_params):
        """
        Init searcher experiments. Because of the bayesian nature of the searcher, only the optimizer is
        being initialized
        :param hyperparams_space: user define space
        :param search_params: skopt Optimizer params
        """
        self._init_optimizer(hyperparams_space, search_params)

    def get_next_experiments(self, n=None):
        """
        Return a list of the next experiments. If n is None, return all the next experiments.
        :param n: number of experiment to return
        :return: (list) the n length experiments list (or all when n is None).
        """
        for hyperparams in self._internal_optimizer.ask(n):
            self._ix = self._ix + 1

            experiment = {'ix': self._ix}

            experiment.update({'hyperparams': dict(zip(self.space.keys(), hyperparams))})

            self.experiments_queue.put(experiment)

            if self._ix == self.n_experiments:

                break

        if n is None:
            n = 1

        # if experiments count left is lower than n return the remainder experiments
        if self.experiments_queue.qsize() % n != 0:
            n = self.experiments_queue.qsize() % n

        next_experiments = [self.experiments_queue.get() for _ in range(n)]

        return next_experiments

    def update_search(self, experiments, metric):
        """
        Update bayesian optimizer search by reporting past experiments results.
        :param experiments: (list) past experiments:
        [
            {
                'ix': 1,
                'hyperparams': {'param': val, ...},
                'scores: {'mertic': val, 'other_metric': val, ...}
            },
            ...
        ]
        :param metric: (str) metric name to extract from experiment scores.
        """
        # iterate experiments and use ask an tell skopt API to update skopt Optimzer bayesian search
        for experiment in experiments:
            self._internal_optimizer.tell(list(experiment['hyperparams'].values()),
                                          experiment['scores'][metric])

    def is_finished(self):
        """
       Check if the searcher work is done.
       :return: (bool) True if the experiments index reached experiments count limit and queue is empty
       """
        return (self._ix == self.n_experiments) & self.experiments_queue.empty()

    @staticmethod
    def _get_skopt_space_vals(param_space, param_name):
        """
        Get user defined single hyperparameter space and modify it to fit skopt Optimizer input.
        It's using skopt.space: Space:
        https://scikit-optimize.github.io/stable/modules/classes.html#module-skopt.space.space
        :param param_space: (dict) user defined hyperparams space
        :return: skopt.space: Space objects
        space
        """
        space = None

        if param_space['type'] == "integer":
            space = skopt.space.Integer(param_space['search_vals'][0],
                                        param_space['search_vals'][1],
                                        name=param_name)
        elif param_space['type'] == "real":
            space = skopt.space.Real(param_space['search_vals'][0],
                                     param_space['search_vals'][1],
                                     prior=param_space['type'],
                                     name=param_name)
        elif param_space['type'] in ["categorical"]:
            space = skopt.space.Categorical(param_space['search_vals'],
                                            name=param_name)
        elif param_space['type'] in ["static"]:
            space = skopt.space.Categorical([param_space['search_vals']],
                                            name=param_name)

        return space
