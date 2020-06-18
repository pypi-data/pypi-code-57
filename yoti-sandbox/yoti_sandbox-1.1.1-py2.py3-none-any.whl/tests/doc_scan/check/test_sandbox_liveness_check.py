from mock import Mock

from yoti_python_sandbox.doc_scan.check import SandboxZoomLivenessCheckBuilder
from yoti_python_sandbox.doc_scan.check.report.breakdown import SandboxBreakdown
from yoti_python_sandbox.doc_scan.check.report.recommendation import (
    SandboxRecommendation,
)


def test_zoom_liveness_check_should_set_correct_liveness_type():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdown_mock = Mock(spec=SandboxBreakdown)

    result = (
        SandboxZoomLivenessCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdown(breakdown_mock)
        .build()
    )

    assert result.liveness_type == "ZOOM"


def test_zoom_liveness_check_build_result_object():
    recommendation_mock = Mock(spec=SandboxRecommendation)
    breakdown_mock = Mock(spec=SandboxBreakdown)

    result = (
        SandboxZoomLivenessCheckBuilder()
        .with_recommendation(recommendation_mock)
        .with_breakdown(breakdown_mock)
        .build()
    )

    assert result.result.report.recommendation is not None
    assert result.result.report.recommendation == recommendation_mock
    assert len(result.result.report.breakdown) == 1
    assert result.result.report.breakdown[0] == breakdown_mock
