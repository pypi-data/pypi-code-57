from torchtrainer.callbacks.training_callback import TrainingCallback
from torchtrainer.trainer import Mode

class LRBatchSchedulerCallBack(TrainingCallback):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def on_batch_end(self, batch, log):
        if log['mode']==Mode.TRAIN:
            self.scheduler.step()
