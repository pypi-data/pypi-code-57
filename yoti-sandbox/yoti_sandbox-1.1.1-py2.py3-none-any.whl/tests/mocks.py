from yoti_python_sdk.http import YotiResponse


class MockResponse(YotiResponse):
    def __init__(self, status_code, text):
        super(MockResponse, self).__init__(status_code, text)


def mocked_request_failed_sandbox_token():
    return MockResponse(500, "Org not found")
