from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as T
from flywheel_cli.ingest.scanners import template
from .conftest import DummyWalker


def test_scan_with_folder_strategy():
    walker = DummyWalker([
        "group/project/subject/session/file",
        "random_file"
    ])

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.FolderConfig(),
        worker_config=None,
        walker=walker
    )

    files = list(scanner.scan("dir"))
    assert len(files) == 2

    # match
    file = files[0]
    assert isinstance(file, T.ItemIn)
    assert file.type == "file"
    assert file.dir == "/group/project/subject/session"
    assert file.files == ["file"]
    assert file.files_cnt == 1
    assert file.bytes_sum == 1
    assert file.context == {
        "group": {"_id": "group"},
        "project": {"label": "project"},
        "subject": {"label": "subject"},
        "session": {"label": "session"}
    }

    # not a match
    file = files[1]
    assert isinstance(file, T.ItemIn)
    assert file.type == "file"
    assert file.dir == "/"
    assert file.files == ["random_file"]
    assert file.files_cnt == 1
    assert file.bytes_sum == 2
    assert file.context == {}


def test_scan_with_template_strategy(mocker):
    walker = DummyWalker([
        "project1/subject1/session1/files/file.dcm",
        "project1/subject1/session1/files/file.txt",
        "subject1/file.dcm"
    ])

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.TemplateConfig(
            group="group_id",
            template=[
                {"pattern": "{project}"},
                {"pattern": "{subject}"},
                {"pattern": "{session}"},
                {"select": [
                    {
                        "pattern": ".*",
                        "scan": "dicom"
                    }
                ]}
            ]
        ),
        worker_config=None,
        walker=walker
    )

    files = list(scanner.scan("dir"))

    assert len(files) == 2

    # match, scan task
    file = files[0]
    assert isinstance(file, T.TaskIn)
    assert file.type == "scan"
    assert file.context == {
        "group": {"_id": "group_id"},
        "project": {"label": "project1"},
        "subject": {"label": "subject1"},
        "session": {"label": "session1"},
        "scanner": {
            "type": "dicom",
            "dir": "/project1/subject1/session1/files",
            "opts": {}
        }
    }

    # not a match
    file = files[1]
    assert isinstance(file, T.ItemIn)
    assert file.type == "file"
    assert file.dir == "/subject1"
    assert file.files == ["file.dcm"]
    assert file.files_cnt == 1
    assert file.bytes_sum == 3
    assert file.context == {
        "group": {"_id": "group_id"},
        "project": {"label": "subject1"}
    }


def test_scan_with_template_strategy_override(mocker):
    walker = DummyWalker([
        "project1/subject1/session1/files/file.dcm",
        "project1/subject1/session1/files/file.txt",
        "subject1/file.dcm"
    ])

    scanner = template.TemplateScanner(
        ingest_config=None,
        strategy_config=config.TemplateConfig(
            group="group_id",
            project="project",
            template=[
                {"pattern": "{project}"},
                {"pattern": "{subject}"},
                {"pattern": "{session}"},
                {"select": [
                    {
                        "pattern": ".*",
                        "scan": "dicom"
                    }
                ]}
            ],
            group_override="group_override",
            project_override="project_override",
        ),
        worker_config=None,
        walker=walker
    )

    files = list(scanner.scan("dir"))

    assert len(files) == 2

    # match, scan task
    file = files[0]
    assert isinstance(file, T.TaskIn)
    assert file.type == "scan"
    assert file.context == {
        "group": {"_id": "group_id"},
        "project": {"label": "project1"},
        "subject": {"label": "subject1"},
        "session": {"label": "session1"},
        "scanner": {
            "type": "dicom",
            "dir": "/project1/subject1/session1/files",
            "opts": {}
        }
    }

    # not a match
    file = files[1]
    assert isinstance(file, T.ItemIn)
    assert file.type == "file"
    assert file.dir == "/subject1"
    assert file.files == ["file.dcm"]
    assert file.files_cnt == 1
    assert file.bytes_sum == 3
    assert file.context == {
        "group": {"_id": "group_override"},
        "project": {"label": "project_override"}
    }
