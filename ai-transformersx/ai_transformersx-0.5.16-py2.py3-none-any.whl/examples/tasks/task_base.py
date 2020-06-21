from collections import OrderedDict

from dataclasses import dataclass, field
import numpy as np
from sklearn.metrics import f1_score
from transformers.data.metrics import acc_and_f1, simple_accuracy
import ai_harness.harnessutils as utils

from ai_transformersx.legacy.configuration import parse_args
from ai_transformersx.legacy.tasks import TransformerTask
from ai_transformersx.legacy.trainer_utils import EvalPrediction

log = utils.getLogger('task')

ACTION_TYPES = OrderedDict([
    ('bert_base', ('bert', 'Base.Bert.bert', 'bert')),
    ('bert_hfl_wwm', ('bert', 'Base.Bert.bert_hfl_wwm', 'bert')),
    ('bert_hfl_wwm_ext', ('bert', 'Base.Bert.bert_hfl_wwm_ext', 'bert')),
    ('distil_bert', ('distilbert', 'Distil.Bert.bert_adamlin', 'distilbert')),
    ('electra_base', ('electra', 'Base.Electra.electra_hfl_disc', 'electra')),
    ('electra_small', ('electra', 'Small.Electra.electra_hfl_disc', 'electra')),
])


@dataclass
class DataArguments:
    data_dir: str = field(default='./dataset/news', metadata={'help': 'input the data dir for processing'})
    save_mid: bool = field(default=True, metadata={'help': 'whether cache the middle data for check'})
    context_min_len: int = field(default=128, metadata={'help': 'context min length'})
    sentence_min_len: int = field(default=10, metadata={'help': 'sentence min length'})
    positive_mode: int = field(default=0, metadata={'help': 'positive mode'})
    negative_mode: int = field(default=0, metadata={'help': 'negative mode'})
    bar_size: int = field(default=1000, metadata={'help': 'the progress bar size'})


class TaskBase:
    def __init__(self):
        self.task_args, self.other_args = parse_args(DataArguments)
        self.task_args.model_args.model_base_dir = './models/pretrained'
        self.task_args.training_args.output_dir = './models/finetuning'

    def __set_args(self, action_type):
        args = ACTION_TYPES.get(action_type)
        self.task_args.model_args.model_type = args[0]
        self.task_args.model_args.model_name = args[1]
        # self.task_args.model_args.freeze_parameter = args[2]

    def train(self, action_type):
        self.task_args.training_args.train()
        self.__set_args(action_type)
        TransformerTask(self.task_args, self._data_processor(),
                        compute_metric=self._compute_metrics).train()

    def eval(self, action_type):
        self.task_args.training_args.do_eval = True
        self.__set_args(action_type)
        TransformerTask(self.task_args, self._data_processor(),
                        compute_metric=self._compute_metrics).eval()

    def _acc_and_f1(self, preds, labels):
        acc = simple_accuracy(preds, labels)
        f1 = f1_score(y_true=labels, y_pred=preds, average="weighted")
        return {
            "acc": acc,
            "f1": f1,
            "acc_and_f1": (acc + f1) / 2,
        }

    def _compute_metrics(self, p: EvalPrediction):
        preds = np.argmax(p.predictions, axis=1)
        result = self._acc_and_f1(preds, p.label_ids)
        return result

    def _data_processor(self):
        raise NotImplementedError
