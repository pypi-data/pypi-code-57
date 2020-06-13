import numpy as np
import daproli as dp

import unittest


class TransformerTest(unittest.TestCase):

    def test_MapTransformer(self):
        data = np.arange(100)
        func = lambda x : x**2

        res1 = dp.map(func, data)
        res2 = dp.MapTransformer(func).transform(data)

        self.assertEqual(res1, res2)

    def test_FilterTransformer(self):
        data = np.arange(100)
        pred = lambda x: x % 2 == 0

        res1 = dp.filter(pred, data)
        res2 = dp.FilterTransformer(pred).transform(data)

        self.assertEqual(res1, res2)

    def test_SplitTransformer(self):
        data = np.arange(100)
        func = lambda x: x % 2 == 0

        res1, res2 = dp.split(func, data)
        res3, res4 = dp.SplitTransformer(func).transform(data)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_ExpandTransformer(self):
        data = np.arange(100)
        func = lambda x : [x, x**2]

        res1, res2 = dp.expand(func, data)
        res3, res4 = dp.ExpandTransformer(func).transform(data)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_CombineTransformer(self):
        data1 = np.arange(0, 100, 2)
        data2 = np.arange(1, 100, 2)
        func = lambda x1, x2: (x1, x2)

        res1 = dp.combine(func, data1, data2)
        res2 = dp.CombineTransformer(func).transform([data1, data2])

        self.assertEqual(res1, res2)

    def test_JoinTransformer(self):
        data1 = np.arange(0, 100, 2)
        data2 = np.arange(1, 100, 2)
        func = lambda x, y: y-x == 1

        res1 = dp.join(func, data1, data2)
        res2 = dp.JoinTransformer(func).transform([data1, data2])

        self.assertEqual(res1, res2)

    def test_ContainerTransformer(self):
        data = np.random.choice(np.arange(100), 100, replace=False)

        res = dp.ContainerTransformer(sorted).transform(data)
        self.assertEqual([i for i in range(100)], res)

    def test_MultiTransformer(self):
        data1 = np.arange(0, 100, 2)
        data2 = np.arange(1, 100, 2)

        func1 = lambda x : x**2
        func2 = lambda x : x**3

        res1, res2 = dp.map(func1, data1), dp.map(func2, data2)

        res3, res4 = dp.MultiTransformer(
            dp.MapTransformer(func1),
            dp.MapTransformer(func2),
        ).transform([data1, data2])

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_PipelineTransformer(self):
        data = np.arange(100)

        res = dp.PipelineTransformer(
            dp.SplitTransformer(lambda x: x % 2 == 1),
            dp.MultiTransformer(
                dp.MapTransformer(lambda x: x * 2),
                dp.MapTransformer(lambda x: x * 3),
                n_jobs=2
            ),
            dp.JoinTransformer(lambda x1, x2: (x1 + x2) % 5 == 0),
            dp.FilterTransformer(lambda x: np.sum(x) < 30),
            dp.ContainerTransformer(sorted),
        ).transform(data)

        self.assertEqual([(0, 15), (4, 21), (12, 3), (16, 9)], res)


