from unittest import mock

from flywheel_migration.deidentify import DeIdProfile
import pytest

from flywheel_cli.ingest import deid, errors, schemas


def test_deid_logger_write_entry():
    write_func = mock.Mock()
    logger = deid.DeidLogger(write_func)
    logger.write_entry(
        {"path": "path/to/1.dcm", "type": "before", "PatientName": "Name",}
    )
    assert list(logger.temp_logs["path/to/1.dcm"].keys()) == ["PatientName"]
    write_func.assert_not_called()
    logger.write_entry(
        {"path": "path/to/1.dcm", "type": "after", "PatientName": "-",}
    )
    assert not logger.temp_logs.get("path/to/1.dcm")

    write_func.assert_called_once()
    _, args, _ = write_func.mock_calls[0]
    assert len(args) == 1
    assert isinstance(args[0], schemas.DeidLogIn)
    assert args[0].src_path == "path/to/1.dcm"
    assert args[0].tags_before["PatientName"] == "Name"
    assert args[0].tags_after["PatientName"] == "-"


def test_load_deid_profile(attr_dict):
    profile = deid.load_deid_profile(
        profile_name="test_profile",
        profiles=[
            attr_dict(
                {
                    "name": "test_profile",
                    "description": "test_profile",
                    "dicom": {
                        "fields": [
                            {"name": "PatientBirthDate", "remove": True},
                            {"name": "PatientName", "remove": True},
                            {"name": "PatientID", "remove": False},
                        ]
                    },
                }
            )
        ],
    )

    assert isinstance(profile, DeIdProfile)
    assert profile.name == "test_profile"


def test_load_deid_profile_invalid_raise(attr_dict):
    with pytest.raises(errors.InvalidDeidProfile) as execinfo:
        deid.load_deid_profile(
            profile_name="test_profile",
            profiles=[
                attr_dict(
                    {
                        "name": "test_profile",
                        "description": "test_profile",
                        "dicom": {"fields": [{"name": "invalid key", "remove": True},]},
                    }
                )
            ],
        )

    # message
    assert "invalid deid profile" in str(execinfo.value).lower()
    # error
    assert "invalid key" in str(execinfo.value).lower()


def test_load_deid_profile_default():
    profile = deid.load_deid_profile(profile_name="minimal", profiles=[])

    assert isinstance(profile, DeIdProfile)
    assert profile.name == "minimal"


def test_load_deid_profile_default_name():
    profile = deid.load_deid_profile(profile_name=None, profiles=[])

    assert isinstance(profile, DeIdProfile)
    assert profile.name == "minimal"


def test_load_deid_profile_unknown_name_raise():
    with pytest.raises(errors.InvalidDeidProfile) as execinfo:
        deid.load_deid_profile(profile_name="non_existing", profiles=[])

    assert "unknown deid profile" in str(execinfo.value).lower()
