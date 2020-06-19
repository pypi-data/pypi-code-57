"""Ingest reporter tests"""
import datetime
import io
from unittest import mock

import pytest

from flywheel_cli.ingest import client
from flywheel_cli.ingest import config
from flywheel_cli.ingest import reporter as R
from flywheel_cli.ingest import schemas as T


@pytest.fixture(scope="function")
def reporter(db):
    cfg = config.ReporterConfig()
    rep = R.Reporter(db.client, cfg)
    rep._fh = io.StringIO()

    return rep


def test_run_until_not_terminal(reporter, attr_dict, mocker):
    ingest_side_effect = [
        attr_dict(dict(status=T.IngestStatus.created)),
        attr_dict(dict(status=T.IngestStatus.created)),
        attr_dict(dict(status=T.IngestStatus.scanning)),
        attr_dict(dict(status=T.IngestStatus.finished)),
    ]
    status_indexes = {
        T.IngestStatus.created: 0,
        T.IngestStatus.scanning: 1,
        T.IngestStatus.finished: 2,
    }

    def set_last_status_idx():
        reporter.last_reported_status_idx = status_indexes[reporter.ingest.status]

    print_status_history_mock = mocker.patch.object(
        reporter, "print_status_history", side_effect=set_last_status_idx
    )
    final_report_mock = mocker.patch.object(reporter, "final_report")
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time")
    client_mock = mock.Mock(spec_set=client.DBClient)
    type(client_mock).ingest = mock.PropertyMock(side_effect=ingest_side_effect)
    reporter.client = client_mock
    reporter.run()

    assert (
        print_status_history_mock.call_count == 3
    )  # because there 3 non terminal state
    time_mock.sleep.assert_called_once_with(
        reporter.config.refresh_interval
    )  # sleep when no status changed
    final_report_mock.assert_called_once()


def test_run_failed(reporter, db, mocker):
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_final_report")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.save_reports")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_status_history")
    sys_mock = mocker.patch("flywheel_cli.ingest.reporter.sys.exit")
    db.create_ingest(status=T.IngestStatus.failed)
    reporter.run()

    sys_mock.assert_called_once_with(1)


def test_run_has_error(reporter, db, mocker):
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_final_report")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.save_reports")
    mocker.patch("flywheel_cli.ingest.reporter.Reporter.print_status_history")
    sys_mock = mocker.patch("flywheel_cli.ingest.reporter.sys.exit")
    db.create_ingest(status=T.IngestStatus.failed)
    task = db.create_task(type=T.TaskType.upload)
    db.create_error(task_id=task.id, code="FFFF", message="message")

    reporter.run()

    sys_mock.assert_called_once_with(1)


def test_print_status_history_no_last(reporter, attr_dict, mocker):
    report_status_mock = mocker.patch.object(reporter, "report_status")
    reporter.ingest = attr_dict(
        dict(history=[["created", 1], ["scanning", 2], ["resolving", 3]])
    )

    reporter.print_status_history()

    assert reporter.last_reported_status_idx == 2
    assert report_status_mock.mock_calls == [
        mock.call(T.IngestStatus.created, follow=True),
        mock.call(T.IngestStatus.scanning, follow=True),
        mock.call(T.IngestStatus.resolving, follow=True),
    ]


def test_print_status_history_with_last(reporter, attr_dict, mocker):
    report_status_mock = mocker.patch.object(reporter, "report_status")
    reporter.ingest = attr_dict(
        dict(
            history=[["created", 1], ["scanning", 2], ["resolving", 3], ["finished", 4]]
        )
    )
    reporter.last_reported_status_idx = 2

    reporter.print_status_history()

    assert reporter.last_reported_status_idx == 3
    report_status_mock.assert_not_called()


def test_report_in_review_status_verbose(reporter, attr_dict, db, mocker):
    mocker.patch("flywheel_cli.ingest.reporter.crayons.blue", side_effect=dummy_style)
    review_mock = mocker.patch.object(reporter.client, "review")
    abort_mock = mocker.patch.object(reporter.client, "abort")
    grp = db.create_container(
        level=0, path="grp", src_context={"_id": "grp"}, dst_context={"_id": "grp"}
    )
    db.create_container(
        level=1, parent_id=grp.id, path="grp/prj", src_context={"label": "prj"}
    )
    db.create_item(files_cnt=5, bytes_sum=25)
    db.create_item(files_cnt=1, bytes_sum=3)
    reporter.ingest = attr_dict(dict(status=T.IngestStatus.in_review))
    reporter.config.assume_yes = True
    reporter.config.verbose = True

    reporter.report_in_review_status()

    review_mock.assert_called_once()
    abort_mock.assert_not_called()
    assert_print(
        reporter,
        [
            "Hierarchy:",
            "Maximum 100 containers are displayed.\n",
            "`- grp (28 bytes) (using)",
            "   `- prj (28 bytes / 2 files) (creating)",
            "",
            "  Groups: 1",
            "  Projects: 1",
            "  Subjects: 0",
            "  Sessions: 0",
            "  Acquisitions: 0",
            "  Files: 2",
            "  Packfiles: 0",
            "",
        ],
    )


def test_report_in_review_status_not_verbose(reporter, attr_dict, db, mocker):
    container_mock = mocker.patch("flywheel_cli.ingest.reporter.ContainerTree")
    review_mock = mocker.patch.object(reporter.client, "review")
    abort_mock = mocker.patch.object(reporter.client, "abort")
    db.create_container(level=0, path="grp", src_context={"_id": "grp"})
    db.create_container(level=1, path="grp/prj1", src_context={"label": "prj1"})
    db.create_container(level=1, path="grp/prj2", src_context={"label": "prj2"})
    db.create_error(code="DD01")
    db.create_error(code="DD01")
    reporter.ingest = attr_dict(dict(status=T.IngestStatus.in_review))
    reporter.config.assume_yes = True

    reporter.report_in_review_status()

    container_mock.assert_not_called()
    review_mock.assert_called_once()
    abort_mock.assert_not_called()
    assert_print(
        reporter,
        [
            "Hierarchy:",
            "  Groups: 1",
            "  Projects: 2",
            "  Subjects: 0",
            "  Sessions: 0",
            "  Acquisitions: 0",
            "  Files: 0",
            "  Packfiles: 0",
            "",
            "Errors summary:",
            "  File Path Conflict in Upload Set (DD01): 2",
            "",
        ],
    )

    reporter.client.review.assert_called_once()
    reporter.client.abort.assert_not_called()


def test_report_in_review_status_assume_yes(reporter, attr_dict, db):
    db.create_ingest(status=T.IngestStatus.in_review)
    reporter.config.assume_yes = True
    reporter.ingest = attr_dict(dict(status=T.IngestStatus.in_review))

    reporter.report_in_review_status()

    assert reporter.client.ingest.status == T.IngestStatus.preparing


def test_report_in_review_status_no_assume_review(reporter, attr_dict, db, mocker):
    prompt_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.util.confirmation_prompt", return_value=True
    )
    db.create_ingest(status=T.IngestStatus.in_review)
    reporter.config.assume_yes = False
    reporter.ingest = attr_dict(dict(status=T.IngestStatus.in_review))

    reporter.report_in_review_status()

    prompt_mock.assert_called_once_with("Confirm upload?")
    assert reporter.client.ingest.status == T.IngestStatus.preparing


def test_report_in_review_status_no_assume_abort(reporter, attr_dict, db, mocker):
    prompt_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.util.confirmation_prompt", return_value=False
    )
    db.create_ingest(status=T.IngestStatus.in_review)
    reporter.config.assume_yes = False
    reporter.ingest = attr_dict(dict(status=T.IngestStatus.in_review))

    reporter.report_in_review_status()

    prompt_mock.assert_called_once_with("Confirm upload?")
    assert reporter.client.ingest.status == T.IngestStatus.aborted


def test_report_in_review_not_in_review_status(reporter, attr_dict, db, mocker):
    prompt_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.util.confirmation_prompt", return_value=False
    )
    db.create_ingest(status=T.IngestStatus.uploading)
    reporter.config.assume_yes = False
    reporter.ingest = attr_dict(dict(status=T.IngestStatus.uploading))

    reporter.report_in_review_status()

    prompt_mock.assert_not_called()
    assert reporter.client.ingest.status == T.IngestStatus.uploading


def test_print_final_report(reporter, db, mocker):
    crayons_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.crayons.magenta", side_effect=dummy_style
    )
    db.create_ingest(
        status=T.IngestStatus.finished,
        history=[
            [T.IngestStatus.created, 5],
            [T.IngestStatus.scanning, 10],
            [T.IngestStatus.finished, 20],
        ],
    )
    scan_task = db.create_task(type="scan")
    resolve_task = db.create_task(type="resolve")
    db.create_error(task_id=scan_task.id, code="FFFF", message="Foo bar error 1")
    db.create_error(task_id=resolve_task.id, code="GGGG", message="Foo bar error 2")

    reporter.print_final_report()

    assert_print(
        reporter,
        [
            "Final report",
            "",
            "The following errors happened:",
            "scan: Foo bar error 1 (FFFF)",
            "resolve: Foo bar error 2 (GGGG)",
            "",
            "Total elapsed time: 15s",
        ],
    )

    crayons_mock.assert_called_once_with("Final report", bold=True)


def test_print_no_replace(reporter):
    reporter.print("test message1")
    assert_print(reporter, ["test message1"])
    assert reporter._fh.getvalue() == "test message1\n"


def test_print_replace(reporter):
    reporter.print(msg="test message1", replace=False)
    reporter.print(msg="test message2", replace=True)
    reporter.print(msg="test message3", replace=False)

    assert_print(
        reporter,
        ["test message1", {"msg": "test message2", "replace": True}, "test message3",],
    )
    assert (
        reporter._fh.getvalue() == "test message1\n\rtest message2\033[Ktest message3\n"
    )


def test_print_status_header(mocker, reporter):
    crayons_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.crayons.magenta", side_effect=dummy_style
    )
    dt = datetime.datetime(1900, 1, 2, 3, 4, 5)
    reporter.print_status_header("header_value", dt)

    assert reporter._fh.getvalue() == "Header value        [1900-01-02 03:04:05]\n"
    crayons_mock.assert_called_once_with("Header value        ", bold=True)


def test_save_reports(reporter, db, mocker):
    open_mock = mock.mock_open()
    mocker.patch.object(R, "open", open_mock)
    db.create_ingest()

    reporter.config = config.ReporterConfig(
        save_audit_logs="audit_log_path",
        save_deid_logs="deid_log_path",
        save_subjects="subjects_path",
    )

    reporter.save_reports()

    assert reporter.client.ingest_id

    assert_print(
        reporter,
        [
            "Saved audit logs to audit_log_path",
            "Saved deid logs to deid_log_path",
            "Saved subjects to subjects_path",
        ],
    )


def test_save_reports_empty(mocker, reporter):
    save_stream_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.Reporter.save_stream_to_file"
    )
    reporter.save_reports()
    assert reporter._fh.getvalue() == ""
    save_stream_mock.assert_not_called()


def test_save_stream_to_file(mocker):
    fp = io.StringIO()
    file_mock = mock.MagicMock()
    file_mock.__enter__.return_value = fp
    open_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.open", return_value=file_mock
    )
    filepath_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.util.get_filepath", return_value="file_path"
    )

    path = R.Reporter.save_stream_to_file(
        stream=["line1\n", "line2\n"], path="path_arg", prefix="prefix"
    )

    assert fp.getvalue() == "line1\nline2\n"
    assert path == "file_path"

    filepath_mock.assert_called_once_with("path_arg", prefix="prefix", extension="csv")

    open_mock.assert_called_once_with("file_path", "w")


def test_save_stream_to_file_not_found(mocker):
    open_mock = mocker.patch("flywheel_cli.ingest.reporter.open")
    filepath_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_filepath")
    filepath_mock.side_effect = [FileNotFoundError(), "path2"]
    get_incremental_filename_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.util.get_incremental_filename"
    )

    path = R.Reporter.save_stream_to_file(
        stream=["line1\n", "line2\n"], path="path_arg", prefix="prefix"
    )

    assert path == "path2"
    assert len(filepath_mock.mock_calls) == 2
    get_incremental_filename_mock.assert_not_called()
    open_mock.assert_called_once_with("path2", "w")


def test_save_stream_to_file_exists(mocker):
    open_mock = mocker.patch("flywheel_cli.ingest.reporter.open")
    filepath_mock = mocker.patch("flywheel_cli.ingest.reporter.util.get_filepath")
    filepath_mock.side_effect = [FileExistsError(), None]
    get_incremental_filename_mock = mocker.patch(
        "flywheel_cli.ingest.reporter.util.get_incremental_filename",
        return_value="path3",
    )

    path = R.Reporter.save_stream_to_file(
        stream=["line1\n", "line2\n"], path="path_arg", prefix="prefix"
    )

    assert path == "path3"
    assert len(filepath_mock.mock_calls) == 1
    get_incremental_filename_mock.assert_called_once_with("path_arg")
    open_mock.assert_called_once_with("path3", "w")


def test_compute_eta_no_finished(reporter, attr_dict):
    reporter.ingest = attr_dict(dict(history=[("uploading", 1)]))
    eta = reporter.compute_eta(0, 10, T.IngestStatus.uploading)

    assert eta is None


def test_compute_eta_no_status_in_history(reporter, attr_dict):
    reporter.ingest = attr_dict(dict(history=[("resolving", 1)]))
    eta = reporter.compute_eta(1, 10, T.IngestStatus.uploading)

    assert eta is None


def test_compute_eta_no_prev(reporter, attr_dict, mocker):
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time.time", return_value=5)
    reporter.ingest = attr_dict({"history": [("uploading", 0)]})

    eta = reporter.compute_eta(1, 21, T.IngestStatus.uploading)

    # ellapsed time = 5
    # finished = 1
    # remaining tasks = 21 - 1  = 20
    # time = 5 * 20
    assert eta == 100
    assert isinstance(reporter.eta_report, T.ReportETA)
    assert reporter.eta_report.eta == 100
    assert reporter.eta_report.report_time == 5
    assert reporter.eta_report.finished == 1
    assert reporter.eta_report.total == 21


def test_compute_eta_with_prev_and_no_count_change(reporter, mocker):
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time.time", return_value=10)
    reporter.eta_report = T.ReportETA(eta=100, report_time=5, finished=1, total=21)

    eta = reporter.compute_eta(1, 21, T.IngestStatus.resolving)
    assert eta == 95
    assert isinstance(reporter.eta_report, T.ReportETA)
    assert reporter.eta_report.eta == 95
    assert reporter.eta_report.report_time == 10
    assert reporter.eta_report.finished == 1
    assert reporter.eta_report.total == 21


def test_compute_eta_old_status(reporter, attr_dict, mocker):
    time_mock = mocker.patch("flywheel_cli.ingest.reporter.time.time", return_value=99)
    reporter.ingest = attr_dict({"history": [("preparing", 0), ("uploading", 5)]})

    eta = reporter.compute_eta(1, 21, T.IngestStatus.preparing)

    # ellapsed time = 5
    # finished = 1
    # remaining tasks = 21 - 1  = 20
    # time = 5 * 20
    assert eta == 100
    assert isinstance(reporter.eta_report, T.ReportETA)
    assert reporter.eta_report.eta == 100
    assert reporter.eta_report.report_time == 99
    assert reporter.eta_report.finished == 1
    assert reporter.eta_report.total == 21


def test_report_status_wo_follow(reporter, mocker):
    print_progress_mock = mocker.patch.object(reporter, "print_progress")

    reporter.report_status(T.IngestStatus.scanning, follow=False)

    print_progress_mock.assert_called_once_with(T.IngestStatus.scanning, last=True)


def test_get_status_elpased_time_not_in_history(reporter, attr_dict):
    reporter.ingest = attr_dict(dict(history=[]))
    ts = reporter.get_status_elpased_time(T.IngestStatus.uploading)

    assert ts == 0


def test_get_status_elapsed_time(reporter, attr_dict, mocker):
    mocker.patch("flywheel_cli.ingest.reporter.time.time", return_value=5)
    reporter.ingest = attr_dict(dict(history=[["finalizing", 0],]))

    ts = reporter.get_status_elpased_time(T.IngestStatus.finalizing)

    assert ts == 5


def test_print_progress_zero_total(reporter, attr_dict):
    reporter.ingest = attr_dict(dict(history=[["resolving", 1]]))
    reporter.progress = T.Progress()
    reporter.progress.stages.resolving.completed = 1
    reporter.progress.stages.resolving.total = 0

    reporter.print_progress(T.IngestStatus.resolving)

    assert_print(
        reporter, [],
    )


def test_print_progress_skip_eta(reporter, attr_dict, mocker):
    mock_compute_eta = mocker.patch.object(reporter, "compute_eta")
    mocker.patch.object(reporter, "get_status_elpased_time", return_value=2)
    reporter.ingest = attr_dict(dict(history=[["resolving", 1]]))
    reporter.progress = T.Progress()
    reporter.progress.stages.resolving.completed = 1
    reporter.progress.stages.resolving.total = 10

    reporter.print_progress(T.IngestStatus.resolving, last=True)

    mock_compute_eta.assert_not_called()
    assert_print(
        reporter, [{"msg": "10.0% (2s)", "replace": True}, ""],
    )


def test_print_progress_w_eta(reporter, attr_dict, mocker):
    mock_compute_eta = mocker.patch.object(reporter, "compute_eta", return_value=5)
    mocker.patch.object(reporter, "get_status_elpased_time", return_value=2)
    reporter.ingest = attr_dict(dict(history=[["resolving", 1]]))
    reporter.progress = T.Progress()
    reporter.progress.stages.resolving.completed = 1
    reporter.progress.stages.resolving.total = 10

    reporter.print_progress(T.IngestStatus.resolving)

    mock_compute_eta.assert_called_once_with(1, 10, T.IngestStatus.resolving)
    assert_print(
        reporter, [{"msg": "10.0% (elapsed: 2s|ETA: 5s)", "replace": True}],
    )


def test_print_progress_scanning_counts(reporter, attr_dict, mocker):
    mocker.patch.object(reporter, "get_status_elpased_time", return_value=2)
    reporter.ingest = attr_dict(dict(history=[["scanning", 1]]))
    reporter.progress = T.Progress()
    reporter.progress.scans.finished = 3
    reporter.progress.scans.total = 10
    reporter.progress.files.total = 2
    reporter.progress.bytes.total = 22
    reporter.progress.stages.scanning.completed = 1
    reporter.progress.stages.scanning.total = 10

    reporter.print_progress(T.IngestStatus.scanning, last=True)

    assert_print(
        reporter, [{"msg": "20.0% - 2 files, 22 bytes (2s)", "replace": True}, ""],
    )


def test_get_uploading_progress_counts(reporter):
    reporter.progress = T.Progress()
    reporter.progress.items.skipped = 1
    reporter.progress.items.finished = 5
    reporter.progress.items.total = 10

    finished, total = reporter.get_uploading_progress_counts()
    assert finished == 6
    assert total == 10


def test_get_scanning_progress_counts(reporter):
    reporter.progress = T.Progress()
    reporter.progress.scans.finished = 5
    reporter.progress.scans.total = 10
    reporter.progress.stages.scanning.completed = 1
    reporter.progress.stages.scanning.total = 10

    finished, total = reporter.get_scanning_progress_counts()
    assert finished == 6
    assert total == 20


def test_format_scanning_progress(reporter):
    reporter.progress = T.Progress(
        bytes=T.StatusCount(total=123456),
        scans=T.StatusCount(finished=10, total=20),
        files=T.StatusCount(total=123),
    )

    msg = reporter.format_scanning_progress("foo bar")

    assert msg == "foo bar - 123 files, 120.6 KB"


def test_format_uploading_progress(mocker, reporter):
    reporter.progress = T.Progress(items=T.StatusCount(failed=2, finished=3, total=4))

    msg = reporter.format_uploading_progress("foo bar")

    assert msg == "foo bar - (2 failed)"


def test_print_upload_summary(reporter):
    reporter.progress = T.Progress(
        items=T.StatusCount(scanned=1, failed=2, finished=3, total=4)
    )
    reporter.print_uploading_summary()

    assert_print(reporter, ["Scanned: 1", "Failed: 2", "Total: 4",])


def assert_print(reporter, writes):
    def replace(msg):
        return f"\r{msg}\033[K"

    msg = ""
    for w in writes:
        if isinstance(w, dict):
            if "replace" in w and w["replace"]:
                msg += replace(w["msg"])
            else:
                msg += f"{w['msg']}\n"
        else:
            msg += f"{w}\n"

    assert reporter._fh.getvalue() == msg


def dummy_style(msg, *args, **kwargs):
    return msg
