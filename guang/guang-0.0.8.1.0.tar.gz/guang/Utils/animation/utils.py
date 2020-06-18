class ExtremeValue:
    """Find Extreme Value
    Example:
    ```
    Value = ExtremeValue()
    for x, y in zip(X, Y):
        x_min, y_min = Value.get_min(x=x, y=y)
        x_max, y_max = Value.get_max(x=x, y=y)
    ```
    """
    def __init__(self):
        self.x_min = {}
        self.x_max = {}

    def get_min(self, **x):
        res = []
        for key in x:
            self.x_min.setdefault(key, np.inf)
            if x[key] < self.x_min[key]:
                self.x_min[key] = x[key]
            res.append(self.x_min[key])
        if len(res) > 1:
            return res
        else:
            return res[0]

    def get_max(self, **x):
        res = []
        for key in x:
            self.x_max.setdefault(key, -np.inf)
            if x[key] > self.x_max[key]:
                self.x_max[key] = x[key]
            res.append(self.x_max[key])
        if len(res) > 1:
            return res
        else:
            return res[0]
