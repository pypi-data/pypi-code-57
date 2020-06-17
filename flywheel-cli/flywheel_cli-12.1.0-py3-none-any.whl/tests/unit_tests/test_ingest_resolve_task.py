import datetime
from unittest import mock
from uuid import uuid4

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import models as M
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import resolve


@pytest.fixture(scope="function")
def fw_resolve_mock(mocker, attr_dict):
    fw_mock = mocker.patch('flywheel_cli.ingest.utils.flywheel.Client')
    fw_mock.return_value.lookup.return_value = attr_dict({
        'id': 'id2',
        'label': 'label2',
        'files': [
            attr_dict({"name": "name1"}),
            attr_dict({"name": "name2"})
        ]
    })
    return fw_mock


@pytest.fixture(scope="function")
def resolve_task():
    task = T.TaskOut(
        type='resolve',
        id=uuid4(),
        ingest_id=uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now()
    )
    resolve_task = resolve.ResolveTask(
        db=mock.Mock(**{
            "batch_writer_insert_container.return_value.batch_size": 999,
        }),
        task=task,
        worker_config=mock.Mock()
    )
    resolve_task.ingest_config = config.IngestConfig(
        src_fs="/tmp",
    )

    return resolve_task


def test_get_dst_context(attr_dict):
    container = attr_dict({
        "id": "id_value",
        "label": "label_value",
        "uid": "uid_value",
        "code": "code_value",
        "extra": 'field'
    })

    ctx = resolve.ResolveTask.get_dst_context(container)
    assert ctx == {
        "_id": "id_value",
        "label": "label_value",
        "uid": "uid_value",
        "code": "code_value"
    }


def test_get_filename_packfile_wo_dst_context():
    item = T.ItemOut(
        id=uuid4(),
        dir="dir",
        type="packfile",
        files=["file1", "file2"],
        files_cnt=2,
        bytes_sum=2,
        ingest_id=uuid4(),
        context={'packfile': {'type': 'zip'}}
    )
    container = T.ContainerOut(
        id=uuid4(),
        level=0,
        path="label_value",
        src_context={'label': 'label_value'},
        ingest_id=uuid4()
    )

    filename = resolve.ResolveTask._get_filename(item, container)
    assert filename == 'label_value.zip'

    item.context = {'packfile': {'type': 'dicom'}}
    filename = resolve.ResolveTask._get_filename(item, container)
    assert filename == 'label_value.dicom.zip'


def test_get_filename_packfile_w_dst_context():
    item = T.ItemOut(
        id=uuid4(),
        dir="dir",
        type="packfile",
        files=["file1", "file2"],
        files_cnt=2,
        bytes_sum=2,
        ingest_id=uuid4(),
        context={'packfile': {'type': 'zip'}}
    )
    container = T.ContainerOut(
        id=uuid4(),
        level=0,
        path="label_value",
        src_context={'label': 'label_value'},
        dst_context={'label': 'label_value2'},
        ingest_id=uuid4()
    )

    filename = resolve.ResolveTask._get_filename(item, container)
    assert filename == 'label_value2.zip'

    item.context = {'packfile': {'type': 'dicom'}}
    filename = resolve.ResolveTask._get_filename(item, container)
    assert filename == 'label_value2.dicom.zip'


def test_get_filename_not_packfile():
    item = T.ItemOut(
        id=uuid4(),
        dir="dir",
        type="file",
        files=["path1/path2/file.ext"],
        files_cnt=1,
        bytes_sum=2,
        ingest_id=uuid4(),
        context={'packfile': 'it_is_ignored'}
    )
    container = T.ContainerOut(
        id=uuid4(),
        level=0,
        path="label_value",
        src_context={'label': 'label_value'},
        dst_context={'label': 'label_value2'},
        ingest_id=uuid4()
    )

    filename = resolve.ResolveTask._get_filename(item, container)
    assert filename == 'file.ext'


def test_fw_property(mocker):
    get_sdk_client_mock = mocker.patch('flywheel_cli.ingest.utils.get_sdk_client')
    db_client_mock = mock.Mock()
    db_client_mock.api_key = 'api_key'

    resolve_task = resolve.ResolveTask(
        db=db_client_mock,
        task=mock.Mock(),
        worker_config=mock.Mock()
    )
    # make sure __init__ does not get the sdk
    get_sdk_client_mock.assert_not_called()

    fw = resolve_task.fw
    assert fw == get_sdk_client_mock.return_value

    get_sdk_client_mock.assert_called_once_with('api_key')


def test_on_success(resolve_task):
    resolve_task._on_success()

    resolve_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review
    )
    resolve_task.db.review.assert_not_called()


def test_on_success_assume_yes(resolve_task):
    resolve_task.ingest_config.assume_yes = True

    resolve_task._on_success()

    resolve_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review
    )
    resolve_task.db.review.assert_called_once()


def test_on_success_detect_duplicates(resolve_task):
    resolve_task.ingest_config.detect_duplicates = True

    resolve_task._on_success()

    resolve_task.db.start_detecting_duplicates.assert_called_once()


def test_on_error(resolve_task):
    resolve_task._on_error()
    resolve_task.db.fail.assert_called_once()
    resolve_task.db.set_ingest_status.assert_not_called()
    resolve_task.db.review.assert_not_called()


def test_resolve_item_containers(fw_resolve_mock, attr_dict, resolve_task):
    item = T.ItemOut(
        id=uuid4(),
        dir="dir",
        type="packfile",
        files=["file1", "file2"],
        files_cnt=2,
        bytes_sum=2,
        ingest_id=uuid4(),
        context=attr_dict({
            "group": {
                "_id": "gid",
            },
            "project": {
                "_id": "pid",
            },
            "session": {
                "_id": "sid",
            }
        })
    )

    container = resolve_task._resolve_item_containers(item)

    assert resolve_task.visited == {'gid', 'gid/<id:pid>'}
    assert isinstance(container, T.ContainerIn)


def test_resolve_container_invalid_context(attr_dict, resolve_task):
    container = resolve_task._resolve_container(
        c_level=1,
        path=['path'],
        context=attr_dict({}),
        parent=None
    )
    assert container is None


def test_resolve_container_visited(attr_dict, resolve_task):
    resolve_task.visited.add('path')

    container = resolve_task._resolve_container(
        c_level=1,
        path=['path'],
        context=attr_dict({
            '_id': 'idval',
            'label': 'labelval'
        }),
        parent=None
    )

    assert container == resolve_task.db.find_one_container.return_value
    args, _ = resolve_task.db.find_one_container.call_args
    assert len(args) == 1
    condition = args[0]
    assert condition.compare(M.Container.path == 'path')


def test_resolve_container_not_visited_no_parent(fw_resolve_mock, attr_dict, resolve_task):
    resolve_task.insert_containers = mock.Mock()

    assert resolve_task.visited == set()

    ctx = attr_dict({
        '_id': 'idval',
        'label': 'labelval'
    })
    container = resolve_task._resolve_container(
        c_level=T.ContainerLevel(1),
        path=['path'],
        context=ctx,
        parent=None
    )

    assert 'path' in resolve_task.visited
    assert isinstance(container, T.ContainerIn)
    assert container.path == 'path'
    assert container.level == 1
    assert container.src_context == ctx
    assert container.dst_context == {
        'label': 'label2',
        '_id': 'id2',
        'files': ['name1', 'name2']
    }
    resolve_task.insert_containers.push.assert_called_once_with(container)


def test_resolve_container_not_visited_parent(fw_resolve_mock, attr_dict, resolve_task):
    assert resolve_task.visited == set()

    ctx = attr_dict({
        '_id': 'idval',
        'label': 'labelval'
    })
    parent = T.ContainerIn(
        id=uuid4(),
        level=1,
        path="label_value",
        src_context={'key1': 'value1'},
        dst_context={'key2': 'value2'},
    )
    container = resolve_task._resolve_container(
        c_level=T.ContainerLevel(1),
        path=['path'],
        context=ctx,
        parent=parent
    )

    assert 'path' in resolve_task.visited
    assert isinstance(container, T.ContainerIn)
    assert container.path == 'path'
    assert container.level == 1
    assert container.src_context == ctx
    assert container.dst_context is None
    assert container.parent_id == parent.id


def test_find_child_by_path(fw_resolve_mock, resolve_task):
    target, dst_files = resolve_task._find_child_by_path(['foo', 'bar'])
    assert target.id == 'id2'
    assert dst_files == ['name1', 'name2']
    fw_resolve_mock.return_value.lookup.assert_called_once_with(['foo', 'bar'])


def test_run(fw_resolve_mock, resolve_task):
    _id = uuid4()
    resolve_task.db.count_all_item.return_value = 1
    resolve_task.db.get_all_item.return_value = [
        T.ItemOut(
            id=_id,
            dir="dir",
            type="packfile",
            files=["file1", "file2"],
            files_cnt=2,
            bytes_sum=2,
            ingest_id=uuid4(),
            context={
                'packfile': {'type': 'zip'},
                "group": {
                    "_id": "gid",
                },
            }
        )
    ]
    resolve_task.update_items = mock.Mock()
    resolve_task._run()

    resolve_task.update_items.push.assert_called_once_with({
        'id':_id,
        'container_id':mock.ANY,
        'existing':False,
        'filename':'label2.zip'
    })
    resolve_task.update_items.flush.assert_called_once()


def test_run_success(fw_resolve_mock, resolve_task):
    resolve_task.db.count_all_item.return_value = 0
    resolve_task.db.get_all_item.return_value = []

    resolve_task.run()

    resolve_task.db.update_task.assert_called_once_with(
        resolve_task.task.id,
        status=T.TaskStatus.completed
    )
    # success
    resolve_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review
    )


def test_run_error(fw_resolve_mock, resolve_task):
    resolve_task.db.get_all_item.side_effect = Exception()
    resolve_task.run()

    # not set ingest status directly
    resolve_task.db.set_ingest_status.assert_not_called()
    # resolve fails the whole ingest
    resolve_task.db.fail.assert_called_once()


def test_batch_size_and_cache_size_equal(resolve_task):
    assert resolve_task.insert_containers.batch_size == resolve_task.cache.max_length
