# pylint: disable=too-few-public-methods
"""Pydantic ingest input and output schemas"""
import datetime
import enum
import typing
import uuid

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from . import config


class Schema(BaseModel):
    """Common base configured to play nice with sqlalchemy"""
    class Config:
        """Enable .from_orm() to load fields from attrs"""
        orm_mode = True


class Enum(enum.Enum):
    """Extended Enum with easy item lookup by instance, name or value"""
    @classmethod
    def get_item(cls, info: typing.Any) -> "Enum":
        """Return enum item for given instance, name or value"""
        for item in cls:
            if info in (item, item.name, item.value):
                return item
        raise ValueError(f"Invalid {cls.__name__} {info}")

    @classmethod
    def has_item(cls, info: typing.Any) -> bool:
        """Return True if info is a valid enum instance, name or value"""
        try:
            cls.get_item(info)
        except ValueError:
            return False
        return True


class Status(Enum):
    """Status enum with transition validation and terminality check"""

    @staticmethod
    def transitions():
        """Define allowed status transitions"""
        raise NotImplementedError

    @classmethod
    def validate_transition(cls, old, new) -> None:
        """Raise ValueError if old -> new is not a valid status transition"""
        old = cls.get_item(old).value if old else None
        new = cls.get_item(new).value
        if old and new not in cls.transitions()[old]:
            # NOTE allowing any status transition from old=None facilitates tests
            raise ValueError(f"Invalid {cls.__name__} transition {old} -> {new}")

    @classmethod
    def is_terminal(cls, info) -> bool:
        """Return True if 'has_item(info)' and the status has no transitions"""
        if cls.has_item(info):
            status = cls.get_item(info).value
            return cls.transitions()[status] == set()
        return False


class FWAuth(BaseModel):
    """Flywheel site and user info model"""
    api_key: str
    host: str
    user: str
    is_admin: bool


# Ingests

class IngestStatus(str, Status):
    """Ingest status"""
    created = "created"
    scanning = "scanning"
    resolving = "resolving"
    detecting_duplicates = "detecting_duplicates"
    in_review = "in_review"
    preparing = "preparing"
    uploading = "uploading"
    finalizing = "finalizing"
    finished = "finished"
    failed = "failed"
    aborted = "aborted"

    @staticmethod
    def transitions():
        """Define allowed transitions"""
        return {
            None: {"created"},
            "created": {"scanning", "aborted"},
            "scanning": {"resolving", "failed", "aborted"},
            "resolving": {"detecting_duplicates", "in_review", "failed", "aborted"},
            "detecting_duplicates": {"in_review", "failed", "aborted"},
            "in_review": {"preparing", "aborted"},
            "preparing": {"uploading", "failed", "aborted"},
            "uploading": {"finalizing", "failed", "aborted"},
            "finalizing": {"finished", "failed", "aborted"},
            "finished": set(),
            "failed": set(),
            "aborted": set(),
        }


class IngestInAPI(Schema):
    """Ingest input schema for API"""
    config: config.IngestConfig
    strategy_config: config.StrategyConfig


class BaseIngestOut(Schema):
    """Base ingest output schema"""
    id: uuid.UUID
    label: str
    fw_host: str
    fw_user: str
    config: config.IngestConfig
    strategy_config: config.StrategyConfig
    status: IngestStatus
    history: typing.List[typing.Tuple[IngestStatus, int]]
    created: datetime.datetime


class IngestOutAPI(BaseIngestOut):
    """Ingest output schema for API"""


class IngestOut(BaseIngestOut):
    """Ingest output schema w/ api-key"""
    api_key: str


# Tasks

class TaskType(str, Enum):
    """Task type enum"""
    scan = "scan"
    extract_uid = "extract_uid"
    resolve = "resolve"  # singleton
    detect_duplicates = "detect_duplicates"  # singleton
    prepare = "prepare"  # singleton
    upload = "upload"
    finalize = "finalize"  # singleton

    @classmethod
    def ingest_status(cls, info) -> IngestStatus:
        """Get the associated ingest status of a task type"""
        status = cls.get_item(info).value
        task_type_ingest_status_map = {
            "scan": IngestStatus.scanning,
            "extract_uid": IngestStatus.scanning,
            "resolve": IngestStatus.resolving,
            "detect_duplicates": IngestStatus.detecting_duplicates,
            "prepare": IngestStatus.preparing,
            "upload": IngestStatus.uploading,
            "finalize": IngestStatus.finalizing,
        }
        return task_type_ingest_status_map[status]


class TaskStatus(str, Status):
    """Task status enum"""
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    canceled = "canceled"

    @staticmethod
    def transitions():
        """Define allowed transitions"""
        return {
            None: {"pending"},
            "pending": {"running", "canceled"},  # cancel via ingest fail/abort
            "running": {"completed", "pending", "failed"},  # retry to pending
            "completed": set(),
            "failed": set(),  # NOTE this will get trickier with user retries
            "canceled": set(),
        }


class TaskIn(Schema):
    """Task input schema"""
    type: TaskType
    item_id: typing.Optional[uuid.UUID]
    context: typing.Optional[dict]
    status: TaskStatus = TaskStatus.pending


class TaskOut(TaskIn):
    """Task output schema"""
    id: uuid.UUID
    ingest_id: uuid.UUID
    status: TaskStatus
    history: typing.List[typing.Tuple[TaskStatus, int]]
    worker: typing.Optional[str]
    error: typing.Optional[str]
    created: datetime.datetime
    retries: int
    completed: typing.Optional[int] = 0  # completed work unit
    total: typing.Optional[int] = 0  # total number of work unit


# Containers

class ContainerLevel(int, Enum):
    """Container level enum (int for simple ordering)"""
    group = 0
    project = 1
    subject = 2
    session = 3
    acquisition = 4


class ContainerIn(Schema):
    """Container input schema"""
    id: uuid.UUID
    parent_id: typing.Optional[uuid.UUID]
    path: str
    level: ContainerLevel
    src_context: dict
    dst_context: typing.Optional[dict]
    dst_path: typing.Optional[str]
    existing: typing.Optional[bool] = False
    error: typing.Optional[bool] = False


class ContainerOut(ContainerIn):
    """Container output schema"""
    id: uuid.UUID
    ingest_id: uuid.UUID
    files_cnt: typing.Optional[int]
    bytes_sum: typing.Optional[int]


# Items

class ItemType(str, Enum):
    """Ingest item type enum"""
    file = "file"
    packfile = "packfile"


class Error(Schema):
    """Item error schema"""
    item_id: typing.Optional[uuid.UUID]
    task_id: typing.Optional[uuid.UUID]
    filepath: typing.Optional[str]
    code: str
    message: typing.Optional[str]


class BaseItem(Schema):
    """Base ingest item schema"""
    container_id: typing.Optional[uuid.UUID]
    dir: str
    type: ItemType
    files: typing.List[str]
    filename: typing.Optional[str]
    files_cnt: int
    bytes_sum: int
    context: typing.Optional[dict]


class ItemIn(BaseItem):
    """Ingest item input schema"""
    id: typing.Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)


class ItemOut(BaseItem):
    """Ingest item output schema"""
    id: uuid.UUID
    ingest_id: uuid.UUID
    container_id: typing.Optional[uuid.UUID]
    existing: typing.Optional[bool]
    skipped: typing.Optional[bool]


class ItemWithContainerPath(Schema):
    """Ingest item with container path for detect duplicates task"""
    id: uuid.UUID
    dir: str
    filename: str
    existing: typing.Optional[bool]
    container_path: typing.Optional[str]


class ItemWithErrorCount(Schema):
    """Ingest item with error count for prepare task"""
    id: uuid.UUID
    existing: typing.Optional[bool]
    error_cnt: int = 0
    container_error: typing.Optional[bool]
    container_path: typing.Optional[str]


# Ingest stats

class StageCount(Schema):
    """Work unit completed/total counts"""
    completed: int = 0
    total: int = 0


class StageProgress(Schema):
    """Work unit counts by ingest status"""
    scanning: StageCount = StageCount()
    resolving: StageCount = StageCount()
    detecting_duplicates: StageCount = StageCount()
    preparing: StageCount = StageCount()
    uploading: StageCount = StageCount()
    finalizing: StageCount = StageCount()


class StatusCount(Schema):
    """Counts by status"""
    scanned: int = 0
    pending: int = 0
    running: int = 0
    failed: int = 0
    canceled: int = 0
    completed: int = 0
    skipped: int = 0
    finished: int = 0
    total: int = 0


class Progress(Schema):
    """Ingest progress with scan task and import- item/file/byte counts by status"""
    scans: StatusCount = StatusCount()
    items: StatusCount = StatusCount()
    files: StatusCount = StatusCount()
    bytes: StatusCount = StatusCount()
    stages: StageProgress = StageProgress()


class ErrorSummary(Schema):
    """Ingest error summary"""
    code: str
    message: str
    description: typing.Optional[str]
    count: int


class Summary(Schema):
    """Ingest scan summary with hierarchy node and file counts"""
    groups: int = 0
    projects: int = 0
    subjects: int = 0
    sessions: int = 0
    acquisitions: int = 0
    files: int = 0
    packfiles: int = 0
    errors: typing.Optional[typing.List[ErrorSummary]]


class TaskError(Schema):
    """Ingest task error"""
    task: uuid.UUID
    type: TaskType
    code: str
    message: str


class Report(Schema):
    """Final ingest report with status, elapsed times and list of errors"""
    status: IngestStatus
    elapsed: typing.Dict[IngestStatus, int]
    errors: typing.List[TaskError]


# Review

class ReviewChange(Schema):
    """Review change"""
    path: str
    skip: typing.Optional[bool]
    context: typing.Optional[dict]


ReviewIn = typing.List[ReviewChange]


# Logs

class AuditLogOut(Schema):
    """Audit log output schema"""
    id: uuid.UUID
    dir: str
    filename: str
    src_path: typing.Optional[str]
    dst_path: typing.Optional[str]
    existing: typing.Optional[bool]
    skipped: typing.Optional[bool]
    status: typing.Optional[TaskStatus]
    error_code: typing.Optional[str]
    error_message: typing.Optional[str]
    container_error: typing.Optional[bool]


class DeidLogIn(Schema):
    """Deid log input schema"""
    src_path: str
    tags_before: dict
    tags_after: dict


class DeidLogOut(DeidLogIn):
    """De-id log output schema"""
    id: uuid.UUID
    created: datetime.datetime


class SubjectOut(Schema):
    """Subject output schema"""
    code: str
    map_values: typing.List[str]


# UID

class UIDIn(Schema):
    """UID input schema"""
    item_id: uuid.UUID
    filename: str
    study_instance_uid: str
    series_instance_uid: str
    sop_instance_uid: str
    acquisition_number: typing.Optional[str]
    session_container_id: typing.Optional[uuid.UUID]
    acquisition_container_id: typing.Optional[uuid.UUID]


class UIDOut(UIDIn):
    """UID output schema"""
    id: uuid.UUID


class ItemWithUIDs(Schema):
    """Ingest item with UIDs"""
    item: ItemIn
    uids: typing.List[UIDIn]



class DetectDuplicateItem(Schema):
    """DetectDuplicateItem used in find_all_item_with_uid to return lightweight objects"""
    id: uuid.UUID
    item_id: uuid.UUID
    session_container_id: typing.Optional[uuid.UUID]
    acquisition_container_id: typing.Optional[uuid.UUID]


# Others

class ReportETA(Schema):
    """ETA report schema"""
    eta: int
    report_time: int
    finished: int
    total: int

class ContainerID(Schema):
    """Container ID for Item"""
    id: uuid.UUID
    container_id: uuid.UUID
