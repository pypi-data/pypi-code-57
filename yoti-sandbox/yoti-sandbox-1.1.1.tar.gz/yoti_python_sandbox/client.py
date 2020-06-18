import json
from json import JSONEncoder

from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.http import SignedRequestBuilder

import yoti_python_sandbox
from .anchor import SandboxAnchor
from .attribute import SandboxAttribute
from .endpoint import SandboxEndpoint
from .sandbox_exception import SandboxException
from .token import YotiTokenRequest
from .token import YotiTokenResponse


class SandboxEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, YotiTokenRequest):
            return o.__dict__()
        if isinstance(o, SandboxAttribute):
            return o.__dict__()
        if isinstance(o, SandboxAnchor):
            return o.__dict__()

        return json.JSONEncoder.default(self, o)


class SandboxClient(object):
    def __init__(self, sdk_id, pem_file, sandbox_url=None):
        if sandbox_url is None:
            sandbox_url = yoti_python_sandbox.DEFAULT_SANDBOX_URL

        self.sdk_id = sdk_id
        self.__endpoint = SandboxEndpoint(sdk_id)
        self.__sandbox_url = sandbox_url

        if isinstance(pem_file, Crypto):
            self.__crypto = pem_file
        else:
            self.__crypto = Crypto.read_pem_file(pem_file, "SandboxClient.__init__")

    def setup_sharing_profile(self, request_token):
        """
        Using the supplied YotiTokenRequest, this function will make a request
        to the defined sandbox environment to create a profile with the supplied values.
        The returned token can be used against the sandbox environment to retrieve the profile
        using the standard YotiClient.

        :param YotiTokenRequest request_token:
        :return: the token for accessing a profile
        """
        request_path = self.__endpoint.get_sandbox_path()
        payload = json.dumps(request_token, cls=SandboxEncoder).encode("utf-8")

        signed_request = (
            SignedRequestBuilder()
            .with_pem_file(self.__crypto)
            .with_base_url(self.__sandbox_url)
            .with_endpoint(request_path)
            .with_payload(payload)
            .with_post()
            .build()
        )

        response_payload = signed_request.execute()
        if response_payload.status_code < 200 or response_payload.status_code >= 300:
            raise SandboxException(
                "Error making request to sandbox service: "
                + str(response_payload.status_code),
                response_payload,
            )

        parsed = json.loads(response_payload.text)
        return YotiTokenResponse(parsed["token"])

    @staticmethod
    def builder():
        """
        Creates an instance of the sandbox client builder

        :return: instance of SandboxClientBuilder
        """
        return SandboxClientBuilder()


class SandboxClientBuilder(object):
    def __init__(self):
        self.__sdk_id = None
        self.__pem_file = None
        self.__sandbox_url = None

    def for_application(self, sdk_id):
        """
        Sets the application ID on the builder

        :param str sdk_id: the SDK ID supplied from Yoti Hub
        :return: the updated builder
        """
        self.__sdk_id = sdk_id
        return self

    def with_pem_file(self, pem_file):
        """
        Sets the pem file to be used on the builder

        :param str pem_file: path to the PEM file
        :return: the updated builder
        """
        self.__pem_file = pem_file
        return self

    def with_sandbox_url(self, sandbox_url):
        """
        Sets the URL of the sandbox environment on the builder

        :param str sandbox_url: the sandbox environment URL
        :return: the updated builder
        """
        self.__sandbox_url = sandbox_url
        return self

    def build(self):
        """
        Using all supplied values, create an instance of the SandboxClient.

        :raises ValueError: one or more of the values is None
        :return: instance of SandboxClient
        """
        if self.__sdk_id is None or self.__pem_file is None:
            raise ValueError("SDK ID/PEM file must not be None")

        return SandboxClient(self.__sdk_id, self.__pem_file, self.__sandbox_url)
