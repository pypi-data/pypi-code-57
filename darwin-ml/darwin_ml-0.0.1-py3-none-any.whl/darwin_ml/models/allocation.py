import numpy as np
import pandas as pd
from pydantic import BaseModel
from creme import (anomaly, cluster, ensemble, linear_model, metrics,
                   naive_bayes, optim, preprocessing, proba, stats)
from loguru import logger

class AllocationModel(BaseModel):
    # Get the average percentage change of the allocation
    rolling_mean_3: float = 0.0
    rolling_mean_5: float = 0.0
    rolling_mean_7: float = 0.0
    rolling_mean_10: float = 0.0
    rolling_sem_3: float = 0.0
    rolling_sem_5: float = 0.0
    rolling_sem_7: float = 0.0
    rolling_sem_10: float = 0.0
    rolling_var_3: float = 0.0
    rolling_var_5: float = 0.0
    rolling_var_7: float = 0.0
    rolling_var_10: float = 0.0
    auto_regression_2: float = 0.0
    auto_regression_4: float = 0.0
    auto_regression_6: float = 0.0
    pct_filled_2: float = 0.0
    pct_filled_4: float = 0.0
    pct_filled_6: float = 0.0
    auto_corr_pct_filled_2: float = 0.0
    auto_corr_pct_filled_4: float = 0.0
    auto_corr_pct_filled_6: float = 0.0

    class Config:
        arbitrary_types_allowed = True

    def space(self):
        arr = [
            self.rolling_mean_3,
            self.rolling_mean_5,
            self.rolling_mean_7,
            self.rolling_mean_10,
            self.rolling_sem_3,
            self.rolling_sem_5,
            self.rolling_sem_7,
            self.rolling_sem_10,
            self.rolling_var_3,
            self.rolling_var_5,
            self.rolling_var_7,
            self.rolling_var_10,
            self.auto_regression_2,
            self.auto_regression_4,
            self.auto_regression_6,
            self.pct_filled_2,
            self.pct_filled_4,
            self.pct_filled_6,
        ]
        return np.array(arr)


class AllocationStatsVariates(BaseModel):
    rolling_mean_3 = stats.RollingMean(window_size=3)
    rolling_mean_5 = stats.RollingMean(window_size=5)
    rolling_mean_7 = stats.RollingMean(window_size=7)
    rolling_mean_10 = stats.RollingMean(window_size=10)

    rolling_sem_3 = stats.RollingSEM(window_size=3)
    rolling_sem_5 = stats.RollingSEM(window_size=5)
    rolling_sem_7 = stats.RollingSEM(window_size=7)
    rolling_sem_10 = stats.RollingSEM(window_size=10)

    rolling_var_3 = stats.RollingVar(window_size=3)
    rolling_var_5 = stats.RollingVar(window_size=5)
    rolling_var_7 = stats.RollingVar(window_size=7)
    rolling_var_10 = stats.RollingVar(window_size=10)

    auto_regression_3 = stats.AutoCorrelation(lag=3)
    auto_regression_4 = stats.AutoCorrelation(lag=4)
    auto_regression_5 = stats.AutoCorrelation(lag=5)

    mean_pct_filled_2 = stats.RollingMean(window_size=2)
    mean_pct_filled_4 = stats.RollingMean(window_size=4)
    mean_pct_filled_6 = stats.RollingMean(window_size=6)

    auto_corr_pct_filled_2 = stats.AutoCorrelation(lag=2)
    auto_corr_pct_filled_4 = stats.AutoCorrelation(lag=4)
    auto_corr_pct_filled_6 = stats.AutoCorrelation(lag=6)

    class Config:
        arbitrary_types_allowed = True

    def zero_complex(self, num):
        if isinstance(num, complex): return 0.0
        return num

    def get_model(self) -> AllocationModel:
        return AllocationModel(
              rolling_mean_3         = self.rolling_mean_3.get(),
              rolling_mean_5         = self.rolling_mean_5.get(),
              rolling_mean_7         = self.rolling_mean_7.get(),
              rolling_mean_10        = self.rolling_mean_10.get(),
              rolling_sem_3          = self.zero_complex(self.rolling_sem_3.get()),
              rolling_sem_5          = self.zero_complex(self.rolling_sem_5.get()),
              rolling_sem_7          = self.zero_complex(self.rolling_sem_7.get()),
              rolling_sem_10         = self.rolling_sem_10.get(),
              rolling_var_3          = self.rolling_var_3.get(),
              rolling_var_5          = self.rolling_var_5.get(),
              rolling_var_7          = self.rolling_var_7.get(),
              rolling_var_10         = self.rolling_var_10.get(),
              auto_regression_2      = self.auto_regression_3.get(),
              auto_regression_4      = self.auto_regression_4.get(),
              auto_regression_6      = self.auto_regression_5.get(),
              pct_filled_2           = self.mean_pct_filled_2.get(),
              pct_filled_4           = self.mean_pct_filled_4.get(),
              pct_filled_6           = self.mean_pct_filled_6.get(),
              auto_corr_pct_filled_2 = self.auto_corr_pct_filled_2.get(),
              auto_corr_pct_filled_4 = self.auto_corr_pct_filled_4.get(),
            auto_corr_pct_filled_6   = self.zero_complex(self.auto_corr_pct_filled_6.get())
        )


class AllocationStepSystem(object):
    def __init__(self):
        self.allo_variates: AllocationStatsVariates = AllocationStatsVariates()

    def update_pct(self, _pct: float):
        self.allo_variates.rolling_mean_3.update(_pct)
        self.allo_variates.rolling_mean_5.update(_pct)
        self.allo_variates.rolling_mean_7.update(_pct)
        self.allo_variates.rolling_mean_10.update(_pct)
        self.allo_variates.rolling_sem_3.update(_pct)
        self.allo_variates.rolling_sem_5.update(_pct)
        self.allo_variates.rolling_sem_7.update(_pct)
        self.allo_variates.rolling_sem_10.update(_pct)
        self.allo_variates.rolling_var_3.update(_pct)
        self.allo_variates.rolling_var_5.update(_pct)
        self.allo_variates.rolling_var_7.update(_pct)
        self.allo_variates.rolling_var_10.update(_pct)
        self.allo_variates.auto_regression_3.update(_pct)
        self.allo_variates.auto_regression_4.update(_pct)
        self.allo_variates.auto_regression_5.update(_pct)

    def update_fill(self, _fill_pct: float):
        self.allo_variates.mean_pct_filled_2.update(_fill_pct)
        self.allo_variates.mean_pct_filled_4.update(_fill_pct)
        self.allo_variates.mean_pct_filled_6.update(_fill_pct)
        self.allo_variates.auto_corr_pct_filled_2.update(_fill_pct)
        self.allo_variates.auto_corr_pct_filled_4.update(_fill_pct)
        
        self.allo_variates.auto_corr_pct_filled_6.update(_fill_pct)

    def step(self, allocation_pct: float,
             allocation_fill: float) -> AllocationModel:
        
        self.update_fill(allocation_fill)
        self.update_pct(allocation_pct)
        return self.allo_variates.get_model()