import numpy as np
import daproli as dp

import unittest


class TransformerTest(unittest.TestCase):

    def test_Mapper(self):
        data = range(100)
        func = lambda x : x**2

        res1 = dp.map(func, data)
        res2 = dp.Mapper(func).transform(data)

        self.assertEqual(res1, res2)

    def test_Filter(self):
        data = range(100)
        pred = lambda x: x % 2 == 0

        res1 = dp.filter(pred, data)
        res2 = dp.Filter(pred).transform(data)

        self.assertEqual(res1, res2)

    def test_Splitter(self):
        data = range(100)
        func = lambda x: x % 2 == 0

        res1, res2 = dp.split(func, data)
        res3, res4 = dp.Splitter(func).transform(data)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_Expander(self):
        data = range(100)
        func = lambda x : [x, x**2]

        res1, res2 = dp.expand(func, data)
        res3, res4 = dp.Expander(func).transform(data)

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_Combiner(self):
        data1 = range(0, 100, 2)
        data2 = range(1, 100, 2)
        func = lambda x1, x2: (x1, x2)

        res1 = dp.combine(func, data1, data2)
        res2 = dp.Combiner(func).transform([data1, data2])

        self.assertEqual(res1, res2)

    def test_Joiner(self):
        data1 = range(0, 100, 2)
        data2 = range(1, 100, 2)
        func = lambda x, y: y-x == 1

        res1 = dp.join(func, data1, data2)
        res2 = dp.Joiner(func).transform([data1, data2])

        self.assertEqual(res1, res2)

    def test_Manipulator(self):
        data = np.random.choice(np.arange(100), 100, replace=False)

        res = dp.Manipulator(sorted).transform(data)
        self.assertEqual([i for i in range(100)], res)

    def test_Union(self):
        data1 = range(0, 100, 2)
        data2 = range(1, 100, 2)

        func1 = lambda x : x**2
        func2 = lambda x : x**3

        res1, res2 = dp.map(func1, data1), dp.map(func2, data2)

        res3, res4 = dp.Union(
            dp.Mapper(func1),
            dp.Mapper(func2),
        ).transform([data1, data2])

        self.assertEqual(res1, res3)
        self.assertEqual(res2, res4)

    def test_Pipeline(self):
        data = range(100)

        res = dp.Pipeline(
            dp.Splitter(lambda x: x % 2 == 1),
            dp.Union(
                dp.Mapper(lambda x: x * 2),
                dp.Mapper(lambda x: x * 3),
                n_jobs=2
            ),
            dp.Joiner(lambda x1, x2: (x1 + x2) % 5 == 0),
            dp.Filter(lambda x1, x2: x1 + x2 < 30),
            dp.Manipulator(sorted),
        ).transform(data)

        self.assertEqual([(0, 15), (4, 21), (12, 3), (16, 9)], res)


