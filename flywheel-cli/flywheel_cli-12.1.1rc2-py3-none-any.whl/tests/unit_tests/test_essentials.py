import datetime as dt
import io
import sys
from unittest.mock import Mock, call

import crayons
import flywheel
import pytest
from flywheel.models import (
    ContainerGroupOutput as Group,
    ContainerProjectOutput as Project,
    ContainerSubjectOutput as Subject,
    ContainerSessionOutput as Session,
    ContainerAcquisitionOutput as Acquisition,
    ContainerFileOutput as File,
    PermissionAccessPermission as Permission,
)

from flywheel_cli.commands import essentials
from flywheel_cli.config import Config


class SysExitMock(Exception):
    pass


@pytest.fixture(scope="function")
def abspath_mock(mocker):
    def _abspath(path):
        return f"/{path.lstrip('/')}"

    return mocker.patch("os.path.abspath", side_effect=_abspath)


@pytest.fixture(scope="function")
def mocks_for_download(mocker, abspath_mock):
    args_mock = Mock(
        spec=["src", "output", "include", "exclude", "config"], src="fw://foo/bar"
    )
    args_mock.config = Mock(spec=Config)
    args_mock.config.assume_yes = True

    fw_mock = mocker.patch.object(
        essentials.sdk_impl, "create_flywheel_client"
    ).return_value
    fw_mock.resolve.return_value.path = [
        Group(),
        Project(id="p_id", label="project label"),
    ]
    fw_mock.create_download_ticket.return_value = {
        "size": 99,
        "file_cnt": 2,
        "ticket": "ticket_id",
    }

    class Mocks:
        fw = fw_mock
        process_download = mocker.patch.object(essentials, "process_download")
        confirmation_prompt = mocker.patch.object(
            essentials.util, "confirmation_prompt"
        )
        abspath = abspath_mock
        args = args_mock
        create_missing_dirs = mocker.patch.object(
            essentials.util, "create_missing_dirs"
        )
        get_incremental_filename = mocker.patch.object(
            essentials.util, "get_incremental_filename"
        )
        get_single_file_download_fn = mocker.patch.object(
            essentials, "get_single_file_download_fn"
        )
        exit = mocker.patch("sys.exit", side_effect=SysExitMock)

    return Mocks


@pytest.fixture(scope="function")
def mocks_for_download_file(mocker, abspath_mock):
    fw_mock = mocker.patch.object(
        essentials.sdk_impl, "create_flywheel_client"
    ).return_value
    fw_mock.resolve.return_value.path = [
        Group(),
        Project(id="p_id", label="project label"),
        File(id="f_id", name="foobar.txt"),
    ]

    class Mocks:
        abspath = abspath_mock
        fw = fw_mock
        create_missing_dirs = mocker.patch.object(
            essentials.util, "create_missing_dirs"
        )
        get_single_file_download_fn = mocker.patch.object(
            essentials, "get_single_file_download_fn"
        )
        process_download = mocker.patch.object(essentials, "process_download")
        exit = mocker.patch("sys.exit", side_effect=SysExitMock)

    return Mocks


@pytest.mark.parametrize(
    "parent_cont,filename",
    [
        (Project(), "foo"),
        (Subject(), "foo"),
        (Session(), "foo"),
        (Acquisition(), "foo"),
    ],
)
def test_get_single_file_download_fn(parent_cont, filename):
    fw = flywheel.Client("foo:bar")

    fn = essentials.get_single_file_download_fn(fw, parent_cont, filename)

    assert callable(fn)
    assert fn.args == (parent_cont.id, filename)
    assert fn.keywords == {"_return_http_data_only": True, "_preload_content": False}


def test_write_stream_to_file():
    def iter_content_mock(*args, **kwargs):
        yield b"foo"
        yield b"bar"

    resp_mock = Mock(
        spec=["iter_content", "close"],
        **{"iter_content.side_effect": iter_content_mock},
    )
    download_fn = Mock(return_value=resp_mock)
    dest = io.BytesIO()

    essentials.write_stream_to_file(download_fn, dest)
    dest.seek(0)
    assert dest.read() == b"foobar"
    resp_mock.close.assert_called_once()


def test_write_stream_to_file_close_exception():
    class TestException(Exception):
        pass

    resp_mock = Mock(
        spec=["iter_content", "close"], **{"iter_content.side_effect": TestException}
    )
    download_fn = Mock(return_value=resp_mock)
    dest = io.BytesIO()

    with pytest.raises(TestException):
        essentials.write_stream_to_file(download_fn, dest)
    resp_mock.close.assert_called_once()


def test_process_download_to_stdout(mocker, capsys):
    write_stream_mock = mocker.patch.object(
        essentials, "write_stream_to_file", return_value=99
    )

    essentials.process_download("download_fn", "foobar.txt", sys.stdout)
    write_stream_mock.assert_called_once_with("download_fn", sys.stdout.buffer)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ("Downloading foobar.txt... DONE\n" "Wrote 99B\n")


def test_process_download_to_file(mocker, capsys):
    open_mock = mocker.patch.object(essentials, "open")
    write_stream_mock = mocker.patch.object(
        essentials, "write_stream_to_file", return_value=99
    )

    essentials.process_download("download_fn", "foobar.txt", "foobar.txt")
    write_stream_mock.assert_called_once_with("download_fn", open_mock().__enter__())
    captured = capsys.readouterr()
    assert captured.out == (
        "Downloading foobar.txt... DONE\n" "Wrote 99B to foobar.txt\n"
    )
    assert captured.err == ""


def test_download_container_to_stdout(mocks_for_download, capsys):
    mocks = mocks_for_download
    mocks.args.output = essentials.STDOUT
    mocks.args.prefix = "scitran"
    mocks.args.config.assume_yes = False

    essentials.download(mocks.args)

    mocks.get_incremental_filename.assert_not_called()
    mocks.create_missing_dirs.assert_not_called()
    mocks.confirmation_prompt.assert_not_called()
    assert mocks.fw.create_download_ticket.call_args[1] == {"prefix": "scitran"}
    download_request = mocks.fw.create_download_ticket.call_args[0][0]
    assert len(download_request.nodes) == 1
    assert download_request.nodes[0].level == "project"
    assert download_request.nodes[0].id == "p_id"
    assert len(download_request.filters) == 1
    download_filter = download_request.filters[0]
    assert download_filter.types.plus == mocks.args.include
    assert download_filter.types.minus == mocks.args.exclude
    args, _ = mocks.process_download.call_args
    download_fn = args[0]
    assert callable(download_fn)
    assert download_fn.args == ("ticket_id",)
    assert download_fn.keywords == {
        "_return_http_data_only": True,
        "_preload_content": False,
    }
    assert args[1] == "project label"
    assert args[2] == essentials.sys.stdout

    captured = capsys.readouterr()
    assert captured.err == "This download will be about 99B comprising 2 files.\n"


def test_download_container_to_file_assume_yes(mocks_for_download, capsys):
    mocks = mocks_for_download
    mocks.args.output = "foobar.tar"
    mocks.args.prefix = None
    mocks.args.config.assume_yes = True

    essentials.download(mocks.args)

    mocks.confirmation_prompt.assert_not_called()
    mocks.process_download.assert_called_once()
    captured = capsys.readouterr()
    assert captured.out == "This download will be about 99B comprising 2 files.\n"
    assert captured.err == ""


def test_download_container_to_file_prompt_confirm(mocks_for_download, capsys):
    mocks = mocks_for_download
    mocks.args.output = "foobar.tar"
    mocks.args.prefix = None
    mocks.args.config.assume_yes = False
    mocks.confirmation_prompt.return_value = True
    mocks.get_incremental_filename.return_value = "incremented"

    essentials.download(mocks.args)

    mocks.confirmation_prompt.assert_called_once_with("Continue?")
    args, _ = mocks.process_download.call_args
    assert args[2] == "incremented"
    captured = capsys.readouterr()
    assert captured.out == "This download will be about 99B comprising 2 files.\n"
    assert captured.err == ""


def test_download_container_to_file_prompt_cancel(mocks_for_download, capsys):
    mocks = mocks_for_download
    mocks.args.output = "foobar.tar"
    mocks.args.prefix = None
    mocks.args.config.assume_yes = False
    mocks.confirmation_prompt.return_value = False

    with pytest.raises(SysExitMock):
        essentials.download(mocks.args)

    mocks.confirmation_prompt.assert_called_once_with("Continue?")
    mocks.exit.assert_called_once_with(1)
    mocks.process_download.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out == "This download will be about 99B comprising 2 files.\n"
    assert captured.err == "Canceled\n"


def test_download_single_file_w_output_filename(mocks_for_download):
    mocks = mocks_for_download
    mocks.fw.resolve.return_value.path = [
        Group(),
        Project(id="p_id", label="label"),
        File(id="f_id", name="foobar.txt"),
    ]
    mocks.args.output = "out_foobar.txt"
    mocks.get_incremental_filename.return_value = "incremented"

    essentials.download(mocks.args)

    mocks.get_incremental_filename.assert_called_once_with("/out_foobar.txt")
    mocks.get_single_file_download_fn.assert_called_once_with(
        mocks.fw, mocks.fw.resolve.return_value.path[-2], "foobar.txt"
    )
    mocks.process_download.assert_called_once_with(
        mocks.get_single_file_download_fn.return_value, "foobar.txt", "incremented"
    )


def test_download_single_file_default_filename(mocks_for_download):
    mocks = mocks_for_download
    mocks.fw.resolve.return_value.path = [
        Group(),
        Project(id="p_id", label="label"),
        File(id="f_id", name="foobar.txt"),
    ]
    mocks.args.output = None
    mocks.get_incremental_filename.return_value = "incremented"

    essentials.download(mocks.args)

    mocks.abspath.assert_called_once_with("foobar.txt")
    mocks.get_incremental_filename.assert_called_once_with("/foobar.txt")
    mocks.create_missing_dirs.assert_called_once_with("incremented")
    args, _ = mocks.process_download.call_args
    assert args[2] == "incremented"


def test_download_container_default_filename(mocks_for_download):
    mocks = mocks_for_download
    mocks.args.output = None
    mocks.args.prefix = None
    mocks.get_incremental_filename.return_value = "incremented"

    essentials.download(mocks.args)

    mocks.abspath.assert_called_once_with("project label.tar")
    mocks.get_incremental_filename.assert_called_once_with("/project label.tar")
    mocks.create_missing_dirs.assert_called_once_with("incremented")
    args, _ = mocks.process_download.call_args
    assert args[2] == "incremented"


def test_download_resolve_error(mocks_for_download, capsys):
    class ResolveError(Exception):
        pass

    mocks = mocks_for_download
    mocks.fw.resolve.side_effect = ResolveError("404 Not found")

    with pytest.raises(SysExitMock):
        essentials.download(mocks.args)

    mocks.exit.assert_called_once_with(1)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "404 Not found\n\nCould not resolve source container\n"


def test_download_file(mocks_for_download_file):
    mocks = mocks_for_download_file

    essentials.download_file("fw://group/project label/files/foobar.txt", "dst.txt")

    mocks.fw.resolve.assert_called_once_with(
        ["group", "project label", "files", "foobar.txt"]
    )
    mocks.abspath.assert_called_once_with("dst.txt")
    mocks.create_missing_dirs.assert_called_once_with("/dst.txt")
    mocks.get_single_file_download_fn.assert_called_once_with(
        mocks.fw, mocks.fw.resolve.return_value.path[-2], "foobar.txt"
    )
    mocks.process_download.assert_called_once_with(
        mocks.get_single_file_download_fn.return_value, "foobar.txt", "/dst.txt"
    )


def test_download_file_not_file(mocks_for_download_file, capsys):
    mocks = mocks_for_download_file
    mocks.fw.resolve.return_value.path = [Project(id="p_id")]

    with pytest.raises(SysExitMock):
        essentials.download_file("fw://group/project", "dst")

    mocks.exit.assert_called_once_with(1)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Can only copy files, not a project\n"


def test_download_file_resolve_error(mocks_for_download_file, capsys):
    class ResolveError(Exception):
        pass

    mocks = mocks_for_download_file
    mocks.fw.resolve.side_effect = ResolveError("404 Not found")

    with pytest.raises(SysExitMock):
        essentials.download_file("fw://group/project", "dst")

    mocks.exit.assert_called_once_with(1)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "404 Not found\n\nCould not resolve source container\n"


@pytest.mark.parametrize(
    "cont,uid,result",
    [
        (None, "foo", "UNKNOWN"),
        (Project(permissions=[]), "foo", "UNKNOWN"),
        (Project(permissions=[Permission("foo", "admin")]), "foo", "admin"),
    ],
)
def test_get_permission_level(cont, uid, result):
    assert essentials._get_permission_level(cont, uid) == result


def test_get_row_for_container_group():
    cont = Group(id="group")

    level, size, modified, name = essentials._get_row_for_container(
        cont, None, None, False
    )

    assert level == "admin"
    assert size == ""
    assert modified == ""
    assert isinstance(name, crayons.ColoredString)
    assert name.s == "group"
    assert name.color == "BLUE"
    assert name.bold


def test_get_row_for_container_group_show_id():
    cont = Group(id="group")

    cid, level, size, modified, name = essentials._get_row_for_container(
        cont, None, None, True
    )

    assert cid == "<id:group>"
    assert level == "admin"
    assert size == ""
    assert modified == ""
    assert isinstance(name, crayons.ColoredString)
    assert name.s == "group"
    assert name.color == "BLUE"
    assert name.bold


def test_get_row_for_container_file():
    parent = Group(label="project")
    f = File(name="foobar.txt", size=99, modified=dt.datetime(1900, 1, 1, 1, 1, 1))

    level, size, modified, name = essentials._get_row_for_container(
        f, parent, None, False
    )

    assert level == "admin"
    assert size == "99B".rjust(6)
    assert modified == "Jan 01 1900 01:01"
    assert name == "files/foobar.txt"


def test_get_row_for_container_file_show_ids():
    parent = Group(label="project")
    f = File(name="foobar.txt", size=99, modified=dt.datetime(1900, 1, 1, 1, 1, 1))

    cid, level, size, modified, name = essentials._get_row_for_container(
        f, parent, None, True
    )

    assert cid == ""
    assert level == "admin"
    assert size == "99B".rjust(6)
    assert modified == "Jan 01 1900 01:01"
    assert name == "files/foobar.txt"
