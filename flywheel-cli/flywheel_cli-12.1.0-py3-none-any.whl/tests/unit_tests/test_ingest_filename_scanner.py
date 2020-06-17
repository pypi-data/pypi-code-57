import pytest

from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.scanners import filename
from .conftest import DummyWalker

def test_validate_opts():
    with pytest.raises(ValueError):
        filename.FilenameScanner.validate_opts(None)

    with pytest.raises(ValueError):
        filename.FilenameScanner.validate_opts({"key": 'value'})

    with pytest.raises(ValueError):
        filename.FilenameScanner.validate_opts(
            {"pattern": None}
        )
    filename.FilenameScanner.validate_opts(
        {"pattern": '{group}-{project._id}'}
    )

def test_scan():
    walker = DummyWalker([
        'path/group_project_session_subject-acquisition.txt',
        'dir1/dir2/file2'
    ])

    scanner = filename.FilenameScanner(
        ingest_config=None,
        strategy_config=None,
        worker_config=None,
        walker=walker,
        opts={"pattern": '{group}_{project}_{session}_{subject}-{acquisition}.txt'},
        context={}
    )

    files = list(scanner.scan('dir'))
    assert len(files) == 2

    # match
    file = files[0]
    assert isinstance(file, T.ItemIn)
    assert file.type == "file"
    assert file.dir == "dir/path"
    assert file.files == ["group_project_session_subject-acquisition.txt"]
    assert file.files_cnt == 1
    assert file.bytes_sum == 1
    assert file.context == {
        'group': {'_id': 'group'},
        'project': {'label': 'project'},
        'session': {'label': 'session'},
        'subject': {'label': 'subject'},
        'acquisition': {'label': 'acquisition'}
    }

    # not a match
    file = files[1]
    assert isinstance(file, T.ItemIn)
    assert file.type == "file"
    assert file.dir == "dir/dir1/dir2"
    assert file.files == ["file2"]
    assert file.files_cnt == 1
    assert file.bytes_sum == 2
    assert file.context == {}
