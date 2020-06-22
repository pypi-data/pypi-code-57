# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with azureml.dataprep."""
from typing import Any, Dict, List
import json
import numpy as np
import pandas as pd

from azureml.automl.core.dataprep_utilities import is_dataflow
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.exceptions import DataException, DataprepException
from azureml.automl.core.shared.limit_function_call_exceptions import MemorylimitException

DATAPREP_INSTALLED = True
try:
    import azureml.dataprep as dprep
except ImportError:
    DATAPREP_INSTALLED = False


def retrieve_numpy_array(dataflow: Any) -> np.array:
    """Retrieve pandas dataframe from dataflow and return underlying ndarray.

    param dataflow: The dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: The retrieved np.ndarray, or the original dataflow value when it is of incorrect type
    """
    reference_code_for_ex = ReferenceCodes._DATAPREP_UTILITIES_NUMPY_ARRAY
    if not is_dataflow(dataflow):
        return dataflow
    try:
        df = dataflow.to_pandas_dataframe(on_error='null')
        if df is None or df.empty:
            raise DataException.create_without_pii("Dataflow resulted in None or empty array.",
                                                   reference_code=reference_code_for_ex)
        if df.shape[1] == 1:
            # if the DF is a single column ensure the resulting output is a 1 dim array by converting
            # to series first.
            return df[df.columns[0]].values
        return df.values
    except DataException:
        raise
    except MemoryError as e:
        generic_msg = 'Failed to retrieve the numpy array from the dataflow due to MemoryError'
        raise MemorylimitException.from_exception(e, reference_code=reference_code_for_ex,
                                                  msg=generic_msg, has_pii=False)
    except Exception as e:
        generic_msg = 'Failed to retrieve the numpy array from the dataflow. Exception Type: {}'
        raise DataException.from_exception(e, reference_code=reference_code_for_ex,
                                           msg=generic_msg.format(type(e))).with_generic_msg(
                                               generic_msg.format('[MASKED]'))


def retrieve_pandas_dataframe(dataflow: Any) -> pd.DataFrame:
    """Retrieve pandas dataframe from dataflow.

    param dataflow: The dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: The retrieved pandas DataFrame, or the original dataflow value when it is of incorrect type
    """
    reference_code_for_ex = ReferenceCodes._DATAPREP_UTILITIES_PANDAS_DATAFRAME
    if not is_dataflow(dataflow):
        return dataflow
    try:
        df = dataflow.to_pandas_dataframe(on_error='null')
        if df is None or df.empty:
            raise DataException.create_without_pii("Dataflow resulted in None or empty dataframe. "
                                                   "Please check your input data and retry.",
                                                   target="retrieve_pandas_dataframe",
                                                   reference_code=reference_code_for_ex)
        return df
    except DataException:
        raise
    except MemoryError as e:
        generic_msg = 'Failed to retrieve the pandas dataframe from the dataflow due to MemoryError'
        raise MemorylimitException.from_exception(e, reference_code=reference_code_for_ex,
                                                  target="retrieve_pandas_dataframe",
                                                  msg=generic_msg, has_pii=False)
    except Exception as e:
        generic_msg = 'Failed to retrieve the pandas dataframe from the dataflow. Exception Type: {}'
        raise DataException.from_exception(e, reference_code=reference_code_for_ex,
                                           target="retrieve_pandas_dataframe",
                                           msg=generic_msg.format(type(e))).with_generic_msg(
                                               generic_msg.format('[MASKED]'))


def resolve_cv_splits_indices(cv_splits_indices: List[dprep.Dataflow]) -> List[List[np.ndarray]]:
    """Resolve cv splits indices.

    param cv_splits_indices: The list of dataflow where each represents a set of split indices
    type: list(azureml.dataprep.Dataflow)
    return: The resolved cv_splits_indices, or the original passed in value when it is of incorrect type
    """
    if cv_splits_indices is None:
        return None
    cv_splits_indices_list = []
    for split in cv_splits_indices:
        if not is_dataflow(split):
            return cv_splits_indices
        else:
            is_train_list = retrieve_numpy_array(split)
            train_indices = []
            valid_indices = []
            for i in range(len(is_train_list)):
                if is_train_list[i] == 1:
                    train_indices.append(i)
                elif is_train_list[i] == 0:
                    valid_indices.append(i)
            cv_splits_indices_list.append(
                [np.array(train_indices), np.array(valid_indices)])
    return cv_splits_indices_list
