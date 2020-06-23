#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
import grpc


class AlicornException(Exception):
    """A base exception for all Alicorn exceptions"""
    pass


class AlicornConfigurationException(AlicornException):
    """Raised on any configuration errors (eg: no ports specified for the server)"""
    pass


class AlicornSignalNotFound(AlicornException):
    """Raised when a signal name does not exist"""
    pass


class AlicornStatusException(AlicornException):
    """Base exception class for raising grpc Status Codes.

    See Also:
        `grpc.StatusCode`
    """
    code = grpc.StatusCode.UNKNOWN
    reason: str = None

    def __init__(self, reason):
        self.reason = reason


class GrpcStatusCancelled(AlicornStatusException):
    code = grpc.StatusCode.CANCELLED


class GrpcStatusUnknown(AlicornStatusException):
    code = grpc.StatusCode.UNKNOWN


class GrpcStatusInvalidArgument(AlicornStatusException):
    code = grpc.StatusCode.INVALID_ARGUMENT


class GrpcStatusDeadlineExceeded(AlicornStatusException):
    code = grpc.StatusCode.DEADLINE_EXCEEDED


class GrpcStatusNotFound(AlicornStatusException):
    code = grpc.StatusCode.NOT_FOUND


class GrpcStatusAlreadyExists(AlicornStatusException):
    code = grpc.StatusCode.ALREADY_EXISTS


class GrpcStatusPermissionDenied(AlicornStatusException):
    code = grpc.StatusCode.PERMISSION_DENIED


class GrpcStatusResourceExhausted(AlicornStatusException):
    code = grpc.StatusCode.RESOURCE_EXHAUSTED


class GrpcStatusFailedPrecondition(AlicornStatusException):
    code = grpc.StatusCode.FAILED_PRECONDITION


class GrpcStatusAborted(AlicornStatusException):
    code = grpc.StatusCode.ABORTED


class GrpcStatusOutOfRange(AlicornStatusException):
    code = grpc.StatusCode.OUT_OF_RANGE


class GrpcStatusUnimplemented(AlicornStatusException):
    code = grpc.StatusCode.UNIMPLEMENTED


class GrpcStatusInternal(AlicornStatusException):
    code = grpc.StatusCode.INTERNAL


class GrpcStatusDataLoss(AlicornStatusException):
    code = grpc.StatusCode.DATA_LOSS


class GrpcStatusUnauthenticated(AlicornStatusException):
    code = grpc.StatusCode.UNAUTHENTICATED
