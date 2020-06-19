import datetime
import io
from unittest import mock
from uuid import uuid4

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import finalize


@pytest.fixture(scope="function")
def finalize_task():
    task = T.TaskOut(
        type="finalize",
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now(),
    )
    ingest = T.IngestOutAPI(
        id=uuid4(),
        label="FOO",
        fw_host="localhost",
        fw_user="dummy_user",
        config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=config.FolderConfig(),
        status=T.IngestStatus.finalizing,
        history=[],
        created=datetime.datetime.utcnow(),
    )
    db_mock = mock.Mock()
    db_mock.count_all_item.return_value = 50
    type(db_mock).ingest = mock.PropertyMock(return_value=ingest)
    finalize_task = finalize.FinalizeTask(
        db=db_mock, task=task, worker_config=mock.Mock()
    )
    finalize_task.db.reset_mock()

    return finalize_task


def test_run_without_audit_log(finalize_task):
    finalize_task.ingest_config = config.IngestConfig(src_fs="/tmp", no_audit_log=True)

    finalize_task._run()

    assert len(finalize_task.db.mock_calls) == 0


def test_run_with_audit_log(mocker, finalize_task):
    fp = io.StringIO()
    file_mock = mock.MagicMock()
    file_mock.__enter__.return_value = fp
    mocker.patch("flywheel_cli.ingest.tasks.finalize.open", return_value=file_mock)
    get_sdk_client_mock = mocker.patch("flywheel_cli.ingest.utils.get_sdk_client")
    finalize_task.db.audit_logs = ["line1", "line2"]
    finalize_task.db.get_all_container.return_value = [
        T.ContainerOut(
            id=uuid4(),
            level=0,
            path="foo",
            src_context={},
            ingest_id=uuid4(),
            dst_context={"_id": "ID"},
        )
    ]

    finalize_task._run()

    get_sdk_client_mock.return_value.upload.assert_called_once_with(
        "group",
        "ID",
        mock.ANY,
        file_mock.__enter__.return_value,
        metadata={
            "info": finalize_task.ingest.dict(
                include={"label", "config", "strategy_config", "created"}
            )
        },
    )


def test_run_success(finalize_task):
    finalize_task.ingest_config = config.IngestConfig(src_fs="/tmp", no_audit_log=True)
    finalize_task.run()

    finalize_task.db.update_task.assert_called_once_with(
        finalize_task.task.id, status=T.TaskStatus.completed
    )
    finalize_task.db.set_ingest_status.assert_called_once_with(T.IngestStatus.finished)


def test_run_error(mocker, finalize_task):
    class TestException(Exception):
        pass

    mocker.patch(
        "flywheel_cli.ingest.tasks.finalize.FinalizeTask._run",
        side_effect=TestException("test error"),
    )
    finalize_task.run()

    finalize_task.db.fail.assert_called_once()
