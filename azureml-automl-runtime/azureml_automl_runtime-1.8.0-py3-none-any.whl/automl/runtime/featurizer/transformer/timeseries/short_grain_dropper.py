# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Drop grains from dataset."""
import pandas as pd

from typing import Any, List, Optional, cast
from warnings import warn

from azureml.automl.core.shared import utilities
from azureml.automl.core.shared.forecasting_exception import NotTimeSeriesDataFrameException
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.time_series_data_frame import TimeSeriesDataFrame
from .forecasting_base_estimator import AzureMLForecastTransformerBase
from azureml.automl.core.shared.exceptions import (
    ConfigException, ClientException, InsufficientDataException)
from azureml.automl.runtime.shared.types import GrainType
from azureml.automl.core.shared.forecasting_verify import Messages
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal


class ShortGrainDropper(AzureMLForecastTransformerBase):
    """Drop short series, or series not found in training set."""

    DROPPING_GRAIN_TEMPL = ("Dropping grain {}. Reason: the grain was not present in the training set "
                            "or was too short.")

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor.

        :param target_rolling_window_size: The size of a target rolling window.
        :param target_lags: The size of a lag of a lag operator.
        :param n_cross_validations: The number of cross validations.
        :param max_horizon: The maximal horizon.
        :raises: ConfigException
        """
        super().__init__()
        self._grains_to_keep = []  # type: List[GrainType]
        self._short_grains = []  # type: List[GrainType]
        self._has_short_grains = False
        self._window_size = kwargs.get(TimeSeries.TARGET_ROLLING_WINDOW_SIZE, 0)  # type: int
        self._lags = kwargs.get(TimeSeries.TARGET_LAGS, [0])  # type: List[int]
        self._cv = kwargs.get(TimeSeriesInternal.CROSS_VALIDATIONS)  # type: Optional[int]
        self._max_horizon = kwargs.get(TimeSeries.MAX_HORIZON, TimeSeriesInternal.MAX_HORIZON_DEFAULT)  # type: int
        self._is_fit = False

    @function_debug_log_wrapped('info')
    def fit(self, X: TimeSeriesDataFrame, y: Any = None) -> 'ShortGrainDropper':
        """
        Define the grains to be stored.

        If all the grains should be dropped, raises DataExceptions.
        :param X: The time series data frame to fit on.
        :param y: Ignored
        :raises: DataException
        """
        reference_code = 'short_grain_dropper.ShortGrainDropper.fit'
        self._raise_wrong_type_maybe(X, reference_code)

        min_points = utilities.get_min_points(self._window_size,
                                              self._lags,
                                              self._max_horizon,
                                              self._cv)
        by_index = (TimeSeriesInternal.DUMMY_ORDER_COLUMN in X.columns)
        for grain, df in X.groupby_grain():
            # To mark grain as short we need to use TimeSeriesInternal.DUMMY_ORDER_COLUMN value or
            # if it is not present, the shape of a data frame. The rows where TimeSeriesInternal.DUMMY_ORDER_COLUMN
            # is NaN were not present in the original data set and finally will be removed, leading to error
            # during rolling origin cross validation.
            if (by_index and df[TimeSeriesInternal.DUMMY_ORDER_COLUMN].notnull().sum() >= min_points) or\
               (not by_index and df.shape[0] >= min_points):
                self._grains_to_keep.append(grain)
            else:
                self._has_short_grains = True
        if not self._grains_to_keep:
            raise InsufficientDataException(
                "All grains are too short please check the data or decrease target_lags, "
                "target_rolling_window_size, n_cross_validations or max_horizon.", has_pii=False,
                reference_code=reference_code)
        self._is_fit = True
        return self

    @function_debug_log_wrapped('info')
    def transform(self, X: TimeSeriesDataFrame, y: Any = None) -> TimeSeriesDataFrame:
        """
        Drop grains, which were not present in training set, or were removed.

        If all the grains should be dropped, raises DataExceptions.
        :param X: The time series data frame to check for grains to drop.
        :param y: Ignored
        :raises: ClientException, DataException
        """
        reference_code = 'short_grain_dropper.ShortGrainDropper.transform'
        if not self._is_fit:
            raise ClientException("ShortGrainDropper transform method called before fit.", has_pii=False,
                                  reference_code=reference_code)
        self._raise_wrong_type_maybe(X, reference_code)
        drop_grains = set()

        def do_keep_grain(df):
            """Do the filtering and add all values to set."""
            keep = df.name in self._grains_to_keep
            if not keep:
                drop_grains.add(df.name)
            return keep

        result = X.groupby_grain().filter(lambda df: do_keep_grain(df))
        if(result.shape[0] == 0):
            raise InsufficientDataException(
                "All grains were removed because "
                "they were too short for horizon, cv and lag settings.", has_pii=False,
                reference_code='short_grain_dropper.ShortGrainDropper.transform')
        return cast(TimeSeriesDataFrame, result)

    def _raise_wrong_type_maybe(self, X: Any, reference_code: str) -> None:
        """Raise exception if X is not TimeSeriesDataFrame."""
        if not isinstance(X, TimeSeriesDataFrame):
            raise NotTimeSeriesDataFrameException(
                Messages.XFORM_INPUT_IS_NOT_TIMESERIESDATAFRAME, has_pii=False, reference_code=reference_code)

    @property
    def grains_to_keep(self) -> List[GrainType]:
        """Return the list of grains to keep."""
        if not self._is_fit:
            raise ClientException("grains_to_keep property is not available before fit.", has_pii=False,
                                  reference_code='short_grain_dropper.ShortGrainDropper.grains_to_keep')
        return self._grains_to_keep

    @property
    def has_short_grains_in_train(self) -> bool:
        """Return true if there is no short grains in train set."""
        if not self._is_fit:
            raise ClientException("has_short_grains_in_train property is not available before fit.", has_pii=False,
                                  reference_code='short_grain_dropper.ShortGrainDropper.has_short_grains_in_train')
        return self._has_short_grains
