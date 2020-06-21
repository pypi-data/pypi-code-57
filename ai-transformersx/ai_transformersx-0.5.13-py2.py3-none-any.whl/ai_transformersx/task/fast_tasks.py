from .fast_task_args import FastTaskArguments
from fast_bert.learner_abs import BertAbsDataBunch, BertAbsLearner
from fast_bert.learner_cls import BertDataBunch, BertLearner
from fast_bert.learner_lm import BertLMDataBunch, BertLMLearner
from fast_bert.learner_qa import BertQADataBunch, BertQALearner
from fast_bert.prediction import BertClassificationPredictor


class TransformersFastTask():
    def __int__(self, args: FastTaskArguments):
        self._args = args


class TransformersFastAbsTask(TransformersFastTask):
    def __int__(self, args: FastTaskArguments):
        super().__int__(args)


class TransformersFastClsTask(TransformersFastTask):
    def __int__(self, args: FastTaskArguments):
        super().__int__(args)

    def create_databunch(self):
        databunch = BertDataBunch(DATA_PATH, LABEL_PATH,
                                  tokenizer='bert-base-uncased',
                                  train_file='train.csv',
                                  val_file='val.csv',
                                  label_file='labels.csv',
                                  text_col='text',
                                  label_col='label',
                                  batch_size_per_gpu=16,
                                  max_seq_length=512,
                                  multi_gpu=True,
                                  multi_label=False,
                                  model_type='bert')


class TransformersFastLmTask(TransformersFastTask):
    def __int__(self, args: FastTaskArguments):
        super().__int__(args)


class TransformersFastQaTask(TransformersFastTask):
    def __int__(self, args: FastTaskArguments):
        super().__int__(args)
