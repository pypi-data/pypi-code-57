import unittest
from ddt import ddt, file_data

from azureml.automl.runtime.featurization._featurized_data_combiners import FeaturizedDataCombiners


@ddt
class TestFeaturizedDataCombiner(unittest.TestCase):
    @file_data("test_featurized_data_combiner.json")
    def test_get(self, is_sparse, is_inference_time, is_low_memory, expected):
        combiner = FeaturizedDataCombiners.get(is_sparse, is_inference_time, is_low_memory)
        assert combiner is not None, "Combiner should not be None"
        actual = combiner.__name__
        msg = "Sparse: {}, Inference: {}, LowMemory: {}, Expected: {}, Actual: {}"
        assert combiner.__name__ == expected, msg.format(is_sparse, is_inference_time, is_low_memory, expected, actual)
