"""Tests for flywheel_cli.ingest.worker module"""
# pylint: disable=W0621
import os
import signal
from unittest import mock

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import errors
from flywheel_cli.ingest.worker import alarm_handler, Worker, WorkerPool


@pytest.fixture(scope="function")
def worker_config():
    return config.WorkerConfig(
        db_url="sqlite:///:memory:",
        worker_name="mock-worker-name",
        sleep_time=99,
        termination_grace_period=15,
        jobs=4,
    )


@pytest.fixture(scope="function")
def worker(sleep_mock, db_mock, event_mock, worker_config):
    shutdown_mock = event_mock()
    # allow one loop by default
    shutdown_mock.is_set.side_effect = [False, True]
    return Worker(worker_config, shutdown=shutdown_mock)


@pytest.fixture(scope="function")
def worker_mock(mocker):
    return mocker.patch("flywheel_cli.ingest.worker.Worker")


@pytest.fixture(scope="function")
def process_mock(mocker):
    return mocker.patch("multiprocessing.Process")


@pytest.fixture(scope="function")
def event_mock(mocker):
    return mocker.patch("multiprocessing.Event")


@pytest.fixture(scope="function")
def worker_pool(worker_config, event_mock, process_mock, worker_mock):
    return WorkerPool(worker_config)


@pytest.fixture(scope="function")
def sleep_mock(mocker):
    return mocker.patch("time.sleep")


@pytest.fixture(scope="function")
def db_mock(mocker):
    return mocker.patch("flywheel_cli.ingest.worker.DBClient")


def pytest_generate_tests(metafunc):
    if "signum" not in metafunc.fixturenames:
        return
    metafunc.parametrize("signum", [signal.SIGTERM, signal.SIGINT])


def test_ingest_worker_pool_start(worker_pool, worker_config, event_mock, worker_mock):
    worker_pool.start()
    assert worker_mock.call_count == 4
    assert len(worker_pool.processes) == 4
    assert worker_mock.mock_calls == [
        mock.call(worker_config, f"mock-worker-name-{i}", event_mock())
        for i in range(4)
    ]


def test_ingest_worker_pool_start_idempotent(worker_pool, worker_mock):
    worker_pool.start()
    worker_pool.start()
    # calling start multiple times won't start more workers
    assert worker_mock.call_count == 4


def test_ingest_worker_shutdown(worker_pool):
    worker_pool.start()
    worker_pool.shutdown()
    # set shutdown event for all worker
    assert all([event.is_set() for _, event in worker_pool.processes])
    # wait for all process to terminate using join
    assert all([p.join.called for p, _ in worker_pool.processes])


def test_ingest_worker_name_from_config(worker_config):
    worker = Worker(worker_config)
    assert worker.name == "mock-worker-name"


def test_ingest_worker_name_explicit(worker_config):
    worker = Worker(worker_config, name="explicit-name")
    assert worker.name == "explicit-name"


def test_ingest_worker_run_task(worker, mocker):
    mocker.patch.object(worker, "wait_for_db")
    create_task_mock = mocker.patch("flywheel_cli.ingest.worker.create_task")
    copy_mock = mocker.patch("copy.copy")
    task_mocks = [mock.Mock(ingest_id="1"), mock.Mock(ingest_id="2")]
    worker.db.next_task.side_effect = task_mocks
    worker.shutdown.is_set.side_effect = [False, False, True]
    worker.run()
    assert create_task_mock.call_count == 2
    assert create_task_mock.mock_calls == [
        mock.call(copy_mock.return_value, task_mocks[0], worker.config),
        mock.call().run(),
        mock.call(copy_mock.return_value, task_mocks[1], worker.config),
        mock.call().run(),
    ]
    assert create_task_mock.return_value.run.call_count == 2


def test_ingest_worker_run_exception_handling(worker, mocker):
    mocker.patch.object(worker, "wait_for_db")
    copy_mock = mocker.patch("copy.copy")
    create_task_mock = mocker.patch("flywheel_cli.ingest.worker.create_task")
    class TestException(Exception):
        pass
    create_task_mock.side_effect = TestException
    worker.shutdown.is_set.side_effect = [False, False, True]
    with pytest.raises(TestException):
        worker.run()
    copy_mock.return_value.fail.assert_called()


def test_ingest_worker_consume_tasks_until_not_shutdown(worker, mocker, sleep_mock):
    worker.shutdown.is_set.side_effect = [False, False, False, True]
    worker.db.next_task.return_value = None
    mocker.patch.object(worker, "wait_for_db")
    worker.run()
    # shutdown event's is_set function fourth call returns True
    # so next_task should be called exactly three times
    assert worker.db.next_task.call_count == 3
    # waits config.sleep_time before check_connection again
    assert sleep_mock.call_count == 3
    sleep_mock.assert_called_with(99)


def test_ingest_worker_wait_for_db(worker, sleep_mock):
    worker.shutdown.is_set.side_effect = [False, False, False]
    worker.db.check_connection.side_effect = [False, False, True]
    worker.wait_for_db()
    # check_connection returns True at the third call
    # and wait_for_db should return immediately
    assert worker.shutdown.is_set.call_count == 3
    assert worker.db.check_connection.call_count == 3
    # waits config.sleep_time before check_connection again
    assert sleep_mock.call_count == 2
    sleep_mock.assert_called_with(99)


def test_ingest_worker_wait_for_database_until_not_shutdown(worker):
    worker.shutdown.is_set.side_effect = [False, False, False, True]
    worker.db.check_connection.side_effect = [False, False, False]
    worker.wait_for_db()
    # shutdown event's is_set function fourth call returns True
    # so check_connection should be called exactly three times
    assert worker.db.check_connection.call_count == 3


def test_ingest_worker_signal_handling(worker, mocker, signum):
    worker.db.next_task.return_value = None
    worker.shutdown.is_set.side_effect = None
    worker.shutdown.is_set.return_value = False
    def set_event():
        worker.shutdown.is_set.return_value = True
    worker.shutdown.set.side_effect = set_event
    wait_for_db_mock = mocker.patch.object(worker, "wait_for_db")
    alarm_mock = mocker.patch("signal.alarm")
    def raise_signal():
        os.kill(os.getpid(), signum)
    wait_for_db_mock.side_effect = raise_signal
    worker.run()
    # set alarm with config.termination_grace_period
    alarm_mock.assert_called_with(15)


def test_ingest_worker_hard_shutdown(worker, mocker):
    worker.db.next_task.return_value = None
    worker.shutdown.is_set.side_effect = None
    worker.shutdown.is_set.return_value = False
    def set_event():
        worker.shutdown.is_set.return_value = True
    worker.shutdown.set.side_effect = set_event
    wait_for_db_mock = mocker.patch.object(worker, "wait_for_db")
    def raise_signal():
        # double CTRL+c
        os.kill(os.getpid(), signal.SIGINT)
        os.kill(os.getpid(), signal.SIGINT)
    wait_for_db_mock.side_effect = raise_signal
    with pytest.raises(errors.WorkerForcedShutdown):
        worker.run()
    # cancel scheduled alarm
    signal.alarm(0)


def test_ingest_worker_alarm_handler():
    with pytest.raises(errors.WorkerShutdownTimeout):
        alarm_handler(None, None)
