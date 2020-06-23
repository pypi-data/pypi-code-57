from google.cloud.error_reporting import Client as StackDriverClient


class Client(StackDriverClient):
    def __init__(self, project=None, credentials=None, _http=None):
        super().__init__(project=project, credentials=credentials, _http=_http)
