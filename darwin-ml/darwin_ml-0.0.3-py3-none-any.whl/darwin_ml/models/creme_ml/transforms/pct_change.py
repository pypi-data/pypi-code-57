import collections
from creme.stats import Univariate
from creme.stats import pearson



class PercentageChange(Univariate):
    """Measures the serial correlation.

    This method computes the Pearson correlation between the current value and the value seen ``n``
    steps before.
    """

    def __init__(self, lag):
        self.window = collections.deque(maxlen=lag)
        self.pct_window = collections.deque(maxlen=lag)
        self.lag = lag

    @property
    def name(self):
        return f'pct_change_{self.lag}'


    def update(self, x):
        # The correlation can be update once enough elements have been seen
        if len(self.window) == self.lag:
            change, _ = self.calculate_change(self.window[0], x)
            self.pct_window.append(change)

        # Add x to the window
        self.window.append(x)
        return self

    def calculate_change(self, previous: float, current: float):
        change = (((current - previous) / current) * 100) 
        if change > 0: return change, 1
        return change, 0


    def get(self):
        pct_len = len(self.pct_window)
        if pct_len > 0: return self.pct_window[-1]
        return 0
    
    def get_class(self):
        if len(self.window) == self.lag:
            if self.window[-1] > self.window[0]: 
                return 1
            else:
                return 0
        return 99
