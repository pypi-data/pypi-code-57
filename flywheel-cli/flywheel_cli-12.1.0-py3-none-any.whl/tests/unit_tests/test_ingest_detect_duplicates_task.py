"""Ingest DetectDuplicatesTask tests"""

import datetime
import uuid
from unittest import mock

from flywheel import Flywheel
from flywheel.models import ContainerUidcheck
import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.tasks import detect_duplicates
from flywheel_cli.ingest.client import db as ingest_db_client


@pytest.fixture(scope="function")
def mocked_detect_duplicates_task(db):
    task = T.TaskOut(
        type="detect_duplicates",
        id=uuid.uuid4(),
        ingest_id=uuid.uuid4(),
        status="pending",
        timestamp=0,
        retries=0,
        history=[],
        created=datetime.datetime.now(),
    )

    spec = dir(ingest_db_client.DBClient)
    spec.extend([
        "batch_writer_insert_error",
        "count_all_item",
        "update_task",
        "batch_writer_update_container",
        "get_all_container"
    ])
    db = mock.Mock(spec=spec)

    db.one_session_container_multiple_study_instance_uid_item_ids.return_value = []
    db.one_study_instance_uid_multiple_session_container_item_ids.return_value = []
    db.one_acquisition_container_multiple_series_instance_uid_item_ids.return_value = []
    db.one_series_instance_uid_multiple_acquisition_container_item_ids.return_value = []
    db.study_instance_uids_in_new_session_container.return_value = []
    db.series_instance_uids_in_new_acquisition_container.return_value = []
    db.find_all_containers_with_item_id.return_value = []
    db.get_all_container.return_value = []

    mocked_detect_duplicates_task = detect_duplicates.DetectDuplicatesTask(
        db=db,
        task=task,
        worker_config=config.WorkerConfig()
    )
    mocked_detect_duplicates_task.ingest_config = config.IngestConfig(
        src_fs="/tmp"
    )
    return mocked_detect_duplicates_task


@pytest.fixture(scope="function")
def detect_duplicates_task(db):
    ingest = db.create_ingest()
    task = db.create_task(
        type="detect_duplicates",
        ingest_id=ingest.id
    )
    mocked_detect_duplicates_task = detect_duplicates.DetectDuplicatesTask(
        db=db.client,
        task=task.schema(),
        worker_config=config.WorkerConfig()
    )
    mocked_detect_duplicates_task.ingest_config = config.IngestConfig(
        src_fs="/tmp"
    )
    return mocked_detect_duplicates_task


@pytest.fixture(scope="function")
def create_item():
    def _create(**kwargs):
        kwargs.setdefault("id", uuid.uuid4())
        kwargs.setdefault("dir", "/dir")
        kwargs.setdefault("existing", False)
        return T.ItemWithContainerPath(**kwargs)
    return _create


@pytest.fixture(scope="function")
def create_uid():
    def _create(db, **kwargs):
        kwargs.setdefault("study_instance_uid", str(uuid.uuid4()))
        kwargs.setdefault("series_instance_uid", str(uuid.uuid4()))
        kwargs.setdefault("sop_instance_uid", str(uuid.uuid4()))
        kwargs.setdefault("filename", "file1")
        return db.create_uid(**kwargs)
    return _create


def test_on_success(mocked_detect_duplicates_task):
    mocked_detect_duplicates_task._on_success()

    mocked_detect_duplicates_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review,
    )
    mocked_detect_duplicates_task.db.review.assert_not_called()


def test_on_success_assume_yes(mocked_detect_duplicates_task):
    mocked_detect_duplicates_task.ingest_config.assume_yes = True

    mocked_detect_duplicates_task._on_success()

    mocked_detect_duplicates_task.db.set_ingest_status.assert_called_once_with(
        status=T.IngestStatus.in_review,
    )
    mocked_detect_duplicates_task.db.review.assert_called_once()


def test_on_error(mocked_detect_duplicates_task):
    mocked_detect_duplicates_task._on_error()

    mocked_detect_duplicates_task.db.fail.assert_called_once()


def test_run_dup_in_fw(mocked_detect_duplicates_task, create_item):
    db_mock = mocked_detect_duplicates_task.db
    db_mock.count_all_item.return_value = 3
    db_mock.duplicated_sop_instance_uid_item_ids.return_value = []
    item_1 = create_item(
        filename="a.txt",
        existing=True,
        container_path="group/project",
    )
    item_2 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="c.txt",
        existing=True,
        container_path="group/project/subject2",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3]
    expected_error_code = errors.DuplicateFilepathInFlywheel.code

    mocked_detect_duplicates_task._run()

    assert mocked_detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_1.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_3.id, "code": expected_error_code}),
        mock.call.flush(),
    ]


def test_run_dup_in_upload_set_first_items(mocked_detect_duplicates_task, create_item):
    db_mock = mocked_detect_duplicates_task.db
    db_mock.count_all_item.return_value = 3
    db_mock.duplicated_sop_instance_uid_item_ids.return_value = []
    item_1 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_2 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="b.txt",
        container_path="group/project/subject2",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3]
    expected_error_code = errors.DuplicateFilepathInUploadSet.code

    mocked_detect_duplicates_task._run()

    assert mocked_detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_2.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_1.id, "code": expected_error_code}),
        mock.call.flush(),
    ]


def test_run_dup_in_upload_set_last_items(mocked_detect_duplicates_task, create_item):
    db_mock = mocked_detect_duplicates_task.db
    db_mock.count_all_item.return_value = 3
    db_mock.duplicated_sop_instance_uid_item_ids.return_value = []
    item_1 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_2 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3]
    expected_error_code = errors.DuplicateFilepathInUploadSet.code

    mocked_detect_duplicates_task._run()

    assert mocked_detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_3.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_2.id, "code": expected_error_code}),
        mock.call.flush(),
    ]


def test_run_dup_in_upload_set_middle_items(mocked_detect_duplicates_task, create_item):
    db_mock = mocked_detect_duplicates_task.db
    db_mock.count_all_item.return_value = 4
    db_mock.duplicated_sop_instance_uid_item_ids.return_value = []
    item_1 = create_item(
        filename="a.txt",
        container_path="group/project/subject",
    )
    item_2 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_3 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_4 = create_item(
        filename="b.txt",
        container_path="group/project/subject",
    )
    item_5 = create_item(
        filename="c.txt",
        container_path="group/project/subject",
    )
    db_mock.get_items_sorted_by_dst_path.return_value = [item_1, item_2, item_3, item_4, item_5]
    expected_error_code = errors.DuplicateFilepathInUploadSet.code

    mocked_detect_duplicates_task._run()

    assert mocked_detect_duplicates_task.insert_errors.mock_calls == [
        mock.call.push({"item_id": item_3.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_4.id, "code": expected_error_code}),
        mock.call.push({"item_id": item_2.id, "code": expected_error_code}),
        mock.call.flush(),
    ]

def test_correct_uids_in_container(db, detect_duplicates_task, create_uid):
    container1_s = db.create_container(path="path/1", level=T.ContainerLevel.session)
    container1_a = db.create_container(path="path/2", level=T.ContainerLevel.acquisition)

    container2_s = db.create_container(path="path/3", level=T.ContainerLevel.session)

    container3_s = db.create_container(path="path/4", level=T.ContainerLevel.session)
    container3_a = db.create_container(path="path/5", level=T.ContainerLevel.acquisition)

    item1 = db.create_item(container_id=container1_a.id)
    create_uid(db, item_id=item1.id, study_instance_uid="study1", series_instance_uid="series1",
        session_container_id=container1_a.id, acquisition_container_id=container1_a.id)
    create_uid(db, item_id=item1.id, study_instance_uid="study1", series_instance_uid="series1",
        session_container_id=container1_a.id, acquisition_container_id=container1_a.id)

    item2 = db.create_item(container_id=container2_s.id)
    create_uid(db, item_id=item1.id, study_instance_uid="study2", series_instance_uid="series2",
        session_container_id=container2_s.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._run()

    assert detect_duplicates_task.insert_errors.push.call_count == 0
    detect_duplicates_task.insert_errors.flush.assert_called_once()


def test_multiple_study_instance_uids_in_container(db, detect_duplicates_task, create_uid):
    container1 = db.create_container(path="path", level=T.ContainerLevel.session)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid3", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container2.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._one_session_multi_study_uids()

    assert detect_duplicates_task.insert_errors.push.call_count == 1
    detect_duplicates_task.insert_errors.push.assert_called_once_with({
        "item_id": item1.id,
        "code": errors.DuplicatedStudyInstanceUID.code
    })

    detect_duplicates_task._one_study_uid_multi_containers()
    assert detect_duplicates_task.insert_errors.push.call_count == 1


def test_study_instance_uids_in_multiple_containers(db, detect_duplicates_task, create_uid):
    container1 = db.create_container(path="path", level=T.ContainerLevel.session)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid1", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid1", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid1", session_container_id=container2.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)

    detect_duplicates_task._one_session_multi_study_uids()
    assert detect_duplicates_task.insert_errors.push.call_count == 0

    detect_duplicates_task._one_study_uid_multi_containers()
    assert detect_duplicates_task.insert_errors.push.call_count == 2
    detect_duplicates_task.insert_errors.push.assert_has_calls([
        mock.call({
            "item_id": item1.id,
            "code": errors.DuplicatedStudyInstanceUIDInContainers.code
        }),
        mock.call({
            "item_id": item2.id,
            "code": errors.DuplicatedStudyInstanceUIDInContainers.code
        }),
    ], any_order=True)


def test_new_study_instance_uids(db, detect_duplicates_task, create_uid, mocker):
    fw_mock = mock.Mock(spec=Flywheel)
    fw_mock.check_uids_exist.return_value = {"sessions": ["uid2"]}
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=fw_mock)

    container1 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container3 = db.create_container(path="path", level=T.ContainerLevel.session, existing=True)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container2.id)

    item3 = db.create_item(container_id=container3.id)
    create_uid(db, item_id=item3.id, study_instance_uid="uid3", session_container_id=container3.id)
    create_uid(db, item_id=item3.id, study_instance_uid="uid3", session_container_id=container3.id)
    create_uid(db, item_id=item3.id, study_instance_uid="uid3", session_container_id=container3.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._check_new_session_container_study_instance_uids()

    fw_mock.check_uids_exist.assert_called_once()
    _, args, _ = fw_mock.check_uids_exist.mock_calls[0]
    assert isinstance(args[0], ContainerUidcheck)

    assert set(["uid1", "uid2"]) == set(args[0]._sessions)
    assert args[0]._acquisitions is None

    assert detect_duplicates_task.insert_errors.push.call_count == 1
    detect_duplicates_task.insert_errors.push.assert_called_once_with(
        {
            "item_id": item2.id,
            "code": errors.StudyInstanceUIDExists.code
        }
    )


def test_new_study_instance_uids_container_error(db, detect_duplicates_task, create_uid, mocker):
    fw_mock = mock.Mock(spec=Flywheel)
    fw_mock.check_uids_exist.return_value = {"sessions": ["uid2"]}
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=fw_mock)

    container1 = db.create_container(path="path", level=T.ContainerLevel.session, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.acquisition, parent_id=container1.id)
    container3 = db.create_container(path="path", level=T.ContainerLevel.acquisition, parent_id=container1.id)

    # ok
    item1 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item1.id, study_instance_uid="uid1", session_container_id=container1.id, acquisition_container_id=container2.id)

    # not ok
    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, study_instance_uid="uid2", session_container_id=container1.id, acquisition_container_id=container3.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._check_new_session_container_study_instance_uids()

    fw_mock.check_uids_exist.assert_called_once()
    _, args, _ = fw_mock.check_uids_exist.mock_calls[0]
    assert isinstance(args[0], ContainerUidcheck)

    assert set(["uid1", "uid2"]) == set(args[0]._sessions)
    assert args[0]._acquisitions is None

    assert detect_duplicates_task.insert_errors.push.call_count == 1
    detect_duplicates_task.insert_errors.push.assert_called_once_with(
        {
            "item_id": item2.id,
            "code": errors.StudyInstanceUIDExists.code
        }
    )

    assert detect_duplicates_task.error_container_ids == {container1.id, container3.id}


def test_multiple_series_instance_uids_in_container(db, detect_duplicates_task, create_uid):
    container1 = db.create_container(path="path", level=T.ContainerLevel.acquisition)
    container2 = db.create_container(path="path", level=T.ContainerLevel.acquisition)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid3", acquisition_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid2", acquisition_container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid2", acquisition_container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid2", acquisition_container_id=container2.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._one_acquisition_multi_series_uids()

    assert detect_duplicates_task.insert_errors.push.call_count == 1
    detect_duplicates_task.insert_errors.push.assert_called_once_with({
        "item_id": item1.id,
        "code": errors.DuplicatedSeriesInstanceUID.code
    })

    detect_duplicates_task._one_series_uid_multi_containers()
    assert detect_duplicates_task.insert_errors.push.call_count == 1


def test_series_instance_uids_in_multiple_containers(db, detect_duplicates_task, create_uid):
    container1 = db.create_container(path="path", level=T.ContainerLevel.acquisition)
    container2 = db.create_container(path="path", level=T.ContainerLevel.acquisition)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid1", acquisition_container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid1", acquisition_container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid1", acquisition_container_id=container2.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._one_acquisition_multi_series_uids()
    assert detect_duplicates_task.insert_errors.push.call_count == 0

    detect_duplicates_task._one_series_uid_multi_containers()
    assert detect_duplicates_task.insert_errors.push.call_count == 2
    detect_duplicates_task.insert_errors.push.assert_has_calls([
        mock.call({
            "item_id": item1.id,
            "code": errors.DuplicatedSeriesInstanceUIDInContainers.code
        }),
        mock.call({
            "item_id": item2.id,
            "code": errors.DuplicatedSeriesInstanceUIDInContainers.code
        }),
    ], any_order=True)


def test_new_series_instance_uids(db, detect_duplicates_task, create_uid, mocker):
    fw_mock = mock.Mock(spec=Flywheel)
    fw_mock.check_uids_exist.return_value = {"acquisitions": ["uid2"]}
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=fw_mock)

    container1 = db.create_container(path="path", level=T.ContainerLevel.acquisition, existing=False)
    container2 = db.create_container(path="path", level=T.ContainerLevel.acquisition, existing=False)
    container3 = db.create_container(path="path", level=T.ContainerLevel.acquisition, existing=True)

    item1 = db.create_item(container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)
    create_uid(db, item_id=item1.id, series_instance_uid="uid1", acquisition_container_id=container1.id)

    item2 = db.create_item(container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid2", acquisition_container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid2", acquisition_container_id=container2.id)
    create_uid(db, item_id=item2.id, series_instance_uid="uid2", acquisition_container_id=container2.id)

    item3 = db.create_item(container_id=container3.id)
    create_uid(db, item_id=item3.id, series_instance_uid="uid3", acquisition_container_id=container3.id)
    create_uid(db, item_id=item3.id, series_instance_uid="uid3", acquisition_container_id=container3.id)
    create_uid(db, item_id=item3.id, series_instance_uid="uid3", acquisition_container_id=container3.id)

    detect_duplicates_task.insert_errors = mock.Mock(spec=ingest_db_client.BatchWriter)
    detect_duplicates_task._check_new_acquisition_container_study_instance_uids()

    fw_mock.check_uids_exist.assert_called_once()
    _, args, _ = fw_mock.check_uids_exist.mock_calls[0]
    assert isinstance(args[0], ContainerUidcheck)

    assert set(["uid1", "uid2"]) == set(args[0]._acquisitions)
    assert args[0]._sessions is None

    assert detect_duplicates_task.insert_errors.push.call_count == 1
    detect_duplicates_task.insert_errors.push.assert_called_once_with(
        {
            "item_id": item2.id,
            "code": errors.SeriesInstanceUIDExists.code
        }
    )


def test_container_errors(db, detect_duplicates_task, create_uid, mocker):
    fw_mock = mock.Mock(spec=Flywheel)
    fw_mock.check_uids_exist.return_value = {"acquisitions": [], "sessions": []}
    mocker.patch("flywheel_cli.ingest.utils.get_sdk_client", return_value=fw_mock)

    group_container = db.create_container(path="group", level=T.ContainerLevel.group)
    project_container = db.create_container(path="group/project", level=T.ContainerLevel.project, parent_id=group_container.id)
    subject_container = db.create_container(path="group/project/subject", level=T.ContainerLevel.project, parent_id=project_container.id, error=True)
    session_container = db.create_container(path="group/project/subject/session", level=T.ContainerLevel.project, parent_id=subject_container.id)
    acquisition_container = db.create_container(path="group/project/subject/session/acquisition", level=T.ContainerLevel.project, parent_id=session_container.id)

    detect_duplicates_task._run()

    assert not db.client.get_container(group_container.id).error
    assert not db.client.get_container(project_container.id).error
    assert db.client.get_container(subject_container.id).error
    assert db.client.get_container(session_container.id).error
    assert db.client.get_container(acquisition_container.id).error
