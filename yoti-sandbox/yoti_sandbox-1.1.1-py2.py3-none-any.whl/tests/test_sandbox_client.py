from yoti_python_sandbox.client import SandboxClient
from yoti_python_sandbox.tests.conftest import PEM_FILE_PATH
from yoti_python_sandbox.token import YotiTokenRequest
from yoti_python_sandbox.token import YotiTokenResponse
from .mocks import mocked_request_failed_sandbox_token
from ..sandbox_exception import SandboxException

try:
    from unittest import mock
except ImportError:
    import mock

import pytest


def test_builder_should_throw_error_for_missing_sdk_id():
    builder = SandboxClient.builder().with_pem_file("some_pem.pem")
    with pytest.raises(ValueError):
        builder.build()


def test_builder_should_throw_error_for_missing_pem_file():
    builder = SandboxClient.builder().for_application("my_application")
    with pytest.raises(ValueError):
        builder.build()


def test_builder_should_build_client():
    client = (
        SandboxClient.builder()
        .for_application("some_app")
        .with_pem_file(PEM_FILE_PATH)
        .with_sandbox_url("https://localhost")
        .build()
    )

    assert client.sdk_id == "some_app"
    assert isinstance(client, SandboxClient)


@mock.patch("yoti_python_sandbox.client.SandboxClient")
def test_client_should_return_token_from_sandbox(sandbox_client_mock):
    sandbox_client_mock.setup_profile_share.return_value = YotiTokenResponse(
        "some-token"
    )

    token_request = (
        YotiTokenRequest.builder().with_remember_me_id("remember_me_pls").build()
    )
    response = sandbox_client_mock.setup_profile_share(token_request)

    assert response.token == "some-token"


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_failed_sandbox_token,
)
def test_client_should_bubble_sandbox_exception(_):
    client = (
        SandboxClient.builder()
        .for_application("some_app")
        .with_pem_file(PEM_FILE_PATH)
        .with_sandbox_url("https://localhost")
        .build()
    )

    token_request = (
        YotiTokenRequest.builder().with_remember_me_id("remember_me_pls").build()
    )

    with pytest.raises(SandboxException) as ex:
        client.setup_sharing_profile(token_request)
        assert isinstance(ex.value, SandboxException)
        assert ex.value.text == "Org not found"
