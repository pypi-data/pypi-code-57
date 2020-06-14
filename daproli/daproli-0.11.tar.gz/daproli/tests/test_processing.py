import numpy as np
import daproli as dp

import unittest


class ProcessingTest(unittest.TestCase):

    def test_map(self):
        data = np.arange(100)
        func = lambda x : x**2

        res1 = dp.map(func, data, n_jobs=1)
        res2 = dp.map(func, data, n_jobs=2)

        self.assertEqual(res1, res2)

    def test_filter(self):
        data = np.arange(100)
        pred = lambda x: x % 2 == 0

        res1 = dp.filter(pred, data, n_jobs=1)
        res2 = dp.filter(pred, data, n_jobs=2)

        self.assertEqual(res1, res2)

    def test_split(self):
        data = np.arange(100)
        func = lambda x: x % 2 == 0

        res1, res2 = dp.split(func, data, n_jobs=1)
        res3, res4 = dp.split(func, data, n_jobs=2)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_expand(self):
        data = np.arange(100)
        func = lambda x : [x, x**2]

        res1, res2 = dp.expand(func, data, n_jobs=1)
        res3, res4 = dp.expand(func, data, n_jobs=2)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_combine(self):
        data1 = np.arange(0, 100, 2)
        data2 = np.arange(1, 100, 2)
        func = lambda x1, x2: (x1, x2)

        res1 = dp.combine(func, data1, data2, n_jobs=1)
        res2 = dp.combine(func, data1, data2, n_jobs=2)

        self.assertEqual(res1, res2)

    def test_join(self):
        data1 = np.arange(0, 100, 2)
        data2 = np.arange(1, 100, 2)
        func = lambda x, y: y-x == 1

        res1 = dp.join(func, data1, data2, n_jobs=1)
        res2 = dp.join(func, data1, data2, n_jobs=2)

        self.assertEqual(res1, res2)
