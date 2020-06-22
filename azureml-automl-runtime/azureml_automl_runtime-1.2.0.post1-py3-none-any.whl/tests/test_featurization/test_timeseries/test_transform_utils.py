import unittest

from azureml.automl.core.shared.forecasting_exception import (InvalidTsdfArgument)
from azureml.automl.runtime.featurizer.transformer.timeseries.transform_utils import OriginTimeMixin

from ...utilities import assert_no_pii_logged


class TestOriginTimeMixin(unittest.TestCase):
    """Tests for OriginTimeMixin."""

    def test_verify_max_horizon_input(self):
        """Test max horison verification."""
        otm = OriginTimeMixin()
        # Should pass.
        otm.verify_max_horizon_input(42)
        # Should also pass.
        otm.verify_max_horizon_input({'a': 1, 'b': 2})
        # Should raise.
        with self.assertRaises(InvalidTsdfArgument) as cm:
            otm.verify_max_horizon_input({'a': 1, 'b': '2'})
        assert_no_pii_logged(cm.exception, 'str')
        with self.assertRaises(InvalidTsdfArgument):
            otm.verify_max_horizon_input({'a': 1, 'b': -2})
        with self.assertRaises(InvalidTsdfArgument):
            otm.verify_max_horizon_input('2')
        with self.assertRaises(InvalidTsdfArgument):
            otm.verify_max_horizon_input(-2)


if __name__ == '__main__':
    unittest.main()
