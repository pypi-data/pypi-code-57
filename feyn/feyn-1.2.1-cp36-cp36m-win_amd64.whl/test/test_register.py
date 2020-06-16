import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal

import feyn

class TestRegister(unittest.TestCase):

    def test_register_truncates_input(self):
        register = feyn.Interaction('in:minmax(f)->i', latticeloc=(0,0,-1), name='myinput')
        register._set_source(0, -1)
        register.state.auto_adapt = False

        out = feyn.Interaction("out:minmax(i)->f", latticeloc=(1,0,-1), name="out")
        out._set_source(0,0)

        g = feyn.Graph(2)
        g[0] = register
        g[1] = out
        o = g.predict({"myinput": np.array([-2,-1,0,1,2])})

        assert_array_almost_equal(o, [-1, -1, 0, 1, 1])

    def test_register_auto_adapts_input(self):
        register = feyn.Interaction('in:minmax(f)->i', latticeloc=(0,0,-1), name='myinput')
        register._set_source(0, -1)
        register.state.auto_adapt = True

        out = feyn.Interaction("out:minmax(i)->f", latticeloc=(1,0,-1), name="out")
        out._set_source(0,0)

        g = feyn.Graph(2)
        g[0] = register
        g[1] = out
        o = g.predict({"myinput": np.array([2,3,4,5,6])})

        assert_array_almost_equal(o, [-1, -0.5, 0, 0.5, 1])

    def test_register_adapts_input_to_fixed_range(self):
        register = feyn.Interaction('in:minmax(f)->i', latticeloc=(0,0,-1), name='myinput')
        register._set_source(0, -1)
        register.state.auto_adapt = False
        register.state.feature_max = 1.0
        register.state.feature_min = 0

        out = feyn.Interaction("out:minmax(i)->f", latticeloc=(1,0,-1), name="out")
        out._set_source(0,0)

        g = feyn.Graph(2)
        g[0] = register
        g[1] = out
        o = g.predict({"myinput": np.array([0.0, 0.5, 1.0])})

        assert_array_almost_equal(o, [-1, 0, 1])


    def test_register_denormalizes_data_to_defined_range(self):
        register = feyn.Interaction('in:minmax(f)->i', latticeloc=(0,0,-1), name='myinput')
        register._set_source(0, -1)
        register.state.auto_adapt = False

        out = feyn.Interaction("out:minmax(i)->f", latticeloc=(1,0,-1), name="out")
        out._set_source(0,0)
        out.state.auto_adapt = False
        out.state.feature_min = -2
        out.state.feature_max = 10

        g = feyn.Graph(2)
        g[0] = register
        g[1] = out

        o = g.predict({"myinput": np.array([0,1])})
        assert_array_equal(o, [4.,10.])

    def test_register_auto_adapts_output(self):
        register = feyn.Interaction('in:minmax(f)->i', latticeloc=(0,0,-1), name='myinput')
        register._set_source(0, -1)
        register.state.auto_adapt = False

        out = feyn.Interaction("out:minmax(i)->f", latticeloc=(1,0,-1), name="out")
        out._set_source(0,0)
        out.state.auto_adapt = True

        g = feyn.Graph(2)
        g[0] = register
        g[1] = out

        g._query({"myinput": np.array([-1,1])}, np.array([-2, 10]))
        o = g.predict({"myinput": np.array([0,1])})
        assert_array_equal(o, [4.,10.])

    def test_register_supports_loss_functions(self):
        register = feyn.Interaction('out:minmax(i)->f', latticeloc=(0,0,-1), name='myinput')
        with self.subTest("valid loss function"):
            register._loss = "mean_absolute_error"

        with self.assertRaises(ValueError):
            register._loss = "mean_uncomfortable_fact"
