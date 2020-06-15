from collections import defaultdict
from contextlib import contextmanager
import re
import urllib

import requests_mock

from modelzoo import config


class MockAPIServer:
    def __init__(self, mocker: requests_mock.Mocker):
        self._mocker = mocker
        self._models = defaultdict(dict)

        self._mocker.post(
            urllib.parse.urljoin(config.get_base_api_url(), "models/create"),
            json=self.create_mock,
            headers={"content-type": "application/json"},
        )
        self._mocker.get(
            urllib.parse.urljoin(config.get_base_api_url(), "models"),
            json=self.list_mock,
            headers={"content-type": "application/json"},
        )
        self._mocker.post(
            re.compile("{}models/(.+)/predict".format(config.get_base_api_url())),
            json=self.predict_mock,
            headers={"content-type": "application/json"},
        )
        self._mocker.get(
            re.compile("{}models/(.+)".format(config.get_base_api_url())),
            json=self.info_mock,
            headers={"content-type": "application/json"},
        )
        self._mocker.post(
            re.compile("{}models/(.+)/start".format(config.get_base_api_url())),
            json=self.start_mock,
            headers={"content-type": "application/json"},
        )
        self._mocker.post(
            re.compile("{}models/(.+)/stop".format(config.get_base_api_url())),
            json=self.stop_mock,
            headers={"content-type": "application/json"},
        )

    def get_models(self):
        return self._models

    def create_mock(self, request, context):
        data = request.json()
        name, files = data["model_name"], data["model_files"]

        # Store in the model state.
        self._models[name]["files"] = files
        self._models[name]["state"] = {"name": "HEALTHY", "description": ""}

        # Mock upload URLs for every model file.
        upload_urls = {}
        for f in files:
            mock_upload_url = "http://s3-upload.com/{}/{}".format(name, f)
            upload_urls[f] = mock_upload_url
            self._mocker.put(mock_upload_url)

        return {"upload_urls": upload_urls}

    def list_mock(self, request, context):
        return self._models

    def info_mock(self, request, context):
        # For now, just return the first model in the "database".
        return self._models[next(iter(self._models))]

    def predict_mock(self, request, context):
        return {"outputs": [4.0]}

    def start_mock(self, request, context):
        return {}

    def stop_mock(self, request, context):
        return {}


@contextmanager
def mock_api_server():
    with requests_mock.Mocker() as m:
        yield MockAPIServer(m)
