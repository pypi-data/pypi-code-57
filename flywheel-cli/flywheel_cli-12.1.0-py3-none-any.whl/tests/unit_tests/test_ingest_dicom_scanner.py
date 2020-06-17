from datetime import datetime
from unittest import mock

import pytest

from flywheel_cli import util
from flywheel_cli.ingest import config
from flywheel_cli.ingest import errors
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.scanners import dicom
from .conftest import AttrDict, DummyWalker


@pytest.fixture(scope="function")
def dummy_scanner():
    scanner = dicom.DicomScanner(
        ingest_config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=None,
        worker_config=config.WorkerConfig(),
        walker=None,
        context={},
    )

    return scanner


@pytest.fixture(scope="function")
def data_for_session(mocker):
    dt = datetime(1900, 1, 2, 3, 4, 5)
    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", return_value=dt)

    context = {
        "subject": {
            "label": "subject_label"
        },
        "session": {
            "label": "session_label"
        }
    }

    dcm = DCMattr_dict({
        "StudyInstanceUID": "uid",
        "PatientID": "patient_id",
        "StudyDate": "study_date",
        "StudyTime": "study_time",
        "SeriesDate": "series_date",
        "SeriesTime": "series_time",
        "_manufacturer": "SIEMENS"
    })

    return context, dcm, dt


def test_determine_dicom_zipname():
    fname = dicom.DicomScanner.determine_dicom_zipname(
        filenames={"id1": "label.dicom.zip"},
        series_label="label1"
    )
    assert fname == "label1.dicom.zip"

    fname = dicom.DicomScanner.determine_dicom_zipname(
        filenames={"id1": "label.dicom.zip"},
        series_label="label"
    )
    assert fname == "label_dup-1.dicom.zip"

    fname = dicom.DicomScanner.determine_dicom_zipname(
        filenames={"id1": "label.dicom.zip", "id2": "label_dup-1.dicom.zip"},
        series_label="label"
    )
    assert fname == "label_dup-2.dicom.zip"


def test_extract_field(attr_dict):
    record = attr_dict({"key1": "value1", "key2": "VaLuE2", "key3": "  value3  "})

    value = dicom.DicomScanner.extract_field(
        record=record,
        fieldname="key"
    )
    assert value == ""

    value = dicom.DicomScanner.extract_field(
        record=record,
        fieldname="key1"
    )
    assert value == "value1"

    value = dicom.DicomScanner.extract_field(
        record=record,
        fieldname="key2"
    )
    assert value == "value2"

    value = dicom.DicomScanner.extract_field(
        record=record,
        fieldname="key3"
    )
    assert value == "value3"


def test_determine_session_label(dummy_scanner, attr_dict):
    # session.label
    label = dummy_scanner.determine_session_label(
        context=attr_dict({
            "session": {
                "label": "label_value"
            }
        }),
        _dcm=None,
        uid=None
    )
    assert label == "label_value"

    # timestamp
    label = dummy_scanner.determine_session_label(
        context=attr_dict({
            "session": {}
        }),
        _dcm=None,
        uid=None,
        timestamp=datetime(1900, 1, 2, 3, 4, 5)
    )
    assert label == "1900-01-02 03:04:05"

    # uid
    label = dummy_scanner.determine_session_label(
        context=attr_dict({}),
        _dcm=None,
        uid="uid"
    )
    assert label == "uid"


def test_determine_acquisition_label(dummy_scanner, attr_dict):
    # acquisition.label
    label = dummy_scanner.determine_acquisition_label(
        context=attr_dict({
            "acquisition": {
                "label": "label_value"
            }
        }),
        dcm=None,
        uid=None
    )
    assert label == "label_value"

    label = dummy_scanner.determine_acquisition_label(
        context=attr_dict({}),
        dcm=attr_dict({}),
        uid=None,
        timestamp=datetime(1900, 1, 2, 3, 4, 5)
    )
    assert label == "1900-01-02 03:04:05"

    label = dummy_scanner.determine_acquisition_label(
        context=attr_dict({}),
        dcm=attr_dict({}),
        uid="uid"
    )
    assert label == "uid"

    label = dummy_scanner.determine_acquisition_label(
        context=attr_dict({}),
        dcm=attr_dict({"SeriesDescription": "value"}),
        uid="uid",
        timestamp=datetime(1900, 1, 2, 3, 4, 5)
    )
    assert label == "value"


def test_determine_acquisition_timestamp(mocker, dummy_scanner):
    def dummy_timestamp(date, time, *args):
        return f"{date}-{time}"

    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", side_effect=dummy_timestamp)

    dcm = DCMattr_dict({
        "SeriesDate": "sdate",
        "SeriesTime": "stime",
        "AcquisitionDate": "adate",
        "AcquisitionTime": "atime"
    })
    # siemens
    dcm["_manufacturer"] = "SIEMENS"
    value = dummy_scanner.determine_acquisition_timestamp(dcm=dcm)
    assert value == "sdate-stime"

    # other manufacturer
    dcm["_manufacturer"] = "manufacturer"
    value = dummy_scanner.determine_acquisition_timestamp(dcm=dcm)
    assert value == "adate-atime"


def test_get_timestamp(mocker, dummy_scanner, attr_dict):
    dicom_mock = mocker.patch("flywheel_migration.dcm.DicomFile.timestamp")

    dummy_scanner.get_timestamp(
        dcm=attr_dict({"date": "datevalue", "time": "timevalue"}),
        date_key="date",
        time_key="time"
    )

    dicom_mock.assert_called_once_with(
        "datevalue",
        "timevalue",
        util.DEFAULT_TZ
    )


def test_get_value_no_deid_profile(dummy_scanner, attr_dict):
    dcm = attr_dict({"key": "value", "empty_value": "", "zero": 0})

    value = dummy_scanner.get_value(
        dcm=dcm,
        key="key"
    )
    assert value == "value"

    value = dummy_scanner.get_value(
        dcm=dcm,
        key="key1"
    )

    assert value is None

    value = dummy_scanner.get_value(
        dcm=dcm,
        key="key1",
        default="default"
    )
    assert value == "default"

    with pytest.raises(ValueError):
        value = dummy_scanner.get_value(
            dcm=dcm,
            key="key1",
            required=True
        )

    with pytest.raises(ValueError):
        value = dummy_scanner.get_value(
            dcm=dcm,
            key="empty_value",
            required=True
        )

    value = dummy_scanner.get_value(
        dcm=dcm,
        key="zero",
        required=True
    )
    assert value == 0


def test_get_value_with_deid_profile():
    # TODO
    pass


def test_scan(mocker, dummy_scanner):
    dcm = DCMattr_dict({
        "StudyInstanceUID": "study_uid",
        "PatientID": "patient_id",
        "StudyDate": "study_date",
        "StudyTime": "study_time",
        "SeriesDate": "series_date",
        "SeriesTime": "series_time",
        "_manufacturer": "SIEMENS",
        "SeriesInstanceUID": "seriesInstanceUid",
        "AcquisitionNumber": "12",
        "SOPInstanceUID": "sopInstanceUid"
    })
    timestamp = datetime(1900, 1, 2, 3, 4, 5)

    mock = mocker.patch("flywheel_cli.ingest.scanners.dicom.DicomFile", return_value=dcm)
    mock.timestamp.return_value = timestamp

    dummy_scanner.context = {
        "subject": {
            "label": "subject_label"
        },
        "session": {
            "label": "session_label"
        }
    }
    dummy_scanner.walker = DummyWalker(["file1.dcm"])

    items = list(dummy_scanner.scan("path"))

    assert len(dummy_scanner.sessions) == 1

    assert len(dummy_scanner.sessions["study_uid"].acquisitions) == 1
    assert len(items) == 1
    assert isinstance(items[0], T.ItemWithUIDs)
    item = items[0].item
    assert isinstance(item, T.ItemIn)
    assert item.dir == "path/file1.dcm"
    assert item.context == {
        "subject": {"label": "subject_label"},
        "session": {
            "uid": "study_uid",
            "label": "session_label",
            "timestamp": timestamp,
            "timezone": str(util.DEFAULT_TZ)
        },
        "acquisition": {
            "uid": "seriesInstanceUid_12",
            "label": "1900-01-02 03:04:05",
            "timestamp": timestamp,
            "timezone": str(util.DEFAULT_TZ)
        },
        "packfile": {
            "type": "dicom",
            "flatten": True
        }
    }
    assert len(items[0].uids) == 1
    uid = items[0].uids[0]
    assert isinstance(uid, T.UIDIn)
    assert uid.study_instance_uid == "study_uid"
    assert uid.series_instance_uid == "seriesInstanceUid"
    assert uid.sop_instance_uid == "sopInstanceUid"
    assert uid.acquisition_number == "12"
    assert uid.filename == "path/file1.dcm"
    assert uid.item_id == item.id


def test_scan_invalid_dicom(mocker, dummy_scanner):
    dcm_1 = DCMattr_dict({
        "StudyInstanceUID": "study_uid",
        "PatientID": "patient_id",
        "StudyDate": "study_date",
        "StudyTime": "study_time",
        "SeriesDate": "series_date",
        "SeriesTime": "series_time",
        "_manufacturer": "SIEMENS",
        "SeriesInstanceUID": "seriesInstanceUid",
        "SOPInstanceUID": "sopInstanceUid"
    })
    dcm_2 = DCMattr_dict({
        "SeriesInstanceUID": "seriesInstanceUid",
        "SOPInstanceUID": "sopInstanceUid"
    })
    timestamp = datetime(1900, 1, 2, 3, 4, 5)

    mock = mocker.patch("flywheel_cli.ingest.scanners.dicom.DicomFile", side_effect=[dcm_1, dcm_2])
    mock.timestamp.return_value = timestamp
    dummy_scanner.walker = DummyWalker(["file1.dcm", "file2.dcm"])

    items = list(dummy_scanner.scan("path"))
    assert len(items) == 2
    item = items[0]
    assert isinstance(item, T.ItemWithUIDs)
    assert isinstance(item.item, T.ItemIn)
    uids = item.uids
    assert isinstance(items[1], T.Error)
    error = items[1]
    assert error.code == errors.InvalidDicomFile.code
    assert error.message == "DICOM is missing StudyInstanceUID"
    assert error.filepath == "path/file2.dcm"


def test_scan_dicom_file(mocker, dummy_scanner):

    dcm = DCMattr_dict({
        "StudyInstanceUID": "uid",
        "PatientID": "patient_id",
        "StudyDate": "study_date",
        "StudyTime": "study_time",
        "SeriesDate": "series_date",
        "SeriesTime": "series_time",
        "_manufacturer": "SIEMENS",
        "SeriesInstanceUID": "seriesInstanceUid",
        "SOPInstanceUID": "sopInstanceUid"
    })
    timestamp = datetime(1900, 1, 2, 3, 4, 5)

    mock = mocker.patch("flywheel_cli.ingest.scanners.dicom.DicomFile", return_value=dcm)
    mock.timestamp.return_value = timestamp

    dummy_scanner.context = {
        "subject": {
            "label": "subject_label"
        },
        "session": {
            "label": "session_label"
        }
    }

    dummy_scanner.scan_dicom_file("path/file.dcm", None, [], 123)

    assert len(dummy_scanner.sessions) == 1
    assert len(dummy_scanner.sessions["uid"].acquisitions) == 1
    assert dummy_scanner.sessions["uid"].acquisitions["seriesInstanceUid"].context == {
        "acquisition": {
            "uid": "seriesInstanceUid",
            "label": "1900-01-02 03:04:05",
            "timestamp": timestamp,
            "timezone": str(util.DEFAULT_TZ)
        }
    }


def test_resolve_session_without_subject_code_fn(dummy_scanner, data_for_session):

    session = dummy_scanner.resolve_session(
        context=data_for_session[0],
        dcm=data_for_session[1]
    )

    assert isinstance(session, dicom.DicomSession)
    assert session.context == {
        "session": {
            "uid": "uid",
            "label": "session_label",
            "timestamp": data_for_session[2],
            "timezone": str(util.DEFAULT_TZ)
        },
        "subject": {"label": "subject_label"}
    }

    assert session.acquisitions == {}
    assert session.secondary_acquisitions == {}
    assert len(dummy_scanner.sessions) == 1

    re_session = dummy_scanner.resolve_session(
        context=data_for_session[0],
        dcm=data_for_session[1]
    )
    assert len(dummy_scanner.sessions) == 1
    assert session == re_session


def test_resolve_acquisition_primary_no_related_acquisition(dummy_scanner, data_for_session):
    context = data_for_session[0]
    context["acquisition"] = {"label": "acquisition_label"}

    dcm = data_for_session[1]
    dcm["SeriesInstanceUID"] = "sid"

    acquisition = dummy_scanner.resolve_acquisition(
        context=context,
        dcm=dcm
    )

    assert isinstance(acquisition, dicom.DicomAcquisition)
    assert acquisition.context == {
        "acquisition": {
            "uid": "sid",
            "label": "acquisition_label",
            "timestamp": data_for_session[2],
            "timezone": str(util.DEFAULT_TZ)
        }
    }

    assert acquisition.files == {}
    assert acquisition.filenames == {}
    assert len(dummy_scanner.sessions["uid"].acquisitions) == 1
    assert len(dummy_scanner.sessions["uid"].secondary_acquisitions) == 0
    assert dummy_scanner.sessions["uid"].acquisitions["sid"] == acquisition

    re_acquisition = dummy_scanner.resolve_acquisition(
        context=context,
        dcm=dcm
    )

    assert re_acquisition == acquisition
    assert len(dummy_scanner.sessions["uid"].acquisitions) == 1
    assert len(dummy_scanner.sessions["uid"].secondary_acquisitions) == 0
    assert dummy_scanner.sessions["uid"].acquisitions["sid"] == re_acquisition


def test_resolve_acquisition_related_acquisition(dummy_scanner, data_for_session):
    context = data_for_session[0]
    context["acquisition"] = {"label": "acquisition_label"}

    dcm = data_for_session[1]
    dcm["SeriesInstanceUID"] = "sid"
    dcm["ReferencedFrameOfReferenceSequence"] = [{
        "RTReferencedStudySequence": [{
            "RTReferencedSeriesSequence": [{
                "SeriesInstanceUID": "sid2"
            }]
        }]
    }]
    dummy_scanner.related_acquisitions = True

    acquisition = dummy_scanner.resolve_acquisition(
        context=context,
        dcm=dcm
    )

    assert isinstance(acquisition, dicom.DicomAcquisition)
    assert acquisition.context == {
        "acquisition": {
            "uid": "sid2",
            "label": "acquisition_label",
            "timestamp": data_for_session[2],
            "timezone": str(util.DEFAULT_TZ)
        }
    }

    assert acquisition.files == {}
    assert acquisition.filenames == {}
    assert len(dummy_scanner.sessions["uid"].acquisitions) == 0
    assert len(dummy_scanner.sessions["uid"].secondary_acquisitions) == 1
    assert dummy_scanner.sessions["uid"].secondary_acquisitions["sid2"] == acquisition


def test_resolve_session_with_subject_code_fn(mocker, attr_dict):
    dt = datetime(1900, 1, 2, 3, 4, 5)
    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", return_value=dt)

    subject_map = {}

    def subject_fn(fields):
        key = ''.join(fields)
        return subject_map.setdefault(key, len(subject_map))

    fn = mock.Mock(side_effect=subject_fn)

    dcm = DCMattr_dict({
        "StudyInstanceUID": "uid",
        "PatientID": "patient_id1",
        "PatientName": "patient_name1",
        "StudyDate": "study_date",
        "StudyTime": "study_time",
        "SeriesDate": "series_date",
        "SeriesTime": "series_time",
        "_manufacturer": "SIEMENS"
    })

    scanner = dicom.DicomScanner(
        ingest_config=config.IngestConfig(
            src_fs="/tmp",
            subject_config=config.SubjectConfig(
                code_serial=1,
                code_format="ex{SubjectCode}",
                map_keys=[
                    'PatientID',
                    "PatientName"
                ]
            )
        ),
        strategy_config=None,
        worker_config=config.WorkerConfig(),
        walker=None,
        get_subject_code_fn=fn
    )

    session = scanner.resolve_session(
        context=attr_dict({}),
        dcm=dcm
    )

    assert session.context == {
        'session': {
            'uid': 'uid',
            'label': '1900-01-02 03:04:05',
            'timestamp': dt,
            'timezone': str(util.DEFAULT_TZ)
        },
        'subject': {'label': 0}
    }

    assert subject_map['patient_id1patient_name1'] == 0
    fn.assert_called_once_with(['patient_id1', 'patient_name1'])


def test_resolve_session_patient_id(mocker, attr_dict):
    dt = datetime(1900, 1, 2, 3, 4, 5)
    mocker.patch("flywheel_migration.dcm.DicomFile.timestamp", return_value=dt)

    dcm = DCMattr_dict({
        "StudyInstanceUID": "uid",
        "PatientID": "patient_id1",
        "PatientName": "patient_name1",
        "StudyDate": "study_date",
        "StudyTime": "study_time",
        "SeriesDate": "series_date",
        "SeriesTime": "series_time",
        "_manufacturer": "SIEMENS"
    })

    scanner = dicom.DicomScanner(
        ingest_config=config.IngestConfig(src_fs="/tmp"),
        strategy_config=None,
        worker_config=config.WorkerConfig(),
        walker=None,
    )

    session = scanner.resolve_session(
        context=attr_dict({}),
        dcm=dcm
    )

    assert session.context == {
        'session': {
            'uid': 'uid',
            'label': '1900-01-02 03:04:05',
            'timestamp': dt,
            'timezone': str(util.DEFAULT_TZ)
        },
        'subject': {'label': 'patient_id1'}
    }


class DCMattr_dict(AttrDict):
    def get_manufacturer(self):
        return getattr(self, "_manufacturer")
