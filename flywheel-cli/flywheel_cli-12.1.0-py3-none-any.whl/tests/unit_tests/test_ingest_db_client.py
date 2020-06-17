import datetime
import inspect
import io
import os
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sqla
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from flywheel_cli.ingest import config, errors
from flywheel_cli.ingest import models as M
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.client import db as ingest_db_client, db_transactions
from flywheel_cli.ingest.errors import IngestIsNotDeletable


def test_create_from_url():
    client = ingest_db_client.DBClient.from_url("sqlite:///:memory:")

    assert isinstance(client, ingest_db_client.DBClient)
    assert client.url == "sqlite:///:memory:"
    assert client._ingest_id is None


def test_create_from_url_with_uuid():
    uuid = uuid4()
    client = ingest_db_client.DBClient.from_url("sqlite:///:memory:", uuid)

    assert isinstance(client, ingest_db_client.DBClient)
    assert client.url == "sqlite:///:memory:"
    assert client._ingest_id == uuid


def test_create_sqlite():
    client = ingest_db_client.DBClient("sqlite:///:memory:")
    assert client.engine.name == "sqlite"
    assert client.check_connection()


def test_check_connection_fail():
    client = ingest_db_client.DBClient("sqlite:///:memory:")
    assert client.engine.name == "sqlite"
    client.engine = None
    assert not client.check_connection()


def test_create_pg():
    client = ingest_db_client.DBClient("postgresql://user:pass@localhost:1234/db")
    assert client.engine.name == "postgresql"
    assert not client.check_connection()


def test_create_ingest(db):
    ingest = db.client.create_ingest(
        config.IngestConfig(src_fs="/tmp"),
        config.FolderConfig(),
        T.FWAuth(
            api_key="api_key",
            host="flywheel.test",
            user="test@flywheel.test",
            is_admin=True,
        ),
    )

    assert isinstance(ingest, T.IngestOutAPI)
    assert isinstance(ingest.id, UUID)
    assert isinstance(ingest.created, datetime.datetime)
    assert ingest.status == "created"
    assert ingest.config.src_fs == "/tmp"
    assert ingest.fw_host == "flywheel.test"
    assert ingest.fw_user == "test@flywheel.test"
    assert db.client.ingest == ingest


def test_get_ingests_empty(db):
    assert list(db.client.list_ingests()) == []


def test_get_ingests(db):
    ingest_1 = db.create_ingest()
    ingest_2 = db.create_ingest()

    ingests = db.client.list_ingests()
    assert inspect.isgenerator(ingests)
    ingests = list(ingests)
    assert len(ingests) == 2
    assert {ingest.id for ingest in ingests} == {ingest_1.id, ingest_2.id}


def test_get_ingest_nonexistent_id(db):
    db.client.bind(uuid4())
    with pytest.raises(NoResultFound):
        db.client.ingest


def test_get_ingest(db):
    ingest = db.create_ingest()
    assert db.client.ingest.id == ingest.id


def test_start_ingest(db):
    db.create_ingest()

    ingest = db.client.start()
    assert ingest.status == "scanning"
    assert len(list(db.client.get_all_task(M.Task.type == T.TaskType.scan))) == 1


def test_set_ingest_status(db):
    db.create_ingest()

    ingest = db.client.set_ingest_status("scanning")
    assert ingest.status == "scanning"
    ingest = db.client.set_ingest_status("failed")
    assert ingest.status == "failed"


def test_set_ingest_status_invalid(db):
    db.create_ingest()
    db.client.set_ingest_status("scanning")

    with pytest.raises(ValueError):
        db.client.set_ingest_status("created")


def test_set_ingest_status_idempotent(db):
    db.create_ingest()

    ingest = db.client.set_ingest_status("scanning")
    assert ingest.status == "scanning"
    ingest = db.client.set_ingest_status("scanning")
    assert ingest.status == "scanning"


def test_abort_ingest(db):
    db.create_ingest()

    ingest = db.client.abort()

    assert ingest.status == "aborted"
    last_history = ingest.history[-1]
    assert last_history[0] == "aborted"
    # abort idempotent
    ingest = db.client.abort()
    assert last_history == ingest.history[-1]


def test_next_task_none(db):
    task = db.client.next_task("worker")
    assert task is None


def test_next_task(db):
    db.create_task(
        status="running", worker="worker",
    )
    task_pending = db.create_task(status="pending", worker="worker",)

    task = db.client.next_task("worker")
    assert task.id == task_pending.id


# Ingest-bound methods


def test_load_subject_csv(db):
    db.create_ingest(
        config={
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": [],
            }
        }
    )

    f = io.BytesIO(b"code-{SubjectCode}\ncode-1,code_a\ncode-2,code_b\n")
    db.client.load_subject_csv(f)
    subjects = list(db.client.subjects)
    assert subjects == ["code-{SubjectCode}\n", "code-1,code_a\n", "code-2,code_b\n"]


def test_status_transitions(db):
    db.create_ingest()
    assert db.client.ingest.status == "created"

    db.client.start()
    assert db.client.ingest.status == "scanning"

    db.client.set_ingest_status("resolving")
    assert db.client.ingest.status == "resolving"

    db.client.set_ingest_status("in_review")
    assert db.client.ingest.status == "in_review"

    db.client.review()
    assert db.client.ingest.status == "preparing"

    db.client.abort()
    assert db.client.ingest.status == "aborted"


def test_progress(db):
    db.create_task(
        status="completed", completed=100, total=100,
    )
    db.create_task(
        status="failed", completed=55, total=99,
    )
    db.create_task(
        status="running", type="prepare", completed=55, total=100,
    )
    item = db.create_item(bytes_sum=99)
    db.create_task(
        status="running", type="upload", item_id=item.id,
    )

    progress = db.client.progress
    assert progress.scans.total == 2
    assert progress.scans.completed == 1
    assert progress.scans.failed == 1
    assert progress.items.running == 1
    assert progress.items.total == 1
    assert progress.files.total == 1
    assert progress.bytes.total == 99
    assert progress.stages.scanning.completed == 155
    assert progress.stages.scanning.total == 199
    assert progress.stages.preparing.completed == 55
    assert progress.stages.preparing.total == 100


def test_summary(db):
    path = ""
    for level in T.ContainerLevel:
        path = os.path.join(path, level.name)
        for i in range(level + 1):
            db.create_container(level=level, path=path if not i else f"{path}_{str(i)}")
    item = db.create_item()
    error = errors.DuplicateFilepathInFlywheel
    db.create_error(item_id=item.id, code=error.code)
    db.create_error(item_id=item.id, code=error.code)

    summary = db.client.summary
    assert summary.groups == 1
    assert summary.projects == 2
    assert summary.subjects == 3
    assert summary.sessions == 4
    assert summary.acquisitions == 5
    assert len(summary.errors) == 1
    assert summary.errors[0].code == error.code
    assert summary.errors[0].message == error.message
    assert summary.errors[0].description == error.description
    assert summary.errors[0].count == 2


def test_report(db):
    task = db.create_task(status="failed",)
    db.create_error(
        task_id=task.id, code="UNKNOWN", message="foo bar error",
    )
    db.client.start()

    report = db.client.report
    assert report.status == "scanning"
    assert "created" in report.elapsed
    assert isinstance(report.elapsed["created"], int)
    assert len(report.errors) == 1
    assert report.errors[0].code == "UNKNOWN"
    assert report.errors[0].message == "foo bar error"


def test_tree(db):
    db.create_container(path="b", src_context={"_id": "b"})
    db.create_container(path="a", src_context={"_id": "a"})
    db.create_container(
        level=1, path="b/c", src_context={"label": "c"},
    )
    db.create_container(
        level=1, path="a/d", src_context={"label": "d"},
    )
    tree = list(db.client.tree)
    assert len(tree) == 4
    assert tree[0].level == 0
    assert tree[0].path == "a"
    assert tree[0].src_context["_id"] == "a"
    assert tree[1].level == 1
    assert tree[1].path == "a/d"
    assert tree[1].src_context["label"] == "d"
    assert tree[2].level == 0
    assert tree[2].path == "b"
    assert tree[2].src_context["_id"] == "b"
    assert tree[3].level == 1
    assert tree[3].path == "b/c"
    assert tree[3].src_context["label"] == "c"


def test_audit_logs(db):
    item_1 = db.create_item()
    item_2 = db.create_item(dir="/dir2", filename="file2", existing=True,)
    db.create_item(
        dir="/dir3", filename="file3", existing=True, skipped=True,
    )
    item_4 = db.create_item(dir="/dir4", filename="file4", skipped=True, existing=True,)
    item_5 = db.create_item(dir="/dir5", filename="file5")
    unknown_error = errors.BaseIngestError
    dup_fw_error = errors.DuplicateFilepathInFlywheel
    dup_upload_set_error = errors.DuplicateFilepathInUploadSet
    db.create_error(
        item_id=item_4.id, code=dup_upload_set_error.code,
    )
    db.create_error(
        item_id=item_4.id, code=dup_fw_error.code,
    )
    db.create_error(
        item_id=item_5.id, code=unknown_error.code, message="Foo bar error message",
    )
    db.create_task(status="completed", type="upload", item_id=item_1.id)
    db.create_task(status="failed", type="upload", item_id=item_2.id)
    db.create_task(status="failed", type="upload", item_id=item_5.id)
    # test that only upload task errors are visible in audit logs
    task = db.create_task(status="failed", type="extract_uid", item_id=item_5.id)
    db.create_error(
        task_id=task.id, code=unknown_error.code, message="Extract uid error",
    )

    container = db.create_container(path="b", src_context={"_id": "b"}, error=True)
    item_6 = db.create_item(dir="/dir6", filename="file6", container_id=container.id)
    logs = list(db.client.audit_logs)

    assert logs == [
        "src_path,dst_path,status,existing,error_code,error_message\n",
        "/tmp/dir/file,dst/file,completed,False,,\n",
        "/tmp/dir2/file2,dst/file2,failed,True,UNKNOWN,Unknown error\n",
        "/tmp/dir3/file3,dst/file3,skipped,True,,\n",
        "/tmp/dir4/file4,dst/file4,skipped,True,DD01,File Path Conflict in Upload Set\n",
        "/tmp/dir4/file4,dst/file4,skipped,True,DD02,File Path Conflict in Flywheel\n",
        "/tmp/dir5/file5,dst/file5,failed,False,UNKNOWN,Foo bar error message\n",
        '/tmp/dir6/file6,dst/file6,skipped,False,UNKNOWN,Skipped due to erroneous parent container\n'
    ]


def test_deid_logs(db):
    db.create_ingest(
        config={
            "deid_profile": "minimal",
            "deid_profiles": [
                {
                    "name": "minimal",
                    "description": "Dsc",
                    "dicom": {
                        "fields": [
                            {"name": "PatientBirthDate", "remove": True},
                            {"name": "PatientName", "remove": True},
                            {"name": "PatientID", "remove": False},
                        ]
                    },
                }
            ],
            "de_identify": True,
        },
    )

    db.create_deid_log(
        src_path="src_path",
        tags_before={
            "StudyInstanceUID": "b1",
            "SeriesInstanceUID": "b2",
            "SOPInstanceUID": "b3",
            "PatientBirthDate": "b4",
            "PatientName": "b5",
            "PatientID": "b6",
        },
        tags_after={
            "StudyInstanceUID": "a1",
            "SeriesInstanceUID": "a2",
            "SOPInstanceUID": "a3",
            "PatientID": "a6",
        },
    )

    logs = list(db.client.deid_logs)

    assert logs == [
        "src_path,type,StudyInstanceUID,SeriesInstanceUID,SOPInstanceUID,PatientBirthDate,PatientName,PatientID\n",
        "src_path,before,b1,b2,b3,b4,b5,b6\n",
        "src_path,after,a1,a2,a3,,,a6\n",
    ]


def test_subjects(db):
    db.create_ingest(
        config={
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": [],
            },
        },
    )
    db.create_subject(code="code-1", map_values=["code_a"])
    subjects = list(db.client.subjects)
    assert subjects == ["code-{SubjectCode}\n", "code-1,code_a\n"]


def test_api_key(db):
    db.create_ingest()
    assert db.client.api_key == "flywheel.test:admin-apikey"


def test_add(db):
    db.create_ingest()
    task = T.TaskIn(type="scan")
    _task = db.client.add(task)
    assert _task.id is not None


def test_get(db):
    ingest = db.create_ingest()
    task_orig = db.create_task(status="failed")

    task = db.client.get_task(task_orig.id)
    assert task.id == task_orig.id
    assert task.ingest_id == ingest.id
    assert task.status == "failed"


def test_get_all(db):
    task_1 = db.create_task(status="failed")
    task_2 = db.create_task(status="failed")

    # TODO conditions test
    tasks = list(db.client.get_all("Task"))
    assert len(tasks) == 2
    for task in tasks:
        assert task.id in [task_1.id, task_2.id]


def test_update(db):
    ingest = db.create_ingest()
    task_orig = db.create_task()

    task = db.client.get_task(task_orig.id)
    assert task.id == task_orig.id
    assert task.ingest_id == ingest.id
    assert task.status == "pending"

    task = db.client.update_task(task_orig.id, status="running")
    assert task.id == task_orig.id
    assert task.ingest_id == ingest.id
    assert task.status == "running"


def test_bulk_insert(db):
    db.create_ingest()
    mappings = [
        {"status": "pending", "type": "scan"},
        {"status": "failed", "type": "scan"},
    ]

    db.client.bulk("insert", "Task", mappings)
    tasks = list(db.client.get_all("Task"))
    assert len(tasks) == 2
    for task in tasks:
        assert task.status in ["pending", "failed"]


def test_bulk_update(db):
    task_1 = db.create_task()
    task_2 = db.create_task(status="running")

    mappings = [
        {"id": task_1.id, "status": "failed",},
        {"id": task_2.id, "status": "failed",},
    ]

    db.client.bulk("update", "Task", mappings)
    tasks = list(db.client.get_all("Task"))
    assert len(tasks) == 2
    for task in tasks:
        assert task.status == "failed"


def test_start_resolving_has_unfinished_task(db):
    ingest_orig = db.create_ingest()
    db.client.start()
    db.create_task()

    ingest = db.client.start_resolving()
    assert ingest.id == ingest_orig.id
    assert ingest.status == "scanning"


def test_start_resolving(db):
    ingest_orig = db.create_ingest()
    db.client.start()

    for task in db.client.get_all("Task"):
        db.client.update_task(task.id, status="running")
        db.client.update_task(task.id, status="completed")

    ingest = db.client.start_resolving()
    assert ingest.id == ingest_orig.id
    assert ingest.status == "resolving"


def test_resolve_subject_existing(db):
    db.create_ingest(
        config={
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": [],
            },
        },
    )
    db.create_subject(code="code-1", map_values=["code_a"])

    subject = db.client.resolve_subject(["code_a"])
    subjects_csv = list(db.client.subjects)
    assert subject == "code-1"
    assert len(subjects_csv) == 2  # header and one row


def test_resolve_subject_non_existing(db):
    db.create_ingest(
        config={
            "subject_config": {
                "code_serial": 1,
                "code_format": "code-{SubjectCode}",
                "map_keys": [],
            },
        },
    )
    subject = db.client.resolve_subject(["code_a"])
    assert subject == "code-2"


def test_start_finalizing(db):
    ingest_orig = db.create_ingest()
    db.client.start()

    for task in db.client.get_all_task():
        db.client.update_task(task.id, status="running")
        db.client.update_task(task.id, status="completed")

    db.client.set_ingest_status("resolving")
    db.client.set_ingest_status("in_review")
    db.client.set_ingest_status("preparing")
    db.client.set_ingest_status("uploading")

    ingest = db.client.start_finalizing()
    assert ingest.id == ingest_orig.id
    assert ingest.status == "finalizing"


def test_fail(db):
    ingest_orig = db.create_ingest()
    db.client.start()

    ingest = db.client.fail()
    assert ingest.id == ingest_orig.id
    assert ingest.status == "failed"


def test_batch_writer_push(db):
    ingest_orig = db.create_ingest()
    task_orig = db.create_task(status="pending")

    batch_writer = db.client.batch_writer_update_tasks(batch_size=1)
    batch_writer.push({"id": task_orig.id, "status": "running"})

    task = db.client.get_task(task_orig.id)
    assert task.id == task_orig.id
    assert task.ingest_id == ingest_orig.id
    assert task.status == "running"


def test_batch_writer_flush(db):
    ingest_orig = db.create_ingest()
    task_orig = db.create_task()

    batch_writer = db.client.batch_writer(
        operation="update", model_name="Task", batch_size=10
    )
    batch_writer.push({"id": task_orig.id, "status": "running"})

    task = db.client.get_task(task_orig.id)
    assert task.id == task_orig.id
    assert task.ingest_id == ingest_orig.id
    assert task.status == "pending"

    batch_writer.flush()

    task = db.client.get_task(task_orig.id)
    assert task.id == task_orig.id
    assert task.ingest_id == ingest_orig.id
    assert task.status == "running"


def test_batch_writer_flush_depends_on(db):
    task_1 = db.create_task()
    task_2 = db.create_task()

    batch_writer_1 = db.client.batch_writer(
        operation="update", model_name="Task", batch_size=10
    )
    batch_writer_1.push({"id": task_1.id, "status": "running"})

    batch_writer_2 = db.client.batch_writer(
        operation="update", model_name="Task", batch_size=10, depends_on=batch_writer_1
    )
    batch_writer_2.push({"id": task_2.id, "status": "running"})

    task = db.client.get_task(task_1.id)
    assert task.status == "pending"
    task = db.client.get_task(task_2.id)
    assert task.status == "pending"

    batch_writer_2.flush()

    task = db.client.get_task(task_1.id)
    assert task.status == "running"
    task = db.client.get_task(task_2.id)
    assert task.status == "running"


def test_batch_writer_flush_depends_on_other_side(db):
    task_1 = db.create_task()
    task_2 = db.create_task()

    batch_writer_1 = db.client.batch_writer(
        operation="update", model_name="Task", batch_size=10
    )
    batch_writer_1.push({"id": task_1.id, "status": "running"})

    batch_writer_2 = db.client.batch_writer(
        operation="update", model_name="Task", batch_size=10, depends_on=batch_writer_1
    )
    batch_writer_2.push({"id": task_2.id, "status": "running"})

    task = db.client.get_task(task_1.id)
    assert task.status == "pending"
    task = db.client.get_task(task_2.id)
    assert task.status == "pending"

    batch_writer_1.flush()

    task = db.client.get_task(task_1.id)
    assert task.status == "running"
    task = db.client.get_task(task_2.id)
    assert task.status == "pending"

    batch_writer_2.flush()

    task = db.client.get_task(task_1.id)
    assert task.status == "running"
    task = db.client.get_task(task_2.id)
    assert task.status == "running"


def test_batch_writer_via_attribute(db):
    db.create_ingest()

    batch_writer = db.client.batch_writer_update_task()
    assert batch_writer.operation == "update"
    assert batch_writer.model_name == "Task"


def test_unknown_attribute(db):
    with pytest.raises(AttributeError):
        db.client.random_attr()


def test_iter_query(db):
    ingest = db.create_ingest()

    mappings = []
    for i in range(20):
        mappings.append(
            {
                "level": 1,
                "src_context": {},
                "ingest_id": ingest.id,
                "path": "path" + str(i),
            }
        )
    db_transactions.bulk(db.session, "insert", M.Container, mappings)
    db.session.commit()

    model_cls = M.Container
    order_by = ingest_db_client._get_paginate_order_by_col(model_cls)
    query = sqla.orm.Query(model_cls).filter(model_cls.ingest_id == ingest.id)

    ids = []
    for t in db.client._iter_query(query, [order_by], model_cls.schema_cls(), 5):
        if str(t.id) not in ids:
            ids.append(str(t.id))

    assert len(ids) == len(mappings)
    db.session.commit()


def test_delete_ingest_status_raise(db):
    ingest = db.create_ingest()

    with pytest.raises(IngestIsNotDeletable):
        db.client.delete_ingest(ingest.id)


def test_delete_ingest_running_tasks_raise(db):
    ingest = db.create_ingest(status="scanning")
    db.create_task(status="running")

    db_transactions.update(db.session, M.Ingest, ingest.id, status="failed")
    db.session.commit()

    with pytest.raises(IngestIsNotDeletable):
        db.client.delete_ingest(ingest.id)


def test_delete_ingest_full(db):
    def gen_data():
        for i in range(3):
            db.create_container()
            db.create_item()
            db.create_task()
            db.create_subject(code=f"code-{i}", map_values=[f"code-{i}"])
            db.create_deid_log()
            db.create_review()

    ingest_1 = db.create_ingest()
    gen_data()
    ingest_2 = db.create_ingest()
    gen_data()

    db.client.abort()

    assert db.session.query(M.Subject.id).count() == 6
    assert db.session.query(M.DeidLog.id).count() == 6
    assert db.session.query(M.Review.id).count() == 6
    assert db.session.query(M.Container.id).count() == 6  # 10 + 2 for tasks
    assert db.session.query(M.Task.id).count() == 6
    assert db.session.query(M.Item.id).count() == 6

    db.client.delete_ingest(ingest_2.id)

    subjects = db.session.query(M.Subject)
    assert subjects.count() == 3

    deid_logs = db.session.query(M.DeidLog)
    assert deid_logs.count() == 3

    reviews = db.session.query(M.Review)
    assert reviews.count() == 3

    containers = db.session.query(M.Container)
    assert containers.count() == 3

    tasks = db.session.query(M.Task)
    assert tasks.count() == 3
    for task in tasks.all():
        assert task.ingest_id == ingest_1.id

    items = db.session.query(M.DeidLog)
    assert items.count() == 3
    for item in items.all():
        assert item.ingest_id == ingest_1.id

    ingests = db.session.query(M.Ingest)
    assert ingests.count() == 1
    assert ingests.all()[0].id == ingest_1.id

    db.session.commit()


def test_get_items_sorted_by_dst_path(db):
    container_1 = db.create_container(path="group/project_a", level=1,)
    container_2 = db.create_container(path="group/project_b", level=1,)
    item_1 = db.create_item(
        id=UUID("00000000-0000-0000-0000-000000000003"),
        filename="a.txt",
        container_id=container_2.id,
    )
    item_2 = db.create_item(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        filename="a.txt",
        container_id=container_2.id,
    )
    item_3 = db.create_item(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        filename="b.txt",
        container_id=container_1.id,
    )
    items = list(db.client.get_items_sorted_by_dst_path())
    assert items[0].id == item_3.id
    assert items[0].container_path == "group/project_a"
    assert items[0].filename == "b.txt"
    assert items[1].id == item_2.id
    assert items[1].container_path == "group/project_b"
    assert items[1].filename == "a.txt"
    assert items[2].id == item_1.id
    assert items[2].container_path == "group/project_b"
    assert items[2].filename == "a.txt"


def test_count_all(db):
    for _ in range(11):
        db.create_item()

    assert db.client.count_all_item() == 11


def test_find_one_ingest_dependent(db):
    db.create_container(path="group")
    db.create_ingest()
    container_2 = db.create_container(path="group")

    container = db.client.find_one_container(M.Container.path == "group")
    assert container.id == container_2.id


def test_find_one_multiple_results(db):
    db.create_container(path="group")
    db.create_container(path="group")

    with pytest.raises(MultipleResultsFound):
        db.client.find_one_container(M.Container.path == "group")


def test_find_one_no_result(db):
    db.create_ingest()

    with pytest.raises(NoResultFound):
        db.client.find_one_container(M.Container.path == "non_existent")


def test_get_items_with_error_count(db):
    ingest1 = db.create_ingest()
    ingest2 = db.create_ingest()
    container_1 = db.create_container(path="group/project_a", level=1, error=True)
    container_2 = db.create_container(path="group/project_b", level=1)
    container_3 = db.create_container(path="group/project_c", level=1, ingest_id=ingest1.id)
    item_1 = db.create_item(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        filename="a.txt",
        container_id=container_1.id,
        existing=True
    )
    item_2 = db.create_item(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        filename="b.txt",
        container_id=container_2.id,
    )
    item_3 = db.create_item(
        id=UUID("00000000-0000-0000-0000-000000000003"),
        filename="b.txt",
        container_id=container_3.id,
        ingest_id=ingest1.id
    )
    db.create_error(
        item_id=item_1.id, code=1,
    )
    db.create_error(
        item_id=item_1.id, code=2,
    )
    db.create_error(
        item_id=item_3.id, code=1,
    )

    items = list(db.client.get_items_with_error_count())
    assert len(items) == 2

    for item in items:
        if item.id == item_1.id:
            assert item.existing
            assert item.error_cnt == 2
            assert item.container_error
            assert item.container_path == "group/project_a"
        else:
            assert not item.existing
            assert item.error_cnt == 0
            assert not item.container_error
            assert item.container_path == "group/project_b"

def test_correct_sop_instace_uids(db):
    db.create_ingest()
    container1 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid2", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid3", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid4", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid5", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid6", session_container_id=container2.id)


    item_ids = db.client.duplicated_sop_instance_uid_item_ids()
    assert len(item_ids) == 0


def test_duplicated_sop_instace_uids(db):
    db.create_ingest()
    container1 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid2", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, sop_instance_uid="uid3", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid1", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid5", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, sop_instance_uid="uid6", session_container_id=container2.id)


    item_ids = db.client.duplicated_sop_instance_uid_item_ids()
    assert set(item_ids) == set([item1.id, item2.id])


def create_uid(db, **kwargs):
    kwargs.setdefault("study_instance_uid", str(uuid4()))
    kwargs.setdefault("series_instance_uid", str(uuid4()))
    kwargs.setdefault("sop_instance_uid", str(uuid4()))
    kwargs.setdefault("filename", "file1")

    return db.create_uid(**kwargs)
