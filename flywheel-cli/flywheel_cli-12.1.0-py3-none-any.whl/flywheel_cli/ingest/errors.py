"""Ingest related exceptions"""
# pylint: disable=C0111,R0903
import typing


class BaseError(Exception):
    """Base exception"""
    message: str = "Unknown exception"

    def __init__(self, msg: typing.Optional[str] = None):
        super().__init__(msg or self.message)


class WorkerShutdownTimeout(BaseError):
    message: str = "Worker shutdown grace period exceeded"


class WorkerForcedShutdown(BaseError):
    message: str = "Forced worker to shutdown immediatly without waiting the grace period"


class AuthenticationError(BaseError):
    """Authentication failed"""
    message: str = "Authentication error"
    code = 403

    def __init__(self, msg: str, code: typing.Optional[int] = None):
        super().__init__(msg)
        if code:
            self.code = code


class InvalidDeidProfile(BaseError):
    """Deid Profile Exception"""
    message: str = "Invalid deid profile"
    errors = None

    def __init__(self, msg: str, errors: typing.Optional[typing.List[str]] = None):
        super().__init__(msg)
        self.message = msg
        self.errors = errors

    def __str__(self):
        msg = self.message
        if self.errors:
            msg += f" ({' '.join(self.errors)})"
        return msg


class IngestIsNotDeletable(BaseError):
    """Deid Profile Exception"""
    message: str = "Could not delete ingest"


class BaseIngestError:
    code: str = "UNKNOWN"
    message: str = "Unknown error"
    description: str = None

    def __init__(self, code: typing.Optional[str] = None):
        if code:
            self.code = code


class DuplicateFilepathInUploadSet(BaseIngestError):
    code = "DD01"
    message = "File Path Conflict in Upload Set"


class DuplicateFilepathInFlywheel(BaseIngestError):
    code = "DD02"
    message = "File Path Conflict in Flywheel"


class DifferentStudyInstanceUID(BaseIngestError):
    code = "DD03"
    message = "Different StudyInstanceUIDs in session"


class DuplicatedStudyInstanceUID(BaseIngestError):
    code = "DD04"
    message = "Duplicate StudyInstanceUID in Container"


class DuplicatedStudyInstanceUIDInContainers(BaseIngestError):
    code = "DD05"
    message = "StudyInstanceUID in Multiple Containers"


class StudyInstanceUIDExists(BaseIngestError):
    code = "DD06"
    message = "Duplicate StudyInstanceUID in Flywheel - UID Already Exists"


class DuplicatedSeriesInstanceUID(BaseIngestError):
    code = "DD07"
    message = "Duplicate SeriesInstanceUID in Container"


class DuplicatedSeriesInstanceUIDInContainers(BaseIngestError):
    code = "DD08"
    message = "SeriesInstanceUID in Multiple Containers"


class DifferentSeriesInstanceUID(BaseIngestError):
    code = "DD09"
    message = "Different SeriesInstanceUIDs in session"


class SeriesInstanceUIDExists(BaseIngestError):
    code = "DD10"
    message = "Duplicate SeriesInstanceUID in Flywheel - UID Already Exists"


class DuplicatedSOPInstanceUID(BaseIngestError):
    code = "DD11"
    message = "Duplicate SOPInstanceUID in Series"


class InvalidSourcePath(BaseIngestError):
    code = "SC01"
    message = "Invalid source path"


class InvalidDicomFile(BaseIngestError):
    code = "SC02"
    message = "Invalid DICOM - missing UID tag"


class ZeroByteFile(BaseIngestError):
    code = "SC03"
    message = "Zero byte file"


def get_error_by_code(code: str):
    errors_map = {cls.code: cls for cls in BaseIngestError.__subclasses__()}
    error_cls = errors_map.get(code)
    if not error_cls:
        # pass requested error code to help debugging
        return BaseIngestError(code=code)
    return error_cls()
