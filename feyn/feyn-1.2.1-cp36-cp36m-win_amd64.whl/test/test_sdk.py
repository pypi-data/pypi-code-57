import unittest

import numpy as np
import pandas as pd

import feyn.losses
from feyn import QLattice

import pytest

class TestSDK(unittest.TestCase):
    def setUp(self):
        self.lt = QLattice()
        self.lt.reset()

    @pytest.mark.focus
    def test_init_arguments_validation(self):
        url = "http://example.com"

        with self.subTest("raises if section is combined with url or token"):
            with self.assertRaises(ValueError):
                QLattice(config="section", url=url, api_token="token")

            with self.assertRaises(ValueError):
                QLattice(config="section", url=url)

            with self.assertRaises(ValueError):
                QLattice(config="section", api_token="token")

        with self.subTest("raises if only url or token is specified"):
            with self.assertRaises(ValueError):
                QLattice(api_token="token")


    def test_can_add_new_registers(self):
        self.assertEqual(len(self.lt.registers), 0)

        # Get a qgraph which has the side effect of creating the registers
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")

        with self.subTest("Registers are available in the qlattice after addition"):
            self.assertEqual(len(self.lt.registers), 3)


    def test_delete_registers(self):
        self.assertEqual(len(self.lt.registers), 0)

        # Get a qgraph which has the side effect of creating the registers
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")

        with self.subTest("Registers can be deleted with del"):
            del(self.lt.registers["age"])
            self.assertEqual(len(self.lt.registers), 2)

        with self.subTest("Registers can be deleted with delete"):
            self.lt.registers.delete("smoker")
            self.assertEqual(len(self.lt.registers), 1)

        with self.assertRaises(ValueError) as ex:
            self.lt.registers.delete("non_existing")

        self.assertIn("non_existing", str(ex.exception))


    def test_qlattice_can_get_qgraph(self):
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")

        self.assertGreater(len(qgraph), 0)

    def test_fit_qgraph(self):
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")

        data = {
            "age": np.array([10, 16, 30, 60]),
            "smoker": np.array([0, 1, 0, 1]),
            "insurable": np.array([1, 1, 1, 0])
        }

        with self.subTest("Can fit with default arguments"):
            qgraph.fit(data, n_samples=100, show=None)

        with self.subTest("Can fit with named loss function"):
            qgraph.fit(data, n_samples=100, loss_function="mean_absolute_error", show=None)

        with self.subTest("Can fit with loss function"):
            qgraph.fit(data, n_samples=100, loss_function=feyn.losses.mean_absolute_error, show=None)

    def test_can_refresh_qgraph_after_updates(self):

        data = {
            "age": [34],
            "smoker": [0],
            "insurable": [1]
        }

        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")
        self.lt.update(qgraph[0])

        qgraph._refresh()
        self.assertGreater(len(qgraph._graphs), 0)

    def test_update_qgraph_with_older_graph(self):
        data = {
            "age": [34],
            "smoker": [0],
            "insurable": [1]
        }

        qg1 = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")
        graph = qg1[0]

        qg2 = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")
        self.lt.update(graph)

    def test_qgraph_sort(self):
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")

        data = {
            "age": np.array([10, 16, 30, 60]),
            "smoker": np.array([0, 1, 0, 1]),
            "insurable": np.array([1, 1, 1, 0])
        }

        qgraph.fit(data, n_samples=100, show=None)

        testdata = {
            "age": np.array([8, 16, 25, 50]),
            "smoker": np.array([0, 0, 1, 1]),
            "insurable": np.array([1, 0, 1, 0])
        }


        with self.subTest("Can sort with data"):
            qg = qgraph.sort(testdata)
            # TODO: Test that it was sorted by loss on the data
            self.assertIsNotNone(qg)

        with self.subTest("Can provide a loss function"):
            qg = qgraph.sort(testdata, loss_function=feyn.losses.mean_absolute_error)
            # TODO: Test that they actually got sorted by that loss function
            self.assertIsNotNone(qg)

        with self.subTest("Can provide the name of a loss function"):
            qg = qgraph.sort(testdata, loss_function="mean_absolute_error")
            # TODO: Test that they actually got sorted by that loss function
            self.assertIsNotNone(qg)

    def test_qgraph_filter(self):
        qgraph = self.lt.get_qgraph(["age", "smoker", "insurable"], "insurable")

        data = {
            "age": np.array([10, 16, 30, 60]),
            "smoker": np.array([0, 1, 0, 1]),
            "insurable": np.array([1, 1, 1, 0])
        }

        qgraph.fit(data, n_samples=100, show=None)

        with self.subTest("Can filter with depth"):
            qg = qgraph.filter(feyn.filters.Depth(1))
            for g in qg:
                self.assertEqual(g.depth, 1)

        with self.subTest("Can filter with edges"):
            qg = qgraph.filter(feyn.filters.Edges(3))
            for g in qg:
                self.assertEqual(g.edges, 3)

        with self.subTest("Can filter with contains"):
            qg = qgraph.filter(feyn.filters.Contains("smoker"))
            for g in qg:
                self.assertTrue("smoker" in g)
