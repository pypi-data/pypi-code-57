import json
import os

# dask
from dask.distributed import LocalCluster, Client

# internal
from .base import _Experimenter


class LocalExperimenter(_Experimenter):
    def __init__(self, run_id='',
                 experiment_name='',
                 description='',
                 problem_name='',
                 mode='research',
                 artifacts_path='',
                 dask_config=None,
                 tune_config=None,
                 evaluation_config=None,
                 logger=None,
                 slack_config=None):
        """

        :param run_id: The experiment name run id
        :param experiment_name: Experiment name (when is production should use the same experiment name)
        :param description: description of the experiment
        :param problem_name: the use case module name (e.g. PredictStockPrices)
        :param mode: execution mode - [research, production]
        :param artifacts_path: path to save experiments artifacts
        :param dask_config: dask client config
        :param tune_config: tuning config used by Searcher object and the tune flow. more info in base.
        :param evaluation_config: metrics and main metric config. more info in base.
        :param logger: a logging logger instance
        :param slack_config: (dict) slack configuration to report a slack recipient.
        Structure: {"slack_token": token, "recipient": #channel/@user}
        """
        # experiment metadata
        super().__init__(run_id,
                         experiment_name,
                         description,
                         problem_name,
                         mode,
                         artifacts_path,
                         dask_config,
                         tune_config,
                         evaluation_config,
                         logger,
                         slack_config)

        # experiments run metadata
        self.run_meta_data.update(
            dict(experiment_name='Unknown' if experiment_name == '' else experiment_name,
                 run_id=self.run_id,
                 description=self.description,
                 problem_name=self.problem_name,
                 artifacts_path=self.artifacts_path,
                 mode=mode)
        )

    def _init_dask_client(self):
        """
        Initialize the experimenter dask client.
        :return: (Client) a Client instance
        """
        # local cluster
        cluster = LocalCluster(**self.dask_config)
        client = Client(cluster)

        return client

    @staticmethod
    def _execute_experiment(execution_callable, experiment, artifacts_path, metrics):
        """

        :param execution_callable: static method that execute single experiment
        :param experiment: the experiment - {'ix': nubmer, 'hyperparams': {'param1': value, ...}}
        :param artifacts_path: - path to save experiment ix artifacts
        :param metrics: metrics list - ['METRIC1', 'METRIC2']
        :return: results dict - structure depend on the user
        """

        # execute the experiment
        execution_callable(experiment, artifacts_path, metrics)

        return experiment

    def _get_experiment_results(self, experiment_executed):
        """

        :param experiment_executed: (dict) the experiment after being executed:
        {'ix': nubmer, 'hyperparams': {'param1': value, ...}}
        :return: (dict) experiment with related score loaded from local json file:
        {'ix': nubmer, 'hyperparams': {'param1': value, ...}, 'scores': {'metric1': val, ..}}
        """
        # local related experiment path
        experiment_artifacts_path = os.path.join(self.artifacts_path, 'experiment_' + str(experiment_executed['ix']))

        # load scores from related path
        with open(experiment_artifacts_path + '/' + 'scores.json', 'r') as f:
            scores = json.load(f).get('scores')

        # add scores
        experiment_executed['scores'] = scores

        return experiment_executed
