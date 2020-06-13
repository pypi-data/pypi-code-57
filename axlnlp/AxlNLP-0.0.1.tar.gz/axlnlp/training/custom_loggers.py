
# comet
from comet_ml import Experiment

# pytorch
from torch import is_tensor

#pytroch lightnig
from pytorch_lightning.loggers import LightningLoggerBase, rank_zero_only

# numpy
import numpy as np

# am
from am import get_logger

logger = get_logger("Custom-Loggers")


class CustomCometLogger(LightningLoggerBase):

    def __init__(self, api_key:str, project_name:str,  workspace:str, experiment_name:str, cv:bool):
        super().__init__()
        self.collected_scores = {}
        self.last_epoch = 0
        self.current_fold = 0
        self.cv = cv

        self._experiment = None
        self.api_key = api_key
        self.project_name = project_name
        self.workspace = workspace
        self.experiment_name = experiment_name

    @property
    def experiment(self):

        #if there is an experiment object set up we use it
        if self._experiment is not None:
            return self._experiment


        #setting up the experiment object
        self._experiment = Experiment(     
                                                api_key=self.api_key, 
                                                project_name=self.project_name,
                                                workspace=self.workspace,
                                            )
        #self.name = self.experiment_name
        self._experiment.set_name(self.experiment_name)
        return self._experiment


    @rank_zero_only
    def log_hyperparams(self, hyperparams):
        if not hyperparams:
            logger.warning("None object passed to hyperparam logging ..")
        else:
            self.experiment.log_parameters(hyperparams)


    @rank_zero_only
    def log_metrics(self, metrics, step=None):

        if not metrics:
            return

        epoch = int(metrics["epoch"])

        # Comet.ml expects metrics to be a dictionary of detached tensors on CPU

        #if the current epoch is larger than the next epoch
        #print(self.last_epoch > epoch,self.last_epoch, epoch)
        if self.last_epoch > epoch:
            self.current_fold += 1

        for key, val in metrics.items():
            if is_tensor(val):
                val = val.cpu().detach()

            if self.cv:
                if epoch not in self.collected_scores:
                    self.collected_scores[epoch] = {}

                if key not in self.collected_scores[epoch]:
                    self.collected_scores[epoch][key] = []

                self.collected_scores[epoch][key].append(val)

                key = key + f"_FOLD_{self.current_fold}"

            self.experiment.log_metric(key, val, step=epoch)

        #save last epoch
        self.last_epoch = epoch


    def log_average_metrics(self):

        if not self.cv:
            raise NotImplementedError(f"Avarge metric logging is not supported for non cv training: {self.cv}")

        for epoch, metrics in self.collected_scores.items():
            for k,v in metrics.items():
                self.experiment.log_metric(k, np.mean(v), epoch=epoch)

    def log_tags(self, tags):
        self.experiment.add_tags(tags)


    #TODO LOG SCORE PER CLASS
    def log_score_per_class(self):
        pass
        
    @property
    def name(self) -> str:
        return self.experiment.project_name

    @name.setter
    def name(self, value: str) -> None:
        self.experiment.set_name(value)


    @property
    def version(self):
        return 1111


    # # @rank_zero_only
    # # def finalize(self, status: str) -> None:
    # #     r"""
    # #     When calling self.experiment.end(), that experiment won't log any more data to Comet. That's why, if you need
    # #     to log any more data you need to create an ExistingCometExperiment. For example, to log data when testing your
    # #     model after training, because when training is finalized CometLogger.finalize is called.

    # #     This happens automatically in the CometLogger.experiment property, when self._experiment is set to None
    # #     i.e. self.reset_experiment().
    # #     """
    # #     self.experiment.end()
    # #     self.reset_experiment()
