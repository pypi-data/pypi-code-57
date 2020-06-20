import json
from copy import copy

# internal
from .reporting import Reporter
from .experimenting import LocalExperimenter

"""
-----------------------------------------------Some definitions:--------------------------------------------------------

[Experiment Design] - a user defined experiment. The [Experiment Design] is being expressed by a func, which will be 
executed by an [Experimenter/s].

[Experiment] - a combination of hyper parameters to be tested while running [Experiment Design].

[Experiment Run] - using the [Experiment Configuration] and [Experiment Design], numerous [Experiments] will be 
executed. The [Experiment Run] will output best [Experiment] (best hyper parameters combination).

[Experiment Configuration] - sets of configurations which will define the [Experiments] to be executed in Experiment 
Run.

[LabManager] - running all the [Experiments Configurations] as defined in a config file. A [LabManager] can perform 
numerous [Experiment Configuration] and [Experiment Design]

[Experimenter] - an entity which perform the tuning/experimenting process. 

[Searcher] - an entity used by an [Experimenter] to create the [Experiments] in Experiment Run. The [Searcher] use the 
defined space in [Experiment Configuration].


-----------------------------------------------Experiment Work Flow:----------------------------------------------------

1) Build Experiment code - data loading, model fitting (CV/Test/etc..), evaluation 
2) Construct the experiments config file to include the desired experimenters and the tuning configuration.
3) Run labs/experimenters. 

------------------------------------------------------------------------------------------------------------------------

"""


class LabManager:
    def __init__(self, config_path, logger=None, slack_config=None):
        """
        Extract the [Experiments Configurations] from config file and construct [Experimenters].
        :param config_path: (str) the config json file path.
        :param logger: (Logger) if user desire a different logger than the default logger, he can use his own defined
        logger. Important - it must be named "Labs" to prevent duplicated logs (logging.getLogger('Labs'))
        :param slack_config: (dict) slack configuration to report a slack recipient. Structure:
        {"slack_token": token, "recipient": #channel/@user}
        """
        # load config file
        with open(config_path, 'r') as fp:
            self._config = json.load(fp)

        # extract [Experiments Configurations] form config file
        self.experimenters_config = [experimenter for experimenter in self._config['experiments']]

        # research/production
        self.mode = self._config['mode']

        # local/docker/kubernetees
        self.type = self._config['type']

        self._reporter = Reporter(logger, slack_config)

        self.experimenters = self.init_experimenters()

    def init_experimenters(self):
        """
        Using the experimenters_config, [Experimenters] objects will be created for each [Experiment Configuration].
        :return: (list) Experimenters objects
        """

        experiments = []

        for experimenter in self.experimenters_config:
            experiment_object = object
            experimenter_config = copy(experimenter)

            # construct experiments
            if self.type == 'local':
                experiment_object = LocalExperimenter(**experimenter_config)

                # set reporter
                experiment_object.set_reporter(self._reporter)

            experiments.append(experiment_object)

        return experiments

    def run_experimenters(self, experiments_callables, subset=None, experiment_callback=None):
        """
        Run the [Experimenters] in self.experimenters sequentially. Each [Experimenter] need it's [Experiment Design]
        func. This is done by experiments_callables (dict), using the it's keys as mapping to [Experiment Design]
        func.
        :param experiments_callables: (dict) mapping between [Experimenter]/[Experiment Configuration] to
        [Experiment Design] func. Structure - {'experiment_name1': func1, 'experiment_name2': func2, ..}
        :param subset: (list) user can select only subset of the [Experimenters]. The subset need to contain a list of
        the desired [Experimenters] experiment_name - ['experiment_name1', 'experiment_name2', ..].
        If None, all selected.
        :param experiment_callback: (callable) a method to apply when [Experimenter] [Experiment] is ended.
        """
        n_experimenters = len(self.experimenters) if subset is None else len(subset)

        self._reporter.report_status('LabManager - start running experimenters')

        self._reporter.report_status('LabManager - {} experimenters are in queue'.format(n_experimenters))

        # select subset
        if subset is None:
            subset = [experiment.experiment_name for experiment in self.experimenters]

        ix = 1

        for experimenter in self.experimenters:
            if experimenter.experiment_name in subset:

                experimenter.run_experiments(experiments_callables[experimenter.experiment_name],
                                             experiment_callback)

                self._reporter.report_status('LabManager - {} experimenters are left'.format(n_experimenters - ix))

                ix = ix + 1

        self._reporter.report_status('LabManager - finish experimenters work')
