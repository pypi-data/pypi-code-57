from mock import Mock

from yoti_python_sandbox.doc_scan.check import SandboxDocumentTextDataCheckBuilder
from yoti_python_sandbox.doc_scan.check.report.breakdown import SandboxBreakdown
from yoti_python_sandbox.doc_scan.check.report.recommendation import (
    SandboxRecommendation,
)
from yoti_python_sandbox.doc_scan.document_filter import SandboxDocumentFilter


def test_should_build_sandbox_document_authenticity_check():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdown_mock = Mock(spec=SandboxBreakdown)

    result = (
        SandboxDocumentTextDataCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdown(breakdown_mock)
        .build()
    )

    assert result.result.report.recommendation is not None
    assert result.result.report.recommendation == recommendation_mock
    assert len(result.result.report.breakdown) == 1
    assert result.result.report.breakdown[0] == breakdown_mock


def test_should_accept_document_filter():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdown_mock = Mock(spec=SandboxBreakdown)
    document_filter_mock = Mock(spec=SandboxDocumentFilter)

    result = (
        SandboxDocumentTextDataCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdown(breakdown_mock)
        .with_document_filter(document_filter_mock)
        .build()
    )

    assert result.document_filter == document_filter_mock


def test_should_accept_with_breakdowns():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdowns_mock = [Mock(spec=SandboxBreakdown), Mock(spec=SandboxBreakdown)]

    result = (
        SandboxDocumentTextDataCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdowns(breakdowns_mock)
        .build()
    )

    assert result.result.report.breakdown == breakdowns_mock
