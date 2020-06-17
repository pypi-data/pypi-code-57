'''
The api take the timeseries methods and send it to the root datup folder
'''

from datup.timeseries.timeseries_errors import (
    compute_mae,
    compute_maep,
    compute_mape,
    compute_mase,
    compute_rmse,
    compute_rmsep
)

from datup.timeseries.ExponentialSmoothing import (ExponentialSmoothing)