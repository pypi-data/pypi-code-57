from abc import ABC, abstractmethod
import os
import json
import datetime
import time
import shutil
import numpy as np
import hashlib

# dask
import dask

# internal
from .searchers import *
from .lab_utils import min_max_comparison, clear_dir
from .reporting import Reporter


class _Experimenter(ABC):
    def __init__(self,
                 run_id='',
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
        :param experiment_name: [Experiment Configuration] name (when is production should use the same experiment name)
        :param description: description of the experiment
        :param problem_name: the use case module name (e.g. PredictStockPrices)
        :param mode: execution mode - [research, production]
        :param artifacts_path: path to save experiments artifacts
        :param dask_config: dask client config
        :param tune_config: tuning config used by Searcher object and the tune flow:
            "tune_config": {
                "space": {
                    ....
                  },
                },
                "search_params": {
                    ..
                },
                "n_experiments": 1,
                "experiments_batch_size": 1,
                "type": "search_type",
                "score_threshold": 0
            }
        :param evaluation_config: metrics and main metric config:
           "evaluation_config": {
                "metrics": {
                  "METRIC1": "min",
                  "METRIC2": "max"
                },
                "main_metric": "METRIC1"
           }
        :param logger: a logging logger instance
        :param slack_config: a Slacker instance
        """

        self.experiment_name = 'ExperimentUnknown' if experiment_name == '' else experiment_name
        self.run_id = self._init_run_id() if run_id is None else run_id

        self.description = description
        self.problem_name = problem_name

        self.artifacts_path = os.path.join(artifacts_path, self.experiment_name)

        # config
        self.dask_config = dask_config
        self.tune_config = tune_config
        self.evaluation_config = evaluation_config

        self.experiments_batch_size = self._init_experiments_batch_size()

        # reporters
        self._reporter = Reporter(logger, slack_config)

        # metadata dictionaries
        self.run_meta_data = {}
        self.run_results = {}
        self.time_records = {}

        # delete or not experiments dirs when run iso finished
        if self.tune_config.get('delete_experiments') is None:
            self.delete_experiments = False
        else:
            self.delete_experiments = self.tune_config['delete_experiments']

        # evaluation
        self.metrics = self.evaluation_config['metrics']
        self.main_metric = self.evaluation_config['main_metric']
        self.score_threshold = self._init_score_threshold()

        # best experiment params
        self.best_experiment = {}

        # searcher instance use in tuning
        self._tune_searcher = self._init_searcher()

        self.mode = mode

    def _init_experiments_batch_size(self):
        """
        Set the experiments count in each execution iteration.
        :return:
        """
        # if user didn't defined batch size
        if self.tune_config.get('experiments_batch_size') is None:
            # if dask config doesn't contain n_workers
            if self.dask_config.get('n_workers') is None:
                # batch size = 1
                return 1
            else:
                # batch size = number of dask workers
                return self.dask_config.get('n_workers')

        return self.tune_config.get('experiments_batch_size')

    def _init_searcher(self):
        """
        Given user defined tune config, initialize the [Experimenter] searcher
        :return: (Searcher) a configured searcher obj
        """
        search_type = self.tune_config['type']
        searcher = None

        if search_type == 'list':
            searcher = ListSearcher(self.tune_config['space'])
        elif search_type == 'grid-search':
            searcher = GridSearcher(self.tune_config['space'])
        elif search_type == 'random-search':
            searcher = RandomSearcher(self.tune_config['space'],
                                      self.tune_config['n_experiments'],
                                      self.tune_config['search_params'])
        elif search_type == 'skopt':
            searcher = SkoptSearcher(self.tune_config['space'],
                                     self.tune_config['n_experiments'],
                                     self.tune_config['search_params'])

        return searcher

    def _init_score_threshold(self):
        """
        Initialize score threshold for tuning process.
        If not defined, set +-inf values
        :return: (float)
        """
        score_threshold = np.float(self.tune_config.get('score_threshold'))

        # user didn't defined
        if score_threshold is None:
            if self.metrics[self.main_metric] == 'min':
                # main metric is minimized
                score_threshold = -np.inf
            elif self.metrics[self.main_metric] == 'max':
                # main metric is maximized
                score_threshold = np.inf

        return score_threshold

    @abstractmethod
    def _init_dask_client(self):
        """
        initialize dask.distributed Client
        :return: (Client) dask client
        """

    def _init_run_id(self):
        """
        Generate run Id using experiment name, current date and md5 hashing:
        [experiment_name]-[timestamp]-[md5([experiment_name]-[timestamp])]
        :return: (str) generate run id
        """
        date_format_suffix = "%Y-%m-%d-%H-%M-%S"
        timestamp = datetime.datetime.now().strftime(date_format_suffix)

        base = self.experiment_name + '-' + timestamp

        run_id = base + '-' + hashlib.md5(base.encode()).hexdigest()

        return run_id

    def _create_run_skeleton(self):
        """
        create the run artifacts skeleton
        /artifacts dir
           /{run_id}
              /final_model
              /experiment_1
              /experiment_2
        """
        # create artifacts run dir if not exist else clear dir
        if not os.path.exists(self.artifacts_path):
            os.makedirs(self.artifacts_path)
        else:
            clear_dir(self.artifacts_path, '')

        # create final_model dir
        if not os.path.exists(os.path.join(self.artifacts_path, 'final_model')):
            os.makedirs(os.path.join(self.artifacts_path, 'final_model'))

    def run_experiments(self, experiment_func, experiment_callback=None):
        """
        Run experimenter experiments. When the experimenter tune is done, save the run report, metadata and shutdown
        dask client.
        :param experiment_func: (callable) The user [Experiment Design].
        :param experiment_callback: (callable) a method to apply when experiment is ended.
        """
        self._reporter.report_status('Experiment {} - start experiments'.format(self.experiment_name))

        client = self._init_dask_client()

        self._create_run_skeleton()

        self._tune(experiment_func, experiment_callback)

        self._save_run_report()

        self._reporter.report_status('Experiment {} - experiments report was generated'.format(self.experiment_name))

        self._update_metadata()

        self._save_run_artifacts()

        self._reporter.report_status('Experiment {} - experiments artifacts were saved'.format(self.experiment_name))

        self._save_run_metadata()

        self._reporter.report_status('Experiment {} - experiments metadata was saved'.format(self.experiment_name))

        client.shutdown()
        client.close()

        self._reporter.report_status('Experiment {} - finished experiments'.format(self.experiment_name))

    def _tune(self, experiment_func, experiment_callback=None):
        """
        Tune process of the experiments. It is executing the tune_flow with the experiment_func.
        The tune process will output the run results and the best_experiment due to main_metric.
        :param experiment_func: (callable) the user [Experiment Design].
        :param experiment_callback: (callable) a method to apply when experiment is ended.
        """
        start_time = time.time()

        results = self._tune_flow(experiment_func, experiment_callback)

        self.run_results = results['experiments_results']

        self.best_experiment = results['best_experiment']

        end_time = time.time()

        self._record_time(start_time, end_time)

    def _tune_flow(self, experiment_func, experiment_callback=None):
        """
        The tune process flow. Getting experiments from Searcher until Searcher finished all experiments
        or score_threshold was reached. The experiments execution is done by batches (experiments_batch_size).
        Each batch is being executed, processed and saved to experiments_results list. dask workers executing the
        experiments by the lazy dask delayed API.

        :param experiment_func: (callable) the user [Experiment Design].
        :param experiment_callback: (callable) a method to apply when experiment is ended.
        :return: (dict) return the tune_flow results. Structure:
        {
            'experiments_results': [
                {
                    'ix': val,
                    'hyperparams': {'pram1': val, ...},
                    'scores': {'METRIC1': val, ...}
                }, ...
            ],
            'best_experiment': {
                    'ix': val,
                    'hyperparams': {'pram1': val, ...},
                    'scores': {'METRIC1': val, ...}
                }
        }
        """
        experiments_results = []

        self._reporter.report_status('Experiment {} Tune - {} experiments '
                                     'are in the oven'.format(self.experiment_name, self._tune_searcher.n_experiments))

        self._reporter.report_status('Experiment {} Tune - start executing experiments'.format(self.experiment_name))

        while not self._tune_searcher.is_finished():

            # get next experiments
            experiments = self._tune_searcher.get_next_experiments(n=self.experiments_batch_size)

            # experiments delayed list
            experiments_delayed = []

            # loop experiments batch
            for experiment in experiments:
                experiment_artifacts_path = os.path.join(self.artifacts_path, 'experiment_' + str(experiment['ix']))

                # delayed
                delayed_experiment = dask.delayed(self._execute_experiment)(experiment_func,
                                                                            experiment,
                                                                            experiment_artifacts_path,
                                                                            list(self.metrics.keys()))
                experiments_delayed.append(delayed_experiment)

            # execute experiments
            experiments_executed = dask.compute(experiments_delayed)[0]

            # get experiments results
            experiments_batch_results = [self._get_experiment_results(
                experiment) for experiment in experiments_executed]

            # sort results by experiment ix
            # experiments_batch_results = sorted(experiments_batch_results, key=lambda i: i['ix'], reverse=False)

            # update Searcher
            self._tune_searcher.update_search(experiments_batch_results, self.main_metric)

            # update experiments_results list
            [experiments_results.append(experiment_results) for experiment_results in experiments_batch_results]

            # report experiments batch results
            [self._report_experiment(experiment_results,
                                     experiment_callback) for experiment_results in experiments_batch_results]

            # check if threshold score was reached
            if self._is_score_threshold_reached(experiments_batch_results):

                break

            # get best experiment
            best_experiment = self._get_best_experiment(experiments_results)

            self._report_best_experiment(best_experiment)

        # get best experiment when tune flow is finished
        best_experiment = self._get_best_experiment(experiments_results)

        self._report_best_experiment(best_experiment)

        self._reporter.report_status('Experiment {} Tune - finished executing experiments'.format(self.experiment_name))

        return {'experiments_results': experiments_results, 'best_experiment': best_experiment}

    @staticmethod
    @abstractmethod
    def _execute_experiment(experiment_func, experiment, artifacts_path, metrics):
        """
        Static method to be executed by dask worker. Will be implemented by [Experimenter] inheritance.
        :param experiment_func: (callable) The user [Experiment Design].
        :param experiment: (dict) the experiment. Structure: {'ix': val, 'hyperparams': {'param1': val, ...}}
        :param metrics: (list) metrics list. Structure: ['METRIC1', 'METRIC2'].
        :param artifacts_path: (str) path to save experiment ix artifacts.
        :return: (dict) experiment results - same structure as input experiment (results will be added later)
        """

    @abstractmethod
    def _get_experiment_results(self, experiments_executed):
        """
        Get experiments batch results. Will be implemented by [Experimenter] inheritance.
        :param experiments_executed: (list) executed experiments dicts. Structure:
        [
            {
                'ix': val,
                'hyperparams': {'param1': val, ...}
            }, ...
        ]
        :return: (list) executed experiments dicts with their scores. Structure:
        [
            {
                'ix': val,
                'hyperparams': {'param1': val, ...},
                'scores': {'METRIC1': val, ..}
            }, ...
        ]
        """

    def _get_best_experiment(self, experiments_results):
        """
        Getting from experiments_results the best experiment due to main metric
        :param experiments_results: (list) experiments results dictionaries. Structure:
        [
            {
                'ix': val,
                'hyperparams': {'pram1': val, ...},
                'scores': {'METRIC1': val, ...}
            }, ...
        ]
        :return: (dict) from experiments_results list, the best experiment dict
        """
        # main metric
        main_metric = self.evaluation_config['main_metric']

        # is main_metric need to be maximized or minimized
        is_max = self.metrics.get(main_metric) == 'max'

        # sort experiments and get the first element of sorting a.k.a best experiment.
        best_experiment = sorted(experiments_results,
                                 key=lambda i: i['scores'][main_metric],
                                 reverse=is_max)[0]

        return best_experiment

    def _is_score_threshold_reached(self, experiments):
        """
        Check if the experiments executed reached the score threshold.
        :param experiments: (list) executed experiments dicts with their scores. Structure:
        [
            {
                'ix': val,
                'hyperparams': {'param1': val, ...},
                'scores': {'METRIC1': val, ..}
            }, ...
        ]
        :return: (bool) if we reached the threshold score
        """
        # iterate experiments
        for experiment in experiments:
            # compare experiment main_metric score with threshold score.
            reached_threshold = min_max_comparison(experiment['scores'][self.main_metric],
                                                   self.score_threshold,
                                                   self.metrics[self.main_metric])
            if reached_threshold:
                return True

        return False

    def _report_experiment(self, experiment_result, experiment_callback=None):
        """
        Report single experiment results internal (logging and slack), external (experiment_callback).
        :param experiment_result: (dict) a single experiment result dict. Structure:
        {
            'ix': val,
            'hyperparams': {'param1': val, ...},
            'scores': {'METRIC1': val, ..}
        }
        :param experiment_callback: (callable) a method to apply when experiment is ended.
        """
        main_metric = self.evaluation_config['main_metric']

        # internal
        self._internal_experiment_report(experiment_result, main_metric)

        # external
        self.external_experiment_report(experiment_callback, self.experiment_name, experiment_result, main_metric)

    def _internal_experiment_report(self, experiment_result, main_metric):
        """
        Report by [Experimenter] Reporter the experiment result.
        :param experiment_result: (dict) a single experiment result dict. Structure:
        {
            'ix': val,
            'hyperparams': {'param1': val, ...},
            'scores': {'METRIC1': val, ..}
        }
        :param main_metric: (str) user defined main metric.
        """
        msg = """Iteration {}:
{} Score: {} 
Hyperparameters: {}""".format(experiment_result['ix'],
                              main_metric,
                              experiment_result['scores'][main_metric],
                              experiment_result['hyperparams'])

        self._reporter.report_status(msg)

    def _report_best_experiment(self, best_experiment):
        """
        Report by [Experimenter] Reporter the best experiment result.
        :param best_experiment: (dict) the best experiment dict. Structure:
        {
            'ix': val,
            'hyperparams': {'param1': val, ...},
            'scores': {'METRIC1': val, ..}
        }
        :return:
        """
        msg = """Best Iteration - {}:
{} Score: {}
Hyperparameters: {}""".format(best_experiment['ix'],
                              self.evaluation_config['main_metric'],
                              best_experiment['scores'][self.main_metric],
                              best_experiment['hyperparams'])
        self._reporter.report_status(msg)

    @staticmethod
    def external_experiment_report(experiment_callback, experiment_name, experiment_result, main_metric):
        """
        Report Using user defined experiment_callback.
        :param experiment_callback: (callable) a method to apply when experiment is ended.
        :param experiment_name: [Experiment Configuration] name (when is production should use
        the same experiment name).
        :param experiment_result: (dict) a single experiment result dict. Structure:
        {
            'ix': val,
            'hyperparams': {'param1': val, ...},
            'scores': {'METRIC1': val, ..}
        }
        :param main_metric: (str) user defined main metric.
        """
        if experiment_callback is not None:
            # get experiment hyperparams
            hyperparams = experiment_result['experiment_result']

            # get experiment ix
            ix = experiment_result['ix']

            # get experiment main_metric score
            score = experiment_result['scores'][main_metric]

            # execute callback
            experiment_callback(experiment_name, ix, hyperparams, score)
    
    def _record_time(self, start, end):
        """
        Populate tune execution time metadata.
        :param start: (float) Start execution time (seconds from epoch)
        :param end: (float) End execution time (seconds from epoch)
        """
        self.time_records['start'] = datetime.datetime.fromtimestamp(start)
        self.time_records['end'] = datetime.datetime.fromtimestamp(end)
        self.time_records['total_time_secs'] = np.round(end-start, 3)
        self.time_records['total_time_mins'] = np.round((end-start)/60, 3)
        self.time_records['total_time_hours'] = np.round((end-start)/60**2, 3)

    def _update_metadata(self):
        """
        Update metadata dict running time.
        """
        self.run_meta_data.update(self.time_records)

    def _save_run_report(self):
        """
        Create a json file of the Experimenter execution results
        """
        # type handling when saving json (numpy types)
        def default(o):
            if isinstance(o, np.int) or isinstance(o, np.int16) or isinstance(o, np.int32) or isinstance(o, np.int64):
                return int(o)
            if isinstance(o, np.float) or isinstance(o, np.float16) or isinstance(o, np.float32) or \
                    isinstance(o, np.float64):
                return float(o)
            raise TypeError

        # save json
        with open(os.path.join(self.artifacts_path, 'final_model', self.experiment_name + '_report.json'),
                  'w', encoding='utf-8') as f:
            json.dump(self.run_results, f, ensure_ascii=False, indent=4, default=default)

    def _clear_experiments(self):
        """
        Clear experiments artifacts dir from the experiments, except of final model dir.
        """
        clear_dir(self.artifacts_path, 'experiment')

    def _save_run_artifacts(self):
        """
        Save best experiment artifacts in final_model dir
        """
        best_experiment_ix = self.best_experiment['ix']

        # artifacts source path
        source = os.path.join(self.artifacts_path, 'experiment_' + str(best_experiment_ix))

        # final_model artifacts destination path
        destination = os.path.join(self.artifacts_path, 'final_model')

        # artifacts source path files
        files = os.listdir(source)

        # copy files to destination
        for f in files:
            file_source = os.path.join(source, f)
            shutil.copy(file_source, destination)

        # clear experiments dirs from artifacts dir
        if self.delete_experiments:
            self._clear_experiments()

    def _save_run_metadata(self):
        """
        Save [Experiment Run] metadata as json file.
        """
        file_path = os.path.join(self.artifacts_path, 'final_model', self.experiment_name + '_metadata.json')

        # type handling when saving json (numpy types)
        def default(o):
            if isinstance(o, np.int) or isinstance(o, np.int16) or isinstance(o, np.int32) or isinstance(o, np.int64):
                return int(o)
            if isinstance(o, np.float) or isinstance(o, np.float16) or isinstance(o, np.float32) or \
                    isinstance(o, np.float64):
                return float(o)
            if isinstance(o, datetime.datetime):
                return str(o)
            raise TypeError

        # save json file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.run_meta_data, f, ensure_ascii=False, indent=4, default=default)

    def set_reporter(self, reporter):
        """
        Set the reporter property. Is being used when self is part of LabManager execution.
        :param reporter: (Reporter) the LabManager Reporter obj
        """
        self._reporter = reporter
