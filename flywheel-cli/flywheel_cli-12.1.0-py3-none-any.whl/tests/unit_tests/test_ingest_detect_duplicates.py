"""Ingest DetectDuplicatesTask tests"""

from uuid import uuid4
from unittest import mock

from flywheel import Flywheel

from flywheel_cli.ingest import detect_duplicates, errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.client import db as db_client


# Item errors

def test_detect_study_instance_uid_conflicts_in_item_ok():
    """ one item, all uid@study_instance_uid is the same """
    item = T.ItemIn(
        id=uuid4(),
        dir="dir",
        type="file",
        files_cnt=2,
        bytes_sum=1,
        files=["file1", "file2"]
    )

    uids = [
        T.UIDIn(
            item_id=item.id,
            filename="file1",
            study_instance_uid="uid1",
            series_instance_uid="uid2",
            sop_instance_uid="uid3"
        ),
        T.UIDIn(
            item_id=item.id,
            filename="file2",
            study_instance_uid="uid1",
            series_instance_uid="uid2",
            sop_instance_uid="uid3"
        )
    ]

    insert_error = mock.Mock(spec=db_client.BatchWriter)

    ret = detect_duplicates.detect_uid_conflicts_in_item(item, uids, insert_error)

    assert ret

    insert_error.push.assert_not_called()


def test_detect_study_instance_uid_conflicts_in_item_error():
    """ one item, different uid@study_instance_uid """
    item = T.ItemIn(
        id=uuid4(),
        dir="dir",
        type="file",
        files_cnt=1,
        bytes_sum=1,
        files=["file1", "file2"]
    )

    uids = [
        T.UIDIn(
            item_id=item.id,
            filename="file1",
            study_instance_uid="uid",
            series_instance_uid="sid",
            sop_instance_uid="uid3"
        ),
        T.UIDIn(
            item_id=item.id,
            filename="file2",
            study_instance_uid="uid1",
            series_instance_uid="sid",
            sop_instance_uid="uid3"
        )
    ]

    insert_error = mock.Mock(spec=db_client.BatchWriter)

    ret = detect_duplicates.detect_uid_conflicts_in_item(item, uids, insert_error)

    assert not ret

    assert insert_error.push.call_count == 1
    insert_error.push.assert_called_once_with(
        {
            "item_id": item.id,
            "code": errors.DifferentStudyInstanceUID.code
        }
    )


def test_detect_series_instance_uid_conflicts_in_item_error():
    """ one item, same uid@series_instance_uid """
    item = T.ItemIn(
        id=uuid4(),
        dir="dir",
        type="file",
        files_cnt=1,
        bytes_sum=1,
        files=["file1", "file2"]
    )

    uids = [
        T.UIDIn(
            item_id=item.id,
            filename="file1",
            study_instance_uid="sid",
            series_instance_uid="uid",
            sop_instance_uid="uid3"
        ),
        T.UIDIn(
            item_id=item.id,
            filename="file2",
            study_instance_uid="sid",
            series_instance_uid="uid1",
            sop_instance_uid="uid3"
        )
    ]

    insert_error = mock.Mock(spec=db_client.BatchWriter)

    ret = detect_duplicates.detect_uid_conflicts_in_item(item, uids, insert_error)

    assert not ret

    assert insert_error.push.call_count == 1
    insert_error.push.assert_called_once_with(
        {
            "item_id": item.id,
            "code": errors.DifferentSeriesInstanceUID.code
        }
    )
