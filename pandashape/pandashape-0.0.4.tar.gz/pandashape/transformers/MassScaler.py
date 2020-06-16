import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from .Transformer import Transformer
from pandashape.enums.Scaling import Scaling


class MassScaler(Transformer):
    def __init__(self, scaling=Scaling.MinMax, skewness_breakpoint=None, inplace=False, suffix='_scaled'):
        self.scaling = scaling
        self.skewness_breakpoint = skewness_breakpoint
        self.suffix = suffix

    def transform(self, series):
        if (self.skewness_breakpoint is not None):
            skewness = abs(1 - series.skew())
            if (self.skewness_breakpoint is not None and skewness < self.skewness_breakpoint):
                pass

        if self.scaling == Scaling.Log:
            # coerce log(0) to 0
            return np.where(series > 0, np.log(series), 0)
        elif self.scaling == Scaling.MinMax:
            scaler = MinMaxScaler()
            return scaler.transform(series)
        elif self.scaling == Scaling.Standard:
            scaler = StandardScaler()
            return scaler.transform(series)
