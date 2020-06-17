import datetime
from unittest import mock
from uuid import uuid4

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import prepare
from flywheel_cli.ingest.tasks.prepare import PrepareTask


@pytest.fixture(scope="function")
def prepare_task(db):
    ingest = db.create_ingest(status="preparing")
    task = db.create_task(
        type="prepare",
        ingest_id=ingest.id
    )

    prepare_task = PrepareTask(
        db=db.client,
        task=task.schema(),
        worker_config=config.WorkerConfig()
    )

    return prepare_task


@pytest.fixture(scope="function")
def prepare_task_mock():
    task = T.TaskOut(
        type="prepare",
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now(),
    )
    prep_task = prepare.PrepareTask(
        db=mock.Mock(**{"batch_writer_update_container.return_value.batch_size": 999}),
        task=task,
        worker_config=mock.Mock(),
    )
    prep_task.ingest_config = config.IngestConfig(src_fs="/tmp")

    return prep_task


def test_create_container(mocker, prepare_task_mock):
    prepare_task_mock.valid_container_paths = {"foo/bar/baz/qux"}
    sdk_mock = mock.Mock(
        **{
            "add_project.return_value": "pid",
            "add_group.return_value": "gid",
            "add_subject.return_value": "sub_id",
            "add_session.return_value": "sid",
        }
    )
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=sdk_mock)

    ids = [uuid4(), uuid4(), uuid4(), uuid4()]
    prepare_task_mock.db.count_all_container.return_value = len(ids)
    prepare_task_mock.db.get_all_container.return_value = [
        T.ContainerOut(
            level=0,
            path="foo",
            src_context={"src1": "src1", "label": "label1"},
            id=ids[0],
            ingest_id=uuid4(),
        ),
        T.ContainerOut(
            level=1,
            path="foo/bar",
            src_context={"src2": "src2", "label": "label2"},
            id=ids[1],
            ingest_id=uuid4(),
            parent_id=ids[0],
        ),
        T.ContainerOut(
            level=2,
            path="foo/bar/baz",
            src_context={"src3": "src3", "label": "label3"},
            id=ids[2],
            ingest_id=uuid4(),
            parent_id=ids[1],
        ),
        T.ContainerOut(
            level=3,
            path="foo/bar/baz/qux",
            src_context={"src4": "src4", "label": "label4"},
            id=ids[3],
            ingest_id=uuid4(),
            parent_id=ids[2],
        ),
    ]
    prepare_task_mock.db.get_items_with_error_count.return_value = []

    prepare_task_mock.update_containers = mock.Mock()

    prepare_task_mock._run()

    # fw calls
    assert sdk_mock.mock_calls == [
        mock.call.add_group({"label": "label1", "src1": "src1"}),
        mock.call.add_project({"label": "label2", "src2": "src2", "group": "gid"}),
        mock.call.add_subject(
            {"src3": "src3", "project": "pid", "code": "label3", "label": "label3"}
        ),
        mock.call.add_session(
            {
                "src4": "src4",
                "project": "pid",
                "subject": {"_id": "sub_id"},
                "label": "label4",
            }
        ),
    ]

    # update calls
    calls = [
        mock.call(
            {
                "id": ids[0],
                "dst_context": {"src1": "src1", "label": "label1", "_id": "gid"},
                "dst_path": "gid",
            }
        ),
        mock.call(
            {
                "id": ids[1],
                "dst_context": {"src2": "src2", "label": "label2", "_id": "pid"},
                "dst_path": "gid/label2",
            }
        ),
        mock.call(
            {
                "id": ids[2],
                "dst_context": {"src3": "src3", "label": "label3", "_id": "sub_id"},
                "dst_path": "gid/label2/label3",
            }
        ),
        mock.call(
            {
                "id": ids[3],
                "dst_context": {"src4": "src4", "label": "label4", "_id": "sid"},
                "dst_path": "gid/label2/label3/label4",
            }
        ),
    ]
    assert prepare_task_mock.update_containers.push.mock_calls == calls


def test_skip_existing(prepare_task_mock):
    prepare_task_mock.db.get_all_container.return_value = []
    id_ = uuid4()
    prepare_task_mock.db.count_all_container.return_value = 1
    prepare_task_mock.db.get_items_with_error_count.return_value = [
        T.ItemWithErrorCount(id=id_, existing=True)
    ]

    prepare_task_mock.ingest_config.skip_existing = True
    prepare_task_mock.update_items = mock.Mock()
    prepare_task_mock.insert_tasks = mock.Mock()

    prepare_task_mock._run()

    prepare_task_mock.update_items.push.assert_called_once_with(
        {"id": id_, "skipped": True,}
    )
    prepare_task_mock.insert_tasks.push.assert_not_called()
    prepare_task_mock.insert_tasks.flush.assert_called_once()


def test_run(prepare_task_mock):
    prepare_task_mock.db.get_all_container.return_value = []
    id_ = uuid4()
    prepare_task_mock.db.count_all_container.return_value = 1
    prepare_task_mock.db.get_items_with_error_count.return_value = [
        T.ItemWithErrorCount(id=id_, existing=False)
    ]

    prepare_task_mock.ingest_config.skip_existing = True
    prepare_task_mock.update_items = mock.Mock()
    prepare_task_mock.insert_tasks = mock.Mock()

    prepare_task_mock._run()

    prepare_task_mock.update_items.push.assert_not_called()
    prepare_task_mock.insert_tasks.push.assert_called_once_with({
        "type": T.TaskType.upload,
        "item_id": id_,
        "status": "pending",
        "context": None
    })
    prepare_task_mock.insert_tasks.flush.assert_called_once()


@pytest.mark.parametrize(
    "skip_existing,item_exists",
    [(True, False), (False, True), (False, False), (True, True),],
)
def test_should_skip_item_skip_existing(prepare_task_mock, skip_existing, item_exists):
    should_skip = skip_existing and item_exists
    prepare_task_mock.ingest_config.skip_existing = skip_existing
    item_not_existing = T.ItemWithErrorCount(id=uuid4(), existing=item_exists)

    assert prepare_task_mock._should_skip_item(item_not_existing) == should_skip


@pytest.mark.parametrize(
    "detect_duplicates,error_cnt",
    [(True, 0), (True, 1), (True, 6), (False, 0), (False, 1), (False, 6),],
)
def test_should_skip_item_detect_duplicates(prepare_task_mock, detect_duplicates, error_cnt):
    should_skip = detect_duplicates and error_cnt > 0
    prepare_task_mock.ingest_config.detect_duplicates = detect_duplicates
    item_wo_error = T.ItemWithErrorCount(id=uuid4(), error_cnt=error_cnt)

    assert prepare_task_mock._should_skip_item(item_wo_error) == should_skip


def test_run_success(prepare_task_mock):
    prepare_task_mock.db.count_all_container.return_value = 0
    prepare_task_mock.db.get_all_container.return_value = []
    prepare_task_mock.db.get_items_with_error_count.return_value = []

    prepare_task_mock.run()

    prepare_task_mock.db.update_task.assert_called_once_with(
        prepare_task_mock.task.id, status=T.TaskStatus.completed
    )
    prepare_task_mock.db.start_finalizing.assert_called_once()


def test_run_error(prepare_task_mock):
    class TestException(Exception):
        pass

    prepare_task_mock.db.get_all_container.return_value = []
    prepare_task_mock.db.get_items_with_error_count.side_effect = TestException("test error")

    prepare_task_mock.run()

    prepare_task_mock.db.fail.assert_called_once()


def test_skip_container(prepare_task, db, mocker):
    sdk_mock = mock.Mock(
        **{
            "add_subject.return_value": "sub_id",
        }
    )
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=sdk_mock)

    container_1 = db.create_container(path="group/project_a", level=2, error=True, src_context={"src": "src1", "label": "label1"},)
    container_2 = db.create_container(path="group/project_b", level=2, src_context={"src": "src2", "label": "label2"})
    container_3 = db.create_container(path="group/project_c", level=2, src_context={"src": "src3", "label": "label3"})
    item_1 = db.create_item(filename="a.txt", container_id=container_1.id)
    item_2 = db.create_item(filename="b.txt", container_id=container_2.id)

    prepare_task._run()

    # testing that container error results in skipped item
    item = db.client.get_item(item_1.id)
    assert item.skipped
    item = db.client.get_item(item_2.id)
    assert not item.skipped

    assert prepare_task.valid_container_paths == {"group/project_b"}

    assert sdk_mock.mock_calls == [
        mock.call.add_subject({'src': 'src2', 'label': 'label2', 'code': 'label2'})
    ]


def test_always_create_project_container(prepare_task, db, mocker):
    sdk_mock = mock.Mock(
        **{
            "add_project.return_value": "pid",
            "add_group.return_value": "gid",
            "add_subject.return_value": "sub_id",
            "add_session.return_value": "sid",
        }
    )
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=sdk_mock)

    con1 = db.create_container(path="group", level="group", error=True, src_context={"src": "src1", "label": "label1"},)
    con2 = db.create_container(path="group/project", level="project", error=True, src_context={"src": "src2", "label": "label2"}, parent_id=con1.id)
    con3 = db.create_container(path="group/project/subject", level="subject", error=True, src_context={}, parent_id=con2.id)
    con4 = db.create_container(path="group/project/subject/session", level="session", error=True, src_context={}, parent_id=con3.id)
    db.create_container(path="group/project/subject/session/acquisition", level="acquisition", error=True, src_context={}, parent_id=con4.id)

    prepare_task._run()

    assert sdk_mock.mock_calls == [
        mock.call.add_group({'src': 'src1', 'label': 'label1'}),
        mock.call.add_project({'src': 'src2', 'label': 'label2', 'group': 'gid'})
    ]
