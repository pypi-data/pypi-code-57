from yoti_python_sdk.http import YotiResponse


class MockResponse(YotiResponse):
    def __init__(self, status_code, text, headers=None, content=None):
        if headers is None:
            headers = dict()

        super(MockResponse, self).__init__(status_code, text, headers, content)


def mock_session_response_config_ok():
    return MockResponse(200, None)


def mock_session_response_config_session_not_found():
    return MockResponse(404, None)
