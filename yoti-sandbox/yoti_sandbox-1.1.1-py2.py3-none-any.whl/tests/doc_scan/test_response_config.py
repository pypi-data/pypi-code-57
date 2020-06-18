from mock import Mock

from yoti_python_sandbox.doc_scan import ResponseConfigBuilder
from yoti_python_sandbox.doc_scan.check_reports import SandboxCheckReports
from yoti_python_sandbox.doc_scan.task_results import SandboxTaskResults


def test_should_accept_task_results():
    task_results_mock = Mock(spec=SandboxTaskResults)

    result = ResponseConfigBuilder().with_task_results(task_results_mock).build()

    assert result.task_results is not None
    assert result.task_results == task_results_mock


def test_should_accept_check_reports():
    check_reports_mock = Mock(spec=SandboxCheckReports)

    result = ResponseConfigBuilder().with_check_reports(check_reports_mock).build()

    assert result.check_reports is not None
    assert result.check_reports == check_reports_mock
