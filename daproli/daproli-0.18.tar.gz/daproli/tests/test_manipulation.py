import daproli as dp

import unittest


class ManipulationTest(unittest.TestCase):

    def test_windowed(self):
        data = range(10)
        res = dp.windowed(data, 2, step=2)

        self.assertEqual([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]], res)

    def test_flatten(self):
        data = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
        res = dp.flatten(data)

        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], res)