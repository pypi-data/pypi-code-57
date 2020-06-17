import datetime
from unittest import mock
from uuid import uuid4

import pytest

from flywheel_cli.ingest.client.db import DBClient
from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import scan


@pytest.fixture(scope="function")
def scan_task():
    task = T.TaskOut(
        type="scan",
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now(),
        context={
            "scanner": {
                "type": "filename",
                "dir": "/tmp",
                "opts": {}
            }
        }
    )
    db_spec = dir(DBClient)
    db_spec.extend([
        "batch_writer_insert_item",
        "batch_writer_insert_task",
        "batch_writer_insert_uid",
        "batch_writer_insert_error",
        "update_task",
        "batch_writer_update_container",
    ])
    mock.Mock(spec=db_spec)

    scan_task = scan.ScanTask(
        db=mock.Mock(spec=db_spec),
        task=task,
        worker_config=config.WorkerConfig()
    )

    scan_task.ingest_config = config.IngestConfig(
        src_fs="/tmp"
    )

    return scan_task


def test_run_insert_item(mocker, scan_task):
    scanner = DummyScanner(
        return_values=[
            T.ItemIn(
                dir="dir",
                type="file",
                files_cnt=1,
                bytes_sum=1,
                files=["file1"]
            )
        ]
    )

    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", return_value=scanner)
    scan_task._initialize()
    scan_task._run()

    scan_task.insert_items.push.assert_called_once_with(
        scanner.return_values[0].dict()
    )
    scan_task.insert_tasks.push.assert_not_called()
    scan_task.insert_items.flush.assert_called_once()


def test_run_insert_task(mocker, scan_task):
    scanner = DummyScanner(
        return_values=[
            T.TaskIn(
                type="scan",
            )
        ]
    )

    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", return_value=scanner)
    scan_task._initialize()
    scan_task._run()

    scan_task.insert_items.push.assert_not_called()
    scan_task.insert_tasks.push.assert_called_once_with(
        scanner.return_values[0].dict()
    )

    scan_task.insert_items.flush.assert_called_once()


def test_run_unexpected_type_raise(mocker, scan_task):
    scanner = DummyScanner(
        return_values=[
            T.StatusCount()
        ]
    )
    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", return_value=scanner)
    scan_task._initialize()
    with pytest.raises(ValueError):
        scan_task._run()


def test_run_success(mocker, scan_task):
    scanner = DummyScanner(return_values=[])
    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", return_value=scanner)
    scan_task.run()

    scan_task.db.update_task.assert_called_once_with(
        scan_task.task.id,
        status=T.TaskStatus.completed
    )
    scan_task.db.start_resolving.assert_called_once()


def test_run_error(mocker, scan_task):
    class TestException(Exception):
        pass

    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", side_effect=TestException("test error"))
    scan_task.run()

    scan_task.db.fail.assert_called_once()


def test_run_with_extract_uid(mocker, scan_task):
    id_ = uuid4()

    item_with_uids = T.ItemWithUIDs(
        item=T.ItemIn(
            id=id_,
            dir="dir",
            type="file",
            files_cnt=1,
            bytes_sum=1,
            files=["file1"]
        ),
        uids=[]
    )
    item_with_uids.uids.append(
        T.UIDIn(
            item_id=item_with_uids.item.id,
            study_instance_uid="study_instance_uid",
            series_instance_uid="series_instance_uid",
            sop_instance_uid="sop_instance_uid",
            filename="filename"
        )
    )
    scanner = DummyScanner(return_values=[item_with_uids])
    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", return_value=scanner)
    scan_task.task.context = {
        "scanner": {
            "type": "dicom",
            "dir": "/tmp",
            "opts": {}
        }
    }
    scan_task.ingest_config.detect_duplicates = True

    scan_task._initialize()
    scan_task._run()

    scan_task.insert_uids.push.assert_called_once_with({
        "item_id": id_,
        "filename": "filename",
        "study_instance_uid": "study_instance_uid",
        "series_instance_uid": "series_instance_uid",
        "sop_instance_uid": "sop_instance_uid"
    })
    scan_task.insert_tasks.push.assert_not_called()

def test_run_create_extract_uid_task(mocker, scan_task):
    id_ = uuid4()
    scanner = DummyScanner(
        return_values=[
            T.ItemIn(
                id=id_,
                dir="dir",
                type="file",
                files_cnt=1,
                bytes_sum=1,
                files=["file1"]
            )
        ]
    )
    mocker.patch("flywheel_cli.ingest.tasks.scan.create_scanner", return_value=scanner)
    scan_task.ingest_config.detect_duplicates = True

    scan_task._initialize()
    scan_task._run()

    scan_task.insert_tasks.push.assert_called_once_with(
        T.TaskIn(
            type="extract_uid",
            item_id=id_
        )
    )
    scan_task.insert_uids.push.assert_not_called()

class DummyScanner():
    def __init__(self, return_values):
        self.return_values = return_values

    def scan(self, _):
        for r_val in self.return_values:
            yield r_val
