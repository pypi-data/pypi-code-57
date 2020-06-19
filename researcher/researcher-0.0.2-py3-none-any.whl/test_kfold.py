import unittest

import numpy as np
import pandas as pd
import tensorflow as tf

from researcher.kfold import *

class TestLosses(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_pickle("researcher/data/example.pkl")

    def test_tf_splitting(self):
        k = KFoldTFSplit(5, self.data, ["text_ids", "attention", "token_types"], ["start_ids", "end_ids"])

        train, val, X_train, y_train, X_val, y_val = k.get_data(4)

        self.assertEqual(240, len(train))
        self.assertEqual(60, len(val))
        self.assertEqual(2, len(y_val))
        self.assertEqual(60, len(y_val[0]))
        self.assertEqual(3, len(X_train))
        self.assertEqual(240, len(X_train[0]))

        train2, val2, X_train, y_train, X_val, y_val = k.get_data(0)

        self.assertEqual(240, len(train2))
        self.assertEqual(60, len(val2))
        self.assertEqual(2, len(y_val))
        self.assertEqual(60, len(y_val[0]))
        self.assertEqual(3, len(X_train))
        self.assertEqual(240, len(X_train[0]))

        self.assertEqual(180, len(set(train2["textID"].values) &set(train["textID"].values)))
        self.assertEqual(0, len(set(val2["textID"].values) &set(val["textID"].values)))

    def test_torch_splitting(self):
        k = KFoldTorchSplit(5, self.data, ["text_ids", "attention", "token_types", "start_ids", "end_ids"], 10)

        train, val, train_df, val_df = k.get_data(4)

        train_df["text"]

        self.assertEqual(24, len(train))
        self.assertEqual((240, 12), train_df.shape)
        self.assertEqual(6, len(val))
        self.assertEqual((60, 12), val_df.shape)

        train2, val2, train_df, val_df = k.get_data(0)

        self.assertEqual(24, len(train2))
        self.assertEqual(6, len(val2))

    def test_torch_all(self):
        k = KFoldTorchSplit(5, self.data, ["text_ids", "attention", "token_types", "start_ids", "end_ids"], 10)

        train, val, _, _ = k.get_data(None)

        self.assertIsNone(val)
        self.assertEqual(30, len(train))