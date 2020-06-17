from datetime import datetime
from unittest import mock

import pytest

from flywheel_cli import util


@pytest.fixture
def mocked_files():
    class TestFile:
        def __init__(self, name):
            self.name = name
            self.size = len(self.name)

    files = [TestFile(name) for name in ("a/b/c", "a/b/d", "a/e", "f",)]
    return files


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("test.dcm", True),
        ("test.DCM", True),
        ("test.dicom", True),
        ("test.DICOM", True),
        ("test.dcm.gz", True),
        ("test.DCM.GZ", True),
        ("test.dicom.gz", True),
        ("test.DICOM.GZ", True),
        ("/full/path/to/test.dcm", True),
        ("", False),
        ("/", False),
        ("/test.txt", False),
        ("/dcm.test", False),
        ("test.dcminst", False),
        ("test.dcm.zip", False),
    ],
)
def test_is_dicom_file(filename, expected):
    assert util.is_dicom_file(filename) == expected


def test_key_with_options():
    # Raises key error if key is missing
    with pytest.raises(KeyError):
        util.KeyWithOptions({})

    # String value
    opts = util.KeyWithOptions("value")
    assert opts.key == "value"
    assert opts.config == {}

    # Other value types
    opts = util.KeyWithOptions(4.2)
    assert opts.key == 4.2
    assert opts.config == {}

    # Dictionary with options
    opts = util.KeyWithOptions({"name": "Test Name", "option": 8.0})
    assert opts.key == "Test Name"
    assert opts.config == {"option": 8.0}

    # Dictionary with key override
    opts = util.KeyWithOptions({"pattern": "Test Pattern",}, key="pattern")
    assert opts.key == "Test Pattern"
    assert opts.config == {}


def test_str_to_filename():
    assert util.str_to_filename("test ?_.dicom.zip") == "test _.dicom.zip"
    assert util.str_to_filename("test ?/.dicom.zip") == "test _.dicom.zip"
    assert util.str_to_filename("test-1?/**test.dicom.zip") == "test-1_test.dicom.zip"


def test_get_filepath_dir_exists(mocker):
    mocker.patch("flywheel_cli.util.os.path.isdir", side_effect=[True])
    datetime_mock = mocker.patch("flywheel_cli.util.datetime.datetime")
    datetime_mock.utcnow.return_value = datetime(1900, 1, 1, 0, 0, 0)
    mocker.patch("flywheel_cli.util.get_cli_version", return_value="0.1.0.test")
    assert util.get_filepath("foo/") == "foo/log-19000101-000000-0.1.0.test.csv"


def test_get_filepath_dir_not_exists(mocker):
    mocker.patch("flywheel_cli.util.os.path.isdir", side_effect=[False])
    with pytest.raises(FileNotFoundError):
        util.get_filepath("foo/")


def test_get_incremental_filename(mocker):
    mocker.patch(
        "flywheel_cli.util.os.path.isfile", side_effect=[True, False, True, False]
    )
    assert util.get_incremental_filename("foo") == "foo(1)"
    assert util.get_incremental_filename("foo/bar(1).txt") == "foo/bar(2).txt"


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (0, "0s"),
        (1, "1s"),
        (60, "1m"),
        (61, "1m 1s"),
        (3601, "1h"),
        (3660, "1h 1m"),
        (90000, "1d 1h"),
    ],
)
def test_hrtime(seconds, expected):
    assert util.hrtime(seconds) == expected


def test_create_missing_dirs_exists(mocker):
    makedirs_mock = mocker.patch("os.makedirs")

    with mock.patch("os.path.exists", return_value=True):
        util.create_missing_dirs("foo/bar")

    makedirs_mock.assert_not_called()


def test_create_missing_dirs_not_exists(mocker):
    makedirs_mock = mocker.patch("os.makedirs")

    with mock.patch("os.path.exists", return_value=False):
        util.create_missing_dirs("foo/bar")

    makedirs_mock.assert_called_once_with("foo")
