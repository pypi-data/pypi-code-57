import collections
from creme.stats import Univariate
from creme.stats import pearson

class PredictionHistory(Univariate):
    """
        Use this history to get an accurate understanding of how the machine learning model has performed. 
        This is a duplication for saving the predictions in redis. Using the step function for training.
    """

    def __init__(self, lag=3):
        self.window = collections.deque(maxlen=lag)
        self.lag = lag

    @property
    def name(self):
        return f'prediction_history_{self.lag}'


    def update(self, x):
        # Add x to the window
        self.window.append(x)
        return self



    def get(self):
        """Get the prediction made at the lag.

        Returns:
            Any: The prediction from the ML algo. Use to 
        """
        pct_len = len(self.window)
        if pct_len == self.lag: return self.window[0]
        return None