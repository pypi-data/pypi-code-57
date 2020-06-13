import torch
from torchnet.meter import AverageValueMeter
from torchtrainer.callbacks.training_callback import TrainingCallback
import pandas as pd

class CalculateAccuracyPerClassCallback(TrainingCallback):
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.average_value_meters = [AverageValueMeter() for x in range(self.num_classes)]

    def on_mode_begin(self, mode, log):
        for class_index, average_value_meter in enumerate(self.average_value_meters):
            average_value_meter.reset()
            log["Class {:d} Accuracy".format(class_index)] = float('NaN')

    def on_batch_end(self, batch, log):
        #batch_size = log['batch_size']
        gt = log['gt'].to("cpu")
        output = log['output'].to("cpu")

        _, preds = torch.max(output, 1)
        for item_index, item_gt in enumerate(gt):
            if(item_gt == preds[item_index]):
                self.average_value_meters[item_gt].add(1)
            else:
                self.average_value_meters[item_gt].add(0)

        for class_index, average_value_meter in enumerate(self.average_value_meters):
            log["Class {:d} Accuracy".format(class_index)] = average_value_meter.value()[0]
