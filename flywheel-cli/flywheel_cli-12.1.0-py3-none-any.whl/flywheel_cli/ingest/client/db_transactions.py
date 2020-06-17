"""Transactions for the DBClient"""
# pylint: disable=W0143

import re
import time
import typing
from uuid import UUID

import sqlalchemy as sqla
from sqlalchemy.orm import Query, Session

from .. import errors
from .. import models as M
from .. import schemas as T


# Transactional crud methods

def add(db: Session, model: M.Base) -> T.Schema:
    """Add an object"""
    db.add(model)
    db.flush()
    return model.schema()


def get(db: Session, model_cls: typing.Type[M.Base], id_: UUID) -> T.Schema:
    """Get object by ID"""
    return db.query(model_cls).filter(model_cls.id == id_).one().schema()


def get_all(db: Session, query: Query, schema: T.Schema) -> typing.List[T.Schema]:
    """Get all object that match the given query"""
    return [schema.from_orm(model) for model in query.with_session(db).all()]


def count_all(db: Session, ingest_id: UUID, model_cls: typing.Type[M.Base]) -> int:
    """Get count of row for the specified model"""
    return (
        db.query(sqla.sql.func.count(model_cls.id).label("count"))
        .filter(model_cls.ingest_id == ingest_id)
        .scalar()
    )


def update(db: Session, model_cls: M.Base, id_: UUID, **updates: typing.Any) -> T.Schema:
    """Update an object with the given update set"""
    model = db.query(model_cls).filter(model_cls.id == id_).one()
    model.update(**updates)
    db.flush()
    return model.schema()


def find_one(db: Session, model_cls: M.Base, *conditions: typing.Any) -> T.Schema:
    """Find one matching row for the given model."""
    query = db.query(model_cls)
    for condition in conditions:
        query = query.filter(condition)
    return query.one().schema()


def bulk(db: Session, operation: str, model_cls: M.Base, mappings: typing.List) -> None:
    """Perform a bulk insert/update of the given list of mapping dictionaries"""
    assert operation in ("insert", "update")

    # TODO revisit layer separation - this is clearly needed for performance,
    # but at the same time completely bypasses both pydantic and the orm...
    # Also, tests randomly use the client and the transaction layer.
    # NOTE below are 2 redundant copies of the orm status init default and
    # timestamp+history population mechanics SANS VALIDATION
    if model_cls is M.Task:
        timestamp = time.time()
        for mapping in mappings:
            if operation == "insert":
                status = mapping.setdefault("status", "pending")
                mapping.setdefault("timestamp", timestamp)
                mapping.setdefault("history", [(status, timestamp)])
            if operation == "update" and "status" in mapping:
                mapping.setdefault("timestamp", timestamp)
                mapping.setdefault("history", [(mapping["status"], timestamp)])

    bulk_method = getattr(db, f"bulk_{operation}_mappings")
    bulk_method(model_cls, mappings)
    db.flush()


def start(db: Session, ingest_id: UUID) -> T.IngestOut:
    """Start the ingest, set ingest status to scanning and kick off
    the initial template scan task.

    Lock on the ingest row until the transaction ends to prevent starting
    multiple initial scan tasks.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    assert ingest.status == T.IngestStatus.created
    ingest.status = T.IngestStatus.scanning
    db.add(M.Task(
        ingest_id=ingest_id,
        type=T.TaskType.scan,
        context={"scanner": {"type": "template", "dir": "/"}},
    ))
    db.flush()
    return ingest.schema()


def review(
    db: Session, ingest_id: UUID, changes: typing.Optional[T.ReviewIn] = None
) -> T.IngestOut:
    """Save review and start preparing, set ingest status to preparing and kick off
    the prepare task.

    Lock on the ingest row until the transaction ends to prevent starting multiple
    prepare tasks.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    assert ingest.status == T.IngestStatus.in_review
    ingest.status = T.IngestStatus.preparing
    if changes is not None:
        for change in changes:
            db.add(M.Review(ingest_id=ingest_id, **change.dict()))
    db.add(M.Task(
        ingest_id=ingest_id,
        type=T.TaskType.prepare,
    ))
    db.flush()
    return ingest.schema()


def abort(db: Session, ingest_id: UUID) -> T.IngestOut:
    """Abort the ingest, set ingest status to aborted and cancel all pending
    tasks.

    Lock on the ingest row until the transaction ends to prevent setting ingest/tasks
    statuses multiple times.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    if ingest.status == T.IngestStatus.aborted:
        return ingest.schema()
    ingest.status = T.IngestStatus.aborted
    _cancel_pending_tasks(db, ingest_id)
    db.flush()
    return ingest.schema()


def next_task(db: Session, worker: str) -> typing.Optional[T.TaskOut]:
    """Get next task which's status is pending and set the status to running.

    Lock on the first task that match and skip any locked ones. This prevents the
    workers to grab the same task.
    """
    query = _for_update(
        db.query(M.Task).filter(M.Task.status == T.TaskStatus.pending),
        skip_locked=True,
    )
    task = query.first()
    if task is None:
        return None
    task.worker = worker
    task.status = T.TaskStatus.running
    db.flush()
    return task.schema()


def get_progress(db: Session, ingest_id: UUID) -> T.Progress:
    """Get ingest scan task and item/file/byte counts by status"""
    progress = T.Progress().dict()
    scan_tasks_by_status = (
        db.query(
            M.Task.status,
            sqla.sql.func.count(M.Task.id).label("count"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
            sqla.or_(M.Task.type == T.TaskType.scan, M.Task.type == T.TaskType.extract_uid)
        )
        .group_by(M.Task.status)
    )
    for row in scan_tasks_by_status:
        progress["scans"][row.status] = row.count
        progress["scans"]["total"] += row.count
        if T.TaskStatus.is_terminal(row.status):
            progress["scans"]["finished"] += row.count

    tasks_by_type = (
        db.query(
            M.Task.type,
            sqla.sql.func.sum(M.Task.completed).label("completed"),
            sqla.sql.func.sum(M.Task.total).label("total"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
        )
        .group_by(M.Task.type)
    )
    for row in tasks_by_type:
        progress["stages"][T.TaskType.ingest_status(row.type)]["completed"] = row.completed
        progress["stages"][T.TaskType.ingest_status(row.type)]["total"] = row.total

    tasks_subq = (
        sqla.orm.Query([
            M.Task.item_id,
            M.Task.status
        ])
        .filter(M.Task.ingest_id == ingest_id, M.Task.type == T.TaskType.upload)
        .subquery()
    )

    items_by_status = (
        db.query(
            tasks_subq.c.status,
            M.Item.skipped,
            sqla.sql.func.count(M.Item.id).label("items"),
            sqla.sql.func.sum(M.Item.files_cnt).label("files"),
            sqla.sql.func.sum(M.Item.bytes_sum).label("bytes"),
        )
        .outerjoin(tasks_subq, M.Item.id == tasks_subq.c.item_id)  # pylint: disable=E1101
        .filter(M.Item.ingest_id == ingest_id)
        .group_by(tasks_subq.c.status, M.Item.skipped)
    )
    for row in items_by_status.all():
        if row.skipped:
            # items skipped via review tracked separately
            status = "skipped"
        elif row.status is None:
            # items that don't have any (upload task) status yet
            status = "scanned"
        else:
            # items with an upload task tracked as the task status
            status = row.status

        for attr in ("items", "files", "bytes"):
            progress[attr][status] = getattr(row, attr)
            progress[attr]["total"] += getattr(row, attr)
            if T.TaskStatus.is_terminal(status):
                progress[attr]["finished"] += getattr(row, attr)
    return T.Progress(**progress)


def get_summary(db: Session, ingest_id: UUID) -> T.Summary:
    """Get ingest hierarchy node and file count by level and type"""
    summary = {}
    containers_by_level = (
        db.query(
            M.Container.level,
            sqla.sql.func.count(M.Container.id).label("count"))
        .filter(M.Container.ingest_id == ingest_id)
        .group_by(M.Container.level)
    )
    for row in containers_by_level.all():
        level_name = T.ContainerLevel.get_item(row.level).name
        summary[f"{level_name}s"] = row.count
    items_by_type = (
        db.query(
            M.Item.type,
            sqla.sql.func.count(M.Item.id).label("count"))
        .filter(M.Item.ingest_id == ingest_id)
        .group_by(M.Item.type)
    )
    for row in items_by_type.all():
        summary[f"{row.type}s"] = row.count
    errors_by_type = (
        db.query(
            M.Error.code,
            sqla.sql.func.count(M.Error.id).label("count")
        )
        .filter(M.Error.ingest_id == ingest_id)
        .group_by(M.Error.code)
    )
    for row in errors_by_type.all():
        error = errors.get_error_by_code(row.code)
        summary.setdefault("errors", []).append({
            "code": error.code,
            "message": error.message,
            "description": error.description,
            "count": row.count,
        })
    return T.Summary(**summary)


def get_report(db: Session, ingest_id: UUID) -> T.Report:
    """Get ingest status, elapsed time per status and list of failed tasks"""
    ingest = _get_ingest(db, ingest_id)
    elapsed = {}
    for old, new in zip(ingest.history, ingest.history[1:]):
        old_status, old_timestamp = old
        new_status, new_timestamp = new  # pylint: disable=W0612
        elapsed[old_status] = new_timestamp - old_timestamp
    task_errors_query = (
        db.query(
            M.Task.id.label("task"),  # pylint: disable=E1101
            M.Task.type,
            M.Error.code,
            M.Error.message,
            M.Error.filepath,
        )
        .join(M.Task.errors)  # pylint: disable=E1101
        .filter(M.Task.ingest_id == ingest_id)
        .order_by(M.Task.created)
    )
    task_errors = []
    for error in task_errors_query.all():
        message = error.message or errors.get_error_by_code(error.code).message
        if error.filepath:
            message = f"{error.filepath}: {message}"
        task_errors.append(T.TaskError(
            task=error.task,
            type=error.type,
            code=error.code,
            message=message,
        ))
    return T.Report(
        status=ingest.status,
        elapsed=elapsed,
        errors=task_errors,
    )


def start_singleton(db: Session, ingest_id: UUID, type_: T.TaskType) -> T.IngestOut:
    """
    Start singleton task (resolve, finalize). Lock on the ingest row until the
    transaction ends to prevent strating singletons multiple times.
    """
    # all scan tasks finished - lock the ingest
    ingest = _get_ingest(db, ingest_id, for_update=True)
    # set status and add scan task (once - noop for 2nd worker)
    if ingest.status != T.TaskType.ingest_status(type_) and not T.IngestStatus.is_terminal(ingest.status):
        ingest.status = T.TaskType.ingest_status(type_)
        db.add(M.Task(ingest_id=ingest_id, type=type_))
        db.flush()
    return ingest.schema()


def has_unfinished_tasks(db: Session, ingest_id: UUID) -> bool:
    """Return true if there are penging/running tasks otherwise false"""
    # pylint: disable=no-member
    pending_or_running = (
        db.query(M.Task.id)
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.status.in_([T.TaskStatus.pending, T.TaskStatus.running])
        )
    )
    return bool(pending_or_running.count())


def has_running_tasks(db: Session, ingest_id: UUID) -> bool:
    """Return true if there are penging/running tasks otherwise false"""
    # pylint: disable=no-member
    running = (
        db.query(M.Task.id)
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.status.in_([T.TaskStatus.running])
        )
    )
    return bool(running.count())


def resolve_subject(db: Session, ingest_id: UUID, map_values: typing.List[str]) -> str:
    """Get existing or create new subject code based on the map values"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    subject = (
        db.query(M.Subject)
        .filter(
            M.Subject.ingest_id == ingest_id,
            M.Subject.map_values == map_values,
        )
        .first()
    )
    if subject is None:
        subject_config = ingest.config["subject_config"]
        subject_config["code_serial"] += 1
        sqla.orm.attributes.flag_modified(ingest, "config")
        subject = M.Subject(
            ingest_id=ingest_id,
            code=subject_config["code_format"].format(
                SubjectCode=subject_config["code_serial"]
            ),
            map_values=map_values,
        )
        db.add(subject)
        db.flush()
    return subject.code


def set_ingest_status(db: Session, ingest_id: UUID, status: T.IngestStatus) -> T.IngestOut:
    """Set ingest status"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    if ingest.status != status:
        ingest.status = status
        db.flush()
    return ingest.schema()


def fail_ingest(db: Session, ingest_id: UUID) -> T.IngestOut:
    """Set ingest status to failed and cancel pending tasks"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    ingest.status = T.IngestStatus.failed
    _cancel_pending_tasks(db, ingest_id)
    db.flush()
    return ingest.schema()


def load_subject_csv(db: Session, ingest_id: UUID, subject_csv: typing.BinaryIO) -> None:
    """
    Load subject codes from csv file.
    Lock on the ingest row to prevent mixing different subject configs.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    subject_config = ingest.config.setdefault("subject_config", {})
    header = subject_csv.readline().decode("utf8").strip()
    code_format, *map_keys = header.split(",")
    if subject_config:
        assert map_keys == subject_config["map_keys"]
    else:
        subject_config["code_format"] = code_format
        subject_config["map_keys"] = map_keys
    subject_config.setdefault("code_serial", 0)

    code_re = re.compile(r"^[^\d]*(\d+)[^\d]*$")
    for line in subject_csv:
        subject = line.decode("utf8").strip()
        code, *map_values = subject.split(",")
        match = code_re.match(code)
        if not match:
            raise ValueError(f"Invalid code in subject csv: {code}")
        code_int = int(match.group(1))
        if code_int > subject_config["code_serial"]:
            subject_config["code_serial"] = code_int
        # NOTE all subjects in memory
        db.add(M.Subject(
            ingest_id=ingest_id,
            code=code,
            map_values=map_values,
        ))
    sqla.orm.attributes.flag_modified(ingest, "config")
    db.flush()


def delete_ingest(db: Session, ingest_id: UUID) -> None:
    """Delete an ingest and all related records"""

    # delete Subject, DeidLog, Review
    _delete(db, M.Subject, M.Subject.ingest_id == ingest_id)
    _delete(db, M.DeidLog, M.DeidLog.ingest_id == ingest_id)
    _delete(db, M.Review, M.Review.ingest_id == ingest_id)

    # execution order is important from now on because of the foreign keys
    _delete(db, M.Task, M.Task.ingest_id == ingest_id)
    _delete(db, M.Item, M.Item.ingest_id == ingest_id)

    # deletion in reverse ContainerLevel order (parent-child relations)
    _delete(db, M.Container, sqla.and_(
        M.Container.ingest_id == ingest_id,
        M.Container.level == T.ContainerLevel.acquisition
    ))
    _delete(db, M.Container, sqla.and_(
        M.Container.ingest_id == ingest_id,
        M.Container.level == T.ContainerLevel.session
    ))
    _delete(db, M.Container, sqla.and_(
        M.Container.ingest_id == ingest_id,
        M.Container.level == T.ContainerLevel.subject
    ))
    _delete(db, M.Container, sqla.and_(
        M.Container.ingest_id == ingest_id,
        M.Container.level == T.ContainerLevel.project
    ))
    _delete(db, M.Container, sqla.and_(
        M.Container.ingest_id == ingest_id,
        M.Container.level == T.ContainerLevel.group
    ))

    _delete(db, M.Ingest, M.Ingest.id == ingest_id)


# Detect duplicates

def one_container_multiple_uid_item_ids(db: Session, ingest_id: UUID, uid_container: str, uid_type: str) -> typing.Set[UUID]:
    """Get Item IDs where 1 container has different UIDs"""
    sub_query = (
        db.query(
            getattr(M.UID, uid_container),
            sqla.sql.func.count(getattr(M.UID, uid_type).distinct()).label("count")
        )
        .filter(M.UID.ingest_id == ingest_id)
        .group_by(getattr(M.UID, uid_container))
        .subquery()
    )
    query = (
        db.query(
            M.Item.id
        )
        .select_from(sub_query)
        .join(M.Item, M.Item.container_id == getattr(sub_query.columns, uid_container))
        .filter(sub_query.columns.count > 1)
    )

    results = query.all()
    item_ids = set()
    for row in results:
        item_ids.add(row[0])

    return item_ids


def one_uid_multiple_session_container_item_ids(db: Session, ingest_id: UUID, uid_container: str, uid_type: str) -> typing.Set[UUID]:
    """Get Item IDs where 1 UID exists in multiple containers"""

    sub_query = (
        db.query(
            getattr(M.UID, uid_type),
            sqla.sql.func.count(getattr(M.UID, uid_container).distinct()).label("count")
        )
        .filter(M.UID.ingest_id == ingest_id)
        .group_by(getattr(M.UID, uid_type))
        .subquery()
    )
    query = (
        db.query(
            M.UID.item_id
        )
        .select_from(sub_query)
        .join(M.UID, getattr(M.UID, uid_type) == getattr(sub_query.columns, uid_type))
        .filter(sub_query.columns.count > 1)
    )

    results = query.all()
    item_ids = set()
    for row in results:
        item_ids.add(row[0])

    return item_ids


def uids_in_new_session_container(db: Session, ingest_id: UUID, uid_container: str, uid_type: str) -> typing.Set[str]:
    """Get StudyInstanceUIDs where the session containers in new"""

    # pylint: disable=C0121
    query = (
        db.query(
            getattr(M.UID, uid_type)
        )
        .join(M.Container, M.Container.id == getattr(M.UID, uid_container))
        .filter(M.UID.ingest_id == ingest_id, M.Container.existing == False)
        .group_by(getattr(M.UID, uid_type))
    )

    results = query.all()

    uids = set()
    for row in results:
        uids.add(row[0])

    return uids


def duplicated_sop_instance_uid_item_ids(db: Session, ingest_id: UUID) -> typing.Set[UUID]:
    """Get Item IDs with duplicated SOPInstanceUIDs"""

    sub_query = (
        db.query(
            M.UID.sop_instance_uid,
            sqla.sql.func.count(M.UID.id).label("count")
        )
        .filter(M.UID.ingest_id == ingest_id)
        .group_by(M.UID.sop_instance_uid)
        .subquery()
    )
    query = (
        db.query(
            M.UID.item_id
        )
        .select_from(sub_query)
        .join(M.UID, M.UID.sop_instance_uid == sub_query.columns.sop_instance_uid)
        .filter(sub_query.columns.count > 1)
    )

    results = query.all()
    item_ids = set()
    for row in results:
        item_ids.add(row[0])

    return item_ids


# Helpers

def _get_ingest(db: Session, ingest_id: UUID, for_update: bool = False) -> M.Ingest:
    """Get ingest by ID and locks on it if requested"""
    query = db.query(M.Ingest).filter(M.Ingest.id == ingest_id)
    if for_update:
        query = _for_update(query)
    return query.one()


def _for_update(query: Query, skip_locked: bool = False) -> Query:
    """Lock as granularly as possible for given query and backend"""
    # with_for_update() locks selected rows in postgres
    # (ignored w/ sqlite - there we use a multiprocessing lock)
    # skip_locked silently skips over records that are currently locked
    # populate_existing to get objects with the latest modifications
    # see: https://github.com/sqlalchemy/sqlalchemy/issues/4774
    return query.with_for_update(skip_locked=skip_locked).populate_existing()


def _cancel_pending_tasks(db: Session, ingest_id: UUID) -> None:
    """Cancel all pending tasks"""
    pending_tasks = _for_update(db.query(M.Task).filter(
        M.Task.ingest_id == ingest_id,
        M.Task.status == T.TaskStatus.pending,
    ))
    for task in pending_tasks:
        task.status = T.TaskStatus.canceled


def _delete(db: Session, model: M.Base, *conditions):
    """Delete DB records without fetching them"""
    return db.execute(model.__table__.delete().where(*conditions))
