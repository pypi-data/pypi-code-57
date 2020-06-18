from mock import Mock

from yoti_python_sandbox.doc_scan import SandboxCheckReportsBuilder
from yoti_python_sandbox.doc_scan.check.sandbox_document_authenticity_check import (
    SandboxDocumentAuthenticityCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_face_match_check import (
    SandboxDocumentFaceMatchCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_document_text_data_check import (
    SandboxDocumentTextDataCheck,
)
from yoti_python_sandbox.doc_scan.check.sandbox_liveness_check import (
    SandboxLivenessCheck,
)


def test_should_build_with_correct_properties():
    authenticity_check_mock = Mock(spec=SandboxDocumentAuthenticityCheck)
    face_match_check_mock = Mock(spec=SandboxDocumentFaceMatchCheck)
    text_data_check_mock = Mock(spec=SandboxDocumentTextDataCheck)
    liveness_check_mock = Mock(spec=SandboxLivenessCheck)
    async_report_delay = 12

    check_reports = (
        SandboxCheckReportsBuilder()
        .with_document_authenticity_check(authenticity_check_mock)
        .with_document_face_match_check(face_match_check_mock)
        .with_document_text_data_check(text_data_check_mock)
        .with_liveness_check(liveness_check_mock)
        .with_async_report_delay(async_report_delay)
        .build()
    )

    assert len(check_reports.document_authenticity_checks) == 1
    assert check_reports.document_authenticity_checks[0] == authenticity_check_mock

    assert len(check_reports.document_face_match_checks) == 1
    assert check_reports.document_face_match_checks[0] == face_match_check_mock

    assert len(check_reports.document_text_data_checks) == 1
    assert check_reports.document_text_data_checks[0] == text_data_check_mock

    assert len(check_reports.liveness_checks) == 1
    assert check_reports.liveness_checks[0] == liveness_check_mock

    assert check_reports.async_report_delay == 12


def test_async_report_delay_not_included_when_not_specified():
    authenticity_check_mock = Mock(spec=SandboxDocumentAuthenticityCheck)

    check_reports = (
        SandboxCheckReportsBuilder()
        .with_document_authenticity_check(authenticity_check_mock)
        .build()
    )

    assert check_reports.async_report_delay is None
