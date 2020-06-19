import unittest

import numpy as np
import pandas as pd
import tensorflow as tf

from researcher.torch_train import *
from researcher.starters import *


def make_ce_losses(cols, loss_fn):
    def losses(y, pred, idx):
        current_y = y.iloc[[idx]]

        loss = 0

        for i, col in enumerate(cols):
            loss += loss_fn(torch.unsqueeze(pred[i][idx], 0), torch.unsqueeze(current_y[col].item(), 0))
        return loss.numpy()

    return losses

class TestLoggers(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_pickle("researcher/data/example.pkl")

    def test_correct_val_loss_logging(self):
        history = {}
        metric = ComplexMetric([LossLogger("test", lambda a, b, c: 10)], make_dict_writer(history), self.data, 4)

        for i in range(20):
            metric.collect(
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])], 
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])],
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])],
                i,
            )
        
        metric.write(0)

        self.assertEqual(1, len(history["test"]))
        self.assertEqual(10.0, history["test"][0])

        metric = ComplexMetric([LossLogger("test", lambda a, b, c: 10)], make_dict_writer(history), self.data, 4)
        for i in range(20):
            metric.collect(
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])], 
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])],
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])],
                i,
            )
        metric.collect(
            [np.array([3, 1, 2, 3, 7, 7, 7]), np.array([3, 1, 2, 3, 7, 7, 7])], 
            [np.array([3, 1, 2, 3, 7, 7, 7]), np.array([3, 1, 2, 3, 7, 7, 7])],
            [np.array([3, 1, 2, 3, 7, 7, 7]), np.array([3, 1, 2, 3, 7, 7, 7])],
            20,
        )
        
        metric.write(1)

        self.assertEqual(2, len(history["test"]))
        self.assertEqual(10.0, history["test"][0])
        self.assertEqual(10.0, history["test"][1])

    def test_epoch_loss_alignment(self):
        history = {}

        tensor_data = self.data.copy()
        tensor_data["start_ids"] = tensor_data["start_ids"].apply(lambda x: torch.argmax(torch.Tensor(x))) 
        tensor_data["end_ids"] = tensor_data["end_ids"].apply(lambda x: torch.argmax(torch.Tensor(x))) 

        metric = ComplexMetric([LossLogger("test", make_ce_losses(["start_ids", "end_ids"], torch.nn.CrossEntropyLoss()))], make_dict_writer(history), tensor_data, 4)

        for i in range(10):
            start_idx = i * 4
            end_idx = i * 4 + 4
            metric.collect(
                torch.Tensor([np.array([i.astype(float) * 99999 for i in self.data["start_ids"][start_idx:end_idx].values]), np.array([i.astype(float) * 99999for i in self.data["end_ids"][start_idx:end_idx].values])]), 
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])],
                [np.array([3, 1, 2, 3]), np.array([3, 1, 2, 3])],
                i,
            )
        
        metric.write(0)

        self.assertEqual(1, len(history["test"]))
        self.assertAlmostEqual(0, history["test"][0])