"""
tree.py
=======
written in Python3

author: C. Lockhart <chris@lockhartlab.org>
"""

from .generic import GenericModel

from sklearn.ensemble import RandomForestClassifier as _RandomForest


# Contents
__all__ = [
    'RandomForest'
]


# Create a RandomForest
class RandomForest(_RandomForest, GenericModel):
    """

    """

    # Initialize instance of class
    def __init__(self, *args, **kwargs):
        # Initialize parent class
        _RandomForest.__init__(self, *args, **kwargs)

    def _log_likelihood(self, y_true, y_pred):
        pass

    def _log_loss(self, y_true, y_pred):
        pass

    def degrees_of_freedom(self, x):
        pass

    def predict_y(self, x, outcome_column=1):
        pass
