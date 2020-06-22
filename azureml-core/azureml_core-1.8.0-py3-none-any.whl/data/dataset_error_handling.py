# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains exceptions for dataset error handling in Azure Machine Learning."""

from azureml.data._dataprep_helper import dataprep, ensure_dataflow


class DatasetValidationError(Exception):
    """Defines an exception for Dataset validation errors.

    :param message: The error message.
    :type message: str
    :param exception: The exception that caused this error.
    :type exception: Exception
    """

    def __init__(self, message, exception=None):
        """Class DatasetValidationError constructor.

        :param message: The error message.
        :type message: str
        :param exception: The exception that caused this error.
        :type exception: Exception
        """
        self.inner_exception = exception
        if exception is not None:
            self.error_code = getattr(exception, 'error_code', None)
            self.validation_error_code = getattr(exception, 'validation_error_code', None)
            self.compliant_message = getattr(exception, 'compliant_message', None)
        super().__init__(message)


class DatasetExecutionError(Exception):
    """Defines an exception for Dataset execution errors.

    :param message: The error message.
    :type message: str
    :param exception: The exception that caused this error.
    :type exception: Exception
    """

    def __init__(self, message, exception):
        """Class DatasetExecutionError constructor.

        :param message: The error message.
        :type message: str
        :param exception: The exception that caused this error.
        :type exception: Exception
        """
        self.inner_exception = exception
        self.error_code = getattr(exception, 'error_code', None)
        self.validation_error_code = getattr(exception, 'validation_error_code', None)
        self.compliant_message = getattr(exception, 'compliant_message', None)

        super().__init__(message)


def _validate_has_data(dataflow, error_message):
    ensure_dataflow(dataflow)
    try:
        dataflow.verify_has_data()
    except (dataprep().api.dataflow.DataflowValidationError,
            dataprep().api.errorhandlers.ExecutionError) as e:
        raise DatasetValidationError(error_message + '\n' + str(e), e)


def _validate_has_columns(dataflow, columns, expected_types=None):
    if expected_types is not None and len(columns) != len(expected_types):
        raise ValueError('Length of `columns` and `expected_types` must be the same')
    ensure_dataflow(dataflow)
    profile = dataflow.keep_columns(columns).take(1)._get_profile()
    if profile.row_count == 0 or profile.row_count is None:
        missing_columns = columns
    else:
        missing_columns = [col for col in columns if col not in profile.columns.keys()]
    if missing_columns:
        raise DatasetValidationError('The specified columns {} do not exist in the current dataset.'
                                     .format(missing_columns))
    if not expected_types:
        return
    mismatch_columns = []
    mismatch_types = []
    for i in range(len(columns)):
        if profile.columns[columns[i]].type != expected_types[i]:
            mismatch_columns.append(columns[i])
            mismatch_types.append(str(expected_types[i])[10:])
    if mismatch_columns:
        raise DatasetValidationError('The specified columns {} do not have the expected types {}.'
                                     .format(mismatch_columns, mismatch_types))


def _try_execute(action, operation=None, dataset_info=None, **kwargs):
    try:
        if len(kwargs) > 0:
            return action(kwargs)
        else:
            return action()
    except Exception as e:
        if dataset_info is not None:
            id = dataset_info.get('id', '')
            name = dataset_info.get('name', '')
            version = dataset_info.get('version', '')
            message = ("in operation '{}' for Dataset(id='{}', name='{}', version={})"
                       .format(operation, id, name, version) + str(e))
        else:
            message = "Execution has failed with: {}".format(str(e))
        raise DatasetExecutionError(message, e)
