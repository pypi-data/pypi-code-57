import pytest

from yoti_python_sandbox.doc_scan.response_config import ResponseConfig
from ...sandbox_exception import SandboxException

try:
    from unittest import mock
except ImportError:
    import mock

from .mocks import mock_session_response_config_session_not_found

SOME_SESSION_ID = "someSessionId"


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mock_session_response_config_session_not_found,
)
def test_configure_session_response_should_raise_sandbox_exception(
    _, doc_scan_sandbox_client
):
    response_config_mock = mock.Mock(spec=ResponseConfig)
    response_config_mock.to_json.return_value = {"some": "object"}

    with pytest.raises(SandboxException) as ex:
        doc_scan_sandbox_client.configure_session_response(
            SOME_SESSION_ID, response_config_mock
        )

    assert "Failed on status code: 404" in str(ex.value)


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mock_session_response_config_session_not_found,
)
def test_configure_application_response_should_raise_sandbox_exception(
    _, doc_scan_sandbox_client
):
    response_config_mock = mock.Mock(spec=ResponseConfig)
    response_config_mock.to_json.return_value = {"some": "object"}

    with pytest.raises(SandboxException) as ex:
        doc_scan_sandbox_client.configure_application_response(response_config_mock)

    assert "Failed on status code: 404" in str(ex.value)
