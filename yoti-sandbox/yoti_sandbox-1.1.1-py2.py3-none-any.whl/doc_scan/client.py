import json

from yoti_python_sdk.http import SignedRequest
from yoti_python_sdk.utils import YotiEncoder

from yoti_python_sandbox.doc_scan import DEFAULT_DOC_SCAN_SANDBOX_URL
from .response_config import ResponseConfig  # noqa: F401
from ..sandbox_exception import SandboxException


class DocScanSandboxClient(object):
    SESSION_RESPONSE_CONFIG_PATH = "/sessions/{session_id}/response-config"
    APPLICATION_RESPONSE_CONFIG_PATH = "/apps/{sdk_id}/response-config"

    def __init__(self, sdk_id, key_file, api_url=DEFAULT_DOC_SCAN_SANDBOX_URL):
        self.__sdk_id = sdk_id
        self.__key_file = key_file
        self.__api_url = api_url

    def configure_session_response(self, session_id, response_config):
        """
        :param session_id: the session ID
        :type session_id: str
        :param response_config: the response config
        :type response_config: ResponseConfig
        :raises SandboxException: if there was an error with the request
        """
        payload = json.dumps(response_config, cls=YotiEncoder).encode("utf-8")
        path = self.SESSION_RESPONSE_CONFIG_PATH.format(session_id=session_id)

        request = (
            SignedRequest.builder()
            .with_pem_file(self.__key_file)
            .with_base_url(self.__api_url)
            .with_endpoint(path)
            .with_param("sdkId", self.__sdk_id)
            .with_payload(payload)
            .with_http_method("PUT")
            .build()
        )
        response = request.execute()

        if response.status_code < 200 or response.status_code >= 300:
            raise SandboxException(
                "Failed on status code: {}".format(str(response.status_code)), response
            )

    def configure_application_response(self, response_config):
        """
        :param response_config: the response config
        :type response_config: ResponseConfig
        :raises SandboxException: if there was an error with the request
        """
        payload = json.dumps(response_config, cls=YotiEncoder).encode("utf-8")
        path = self.APPLICATION_RESPONSE_CONFIG_PATH.format(sdk_id=self.__sdk_id)

        request = (
            SignedRequest.builder()
            .with_pem_file(self.__key_file)
            .with_base_url(self.__api_url)
            .with_endpoint(path)
            .with_payload(payload)
            .with_http_method("PUT")
            .build()
        )
        response = request.execute()

        if response.status_code < 200 or response.status_code >= 300:
            raise SandboxException(
                "Failed on status code: {}".format(str(response.status_code)), response
            )
