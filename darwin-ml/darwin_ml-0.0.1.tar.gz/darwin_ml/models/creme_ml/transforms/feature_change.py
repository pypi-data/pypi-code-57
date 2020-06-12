import collections
from creme.stats import Univariate
from creme.stats import pearson





class FeatureWindow(Univariate):
    """
        # Feature Windowing Function

        Store all of the features in a window according to the number of steps we're predicting on.

        The idea here is to store all of the features relavent to the ml problem for a single call:
        ```py
            fch = FeatureChange(lag=3)
            feature_1 = {"feature_data": [1, 2, 3, 4, 5, 6]}
            feature_2 = {"feature_data": [4, 5, 6, 8, 9, 10]}
            feature_3 = {"feature_data": [1 ...]}
            feature_4 = {"feature_data": [2 ...]}
            fch.update(feature_1).update(feature_2).update(feature_3).update(feature_4)
            fch.get() 
            # Should return feature_2
            >>> {"feature_data": [4, 5, 6, 8, 9, 10]}
        ```
    """

    def __init__(self, lag):
        self.window = collections.deque(maxlen=lag)
        self.lag = lag

    @property
    def name(self):
        return f'feature_window_{self.lag}'


    def update(self, x):
        # Add x to the window
        self.window.append(x)
        return self

    def get(self):
        pct_len = len(self.window)
        if pct_len == self.lag or pct_len > 0: return self.window[0]
        return None
