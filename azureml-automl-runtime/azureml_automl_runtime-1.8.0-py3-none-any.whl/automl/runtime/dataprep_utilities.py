# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with azureml.dataprep."""
from typing import Any, cast, Dict, List
import json
import logging
import numpy as np
import pandas as pd

from azureml.automl.core.shared.exceptions import (AutoMLException,
                                                   ClientException,
                                                   ConfigException,
                                                   DataException,
                                                   EmptyDataException,
                                                   MemorylimitException)
from azureml.automl.core.dataprep_utilities import is_dataflow
from azureml.automl.core.shared.reference_codes import ReferenceCodes

DATAPREP_INSTALLED = True
try:
    import azureml.dataprep as dprep
except ImportError:
    DATAPREP_INSTALLED = False

try:
    from azureml.dataprep import DataPrepException as DprepException
    NEW_DATAPREP_VERSION = True
except ImportError:
    # TODO Task 748385 Clean up this branch once dataprep min version is updated to 1.6.0
    from azureml.dataprep import ExecutionError as DprepException
    NEW_DATAPREP_VERSION = False

logger = logging.getLogger(__name__)


def retrieve_numpy_array(dataflow: Any) -> np.ndarray:
    """Retrieve pandas dataframe from dataflow and return underlying ndarray.

    param dataflow: The dataflow to retrieve
    type: azureml.dataprep.Dataflow
    return: The retrieved np.ndarray, or the original dataflow value when it is of incorrect type
    """
    reference_code_for_ex = ReferenceCodes._DATAPREP_UTILITIES_NUMPY_ARRAY
    if not is_dataflow(dataflow):
        return cast(np.ndarray, dataflow)
    try:
        df = dataflow.to_pandas_dataframe(on_error='null')  # type: pd.Dataframe
        if df is None or df.empty:
            raise EmptyDataException.create_without_pii(
                "Dataflow resulted in None or empty array.",
                reference_code=reference_code_for_ex)
        if df.shape[1] == 1:
            # if the DF is a single column ensure the resulting output is a 1 dim array by converting
            # to series first.
            return cast(np.ndarray, df[df.columns[0]].values)
        ret_array = cast(np.ndarray, df.values)
    except AutoMLException:
        raise
    except DprepException as e:
        dataprep_error_handler(e)
    except MemoryError as e:
        generic_msg = 'Failed to retrieve the numpy array from the dataflow due to MemoryError'
        raise MemorylimitException.from_exception(e, reference_code=reference_code_for_ex,
                                                  msg=generic_msg, has_pii=False)
    except Exception as e:
        generic_msg = 'Failed to retrieve the numpy array from the dataflow. Exception Type: {}'
        raise DataException.from_exception(e, reference_code=reference_code_for_ex,
                                           msg=generic_msg.format(type(e))).with_generic_msg(
                                               generic_msg.format('[MASKED]'))
    return ret_array


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
            raise EmptyDataException.create_without_pii(
                "Dataflow resulted in None or empty dataframe. Please check your input data and retry.",
                target="retrieve_pandas_dataframe",
                reference_code=reference_code_for_ex)
    except AutoMLException:
        raise
    except MemoryError as e:
        generic_msg = 'Failed to retrieve the pandas dataframe from the dataflow due to MemoryError'
        raise MemorylimitException.from_exception(e, reference_code=reference_code_for_ex,
                                                  target="retrieve_pandas_dataframe",
                                                  msg=generic_msg, has_pii=False)
    except DprepException as e:
        dataprep_error_handler(e)
    except Exception as e:
        generic_msg = 'Failed to retrieve the pandas dataframe from the dataflow. Exception Type: {}'
        raise DataException.from_exception(e, reference_code=reference_code_for_ex,
                                           target="retrieve_pandas_dataframe",
                                           msg=generic_msg.format(type(e))).with_generic_msg(
                                               generic_msg.format('[MASKED]'))
    return df


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


def dataprep_error_handler(e: DprepException) -> None:
    if "OutOfMemory" in e.error_code:
        generic_msg = 'Failed to get data from DataPrep due to MemoryError. ErrorCode: {0}. Message: {1}'.format(
            e.error_code, getattr(e, 'compliant_message', ''))
        raise MemorylimitException.from_exception(e, msg=generic_msg, has_pii=False)
    elif "StreamAccess.NotFound" in e.error_code:
        generic_msg = 'The provided path was not found. ErrorCode: {0}. Message: {1}'.format(
            e.error_code, getattr(e, 'compliant_message', ''))
    elif "StreamAccess.Authentication" in e.error_code:
        generic_msg = 'The provided path could not be accessed. ErrorCode: {0}. Message: {1}'.format(
            e.error_code, getattr(e, 'compliant_message', ''))
    elif "DatastoreResolution.NotFound" in e.error_code:
        generic_msg = 'The provided datastore was not found. ErrorCode: {0}. Message: {1}'.format(
            e.error_code, getattr(e, 'compliant_message', ''))
    elif "MissingSecrets" in e.error_code:
        generic_msg = 'Failed to get data from DataPrep due to missing secrets. ErrorCode: {0}. Message: {1}.'.format(
            e.error_code, getattr(e, 'compliant_message', ''))
    else:
        generic_msg = 'Failed to get data from DataPrep. ErrorCode: {0}. Message: {1}'.format(
            e.error_code, getattr(e, 'compliant_message', ''))
        if NEW_DATAPREP_VERSION:
            raise ClientException.from_exception(e).with_generic_msg(generic_msg)
        else:
            # This is for backwards compatibility.
            # TODO Task 748385. Clean up this branch once dataprep min version is updated to 1.6.0
            raise DataException.from_exception(e).with_generic_msg(generic_msg)
    raise ConfigException.from_exception(e).with_generic_msg(generic_msg)
