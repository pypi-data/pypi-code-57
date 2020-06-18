from ai_transformersx.data import DataProcessor

import pandas as pd

from ai_transformersx.train import InputExample
from ..task_base import TaskBase, DataArguments
from ai_harness.fileutils import join_path
from ai_harness.harnessutils import getLogger

log = getLogger("task")


class SentimentDataProcessor(DataProcessor):
    def __init__(self, config: DataArguments):
        self._config = config

    def _get_example(self, file_name, type):
        pd_all = pd.read_csv(join_path(self._config.data_dir, file_name))

        log.info("Read data from {}, length={}".format(join_path(self._config.data_dir, file_name), len(pd_all)))
        examples = []
        for i, d in enumerate(pd_all.values):
            examples.append(InputExample(guid=type + '_' + str(i),
                                         text_a=d[1],
                                         label=str(d[0])))

        return examples

    def get_train_examples(self):
        return self._get_example('train.csv', 'train')

    def get_dev_examples(self):
        return self._get_example('dev.csv', 'dev')

    def get_labels(self):
        return ['0', '1', '2', '3']

    def data_dir(self):
        return self._config.data_dir


class SentimentTask(TaskBase):
    def __init__(self):
        super().__init__()
        self.task_args.model_args.num_labels = 4

    def _data_processor(self):
        return SentimentDataProcessor(self.other_args[0])
