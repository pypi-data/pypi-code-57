import itertools
from unittest.mock import Mock

import pytest

from flywheel_cli.ingest.models import Task


def test_task_status_mixin_timestamp_and_history(db, mocker):
    time_mock = Mock(time=itertools.count().__next__)
    mocker.patch("flywheel_cli.ingest.models.time", new=time_mock)
    mocker.patch("flywheel_cli.ingest.client.db_transactions.time", new=time_mock)
    db.create_ingest()

    # the scan task added via start should set history
    db.client.start()  # NOTE ingest status bumped count twice
    task = next(db.client.get_all_tasks())

    assert task.history == [("pending", 2)]

    # updating task status via client should be validated
    with pytest.raises(ValueError):
        task = db.client.update_task(task.id, status="failed")

    # bulk cancel via abort should set history
    db.client.abort()  # NOTE ingest status bumps count once
    task = next(db.client.get_all_tasks())

    assert task.history == [("pending", 2), ("canceled", 4)]

    # tasks bulk-inserted via client should set history
    tasks = db.client.batch_writer_insert_tasks()
    tasks.push({"type": "scan"})
    tasks.flush()
    task = next(db.client.get_all_tasks(Task.status == "pending"))

    assert task.history == [("pending", 5)]
