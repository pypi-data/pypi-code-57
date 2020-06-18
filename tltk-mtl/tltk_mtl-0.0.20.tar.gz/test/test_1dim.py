import unittest
import sys
import os
import tltk_mtl as MTL
import numpy as np
import time


class TestStringMethods(unittest.TestCase):
    def test_one_dim_and(self):
        mode = 'cpu_threaded'

        Ar1 = 1
        br1 = 160

        Ar2 = 1
        br2 = 4500

        traces = {}
        traces['data1'] = np.array([100, 140, 130, 100, 160], dtype=np.float32)
        traces['data2'] = np.array(
            [4000, 4100, 4600, 4150, 4200], dtype=np.float32)

        time_stamps = np.array([1, 2, 3, 4, 5], dtype=np.float32)

        pred1 = MTL.Predicate('data1', Ar1, br1)
        pred2 = MTL.Predicate('data2', Ar2, br2)

        root = MTL.And(pred1, pred2, mode)
        root.eval_interval(traces, time_stamps)

        self.assertEqual(root.robustness, 60)

    def test_one_dim_or(self):

        mode = 'cpu_threaded'

        Ar1 = 1
        br1 = 160

        Ar2 = 1
        br2 = 4500

        traces = {}
        traces['data1'] = np.array([100, 140, 130, 100, 160], dtype=np.float32)
        traces['data2'] = np.array(
            [4000, 4100, 4600, 4150, 4200], dtype=np.float32)

        time_stamps = np.array([1, 2, 3, 4, 5], dtype=np.float32)

        pred1 = MTL.Predicate('data1', Ar1, br1)
        pred2 = MTL.Predicate('data2', Ar2, br2)

        root = MTL.Or(pred1, pred2, mode)
        root.eval_interval(traces, time_stamps)
        self.assertEqual(root.robustness, 500)

    def test_one_dim_until_ex1(self):

        mode = 'cpu_threaded'

        Ar1 = 1
        br1 = 140

        Ar2 = 1
        br2 = 4500

        traces = {}
        traces['data1'] = np.array([100, 139, 150, 100, 160], dtype=np.float32)
        traces['data2'] = np.array(
            [4600, 4700, 4400, 4150, 4200], dtype=np.float32)

        time_stamps = np.array([1, 2, 3, 4, 5], dtype=np.float32)

        pred1 = MTL.Predicate('data1', Ar1, br1)
        pred2 = MTL.Predicate('data2', Ar2, br2)

        root = MTL.Until(0, float('inf'), pred1, pred2, mode)
        root.eval_interval(traces, time_stamps)

        self.assertEqual(root.robustness, 1)

    def test_one_dim_until_ex2(self):

        mode = 'cpu_threaded'

        Ar1 = 1
        br1 = 140

        Ar2 = 1
        br2 = 4500

        traces = {}
        traces['data1'] = np.array([100, 149, 150, 100, 160], dtype=np.float32)
        traces['data2'] = np.array(
            [4600, 4700, 4400, 4150, 4200], dtype=np.float32)

        time_stamps = np.array([1, 2, 3, 4, 5], dtype=np.float32)

        pred1 = MTL.Predicate('data1', Ar1, br1)
        pred2 = MTL.Predicate('data2', Ar2, br2)

        root = MTL.Until(0, float('inf'), pred1, pred2, mode)
        root.eval_interval(traces, time_stamps)

        self.assertEqual(root.robustness, -9)

    def test_one_dim_eventually(self):

        mode = 'cpu_threaded'

        Ar1 = 1
        br1 = 110

        traces = {}
        traces['data1'] = np.array([165, 149, 150, 100, 160], dtype=np.float32)
        time_stamps = np.array([1, 2, 3, 4, 5], dtype=np.float32)

        pred1 = MTL.Predicate('data1', Ar1, br1)

        root = MTL.Finally(0, float('inf'), pred1, mode)
        root.eval_interval(traces, time_stamps)

        self.assertEqual(root.robustness, 10)

    def test_one_dim_always(self):

        mode = 'cpu_threaded'

        Ar1 = 1
        br1 = 110

        traces = {}
        traces['data1'] = np.array([80, 90, 150, 100, 160], dtype=np.float32)
        time_stamps = np.array([1, 2, 3, 4, 5], dtype=np.float32)

        pred1 = MTL.Predicate('data1', Ar1, br1)

        root = MTL.Global(0, float('inf'), pred1, mode)
        root.eval_interval(traces, time_stamps)

        self.assertEqual(root.robustness, -50)


if __name__ == '__main__':

    unittest.main()
