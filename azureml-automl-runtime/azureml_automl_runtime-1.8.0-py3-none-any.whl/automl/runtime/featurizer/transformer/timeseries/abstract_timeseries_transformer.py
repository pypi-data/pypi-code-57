# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""abstract_timeseries_transformer.py, a file for storing abstract class for transformers operating on time series."""
from typing import Any, cast, Dict, List, Optional, Set, Union
import abc
import warnings
from collections import OrderedDict

import numpy as np
import pandas as pd

from pandas.tseries.frequencies import to_offset
from pandas.tseries.offsets import QuarterOffset, SemiMonthOffset, DateOffset

from azureml.automl.core.constants import FeatureType
from azureml.automl.core.shared import constants
from azureml.automl.core.constants import TransformerParams, SupportedTransformers
from azureml.automl.core.shared.constants import TimeSeriesInternal, TimeSeries
from azureml.automl.runtime.shared import forecasting_utils
from azureml.automl.core.shared.exceptions import (
    ConfigException, EmptyDataException,
    ClientException, AutoMLException, InvalidDataTypeException,
    InsufficientDataException, InvalidValueException)
from azureml.automl.core.shared.forecasting_exception import (
    DataFrameMissingColumnException, GrainAbsent, DataFrameValueException, ForecastingDataException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.featurizer.transformer.timeseries.missingdummies_transformer import \
    MissingDummiesTransformer
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.runtime.shared.time_series_data_frame import TimeSeriesDataFrame
from azureml.automl.runtime.shared.types import DataInputType, DataSingleColumnInputType, ColumnTransformerParamType
from ..automltransformer import AutoMLTransformer
from .time_series_imputer import TimeSeriesImputer
from .forecasting_pipeline import AzureMLForecastPipeline
from ....frequency_fixer import fix_df_frequency

warnings.simplefilter("ignore")


class AbstractTimeSeriesTransformer(AutoMLTransformer):
    """The abstract class, encapsulating common steps in data pre processing."""
    TYPE_ERROR_TEMPLATE = ("Forecasting task can be ran only on pandas dataframes. "
                           "{} was given.")
    DATA_FRAME_EMPTY = "The provided data frame is empty."
    MISSING_Y = 'missing_y'  # attribute name to look for. Used for backward compatibility check.

    def __init__(self,
                 featurization_config: Optional[FeaturizationConfig] = None,
                 **kwargs: Any) -> None:
        """
        Construct for the class.

        :param featurization_config: FeaturizationConfig object for custom featurization.
        :param kwargs: dictionary contains metadata for TimeSeries.
                   time_column_name: The column containing dates.
                   grain_column_names: The set of columns defining the
                   multiple time series.
                   origin_column_name: latest date from which actual values
                   of all features are assumed to be known with certainty.
                   drop_column_names: The columns which will needs
                   to be removed from the data set.
                   group: the group column name.
                   country_or_region: the data origin coutry used to generate holiday feature
        :type kwargs: dict
        """
        super().__init__()
        if constants.TimeSeries.TIME_COLUMN_NAME not in kwargs.keys():
            raise ConfigException("{} must be set".format(constants.TimeSeries.TIME_COLUMN_NAME), has_pii=False,
                                  reference_code="abstract_timeseries_transformer.\
                                      AbstractTimeSeriesTransformer.__init__")
        self.time_column_name = cast(str, kwargs[constants.TimeSeries.TIME_COLUMN_NAME])
        grains = kwargs.get(constants.TimeSeries.GRAIN_COLUMN_NAMES)
        if isinstance(grains, str):
            grains = [grains]
        self.grain_column_names = cast(List[str], grains)
        self.drop_column_names = cast(List[Any], kwargs.get(constants.TimeSeries.DROP_COLUMN_NAMES))
        self._featurization_config = self._convert_featurization_config(featurization_config)
        if self._featurization_config.drop_columns is not None and \
                len(self._featurization_config.drop_columns) > 0:
            drop_column_names_set = set(self.drop_column_names)
            for col in self._featurization_config.drop_columns:
                if col not in drop_column_names_set:
                    self.drop_column_names.append(col)

        # Used to make data compatible with timeseries dataframe
        self.target_column_name = constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
        self.origin_column_name = \
            kwargs.get(constants.TimeSeriesInternal.ORIGIN_TIME_COLUMN_NAME,
                       constants.TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT)
        self.dummy_grain_column = constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN
        self.group_column = kwargs.get(constants.TimeSeries.GROUP_COLUMN, None)

        self.original_order_column = constants.TimeSeriesInternal.DUMMY_ORDER_COLUMN
        self.engineered_feature_names = None                       # type: Optional[List[str]]
        self._fit_column_order = np.array([])
        self._fit_column_order_no_ts_value = np.array([])
        self._engineered_feature_name_objects = {}             # type: Dict[str, Optional[Any]]
        # We keep the list of columns in case if the class is invoked without data frame.
        self._columns = None
        # For the same purpose we need to store the imputer for y values.
        self._y_imputers = {}  # type: Dict[str, TimeSeriesImputer]
        self.dict_latest_date = {}   # type: Dict[str, pd.Timestamp]
        self.country_or_region = kwargs.get(constants.TimeSeries.COUNTRY_OR_REGION, None)
        self.boolean_columns = []  # type: List[str]
        self.pipeline = None  # type: Optional[AzureMLForecastPipeline]
        self.freq_offset = None  # type: Optional[pd.DateOffset]
        self.freq = None  # type: Optional[str]
        self._unknown_train_part = None  # type: Optional[TimeSeriesDataFrame]
        self._known_train_part = None  # type: Optional[TimeSeriesDataFrame]
        self._in_fit_transform = False  # type: bool
        self.missing_y = self._init_missing_y()

    def _init_missing_y(self):
        """ Initialize missing_y column to the TimeSeriesDataFrame."""
        out = MissingDummiesTransformer(
            [constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN]
        )
        return out

    def _do_construct_pre_processing_pipeline(self,
                                              tsdf: TimeSeriesDataFrame,
                                              drop_column_names: Optional[List[str]]) -> AzureMLForecastPipeline:
        from .drop_columns import DropColumns
        self._logger_wrapper('info', 'Start construct pre-processing pipeline ({}).'.format(self.__class__.__name__))
        processing_pipeline = self._construct_pre_processing_pipeline(tsdf, drop_column_names)
        # Don't add dropColumn transfomer if there is nothing to drop
        if drop_column_names is not None and len(drop_column_names) > 0:
            processing_pipeline.add_pipeline_step('drop_irrelevant_columns',
                                                  DropColumns(drop_column_names),
                                                  prepend=True)
        self._logger_wrapper('info', 'Finish Construct Pre-Processing Pipeline ({}).'.format(self.__class__.__name__))
        return processing_pipeline

    @abc.abstractmethod
    def _construct_pre_processing_pipeline(self,
                                           tsdf: TimeSeriesDataFrame,
                                           drop_column_names: Optional[List[str]]) -> AzureMLForecastPipeline:
        """
        Construct the pre processing pipeline and stores it in self.pipeline.

        :param tsdf: The time series data frame.
        :type tsdf: TimeSeriesDataFrame
        :param drop_column_names: The columns to be dropped.
        :type drop_column_names: list

        """
        pass

    def _impute_target_value(self, tsdf: TimeSeriesDataFrame) -> TimeSeriesDataFrame:
        """Perform the y imputation based on frequency."""
        if self._is_using_customized_target_imputer():
            target_imputer = self._get_target_imputer(tsdf)
        else:
            target_imputer = self._get_target_imputer()
        if not hasattr(self, AbstractTimeSeriesTransformer.MISSING_Y):
            self.missing_y = self._init_missing_y()
        new_tsdf = self.missing_y.fit_transform(tsdf)
        return cast(TimeSeriesDataFrame, target_imputer.fit_transform(new_tsdf))

    @function_debug_log_wrapped('info')
    def fit_transform(self,
                      X: DataInputType,
                      y: Optional[DataSingleColumnInputType] = None, **fit_params: Any) -> pd.DataFrame:
        """
        Wrap fit and transform functions in the Data transformer class.

        :param X: Dataframe representing text, numerical or categorical input.
        :type X: numpy.ndarray or pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray or pandas.DataFrame

        :return: Transformed data.

        """
        self._in_fit_transform = True
        self._partial_fit(X, y)
        transformed = self.transform(X, y)
        self._in_fit_transform = False
        return transformed

    def construct_tsdf(self,
                       X: DataInputType,
                       y: Optional[DataSingleColumnInputType] = None) -> TimeSeriesDataFrame:
        """Contruct timeseries dataframe."""
        self._columns = X.columns
        has_dummy_grain = False
        if self.grain_column_names is None or len(self.grain_column_names) == 0\
           or (self.dummy_grain_column not in X.columns and self.dummy_grain_column == self.grain_column_names[0]):
            X[self.dummy_grain_column] = self.dummy_grain_column
            self.grain_column_names = [self.dummy_grain_column]
            has_dummy_grain = True
        # Ensure that grain_column_names is always list.
        if isinstance(self.grain_column_names, str):
            self.grain_column_names = [self.grain_column_names]
        X[self.target_column_name] = y if y is not None else np.NaN

        # TODO: Currently we are not checking if y values contain NaNs.
        # This is a potential source of bugs. In future we will need to infer the NaNs
        # or drop the columns with NaNs or throw the error.
        try:
            tsdf = self._create_tsdf_from_data(X,
                                               time_column_name=self.time_column_name,
                                               target_column_name=self.target_column_name,
                                               grain_column_names=self.grain_column_names)

        except AutoMLException:
            raise
        except Exception as e:
            msg = ("Internal error formatting time-series data: {}. "
                   "Please contact product support.")
            pii_msg = msg.format(str(e))
            gen_msg = msg.format('[Masked]')
            raise ClientException.from_exception(
                e, pii_msg,
                reference_code='abstract_timeseries_transformer.AbstractTimeSeriesTransformer.construct_tsdf',
                has_pii=True).with_generic_msg(gen_msg)
        finally:
            # Drop the target column we have added.
            X.drop(self.target_column_name, inplace=True, axis=1)
            if has_dummy_grain:
                X.drop(self.dummy_grain_column, inplace=True, axis=1)

        return tsdf

    def _partial_fit(self,
                     X: DataInputType,
                     y: Optional[DataSingleColumnInputType] = None) -> None:
        """
        Partial fit method to fit the transform

        *Note* This method is a lazy fit, it does not transforms the training data set to save the time.
        It saves time and memory during call to fit_transform. In the fit-transform we have to save the
        order of columns in the transformed data set. To achieve that we need to perform transformation
        but if the data set is big we can not do it in fit(), because we do not want to do transformation twice.
        To avoid this we analyze the data set in _partial_fit and then transform it in the transform()
        but only if we do not know the order of columns.
        :param X: Dataframe representing text, numerical or categorical input.
        :param y: To match fit signature.

        :return: DataTransform object.
        :raises: DataException for non-dataframe and empty dataframes.
        """
        reference_code = 'abstract_timeseries_transformer.AbstractTimeSeriesTransformer._partial_fit'
        self._raise_type_error_maybe(X, reference_code=reference_code)
        self._validate_customized_column_purpose(X)
        # If there are columns of dtype boolean, remember them for further encoding.
        # Note, we can not rely on dtypes, because when the data frame is constructed from the
        # array as in
        self.boolean_columns = [
            colname for colname in filter(
                lambda col: any(
                    isinstance(val, bool) for val in X[col]),
                X.columns.values)]
        self.add_dummy_order_column(X)
        tsdf = self.construct_tsdf(X, y)
        X.drop(self.original_order_column, axis=1, inplace=True)
        all_drop_column_names = [x for x in tsdf.columns if
                                 np.sum(tsdf[x].notnull()) == 0]
        if isinstance(self.drop_column_names, str):
            all_drop_column_names.extend([self.drop_column_names])
        elif self.drop_column_names is not None:
            all_drop_column_names.extend(self.drop_column_names)
        self.drop_column_names = all_drop_column_names
        # We want to infer frequency only if it was not set in the constructor.
        freq_offset = self.parameters.get(TimeSeries.FREQUENCY)  # type: Optional[pd.DateOffset]
        if freq_offset is not None:
            self.freq_offset = freq_offset
            self.freq = self.freq_offset.freqstr
        else:
            self.freq_offset = tsdf.infer_freq()
            # If the data frame has one row or less, then validation did not worked correctly
            # and hence the frequency can not be calculated properly.
            # It is a ClientException because validation should not allow this error to go through.
            if self.freq_offset is None:
                raise DataFrameValueException("All grains in the data frame contain less then 2 values.",
                                              reference_code="abstract_timeseries_transformer.\
                                                  AbstractTimeSeriesTransformer._partial_fit", has_pii=False)
            self.freq = self.freq_offset.freqstr
        # Create the imputer for y values.
        self._y_imputers = {}
        dfs = []
        dfs_unknown = []
        for grain, df_one in tsdf.groupby_grain():
            if all(pd.isnull(v) for v in df_one.ts_value):
                msg = ("The grain {} does not contain data points. "
                       "Please remove it and run the experiment again.")
                raise InsufficientDataException(
                    msg.format(grain),
                    reference_code=ReferenceCodes._TST_NO_DATA_IN_GRAIN
                ).with_generic_msg(msg.format('[Masked]'))
            # Save the latest dates for the training set.
            # Create the dictionary on the already created groupby object.
            # For the purposes of fit we need to remove all NaN suffix.
            last_nan = np.max(np.where(pd.notna(df_one.ts_value)))
            df_unknown = df_one[last_nan:].copy()
            df_one = df_one[:last_nan + 1]
            if df_unknown.shape[0] > 1:
                df_unknown = self._impute_target_value(df_unknown)
                dfs_unknown.append(df_unknown[1:])
            self.dict_latest_date[grain] = max(df_one.time_index)
            self._y_imputers[grain] = self._get_target_imputer(grain_df=df_one)
            dfs.append(df_one)
        if len(dfs_unknown) > 0:
            self._unknown_train_part = pd.concat(dfs_unknown)
        self._known_train_part = cast(TimeSeriesDataFrame, pd.concat(dfs))
        # clean up memory.
        del dfs
        self.pipeline = self._do_construct_pre_processing_pipeline(self._known_train_part, self.drop_column_names)
        # Mark the places where target was null.
        if not hasattr(self, AbstractTimeSeriesTransformer.MISSING_Y):
            self.missing_y = self._init_missing_y()
        self._known_train_part = self.missing_y.fit_transform(self._known_train_part)
        self._known_train_part = self._impute_target_value(cast(TimeSeriesDataFrame, self._known_train_part))
        # Make sure we will estimate the column order again if we will re fit.
        self._fit_column_order = np.array([])
        self._fit_column_order_no_ts_value = np.array([])

    def _fit_columns_order(
            self) -> 'TimeSeriesDataFrame':
        """
        The second part of fitting routime: run the transform and save columns order.

        The last part of fitting procedure. This part actially transform the data set and save the columns order.
        :return: transformed TimeSeriesDataFrame containing rows before the last known y inclusive.
        """
        if self.pipeline is None:
            raise ClientException('_partial_fit must be called before calling _fit_columns_order.',
                                  reference_code="abstract_timeseries_transformer.\
                                      AbstractTimeSeriesTransformer._fit_columns_order", has_pii=False)
        if self._known_train_part is not None:
            transformed_train_df = self.pipeline.fit_transform(
                self._known_train_part, self._known_train_part.ts_value.values)
        else:
            raise ClientException("Training failed due to missing known trained parts.", has_pii=False)
        # Remember all the columns except for self.original_order_column
        target_missing_dummy_name = MissingDummiesTransformer.get_column_name(TimeSeriesInternal.DUMMY_TARGET_COLUMN)
        self._fit_column_order = transformed_train_df.columns.values[transformed_train_df.columns.values !=
                                                                     self.original_order_column]
        # Drop the missing dummy column tracker from column order
        self._fit_column_order = self._fit_column_order[self._fit_column_order !=
                                                        target_missing_dummy_name]

        # We may want to keep the column order without target value,
        # because during prediction this column will not be present and will be
        # only transiently created in LagLeadOperator and in RollingWindow.
        # To save memory we will just remove the transformed_train_df.ts_value_colname from the array
        # of column names.
        arr_no_target = self._fit_column_order[self._fit_column_order !=
                                               transformed_train_df.ts_value_colname]
        self._fit_column_order_no_ts_value = arr_no_target
        return cast(TimeSeriesDataFrame, transformed_train_df)

    @function_debug_log_wrapped('info')
    def fit(self,
            X: DataInputType,
            y: Optional[DataSingleColumnInputType] = None) -> 'AbstractTimeSeriesTransformer':
        """
        The fit method to fit the transform.

        :param X: Dataframe representing text, numerical or categorical input.
        :param y: To match fit signature.

        :return: DataTransform object.
        :raises: DataException for non-dataframe and empty dataframes.
        """
        self._partial_fit(X, y)
        self._fit_columns_order()
        self._unknown_train_part = None
        self._known_train_part = None
        return self

    @function_debug_log_wrapped('info')
    def transform(self,
                  df: DataInputType,
                  y: Optional[DataSingleColumnInputType] = None) -> pd.DataFrame:
        """
        Transform the input raw data with the transformations identified in fit stage.

        :param df: Dataframe representing text, numerical or categorical input.
        :type df: pandas.DataFrame
        :param y: To match fit signature.
        :type y: numpy.ndarray

        :return: pandas.DataFrame
        :raises: ClientException

        """
        reference_code = 'abstract_timeseries_transformer.AbstractTimeSeriesTransformer.transform'
        self._raise_type_error_maybe(df, reference_code=reference_code)
        self._raise_no_fit_exception_maybe(reference_code=reference_code)
        # We know that the pipeline is not None, because otherwise
        # _raise_no_fit_exception_maybe will throw the error.
        # mypy do not see this assertion.
        assert(self.pipeline is not None)

        # Try to remove points from the data frame which are not aligned with
        # frequency obtained during fit time only if y was not provided only i.e. in the transform time.
        if not self._in_fit_transform:
            effective_grain = self.grain_column_names  # type: Optional[List[str]]
            latest_dates = self.dict_latest_date
            if self.grain_column_names == [constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN] and \
                    self.grain_column_names[0] not in df.columns:
                effective_grain = None
                latest_dates = self.dict_latest_date[constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN]
            df_fixed = fix_df_frequency(
                df,
                self.time_column_name,
                effective_grain,
                latest_dates,
                self.freq_offset)
            if df_fixed.shape[0] != 0:
                df = df_fixed
            del df_fixed

        has_dummy_grain = False
        if self.dummy_grain_column in self.grain_column_names:
            has_dummy_grain = True
            df[self.dummy_grain_column] = self.dummy_grain_column

        target_was_appended = False

        # Dealing with fake imputed row removal, save the original row sequence
        # number then later use it to restore the order after featurization
        # Drop existing index if there is any
        self.add_dummy_order_column(df)
        if y is not None:
            # transform training data
            target_was_appended = True
            df[self.target_column_name] = y
            if self._fit_column_order.shape[0] == 0:
                # If we do not have elemnents in  _fit_column_order
                # we did not finished pipeline fitting and need to do it here.
                tsdf = self._known_train_part if self._unknown_train_part is None else pd.concat(
                    [self._known_train_part, self._unknown_train_part])
                transformed_data = self._fit_columns_order()
                # The problem: if look back features are enabled, we will get NaNs in the places
                # where the target is missing.
                if self._unknown_train_part is not None:
                    tsdf_unknown = self.pipeline.transform(self._unknown_train_part)
                    transformed_data = pd.concat([transformed_data, tsdf_unknown])
                self._unknown_train_part = None
                self._known_train_part = None
            else:
                tsdf = self._create_tsdf_from_data(
                    df,
                    time_column_name=self.time_column_name,
                    target_column_name=self.target_column_name,
                    grain_column_names=self.grain_column_names)
                if not hasattr(self, AbstractTimeSeriesTransformer.MISSING_Y):
                    self.missing_y = self._init_missing_y()
                tsdf = self.missing_y.transform(tsdf)
                tsdf = self._impute_target_value(cast(TimeSeriesDataFrame, tsdf))
                transformed_data = self.pipeline.transform(tsdf)

        else:
            tsdf = self._create_tsdf_from_data(df,
                                               time_column_name=self.time_column_name,
                                               target_column_name=None,
                                               grain_column_names=self.grain_column_names)
            scoring_freq = tsdf.infer_freq(return_freq_string=False)

            if self.freq_offset is not None and scoring_freq is not None and self.freq_offset != scoring_freq:
                # Before raising exception we need to check if the dates at new data frame can be aligned
                # with the previous.
                exception_text = "Scoring data frequency is not consistent with training data."
                self._check_phase(tsdf, scoring_freq, exception_text, False)
            # preserve the index because the input X_test may not be continuous
            transformed_data = self.pipeline.transform(tsdf)

        # We are doing inner join, which will remove the imputed rows and preserve the rows order
        # in the output data frame.
        transformed_data = transformed_data[transformed_data[self.original_order_column].notnull()]
        transformed_data.sort_values(by=[self.original_order_column], inplace=True)
        transformed_data.pop(self.original_order_column)

        # We may have previously modified data frame. Remove the dummy grain if we have added it.
        if has_dummy_grain:
            df.drop(self.dummy_grain_column, axis=1, inplace=True)
        if target_was_appended:
            df.drop(self.target_column_name, axis=1, inplace=True)
        df.drop(self.original_order_column, axis=1, inplace=True)

        # drop the dummy column used to select lag_option in LagLeadOperator
        target_missing_dummy_name = MissingDummiesTransformer.get_column_name(TimeSeriesInternal.DUMMY_TARGET_COLUMN)
        if target_missing_dummy_name in transformed_data.columns:
            transformed_data.drop(target_missing_dummy_name, axis=1, inplace=True)

        if self.engineered_feature_names is None:
            self.engineered_feature_names = transformed_data.columns.values.tolist()
            if self.target_column_name in self.engineered_feature_names:
                self.engineered_feature_names.remove(self.target_column_name)
            # Generate the json objects for engineered features
            self._generate_json_for_engineered_features(tsdf)
        # Make sure that the order of columns is the same as in training set.
        transformed_data = pd.DataFrame(transformed_data)
        if y is not None or self.target_column_name in transformed_data.columns:
            transformed_data = transformed_data[self._fit_column_order]
        else:
            transformed_data = transformed_data[self._fit_column_order_no_ts_value]
        return transformed_data

    def _check_phase(self,
                     scoring_tsdf: TimeSeriesDataFrame,
                     scoring_freq: DateOffset,
                     freq_diff_exception: str,
                     has_pii: bool = True) -> None:
        """
        Check the phase of the data.

        If phases are different, raise the exception.
        :param scoring_tsdf: The time series data frame used for scoring/testing.
        :param scoring_freq: The frequency of scoring time series data frame.
        :param freq_diff_exception: The text of an exception if scores are different.
        :param has_pii: denote if the freq_diff_exception contains the PII (False by default).
        :raises: DataException
        """
        for grain, df_one in scoring_tsdf.groupby_grain():
            date_before = self.dict_latest_date.get(grain)
            if date_before is None:
                raise GrainAbsent('One of grains is not contained in the training set.',
                                  reference_code="abstract_timeseries_transformer.\
                                      AbstractTimeSeriesTransformer._check_phase", has_pii=False)
            # Create a date grid.
            date_grid = pd.date_range(start=date_before,
                                      end=df_one.time_index.max(),
                                      freq=self.freq_offset)
        # Raise exception only if times are not align.
        # QS-JAN aligns with QS-OCT
        if any([tstamp not in date_grid for tstamp in df_one.time_index]):
            raise ForecastingDataException(
                freq_diff_exception, has_pii=has_pii,
                reference_code="abstract_timeseries_transformer.AbstractTimeSeriesTransformer._check_phase")

    @abc.abstractmethod
    def _generate_json_for_engineered_features(self, tsdf: pd.DataFrame) -> None:
        """
        Create the transformer json format for each engineered feature.

        :param tsdf: The time series data frame.
        """
        pass

    def get_engineered_feature_names(self) -> Optional[List[str]]:
        """
        Get the transformed column names.

        :return: list of strings
        """
        return self.engineered_feature_names

    def _create_tsdf_from_data(self,
                               data: pd.DataFrame,
                               time_column_name: str,
                               target_column_name: Optional[str] = None,
                               grain_column_names: Optional[Union[str, List[str]]] = None) -> TimeSeriesDataFrame:
        """
        Given the input data, construct the time series data frame.

        :param data: data used to train the model.
        :type data: pandas.DataFrame
        :param time_column_name: Column label identifying the time axis.
        :type time_column_name: str
        :param target_column_name: Column label identifying the target column.
        :type target_column_name: str
        :param grain_column_names:  Column labels identifying the grain columns.
                                Grain columns are the "group by" columns that identify data
                                belonging to the same grain in the real-world.

                                Here are some simple examples -
                                The following sales data contains two years
                                of annual sales data for two stores. In this example,
                                grain_colnames=['store'].

                                >>>          year  store  sales
                                ... 0  2016-01-01      1     56
                                ... 1  2017-01-01      1     98
                                ... 2  2016-01-01      2    104
                                ... 3  2017-01-01      2    140

        :type grain_column_names: str, list or array-like
        :return: TimeSeriesDataFrame

        """
        if time_column_name not in data.columns:
            raise DataFrameMissingColumnException(
                pii_message=TimeSeriesDataFrame.TIME_ABSENT_TEMPL % time_column_name,
                reference_code="abstract_timeseries_transformer.\
                                AbstractTimeSeriesTransformer._create_tsdf_from_data",
                target=DataFrameMissingColumnException.TIME_COLUMN)
        data[time_column_name] = pd.to_datetime(data[time_column_name])
        # Drop the entire row if time index not exist
        data = data.dropna(subset=[time_column_name], axis=0).reset_index(drop=True)
        data = data.infer_objects()
        # Check if data has the designated origin column/index
        # If not, don't try to set it since this will trigger an exception in TSDF
        origin_present = self.origin_column_name is not None \
            and (self.origin_column_name in data.index.names or
                 self.origin_column_name in data.columns)
        origin_setting = self.origin_column_name if origin_present else None
        tsdf = TimeSeriesDataFrame(data, time_colname=time_column_name,
                                   ts_value_colname=target_column_name,
                                   origin_time_colname=origin_setting,
                                   grain_colnames=grain_column_names
                                   )
        self._encode_boolean_columns(tsdf)
        return tsdf

    def _raise_no_fit_exception_maybe(self, reference_code: str) -> None:
        """
        Raise the exception if fit was not called.

        :raises: ClientException
        """
        if not self.pipeline:
            raise ClientException.create_without_pii("Fit not called.", reference_code=reference_code)

    def _raise_type_error_maybe(self, X: Any, reference_code: str) -> None:
        """
        Raise error if X is not a pandas dataframe.

        :param X: The input data which type have to be checked.
        """
        if not isinstance(X, pd.DataFrame):
            raise InvalidDataTypeException(
                self.TYPE_ERROR_TEMPLATE.format(type(X)), reference_code=reference_code).with_generic_msg(
                    self.TYPE_ERROR_TEMPLATE.format('[Masked]'))
        if X.shape[0] == 0:
            raise EmptyDataException(self.DATA_FRAME_EMPTY, has_pii=False, reference_code=reference_code)

    def _encode_boolean_columns(self, tsdf: TimeSeriesDataFrame) -> None:
        """
        If the boolean columns were detected encode it as 0 and 1.

        *Note* this method modifies the data frame inplace.
        :param tsdf: The time series dataframe to be modified.

        """
        if self.boolean_columns:
            for col in self.boolean_columns:
                if col in tsdf.columns:
                    tsdf[col] = tsdf[col].apply(lambda x: np.nan if pd.isnull(x) else int(x))

    def add_dummy_order_column(self, X: pd.DataFrame) -> None:
        """
        Add the dummy order column to the pandas data frame.

        :param X: The data frame which will undergo order column addition.
        """
        X.reset_index(inplace=True, drop=True)
        X[self.original_order_column] = X.index

    def _get_target_imputer(self, grain_df: Optional[pd.DataFrame] = None) -> TimeSeriesImputer:
        """
        Get target value imputer based on the featurization config.

        :param grain_df: A timeseries dataframe that contains target column for imputation.
        """
        custom_imputer = None
        if grain_df is not None:
            custom_imputer = self._get_customized_target_imputer(grain_df)
        if custom_imputer is not None:
            return custom_imputer
        return self._get_default_target_imputer(grain_df)

    def _get_customized_target_imputer(self, tsdf: TimeSeriesDataFrame) -> Optional[TimeSeriesImputer]:
        """
        Get target value imputer based on the featurization config.

        :param tsdf: A timeseries dataframe that contains target column for imputation.
        :return: Customized target imputer.
        """
        transformer_params = self._featurization_config.transformer_params
        if transformer_params is not None and transformer_params.get(SupportedTransformers.Imputer) is not None:
            for cols, params in transformer_params.get(SupportedTransformers.Imputer):
                if self.target_column_name in cols:
                    fill_value = self._get_numerical_imputer_value(self.target_column_name, 0, tsdf, params)
                    imputer = TimeSeriesImputer(input_column=[self.target_column_name],
                                                option='fillna', value=fill_value, freq=self.freq_offset)
                    return imputer
        return None

    def _is_using_customized_target_imputer(self) -> bool:
        """
        Return whether target imputer is customized.
        """
        if self._featurization_config.transformer_params is not None:
            for cols, _ in self._featurization_config.transformer_params[SupportedTransformers.Imputer]:
                if self.target_column_name in cols:
                    return True
        return False

    def _get_default_target_imputer(self, grain_df: Optional[pd.DataFrame] = None) -> TimeSeriesImputer:
        """

        :param grain_df: A timeseries dataframe that contains target column for imputation.
        :return: Default target timeseries imputer.
        """
        if grain_df is None:
            return TimeSeriesImputer(
                input_column=[self.target_column_name],
                option='fillna', method='ffill',
                freq=self.freq_offset)
        else:
            return TimeSeriesImputer(
                input_column=[self.target_column_name],
                value={self.target_column_name: grain_df[self.target_column_name].median()},
                freq=self.freq_offset)

    def _get_x_imputer(self,
                       tsdf: TimeSeriesDataFrame,
                       numerical_columns: List[str],
                       datetime_columns: List[str],
                       imputation_dict: Dict[str, float],
                       datetime_imputation_dict: Dict[str, float]) -> TimeSeriesImputer:
        """
        Get a chained x value imputer based on the featurization config.

        :param input_column_list: All the imputation value list.
        :param default_imputation_dict: The default value for x imputation.
        """
        if self._has_valid_customized_imputer():
            for cols, params in self._featurization_config.transformer_params[SupportedTransformers.Imputer]:
                # Replace the imputation parameter to custom if we can.
                # Remove the special columns from imputer parameters
                # even if user has specified imputer for time or grain column.
                special_columns = self.grain_column_names + [self.time_column_name, self.target_column_name]
                for col in filter(lambda x: x not in special_columns, cols):
                    if col not in tsdf.columns:
                        msg = ("The column '{}' specified in the "
                               "FeaturizationConfig's custom transforms "
                               "is not present in the data frame.")
                        raise InvalidValueException(
                            msg.format(col),
                            reference_code=ReferenceCodes._TST_FEATURIZATION_TRANSFORM).with_generic_msg(
                                msg.format('[Masked]'))
                    imputation_dict[col] = self._get_numerical_imputer_value(
                        col, cast(float, imputation_dict.get(col)), tsdf, params
                    )

        if len(datetime_columns) > 0:
            impute_missing = TimeSeriesImputer(option='fillna',
                                               input_column=numerical_columns + datetime_columns,
                                               method=OrderedDict({'ffill': datetime_columns,
                                                                   'bfill': datetime_columns}),
                                               value={**imputation_dict, **datetime_imputation_dict},
                                               freq=self.freq_offset)
        else:
            impute_missing = TimeSeriesImputer(option='fillna',
                                               input_column=numerical_columns,
                                               value=imputation_dict,
                                               freq=self.freq_offset)

        return impute_missing

    def _get_numerical_imputer_value(
            self,
            col: str,
            default_value: Union[int, float],
            tsdf: TimeSeriesDataFrame,
            transformer_params: Dict[str, Any]
    ) -> Union[int, float]:
        """
        Get the numerical imputer value by using featurization config.

        :param col: The column name.
        :param default_value: The default value if no customized imputer is used.
        :param tsdf: The TimeSeriesDataFrame used for imputation.
        :param transformer_params: The parameters that define the transformer.
        :return: A numeric value.
        """
        strategy = transformer_params.get(TransformerParams.Imputer.Strategy)
        fill_value = transformer_params.get(TransformerParams.Imputer.FillValue)
        if strategy == TransformerParams.Imputer.Constant and fill_value is not None:
            return cast(Union[int, float], fill_value)
        elif strategy == TransformerParams.Imputer.Mean:
            return cast(Union[int, float], tsdf[col].mean())
        elif strategy == TransformerParams.Imputer.Median:
            return cast(Union[int, float], tsdf[col].median())
        elif strategy == TransformerParams.Imputer.Mode:
            return cast(Union[int, float], tsdf[col].mode()[0])
        return default_value

    def _get_date_columns(self, tsdf: TimeSeriesDataFrame) -> List[str]:
        """
        Get The date columns in the TimeseriesDataFrame.

        :param tsdf: The TimeseriesDataFrame.
        :return: A list of column names.
        """
        return self._get_columns_by_type(tsdf, [np.datetime64], FeatureType.DateTime)

    def _get_numerical_columns(self, tsdf: TimeSeriesDataFrame) -> List[str]:
        """
        Get The numerical columns in the TimeseriesDataFrame.

        :param tsdf: The TimeseriesDataFrame.
        :return: A list of column names.
        """
        numerical_columns = self._get_columns_by_type(tsdf, [np.number], FeatureType.Numeric)
        if self.target_column_name in numerical_columns:
            numerical_columns.remove(self.target_column_name)
        if self.original_order_column in numerical_columns:
            numerical_columns.remove(self.original_order_column)
        return numerical_columns

    def _get_columns_by_type(self,
                             tsdf: TimeSeriesDataFrame,
                             selected_types: List[Any],
                             selected_purpose: str) -> List[str]:
        """
        Get the columns by column type and purpose.

        :param tsdf: The TimeSeriesDataFrame.
        :param selected_types: The selected types.
        :param selected_purpose: The selected column purpose.
        :return: A list of column names.
        """
        include_cols = self._get_included_columns(tsdf, selected_purpose)
        exclude_cols = self._get_excluded_columns(tsdf, selected_purpose)
        columns = [x for x in tsdf.select_dtypes(selected_types).columns
                   if (x not in (self.drop_column_names or []) and
                       x not in exclude_cols and x not in include_cols)]
        for col in include_cols:
            columns.append(col)
        return columns

    def _get_included_columns(self, tsdf: TimeSeriesDataFrame, include_purpose: str) -> Set[str]:
        """
        Get the columns included by column purpose from featurization config.

        :param tsdf: The TimeSeriesDataFrame.
        :param include_purpose: the include purpose.
        :return: A set of column names.
        """
        if self._featurization_config.column_purposes is None:
            return set()
        return {col for col, purpose in self._featurization_config.column_purposes.items()
                if purpose == include_purpose and col in tsdf.columns}

    def _get_excluded_columns(self, tsdf: TimeSeriesDataFrame, exclude_purpose: str) -> Set[str]:
        """
        Get the columns exclude by column purpose from featurization config.

        :param tsdf: The TimeSeriesDataFrame.
        :param exclude_purpose: the exclude purpose.
        :return: A set of column names.
        """
        if self._featurization_config.column_purposes is None:
            return set()
        return {col for col, purpose in self._featurization_config.column_purposes.items()
                if purpose != exclude_purpose and col in tsdf.columns}

    def _convert_featurization_config(
        self, featurization_config: Optional[Union[str, FeaturizationConfig]]
    ) -> FeaturizationConfig:
        """
        Convert the input featurization config for type checking.

        :param featurization_config: the featurization config could be None, str, FeaturizationConfig.
        :return: A FeaturizationConfig.
        """
        if featurization_config is not None and isinstance(featurization_config, FeaturizationConfig):
            return featurization_config
        else:
            return FeaturizationConfig()

    def _validate_customized_column_purpose(self, tsdf: DataInputType) -> None:
        """
        Validate whether the column data can be transformed to customized column purpose type.

        :param tsdf: The TimeSeriesDataFrame.
        :raise: InvalidDataTypeException when converting the input type to the customized types.
        """
        if self._featurization_config.column_purposes is None:
            return None
        for col, purpose in self._featurization_config.column_purposes.items():
            if col in tsdf.columns:
                try:
                    if purpose == FeatureType.Categorical:
                        tsdf[col] = tsdf[col].astype(np.object)
                    elif purpose == FeatureType.DateTime:
                        tsdf[col] = pd.to_datetime(tsdf[col])
                    elif purpose == FeatureType.Numeric:
                        tsdf[col] = tsdf[col].astype(np.number)
                except Exception as e:
                    type_convert_dict = {
                        FeatureType.Categorical: 'category', FeatureType.Numeric: 'np.float',
                        FeatureType.DateTime: 'np.datetime64'
                    }
                    raise InvalidDataTypeException(
                        "Type conversion failed for converting the input column {} to the target column purpose {}"
                        "because of {}.\nPlease check whether your column can be converted to {} by using"
                        " `pd.astype` and try again.".format(col, purpose, e, type_convert_dict.get(purpose)),
                        target='column_purposes',
                        has_pii=True,
                        reference_code=ReferenceCodes._ABSTRACT_TS_TRANSFROMER_COLUMN_PURPOSE_CONVERSION_ERROR
                    ).with_generic_msg("Invalid type conversion for customized column purposes.")

    def _has_valid_customized_imputer(self) -> bool:
        """
        Check whether the featurization config has valid imputer or not.
        """
        return self._featurization_config is not None and self._featurization_config.transformer_params is not None \
            and self._featurization_config.transformer_params.get(SupportedTransformers.Imputer) is not None

    @property
    def columns(self) -> Optional[List[str]]:
        """
        Return the list of expected columns.

        :returns: The list of columns.
        :rtype: list

        """
        return self._columns

    @property
    def y_imputers(self) -> Dict[str, TimeSeriesImputer]:
        """
        Return the imputer for target column.

        :returns: imputer for target column.
        :rtype: dict

        """
        return self._y_imputers
