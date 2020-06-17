import datetime
from unittest import mock
from uuid import uuid4

import pytest

from .conftest import DummyWalker
from flywheel_cli.ingest import config, errors
from flywheel_cli.ingest import models as M
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.client import db as ingest_db_client
from flywheel_cli.ingest.tasks.extract_uid import ExtractUIDTask


@pytest.fixture(scope="function")
def extract_task(db):
    ingest = db.create_ingest()
    item = db.create_item(
        files=["file1.dcm", "file.txt"],
        files_cnt=2,
        context={"session": {"label": "session_label"}, "acquisition": {"label": "acquisition_label"}}
    )
    task = db.create_task(
        type="extract_uid",
        item_id=item.id,
        ingest_id=ingest.id
    )

    extract_task = ExtractUIDTask(
        db=db.client,
        task=task.schema(),
        worker_config=config.WorkerConfig()
    )

    return extract_task


@pytest.fixture(scope="function")
def mocked_extract_task():
    task = T.TaskOut(
        type='extract_uid',
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        retries=0,
        history=[],
        created=datetime.datetime.now()
    )

    spec = dir(ingest_db_client.DBClient)
    spec.extend([
        "get_item",
        "batch_writer_insert_uid",
        "batch_writer_insert_error",
        "batch_writer_update_item",
        "update_task",
        "batch_writer_update_container"
    ])

    db = mock.Mock(spec=spec)
    db.get_item.return_value = T.ItemOut(
        id=uuid4(),
        ingest_id=uuid4(),
        type="file",
        files=[],
        files_cnt=2,
        bytes_sum=2,
        dir="dir"
    )

    extract_task = ExtractUIDTask(
        db=db,
        task=task,
        worker_config=config.WorkerConfig()
    )

    return extract_task


def test_run_insert_error(extract_task):
    extract_task.walker = DummyWalker(["file1.dcm"])
    extract_task._run()

    d = extract_task.db.sessionmaker()
    uids = d.query(M.UID)
    assert uids.count() == 0
    errs = d.query(M.Error)
    assert errs.count() == 1
    error = errs.all()[0]
    d.close()

    assert error.code == errors.InvalidDicomFile.code
    assert error.filepath == "file1.dcm"
    assert error.task_id == extract_task.task.id


def test_run_insert_uid(mocker, extract_task, attr_dict):
    dicom_mock = mocker.patch("flywheel_cli.ingest.tasks.extract_uid.DicomFile")
    dicom_mock.return_value = attr_dict({
        "SeriesInstanceUID": "uid1",
        "StudyInstanceUID": "uid2",
        "SOPInstanceUID": "uid3",
        "AcquisitionNumber": "12"
    })
    extract_task.walker = DummyWalker(["file1.dcm"])
    extract_task._run()

    d = extract_task.db.sessionmaker()
    uids = d.query(M.UID)
    assert uids.count() == 1
    uid = uids.all()[0]
    item = d.query(M.Item).all()[0]
    d.close()

    assert uid.study_instance_uid == 'uid2'
    assert uid.series_instance_uid == 'uid1'
    assert uid.sop_instance_uid == 'uid3'
    assert uid.acquisition_number == '12'
    assert uid.filename == "file1.dcm"
    assert uid.item_id == extract_task.task.item_id

    assert item.context["session"]["uid"] == "uid2"
    assert item.context["acquisition"]["uid"] == "uid1_12"


def test_run_success(mocked_extract_task):
    mocked_extract_task.run()

    mocked_extract_task.db.update_task.assert_called_once_with(
        mocked_extract_task.task.id,
        status=T.TaskStatus.completed
    )
    mocked_extract_task.db.start_resolving.assert_called_once()


def test_run_error(mocked_extract_task):
    class TestException(Exception):
        pass

    mocked_extract_task.db.get_item.side_effect = TestException("test error")
    mocked_extract_task.run()

    mocked_extract_task.db.fail.assert_called_once()


def test_scan_dicom_file_partial(mocker, attr_dict, mocked_extract_task):
    dicom_mock = mocker.patch("flywheel_cli.ingest.tasks.extract_uid.DicomFile")
    dicom_mock.return_value = attr_dict({
        "StudyInstanceUID": "uid2",
        "SeriesInstanceUID": "uid3",
    })

    result = mocked_extract_task._scan_dicom_file(mock.Mock(), [], "path", uuid4())
    assert isinstance(result, T.Error)
    assert result.code == errors.InvalidDicomFile.code
    assert result.message == "Skipped file path because of missing sop_instance_uid"
