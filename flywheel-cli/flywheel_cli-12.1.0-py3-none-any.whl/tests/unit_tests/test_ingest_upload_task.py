import datetime
import io
import tempfile
import zipfile
from unittest import mock
from uuid import uuid4

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import upload


@pytest.fixture(scope="function")
def create_walker_mock(mocker):
    create_walker_mock = mocker.patch("flywheel_cli.ingest.config.IngestConfig.create_walker")
    file_mock = mock.MagicMock()
    file_mock.__enter__.return_value = io.BytesIO()

    def remove_prefix(subdir, path):
        if path.startswith(subdir):
            path = path[len(subdir):]
        return path.lstrip("/")

    create_walker_mock.return_value.remove_prefix.side_effect = remove_prefix
    create_walker_mock.return_value.open.return_value = file_mock
    return create_walker_mock

@pytest.fixture(scope="function")
def upload_task_with_walker_mock(create_walker_mock):
    task = T.TaskOut(
        type="upload",
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now(),
        item_id=uuid4(),
    )
    cfg = config.WorkerConfig()
    db_mock = mock.Mock()
    db_mock.api_key = "api_key"

    upload_task_with_walker_mock = upload.UploadTask(
        db=db_mock,
        task=task,
        worker_config=cfg
    )
    upload_task_with_walker_mock.walker = create_walker_mock()
    upload_task_with_walker_mock.ingest_config = config.IngestConfig(src_fs="src_fs")

    return upload_task_with_walker_mock

def test_create_packfile_tempfile(attr_dict, upload_task_with_walker_mock):
    upload_task_with_walker_mock.worker_config = config.WorkerConfig(
        max_tempfile=0
    )

    ctx = attr_dict({
        "packfile": {
            "type": "zip"
        }
    })

    tmpfile, _ = upload_task_with_walker_mock.create_packfile(
        context=ctx,
        filename="filename",
        files=["file1", "file2"],
        subdir="subdir"
    )

    assert isinstance(tmpfile, type(tempfile.TemporaryFile()))

    upload_task_with_walker_mock.worker_config = config.WorkerConfig(
        max_tempfile=10
    )

    tmpfile, _ = upload_task_with_walker_mock.create_packfile(
        context=ctx,
        filename="filename",
        files=["file1", "file2"],
        subdir=None
    )

    assert isinstance(tmpfile, type(tempfile.SpooledTemporaryFile()))


def test_create_packfile_wo_subdir(attr_dict, upload_task_with_walker_mock):
    ctx = attr_dict({
        "packfile": {
            "type": "zip"
        }
    })

    tempfile, metadata = upload_task_with_walker_mock.create_packfile(
        context=ctx,
        filename="filename",
        files=["path1/file1.dicom", "path2/file2.dicom"],
        subdir=None
    )

    zip_file = zipfile.ZipFile(tempfile)
    assert set(zip_file.namelist()) == {
        'path1/',
        'path2/',
        'path1/file1.dicom',
        'path2/file2.dicom'
    }

    calls = [
        mock.call("path1/file1.dicom", "rb"),
        mock.call("path2/file2.dicom", "rb")
    ]
    upload_task_with_walker_mock.walker.open.assert_has_calls(calls, any_order=True)
    upload_task_with_walker_mock.walker.remove_prefix.assert_not_called()

    assert metadata == {
        "name": "filename",
        "zip_member_count": 2,
        "type": "zip"
    }


def test_create_packfile_w_subdir(attr_dict, upload_task_with_walker_mock):
    ctx = attr_dict({
        "packfile": {
            "type": "zip"
        }
    })

    tempfile, metadata = upload_task_with_walker_mock.create_packfile(
        context=ctx,
        filename="filename",
        files=["path/file1.dicom", "file2.dicom"],
        subdir="subdir"
    )

    zip_file = zipfile.ZipFile(tempfile)
    assert set(zip_file.namelist()) == {
        'path/',
        'path/file1.dicom',
        'file2.dicom'
    }

    calls = [
        mock.call("subdir/path/file1.dicom", "rb"),
        mock.call("subdir/file2.dicom", "rb")
    ]
    upload_task_with_walker_mock.walker.open.assert_has_calls(calls, any_order=True)

    calls = [
        mock.call("subdir", "subdir/path/file1.dicom"),
        mock.call("subdir", "subdir/file2.dicom")
    ]
    upload_task_with_walker_mock.walker.remove_prefix.assert_has_calls(calls, any_order=True)

    assert metadata == {
        "name": "filename",
        "zip_member_count": 2,
        "type": "zip"
    }


def test_create_packfile_flatten(attr_dict, upload_task_with_walker_mock):
    ctx = attr_dict({
        "packfile": {
            "type": "zip",
            "flatten": True
        }
    })

    tempfile, metadata = upload_task_with_walker_mock.create_packfile(
        context=ctx,
        filename="filename",
        files=["path/file1.dicom", "file2.dicom"],
        subdir=None
    )

    zip_file = zipfile.ZipFile(tempfile)
    assert set(zip_file.namelist()) == {
        'file1.dicom',
        'file2.dicom'
    }

    calls = [
        mock.call("path/file1.dicom", "rb"),
        mock.call("file2.dicom", "rb")
    ]
    upload_task_with_walker_mock.walker.open.assert_has_calls(calls, any_order=True)
    upload_task_with_walker_mock.walker.remove_prefix.assert_not_called()

    assert metadata == {
        "name": "filename",
        "zip_member_count": 2,
        "type": "zip"
    }


def test_initialize_wo_deid(upload_task_with_walker_mock):
    upload_task_with_walker_mock.ingest_config = config.IngestConfig(
        src_fs="src_fs"
    )
    upload_task_with_walker_mock._initialize()

    assert upload_task_with_walker_mock.deid_profile is None


def test_initialize_w_deid(upload_task_with_walker_mock):
    upload_task_with_walker_mock.ingest_config = config.IngestConfig(
        src_fs="src_fs",
        deid_profile="minimal",
        deid_profiles=[{
            "name": "minimal",
            "description": "Dsc",
            "dicom": {
                "fields": [
                    {"name": "PatientBirthDate", "remove": True},
                    {"name": "PatientName", "remove": True},
                    {"name": "PatientID", "remove": False}
                ]
            }
        }],
        de_identify=True
    )
    upload_task_with_walker_mock._initialize()

    assert upload_task_with_walker_mock.deid_profile is not None
    assert upload_task_with_walker_mock.deid_profile.name == "minimal"


def test_run_packfile(mocker, upload_task_with_walker_mock):
    get_sdk_client_mock = mocker.patch("flywheel_cli.ingest.utils.get_sdk_client")

    setup_upload_task_with_walker_mock(
        upload_task_with_walker_mock=upload_task_with_walker_mock,
        get_item=T.ItemOut(
            id=uuid4(),
            dir="dir",
            type="packfile",
            files=["file1", "file2"],
            files_cnt=2,
            bytes_sum=2,
            ingest_id=uuid4(),
            context={"packfile": {"type": "zip"}},
            container_id=uuid4(),
            filename="filename"
        ),
        get_container=T.ContainerOut(
            id=uuid4(),
            level=0,
            path="label_value",
            src_context={"label": "label_value"},
            dst_context={"_id": "id_val"},
            ingest_id=uuid4()
        )
    )

    upload_task_with_walker_mock._run()

    get_sdk_client_mock.assert_called_once_with("api_key")
    get_sdk_client_mock.return_value.upload.assert_called_once_with(
        "group",
        "id_val",
        "filename",
        TempFileObject,
        {
            "name": "filename",
            "zip_member_count": 2,
            "type": "zip"
        }
    )


def test_run_single_file(mocker, upload_task_with_walker_mock):
    get_sdk_client_mock = mocker.patch("flywheel_cli.ingest.utils.get_sdk_client")
    setup_upload_task_with_walker_mock(upload_task_with_walker_mock)
    file_mock = io.BytesIO()
    upload_task_with_walker_mock.walker.open.return_value = file_mock

    upload_task_with_walker_mock._run()

    get_sdk_client_mock.assert_called_once_with("api_key")
    get_sdk_client_mock.return_value.upload.assert_called_once_with(
        "group",
        "id_val",
        "file",
        file_mock,
        None
    )

def test_run_success(mocker, upload_task_with_walker_mock):
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client")

    setup_upload_task_with_walker_mock(upload_task_with_walker_mock)

    upload_task_with_walker_mock.ingest_config = config.IngestConfig(
        src_fs="src_fs"
    )

    upload_task_with_walker_mock.run()

    upload_task_with_walker_mock.db.update_task.assert_called_once_with(
        upload_task_with_walker_mock.task.id,
        status=T.TaskStatus.completed
    )
    upload_task_with_walker_mock.db.start_finalizing.assert_called_once()


def test_run_error(mocker, upload_task_with_walker_mock):
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", side_effect=Exception())

    setup_upload_task_with_walker_mock(upload_task_with_walker_mock)

    upload_task_with_walker_mock.ingest_config = config.IngestConfig(
        src_fs="src_fs",
        max_retries=3
    )

    upload_task_with_walker_mock.run()

    upload_task_with_walker_mock.db.update_task.assert_called_once_with(
        upload_task_with_walker_mock.task.id,
        status=T.TaskStatus.pending,
        retries=1
    )
    upload_task_with_walker_mock.db.start_finalizing.assert_not_called()

def test_run_error_fail(mocker, upload_task_with_walker_mock):
    class TestException(Exception):
        pass

    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", side_effect=TestException("test error"))

    setup_upload_task_with_walker_mock(upload_task_with_walker_mock)
    upload_task_with_walker_mock.task.retries = 3

    upload_task_with_walker_mock.ingest_config = config.IngestConfig(
        src_fs="src_fs",
        max_retries=3
    )

    upload_task_with_walker_mock.run()

    upload_task_with_walker_mock.db.start_finalizing.assert_called_once()


def setup_upload_task_with_walker_mock(upload_task_with_walker_mock, get_item=None, get_container=None):
    db_mock = upload_task_with_walker_mock.db

    container_id = uuid4()

    if get_item is not None:
        db_mock.get_item.return_value = get_item
    else:
        db_mock.get_item.return_value = T.ItemOut(
            id=uuid4(),
            dir="dir",
            type="file",
            files=["file"],
            files_cnt=1,
            bytes_sum=2,
            ingest_id=uuid4(),
            context={"ignored": "data"},
            container_id=container_id,
            filename="filename"
        )

    if get_container is not None:
        db_mock.get_container.return_value = get_container
    else:
        db_mock.get_container.return_value = T.ContainerOut(
            id=container_id,
            level=0,
            path="label_value",
            src_context={"label": "label_value"},
            dst_context={"_id": "id_val"},
            ingest_id=uuid4()
        )


class _TempFileObject():
    classes = [
        type(tempfile.TemporaryFile()),
        tempfile.SpooledTemporaryFile
    ]
    def __eq__(self, other):
        for c in self.classes:
            if isinstance(other, c):
                return True
        return False

TempFileObject = _TempFileObject()
