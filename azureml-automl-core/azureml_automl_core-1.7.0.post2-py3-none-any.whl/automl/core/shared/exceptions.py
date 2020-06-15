# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Exceptions thrown by AutoML."""
import json
from typing import Any, cast, Dict, List, Optional, Type, TypeVar

from ._error_response_constants import ErrorCodes
from azureml.automl.core.shared.constants import ClientErrors


ExceptionT = TypeVar('ExceptionT', bound='AutoMLException')

NON_PII_MESSAGE = '[Hidden as it may contain PII]'


class ErrorTypes:
    """Possible types of errors."""

    User = 'User'
    Service = 'Service'
    Client = 'Client'
    Resource = 'Resource'
    Unclassified = 'Unclassified'
    All = {User, Service, Client, Resource, Unclassified}


class AutoMLException(Exception):
    """Exception with an additional field specifying what type of error it is."""

    def __init__(self,
                 exception_message: str = "",
                 target: Optional[str] = None,
                 details: Optional[List[str]] = None,
                 message_format: Optional[str] = None,
                 message_parameters: Optional[Dict[str, str]] = None,
                 reference_code: Optional[str] = None,
                 has_pii: bool = True):
        """
        Construct a new AutoMLException.

        :param exception_message: A message describing the error.
        :type exception_message: str
        :param error_type: Error code corresponding to the exception. Defaults to Unclassified.
        :type error_type: str
        :param target: The name of the element that caused the exception to be thrown.
        :type target: str
        :param details: Any additional information for the error, such as other error responses or stack traces.
        :type details: builtin.list(str)
        :param message_format: Un-formatted version of the exception_message with no variable substitution.
        :type message_format: str
        :param message_parameters: Value substitutions corresponding to the contents of message_format
        :type message_parameters: Dictionary[str, str]
        :param reference_code: Indicator of the module or code where the failure occurred
        :type reference_code: str
        :param has_pii: Boolean representing whether the Exception message has any PII information.
        :type has_pii: bool
        """
        super().__init__(exception_message)
        self._exception_message = exception_message
        self._target = target
        self._details = details
        self._message_format = message_format
        self._message_parameters = message_parameters
        self._reference_code = reference_code or target
        self._inner_exception = None     # type: Optional[BaseException]
        self._has_pii = has_pii
        if has_pii:
            self._generic_msg = None            # type: Optional[str]
        else:
            self._generic_msg = exception_message
            if not self._message_format:
                self._message_format = exception_message

    def __repr__(self) -> str:
        """Return string representation of the exception."""
        inner_exception_message = None
        if self._inner_exception:
            inner_exception_message = "{}: {}".format(
                self._inner_exception.__class__.__name__,
                str(self._inner_exception)
            )
        return self._exception_msg_format(
            self.__class__.__name__,
            self._exception_message,
            inner_exception_message,
            self._serialize_json(indent=4, filter_fields=['message_format', 'message_parameters', 'reference_code'])
        )

    def __str__(self) -> str:
        """Return string representation of the exception."""
        return self.__repr__()

    def _exception_msg_format(
            self,
            error_name: str,
            message: str,
            inner_exception_message: Optional[str],
            error_response: Optional[str]
    ) -> str:
        return "{}:\n\tMessage: {}\n\tInnerException: {}\n\tErrorResponse \n{}".format(
            error_name,
            message,
            inner_exception_message,
            error_response)

    def get_pii_free_exception_msg_format(self) -> str:
        # Update exception message to be PII free
        # Update inner exception to log exception type only
        # Update Error Response to contain PII free message
        pii_free_msg = self.pii_free_msg()
        return self._exception_msg_format(
            self.__class__.__name__,
            pii_free_msg,
            self._inner_exception.__class__.__name__,
            self._serialize_json(
                indent=4, filter_fields=['message_format', 'message_parameters', 'reference_code'],
                error_msg=pii_free_msg
            )
        )

    @classmethod
    def from_exception(cls: 'Type[ExceptionT]',
                       e: BaseException,
                       msg: Optional[str] = None,
                       target: Optional[str] = None,
                       reference_code: Optional[str] = None,
                       has_pii: bool = True) -> ExceptionT:
        """
        Convert an arbitrary exception to this exception type. The resulting exception is marked as containing PII.

        :param e: the original exception object
        :param msg: optional message to use instead of the original exception message
        :param target: optional string pointing to the target of the exception
        :param reference_code: Indicator of the module or code where the failure occurred
        :param has_pii: whether this exception contains PII or not
        :return: a new exception of this type, preserving the original stack trace
        """
        if not msg and isinstance(e, cls):
            return cast(ExceptionT, e)

        # If given exception is not AutoMLException and safe message to override is not given,
        # then mark has_pii = True
        if not isinstance(e, AutoMLException) and not msg:
            has_pii = True

        if isinstance(e, MemoryError):
            new_exception = cast(ExceptionT,
                                 MemorylimitException(exception_message=(msg or str(e)),
                                                      target=target,
                                                      reference_code=reference_code or target,
                                                      has_pii=has_pii).with_traceback(e.__traceback__))
        else:
            new_exception = cast(ExceptionT,
                                 cls(exception_message=(msg or str(e)),
                                     target=target,
                                     reference_code=reference_code or target,
                                     has_pii=has_pii).with_traceback(e.__traceback__))

        new_exception._inner_exception = e
        return new_exception

    @classmethod
    def create_without_pii(cls: 'Type[ExceptionT]', msg: str = "",
                           target: Optional[str] = None, reference_code: Optional[str] = None) -> ExceptionT:
        """
        Create an exception that is tagged as not containing PII.

        :param msg: optional message to use instead of the original exception message
        :param target: optional string pointing to the target of the exception
        :param reference_code: Indicator of the module or code where the failure occurred
        :return:
        """
        exception = cls(exception_message=msg,
                        target=target,
                        message_format=msg,
                        reference_code=reference_code or target,
                        has_pii=False)
        return exception

    def with_generic_msg(self: ExceptionT, msg: str) -> ExceptionT:
        """
        Attach a generic error message that will be used in telemetry if this exception contains PII.

        :param msg: the generic message to use
        :return: this object
        """
        self._generic_msg = msg
        # Until we deprecate _generic_msg, copy it over to message_format which also will be pushed to the service
        self._message_format = msg
        self._has_pii = True
        return self

    @property
    def has_pii(self) -> bool:
        """Check whether this exception's message contains PII or not."""
        return cast(bool, getattr(self, '_has_pii', False))

    @property
    def target(self) -> Optional[str]:
        """Name of the element that caused the exception to be thrown."""
        return self._target

    def pii_free_msg(self, scrubbed: bool = True) -> str:
        """
        Fallback message to use for situations where printing PII-containing information is inappropriate.

        :param scrubbed: If true, return a generic '[Hidden as it may contain PII]' as a fallback, else an empty string
        :return: Log safe message for logging in telemetry
        """
        # If message_format is specified, prefer that over the generic_msg.
        fallback_message = (getattr(self, '_message_format', None) or
                            getattr(self, '_generic_msg', None) or
                            NON_PII_MESSAGE if scrubbed else ''
                            )  # type: str
        message = self._exception_message or fallback_message if not self.has_pii else fallback_message  # type: str
        return message

    @property
    def error_type(self):
        """Get the root error type for this exception."""
        return self._get_all_error_codes()[0]

    @property
    def error_code(self):
        """Get the error code for this exception."""
        return getattr(self, "_error_code", self.error_type)

    def _get_all_error_codes(self) -> List[str]:
        error_response_json = json.loads(self._serialize_json()).get("error")
        if error_response_json is None:
            return [ErrorTypes.Unclassified]
        codes = [error_response_json.get('code', ErrorTypes.Unclassified)]
        inner_error = error_response_json.get(
            'inner_error', error_response_json.get('innerError', None))
        while inner_error is not None:
            code = inner_error.get('code')
            if code is None:
                break
            codes.append(code)
            inner_error = inner_error.get(
                'inner_error', inner_error.get('innerError', None))
        return codes

    def _serialize_json(
            self,
            indent: Optional[int] = None,
            filter_fields: Optional[List[str]] = None,
            error_msg: Optional[str] = None
    ) -> str:
        """
        Serialize this exception as an ErrorResponse json.

        :return: json string
        """
        if filter_fields is None:
            filter_fields = []
        error_ret = {}
        error_out = {}  # type: Any
        for super_class in self.__class__.mro():
            if super_class.__name__ == AutoMLException.__name__:
                break
            try:
                error_code = getattr(super_class, '_error_code')
                if error_out != {}:
                    # Flatten the tree in case we have something like System > System > System > System
                    prev_code = error_out.get('code')
                    if prev_code is None or error_code != prev_code:
                        error_out = {"code": error_code, "inner_error": error_out}
                else:
                    error_out = {"code": error_code}
            except AttributeError:
                break

        if error_msg:
            error_out['message'] = error_msg
        else:
            error_out['message'] = self._exception_message
        if self._target is not None:
            error_out['target'] = self._target
        if self._details is not None:
            error_out['details'] = self._details
        # These are not a part of standard error response per Microsoft guidelines, plus it's redundant to show it
        # to the user.
        if self._message_format is not None and 'message_format' not in filter_fields:
            error_out['message_format'] = self._message_format
        if self._message_parameters is not None and 'message_parameters' not in filter_fields:
            error_out['message_parameters'] = json.dumps(self._message_parameters)
        if self._reference_code is not None and 'reference_code' not in filter_fields:
            error_out['reference_code'] = self._reference_code
        error_ret['error'] = error_out

        return json.dumps(error_ret, indent=indent, sort_keys=True)


class UserException(AutoMLException):
    """
    Exception related to user error.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.USER_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new UserException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class DataException(UserException):
    """
    Exception related to data validations.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    # Targets
    MISSING_DATA = 'MissingData'

    _error_code = ErrorCodes.INVALIDDATA_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DataException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class ConfigException(UserException):
    """
    Exception related to invalid user config.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.VALIDATION_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new ConfigException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class ClientException(AutoMLException):
    """
    Exception related to client.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.SYSTEM_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new ClientException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class ServiceException(ClientException):
    """
    Exception related to JOS.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.SERVICE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new ServiceException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class DataErrorException(ClientException):
    """
    Exception related to errors seen while processing data at training or inference time.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.DATA_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DataErrorException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class FitException(ClientException):
    """
    Exception related to fit in external pipelines, models, and transformers.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.FIT_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new FitException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class TransformException(ClientException):
    """
    Exception related to transform in external pipelines and transformers.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.TRANSFORM_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new TransformException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class PredictionException(ClientException):
    """
    Exception related to prediction in external pipelines and transformers.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.PREDICTION_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new PredictionException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class UntrainedModelException(ClientException):
    """UntrainedModelException."""

    def __init__(self, exception_message="Fit needs to be called before predict.", target=None, **kwargs):
        """
        Create a UntrainedModelException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__("UntrainedModelException: {0}".format(exception_message), target=target, **kwargs)


class InvalidArgumentException(ClientException):
    """Exception related to arguments that were not expected by a component."""

    _error_code = ErrorCodes.BADARGUMENT_ERROR

    def __init__(self, exception_message, error_detail=None, target=None, **kwargs):
        """Create a InvalidArgumentException."""
        if error_detail is not None:
            super().__init__(
                exception_message="InvalidArgumentException: {0}, {1}".format(exception_message, error_detail),
                target=target, **kwargs)
        else:
            super().__init__(exception_message="InvalidArgumentException: {0}".format(exception_message),
                             target=target, **kwargs)


class RawDataSnapshotException(ClientException):
    """
    Exception related to capturing the raw data snapshot to be used at the inference time.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.RAWDATASNAPSHOT_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new RawDataSnapshotException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class ResourceException(UserException):
    """
    Exception related to insufficient resources on the user compute.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new ResourceException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class OnnxConvertException(ClientException):
    """Exception related to ONNX convert."""

    # TODO - define a code for this
    # _error_code = ErrorCodes.ONNX_ERROR


class DataprepException(ClientException):
    """Exceptions related to Dataprep."""

    # TODO - define a code for this
    # _error_code = ErrorCodes.DATAPREPVALIDATION_ERROR


class DeleteFileException(ClientException):
    """Exceptions related to file cleanup."""

    _error_code = ErrorCodes.DELETE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DeleteFileException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class DataShapeException(UserException):
    """The class of errors related to the data frame shape."""

    _error_code = ErrorCodes.DATASHAPE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DataShapeException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class LabelMissingException(DataException):
    """Exception related to label missing from input data.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.INPUTLABELMISSING_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new LabelMissingException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class FeaturizationOffException(DataException):
    """Exception related to featurization not being enabled.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.FEATURIZATIONOFF_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new FeaturizationOffException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class DataSamplesSizeException(DataException):
    """Exception related to X and y having different number of samples.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.DATASAMPLESMISMATCH_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DataSamplesMismatchException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class EmptyDataException(DataException):
    """Exception related to the input data is empty.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.EMPTYDATA_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new EmptyDataException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class InvalidDataTypeException(DataException):
    """Exception related to the input data type is invalid.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.INVALIDDATATYPE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new InvalidDataTypeException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class ValidationException(UserException):
    """An exception representing errors caught when validating inputs.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.VALIDATION_ERROR


class ArgumentException(ValidationException):
    """
    Exception related to invalid user config.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.VALIDATION_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new ConfigException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class BadArgumentException(ValidationException):
    """An exception related to data validation.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.BADARGUMENT_ERROR


class MissingValueException(BadArgumentException):
    """An exception related to data validation.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.BLANKOREMPTY_ERROR


class InvalidValueException(BadArgumentException):
    """An exception related to data validation.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.INVALID_ERROR


class MalformedValueException(BadArgumentException):
    """An exception related to data validation.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.MALFORMED_ERROR


class OutOfRangeException(BadArgumentException):
    """An exception related to value out of range.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.OUTOFRANGE_ERROR


class MissingArgumentException(BadArgumentException):
    """An exception related to missing required argument.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    :type exception_message: str
    """

    _error_code = ErrorCodes.BLANKOREMPTY_ERROR


class ScenarioNotSupportedException(ConfigException):
    """An exception related to scenario not supported.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.SCENARIONOTSUPORTED_ERROR


class UnhashableEntryException(DataException):
    """An exception related to unhashable entry in the input data.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.UNHASHABLEENTRY_ERROR


class InsufficientDataException(DataException):
    """An exception related to insufficient input data.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.INSUFFICIENTDATA_ERROR


class OutOfBoundDataException(DataException):
    """An exception related to inifity input data.

    :param exception_message: A message describing the error.
    :type exception_message: str
    """

    _error_code = ErrorCodes.OUTOFBOUNDDATA_ERROR


class DataFormatException(DataException):
    """Exception related to input data not being in the expected format.

    :param exception_message: Details on the exception.
    """

    _error_code = ErrorCodes.DATAFORMAT_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DataFormatException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class AllLabelsMissingException(DataException):
    """Exception related to input data missing all labels.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.ALLLABELSMISSING_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new AllLabelsMissingException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class DiskSpaceUnavailableException(UserException):
    """Exception related to insufficient disk space."""

    _error_code = ErrorCodes.DISKSPACEUNVAILABLE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new DiskSpaceUnavailableException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class AutoMLEnsembleException(ClientException):
    """Exception for AutoML ensembling related errors."""

    # Targets
    CONFIGURATION = 'Configuration'
    MISSING_MODELS = 'MissingModels'
    MODEL_NOT_FIT = 'ModelNotFit'

    _error_code = ErrorCodes.AUTOMLENSEMBLE_ERROR

    def __init__(self, exception_message, error_detail=None, target=None, **kwargs):
        """Create an AutoMLEnsemble exception."""
        if error_detail is not None:
            super().__init__(
                exception_message="AutoMLEnsembleException: {0}, {1}".format(exception_message, error_detail),
                target=target, **kwargs)
        else:
            super().__init__(exception_message="AutoMLEnsembleException: {0}".format(exception_message), **kwargs)


class PipelineRunException(ClientException):
    """Exception for pipeline run related errors."""

    # Targets
    PIPELINE_RUN_REQUIREMENTS = 'PipelineRunRequirements'
    PIPELINE_RUN = 'PipelineRun'
    PIPELINE_OUTPUT = 'PipelineOutput'

    _error_code = ErrorCodes.PIPELINEEXECUTION_ERROR

    def __init__(self, exception_message, error_detail=None, target=None, **kwargs):
        """Create a PipelineRunException exception."""
        if error_detail is not None:
            super().__init__(
                exception_message="PipelineRunException: {0}, {1}".format(exception_message, error_detail),
                target=target, **kwargs)
        else:
            super().__init__(exception_message="PipelineRunException: {0}".format(exception_message),
                             target=target, **kwargs)


class JasmineServiceException(ServiceException):
    """
    Exception related to the class of errors by Jasmine.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.JASMINESERVICE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new JasmineServiceException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class RunStateChangeException(ServiceException):
    """
    Exception related to failing to change the state of the run.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.STATECHANGE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new RunStateChangeException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class CacheException(ClientException):
    """
    Exception related to cache store operations.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.CACHESTORE_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new CacheException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class MemorylimitException(ResourceException):
    """Exception to raise when memory exceeded."""

    _error_code = ErrorCodes.INSUFFICIENTMEMORY_ERROR

    def __init__(self, exception_message=None, target=None, **kwargs):
        """Constructor.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        message = ClientErrors.EXCEEDED_MEMORY if exception_message is None else exception_message
        super().__init__(message, target, **kwargs)


class OptionalDependencyMissingException(ScenarioNotSupportedException):
    """An exception raised when an a soft dependency is missing.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.OPTIONALDEPENDENCYMISSING_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new OptionalDependencyMissingException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)


class ManagedEnvironmentCorruptedException(ClientException):
    """An exception raised when managed environment has issues with package dependencies.

    :param exception_message: Details on the exception.
    :param target: The name of the element that caused the exception to be thrown.
    """

    _error_code = ErrorCodes.MANAGEDENVIRONMENTCORRUPTED_ERROR

    def __init__(self, exception_message="", target=None, **kwargs):
        """
        Construct a new ManagedEnvironmentCorruptedException.

        :param exception_message: Details on the exception.
        :param target: The name of the element that caused the exception to be thrown.
        """
        super().__init__(exception_message, target, **kwargs)
