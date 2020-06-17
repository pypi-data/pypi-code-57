import datetime
import uuid
from unittest import mock

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import (factory, finalize, prepare, resolve,
                                       scan, upload)


def pytest_generate_tests(metafunc):
    scenarios = [
        ("scan_task", {"task_type": "scan", "task_cls": scan.ScanTask}),
        ("resolve_task", {"task_type": "resolve", "task_cls": resolve.ResolveTask}),
        ("prepare_task", {"task_type": "prepare", "task_cls": prepare.PrepareTask}),
        ("upload_task", {"task_type": "upload", "task_cls": upload.UploadTask}),
        ("finalize_task", {"task_type": "finalize", "task_cls": finalize.FinalizeTask}),
    ]

    idlist = []
    argvalues = []
    for scenario in scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])

    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="function")

def test_create_task(task_type, task_cls):
    task_out = T.TaskOut(
        id=uuid.uuid4(),
        type=task_type,
        created=datetime.datetime.now(),
        status="pending",
        timestamp=0,
        history=[("pending", 1)],
        ingest_id=uuid.uuid4(),
        retries=0,
    )
    db_client = mock.Mock()
    cfg = config.WorkerConfig()

    task = factory.create_task(
        client=db_client,
        task=task_out,
        worker_config=cfg
    )

    assert isinstance(task, task_cls)
    assert task.db == db_client
    assert task.task == task_out
    assert task.worker_config == cfg
