"""
test_generic.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from izzy.classification import classify

from hypothesis import given
import hypothesis.strategies as st
import numpy as np
import unittest


# Test generic.py
class TestGeneric(unittest.TestCase):
    # Tests that we know how to classify
    @given(st.integers(min_value=2, max_value=10),
           st.integers(min_value=100, max_value=100000),
           st.floats(min_value=0.2, max_value=0.8))
    def test_classify(self, n_classes, n_samples, threshold):
        # Generate random probabilities
        y_prob = np.random.rand(n_samples, n_classes)

        # Classify using known calculation
        if n_classes == 2:
            y_pred1 = y_prob[:, 1] > threshold
        else:
            y_pred1 = np.argmax(y_prob, axis=1)

        # Classify using izzy function
        y_pred2 = classify(y_prob, threshold=threshold)

        # Assert equal
        np.testing.assert_almost_equal(y_pred1, y_pred2)
