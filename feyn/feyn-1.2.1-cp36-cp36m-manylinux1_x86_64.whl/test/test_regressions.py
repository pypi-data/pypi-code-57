"""
This file contains regression errors observed in production. Some of these tests may
be a bit gnarly formulated, they may be a bit more fragile, and they probably do not
smell like a requirement specification for the feyn.

The idea is, that these can be deleted whenever they become too annoying.
"""

import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal

import feyn

class TestMiscRegressions(unittest.TestCase):
    
    def test_graph_handles_nans(self):
        in_reg = feyn.Interaction("in:minmax(f)->i", (0,-1,-1), name="in_reg")
        tanh = feyn.Interaction("cell:tanh(i)->i", (0,0,0))
        out_reg = feyn.Interaction("out:minmax(i)->f", (1,-1,-1), name="out_reg")

        g = feyn.Graph(3)
        g[0] = in_reg
        g[1] = tanh
        g[2] = out_reg
        
        in_reg._set_source(0, -1)
        tanh._set_source(0, 0)
        out_reg._set_source(0, 1)

        with self.subTest("ValueError when Nan in input"):
            with self.assertRaises(ValueError) as ctx:
                data = { "in_reg": [np.nan] }
                g.predict(data)

            self.assertIn("nan", str(ctx.exception))

        with self.subTest("ValueError when inf in input"):
            with self.assertRaises(ValueError) as ctx:
                data = { "in_reg": [np.inf] }
                g.predict(data)

            self.assertIn("inf", str(ctx.exception))

        with self.subTest("ValueError when Nan in output"):
            with self.assertRaises(ValueError) as ctx:
                data = {
                    "in_reg": np.array([1.0]),
                    "out_reg": np.array([np.nan])
                }
                g._fit(data, epochs=1, loss_function=feyn.losses.mean_squared_error)

            self.assertIn("nan", str(ctx.exception))

