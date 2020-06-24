'''stub for rolling ball backround subtraction. 
Mainly kept as illustration for how to parallelize an expensive function.
'''
from cv2_rolling_ball import subtract_background_rolling_ball


class StackSubtractBackground(ImageFormatter):
    '''Rolling ball background subtraction.

    Expects the first axis to be the time axis and the second and third to be x and y.
    Data is converted to uint8. It is recommended to apply normalization with clipping enabled
    before and after background subtraction (using a filter pipeline).
    '''
    DEFAULT_PARAMS = {'radius': 10, 'light_background': False, 'use_paraboloid': False, 'do_presmooth': False}

    @property
    def input_dim(self): return None

    @property
    def output_dim(self): return None

    def apply(self, data):
        from cv2_rolling_ball import subtract_background_rolling_ball
        self.cache = np.copy(data)  # cache the input in case we need to revert later
        data = self._convert_uint(data)  # first rescale and convert to uint
        for plane in range(data.shape[0]):
            data[plane, :, :, 0], _ = subtract_background_rolling_ball(
                data[plane, :, :, 0],
                self.parameters['radius'],
                light_background=self.parameters['light_background'],
                use_paraboloid=self.parameters['use_paraboloid'],
                do_presmooth=self.parameters['do_presmooth']
            )
        return data

    def revert(self, data):
        try:
            return self.cache
        except AttributeError:
            raise NotReversibleError(
                'No cached data found. Use the same object for applying and reverting the formatter.')

    def get_output_shape(self, input_shape): return input_shape

    def get_revert_output_shape(self, output_shape): return output_shape

    def _convert_uint(self, data):
        data -= np.min(data)
        data = ((2**8 - 1) * data / np.max(data)).astype(np.uint8)
        return data


class StackSubtractBackgroundParallel(StackSubtractBackground):
    '''Performance optimized version of StackSubtractBackground.'''

    def apply(self, data):
        import multiprocessing as mp
        import gzip
        import pickle
        pool = mp.Pool(mp.cpu_count())

        self.cache = np.copy(data)  # cache the input in case we need to revert later

        global _results  # results need to be global because the

        data = self._convert_uint(data)  # first rescale and convert to uint
        for plane in range(data.shape[0]):
            # print(data[plane, :, :, 0].shape)
            # _subtract_bg(data[plane, :, :, 0], plane, self.parameters)
            pool.apply_async(_subtract_bg, args=(data[plane, :, :, 0], plane, self.parameters),
                             callback=_collect_result)
        pool.close()
        pool.join()
        _results.sort(key=lambda x: x[1])
        for r, i in _results:
            data[i, :, :, 0] = r
        return data


#################################
'''Global functions and variable required for StackSubtractBackgroundParallel.'''
_results = []


def _collect_result(result):
    global _results
    _results.append(result)


def _subtract_bg(plane, i, parameters):
    plane, _ = subtract_background_rolling_ball(
        plane,
        parameters['radius'],
        light_background=parameters['light_background'],
        use_paraboloid=parameters['use_paraboloid'],
        do_presmooth=parameters['do_presmooth']
    )
    return plane, i
#################################


@unittest.skip  # skipping this test until vscode supports debugging multiprocessing code
class TestStackSubtractBackgroundParallel(BaseFormattingTest):
    def setUp(self):
        np.random.seed(42)
        self.stack = np.random.normal(size=(5, 32, 32, 1))
        self.expected_input_dim = None
        self.expected_output_dim = None
        self.expected_output_shape = (5, 32, 32, 1)
        self.formatter = micdata.formatting.StackSubtractBackgroundParallel()
        self.output_data = os.path.join(os.path.dirname(__file__), 'data', 'bg_res.pkl.gz')

    def test_apply(self):
        inp = np.copy(self.stack)
        out = self.formatter.apply(inp)
        self.assertEqual(out.shape, self.expected_output_shape)
        with gzip.open(self.output_data, 'r') as f:
            true_out = pickle.load(f)
        self.assertTrue(np.array_equal(out, true_out))
        # testing revert here to avoid calling format once again
        reverted = self.formatter.revert(out)
        self.assertTrue(np.array_equal(self.stack, reverted))
        self.formatter.parameters['radius'] = 2
        out = self.formatter.apply(inp)
        self.assertGreater(np.mean(true_out), np.mean(out))

    def test_revert(self):
        self.assertRaises(micdata.formatting.NotReversibleError, self.formatter.revert, self.stack.shape)

    def test__subtract_bg(self):
        inp = np.zeros((32, 32), dtype=np.uint8)
        out, _ = micdata.formatting._subtract_bg(inp, 0, self.formatter.DEFAULT_PARAMS)
        self.assertTrue(np.array_equal(out, inp))


class TestStackSubtractBackground(BaseFormattingTest):
    def setUp(self):
        np.random.seed(42)
        self.stack = np.random.normal(size=(5, 32, 32, 1))
        self.expected_input_dim = None
        self.expected_output_dim = None
        self.expected_output_shape = (5, 32, 32, 1)
        self.formatter = micdata.formatting.StackSubtractBackground()
        self.output_data = os.path.join(os.path.dirname(__file__), 'data', 'bg_res.pkl.gz')

    def test_apply(self):
        inp = np.copy(self.stack)
        out = self.formatter.apply(inp)
        self.assertEqual(out.shape, self.expected_output_shape)
        with gzip.open(self.output_data, 'r') as f:
            true_out = pickle.load(f)
        self.assertTrue(np.array_equal(out, true_out))
        # testing revert here to avoid calling format once again
        reverted = self.formatter.revert(out)
        self.assertTrue(np.array_equal(self.stack, reverted))
        self.formatter.parameters['radius'] = 2
        out = self.formatter.apply(inp)
        self.assertGreater(np.mean(true_out), np.mean(out))

    def test_revert(self):
        self.assertRaises(micdata.formatting.NotReversibleError, self.formatter.revert, self.stack.shape)
