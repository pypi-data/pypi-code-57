import io
import os
import zipfile
from unittest import mock

import certifi
import flywheel_migration
import pytest
import pytz
from pydantic.error_wrappers import ValidationError

from flywheel_cli import util
from flywheel_cli.ingest import config
from .conftest import AttrDict

@pytest.fixture(scope="function")
def open_mock(mocker):
    file_mock = mock.MagicMock()
    file_mock.__enter__.return_value = io.BytesIO()

    o_mock = mocker.patch("flywheel_cli.ingest.config.open", return_value=file_mock)
    return o_mock

@pytest.fixture(scope="function")
def file_exists_mock(mocker):
    exists_mock = mocker.patch("flywheel_cli.ingest.config.os.path.exists", return_value=True)
    return exists_mock

def test_read_config_file_not_existing(mocker):
    exists_mock = mocker.patch("flywheel_cli.ingest.config.os.path.exists", return_value=False)
    ret = config.read_config_file("path")

    assert ret is None
    exists_mock.assert_called_once_with("path")


def test_read_config_file_yaml_invalid(open_mock, file_exists_mock):
    f = io.StringIO("\"a invalid YAML")
    open_mock.return_value.__enter__.return_value = f

    with pytest.raises(config.ConfigError) as execinfo:
        config.read_config_file("random/path.yaml")

    assert "Unable to parse YAML config file:" in str(execinfo.value)

def test_read_config_file_yaml_valid(open_mock, file_exists_mock):
    f = io.StringIO("- sample string\n- second line")
    open_mock.return_value.__enter__.return_value = f

    cfg = config.read_config_file("random/path.yaml")
    assert cfg == [
        "sample string",
        "second line"
    ]

def test_read_config_file_yml_extension_valid(open_mock, file_exists_mock):
    f = io.StringIO("- sample string\n- second line")
    open_mock.return_value.__enter__.return_value = f

    cfg = config.read_config_file("random/path.yml")
    assert cfg == [
        "sample string",
        "second line"
    ]

def test_read_config_file_json_invalid(open_mock, file_exists_mock):
    f = io.StringIO("{a invalid JSON")
    open_mock.return_value.__enter__.return_value = f

    with pytest.raises(config.ConfigError) as execinfo:
        config.read_config_file("random/path.json")

    assert "Unable to parse JSON file:" in str(execinfo.value)

def test_read_config_file_json_valid(open_mock, file_exists_mock):
    f = io.StringIO("{\"key\": \"value\"}")
    open_mock.return_value.__enter__.return_value = f

    cfg = config.read_config_file("random/path.json")
    assert cfg == {"key": "value"}

def test_read_config_file_invalid_extension(file_exists_mock):
    with pytest.raises(config.ConfigError) as execinfo:
        config.read_config_file("random/path.io")

    assert "Only YAML and JSON files are supported" in str(execinfo.value)

def test_load_config_default(mocker):
    read_config_file_mock = mocker.patch("flywheel_cli.ingest.config.read_config_file", return_value=None)
    args = AttrDict({}, allow_default=True)
    ret = config.load_config(
        cls=config.GeneralConfig,
        args=args
    )

    assert isinstance(ret, config.GeneralConfig)

    # assert default keys
    cfg = dict(config.GeneralConfig())
    cfg2 = dict(ret)
    for key in cfg:
        assert cfg[key] == cfg2[key]

    filename = cfg2["config_file"]
    assert filename.endswith(".config/flywheel/cli.yml")
    read_config_file_mock.assert_called_once_with(filename)

def test_load_config_no_config_file(mocker):
    read_config_file_mock = mocker.patch("flywheel_cli.ingest.config.read_config_file", return_value=None)
    args = AttrDict({"no_config": True}, allow_default=True)
    ret = config.load_config(
        cls=config.GeneralConfig,
        args=args
    )

    assert isinstance(ret, config.GeneralConfig)

    # assert default keys
    cfg = dict(config.GeneralConfig())
    cfg2 = dict(ret)

    for key in cfg:
        if key == "no_config":
            assert cfg2[key]
        else:
            assert cfg[key] == cfg2[key]

    filename = cfg2["config_file"]
    assert filename.endswith(".config/flywheel/cli.yml")
    read_config_file_mock.assert_not_called()

def test_load_config_value_order(mocker, open_mock, file_exists_mock):
    # order:
    # args
    # config->snake_name
    # config->dash_name
    cfg_init_mock = mocker.patch("flywheel_cli.ingest.config.IngestConfig.__init__", return_value=None)

    f = io.StringIO(
        "src_fs: 2\n"
        "src-fs: 3\n"
        "compression_level: 10\n"
        "compression-level: 20\n"
        "ignore_unknown_tags: true\n"
        "ignore-unknown-tags: true\n"
        "de_identify: false\n"
        "de-identify: false\n"
        "skip_existing: null\n"
        "skip-existing: true\n"
    )
    open_mock.return_value.__enter__.return_value = f

    args = AttrDict({
        "src_fs": "1",
        "compression_level": None,
        "ignore_unknown_tags": False,
        "de_identify": None,
        "config_file": "config.yaml"
        },
        allow_default=True
    )

    config.load_config(
        cls=config.IngestConfig,
        args=args
    )

    cfg_init_mock.assert_called_once_with(
        compression_level=10,
        de_identify=False,
        ignore_unknown_tags=False,
        skip_existing=True,
        src_fs="1"
    )

def test_add_arguments():
    class DummyConfig(config.BaseConfig):
        param1: bool
        param2: str
        param3: bool = False
        param4: str = "default"

        class ArgparserConfig:
            param1 = {
                "positional": True,
                "nargs": "?",
                "metavar": "param1",
                "help": "param1 value",
            }
            param2 = {
                "positional": False,
                "nargs": "??",
                "metavar": "param2",
                "help": "param2 value",
            }
            param3 = {
                "flags": ["-p", "--param3"],
                "group": "logging",
                "help": "param3 value",
            }
            param4 = {
                "flags": ["-x", "--param4"],
                "help": "param4 value",
            }

    cfg = DummyConfig
    parser = mock.Mock()
    config.add_arguments(cfg, parser)

    assert parser.mock_calls == [
        mock.call.add_argument(
            "param1",
            action="store_true",
            help="param1 value",
            metavar="param1",
            nargs="?"
        ),
        mock.call.add_argument(
            "--param2",
            dest="param2",
            help="param2 value",
            metavar="param2",
            nargs="??"
        ),
        mock.call.add_argument(
            "-p",
            "--param3",
            action="store_true",
            dest="param3",
            help="param3 value (default: False)"
        ),
        mock.call.add_argument(
            "-x",
            "--param4",
            dest="param4",
            help="param4 value (default: default)"
        )
    ]

# GeneralConfig
def test_general_config_get_api_key_not_logged_in(mocker):
    mocker.patch("flywheel_cli.ingest.config.sdk_impl.load_config", return_value=None)
    with pytest.raises(Exception):
        config.GeneralConfig.get_api_key()

def test_general_config_get_api_key_logged_in(mocker):
    mocker.patch("flywheel_cli.ingest.config.sdk_impl.load_config", return_value={"key": "apikey"})
    key = config.GeneralConfig.get_api_key()
    assert key == "apikey"

def test_general_config_configure_ca_certs():
    cfg = config.GeneralConfig(
        ca_certs="some_cert"
    )

    cfg.configure_ca_certs()

    assert certifi.where() == "some_cert"

def test_general_config_configure_timezone():
    tz = pytz.timezone('Europe/Amsterdam')

    cfg = config.GeneralConfig(
        timezone="Europe/Amsterdam"
    )

    cfg.configure_timezone()

    assert flywheel_migration.util.DEFAULT_TZ == tz
    assert util.DEFAULT_TZ == tz
    assert os.environ["TZ"] == "Europe/Amsterdam"

def test_general_config_configure_timezone_raise():
    cfg = config.GeneralConfig(
        timezone="timezone_param"
    )

    with pytest.raises(config.ConfigError):
        cfg.configure_timezone()

def test_general_config_configure_timezone_noop():
    cfg = config.GeneralConfig(
        timezone=None
    )

    default_tz = flywheel_migration.util.DEFAULT_TZ
    del os.environ["TZ"]

    cfg.configure_timezone()

    assert flywheel_migration.util.DEFAULT_TZ == default_tz
    assert util.DEFAULT_TZ == default_tz
    assert "TZ" not in os.environ

def test_general_config_startup_initialize(mocker):
    ca_mock = mocker.patch("flywheel_cli.ingest.config.GeneralConfig.configure_ca_certs")
    timezone_mock = mocker.patch("flywheel_cli.ingest.config.GeneralConfig.configure_timezone")

    cfg = config.GeneralConfig()
    cfg.startup_initialize()

    ca_mock.assert_called_once()
    timezone_mock.assert_called_once()

def test_general_config_exclusive_logging_flags_raise():
    config.GeneralConfig(
        debug=True
    )

    with pytest.raises(ValueError):
        config.GeneralConfig(
            debug=True,
            quiet=True
        )

# ManageConfig
def test_manage_config_properties():
    cfg = config.ManageConfig(
        ingest_url="some_host/ingests/a1234567-a123-a123-a123-a12345678901"
    )

    assert cfg.ingest_url == {
        "cluster": "some_host",
        "ingest_id": "a1234567-a123-a123-a123-a12345678901"
    }

    assert cfg.cluster == "some_host"
    assert cfg.ingest_id == "a1234567-a123-a123-a123-a12345678901"

def test_manage_config_validate_ingest_url_from_config_raise(mocker):
    mocker.patch("flywheel_cli.ingest.config.read_config_file", return_value={"ingest_operation_url": {"key": "value"}})

    with pytest.raises(ValueError):
        config.ManageConfig()

def test_manage_config_validate_ingest_url_from_config(mocker):
    val = {
        "cluster": "some_host",
        "ingest_id": "a1234567-a123-a123-a123-a12345678901"
    }
    mocker.patch("flywheel_cli.ingest.config.read_config_file", return_value={"ingest_operation_url": val})

    cfg = config.ManageConfig()

    assert cfg.ingest_url == val
    assert cfg.cluster == val["cluster"]
    assert cfg.ingest_id == val["ingest_id"]

# ClusterConfig
def test_cluster_config_save_ingest_operation_url_raise():
    with pytest.raises(config.ConfigError):
        cfg = config.ClusterConfig()
        cfg.save_ingest_operation_url("id")

def test_cluster_config_save_ingest_operation_url(open_mock, mocker):
    f = io.StringIO()
    open_mock.return_value.__enter__.return_value = f
    mocker.patch("flywheel_cli.ingest.config.os.makedirs")

    cfg = config.ClusterConfig(
        cluster="cluster/url"
    )
    url = cfg.save_ingest_operation_url("id")

    assert f.getvalue().strip() == "ingest_operation_url: cluster/url/ingests/id"
    assert url == "cluster/url/ingests/id"

# IngestConfig
def test_ingest_config_validate_compression_level():
    def assert_valid(level):
        cfg = config.IngestConfig(
            src_fs="path",
            compression_level=level
        )
        assert cfg.compression_level == level

    def assert_invalid(level):
        with pytest.raises(ValidationError):
            config.IngestConfig(
                src_fs="path",
                compression_level=level
            )

    # valid -1..8 (inclusive)
    assert_valid(-1)
    assert_valid(8)

    #invalid
    assert_invalid(-2)
    assert_invalid(9)

def test_ingest_config_create_walker_partial_args(mocker):
    walker_mock = mocker.patch("flywheel_cli.ingest.config.walker.create_walker")
    cfg = config.IngestConfig(
        src_fs="/tmp"
    )
    cfg.create_walker()

    walker_mock.assert_called_once_with(
        "/tmp",
        exclude=None,
        exclude_dirs=None,
        include=None,
        include_dirs=None,
        follow_symlinks=False,
    )

def test_ingest_config_create_walker_full_args(mocker):
    walker_mock = mocker.patch("flywheel_cli.ingest.config.walker.create_walker")
    cfg = config.IngestConfig(
        src_fs="/tmp",
        include=["include"],
        exclude=["exclude"],
        include_dirs=["include_dirs"],
        exclude_dirs=["exclude_dirs"],
        symlinks=True
    )
    cfg.create_walker()

    walker_mock.assert_called_once_with(
        "/tmp",
        exclude=["exclude"],
        exclude_dirs=["exclude_dirs"],
        include=["include"],
        include_dirs=["include_dirs"],
        follow_symlinks=True,
    )

def test_ingest_config_register_encoding_aliases(mocker):
    encoding_mock = mocker.patch("encodings.aliases.aliases")
    cfg = config.IngestConfig(
        src_fs="path",
        encodings=["a=b", "c=d"]
    )

    cfg.register_encoding_aliases()
    assert encoding_mock.mock_calls == [
        mock.call.__setitem__("a", "b"),
        mock.call.__setitem__("c", "d")
    ]

def test_ingest_config_get_compression_type_zero():
    cfg = config.IngestConfig(
        src_fs="path",
        compression_level=0
    )
    compresion = cfg.get_compression_type()
    assert compresion == zipfile.ZIP_STORED

def test_ingest_config_get_compression_type_not_zero():
    cfg = config.IngestConfig(
        src_fs="path",
        compression_level=5
    )
    compresion = cfg.get_compression_type()
    assert compresion == zipfile.ZIP_DEFLATED

# WorkerConfig
def test_worker_config_db_url_none(mocker):
    mocker.patch("flywheel_cli.ingest.config.os.urandom", return_value=b"random")
    cfg = config.WorkerConfig()

    assert cfg.db_url.endswith("flywheel_cli_ingest_72616e646f6d.db")

def test_worker_config_db_url_not_none():
    cfg = config.WorkerConfig(
        db_url="sqlite:///random_path.db"
    )

    assert cfg.db_url == "sqlite:///random_path.db"

# DicomConfig
def test_dicom_config_invalid_group_id():
    with pytest.raises(ValidationError):
        config.DicomConfig(
            group="$groupid",
            project="projectid"
        )
