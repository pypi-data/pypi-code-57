import json
import logging
import os
import re
import unittest
from pprint import pformat

from httmock import HTTMock, urlmatch

from nomnomdata.engine.test_creds import update_creds


class NominodeMock(HTTMock):
    def __init__(self, task_parameters):
        super().__init__(self.api_match)
        self.logger = logging.getLogger("nomigen.nominode-mock")
        self.params = task_parameters
        self.secrets = self.params.pop("config", {})
        self.api_calls = []

    def __enter__(self):
        super().__enter__()
        self.old_environ = os.environ.copy()
        os.environ["execution_uuid"] = "TEST_UUID"
        os.environ["project_uuid"] = "TEST_PROJECT"
        os.environ["nomnom_api"] = "http://127.0.0.1:9090"
        os.environ["token"] = "token"
        return self

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)
        os.environ.clear()
        os.environ.update(self.old_environ)

    @urlmatch(netloc=r"(.*\.)?127.0.0.1:9090$")
    def api_match(self, url, request):
        match = re.match(r"/connection/(?P<uuid>.+)/update", url.path)
        if match:
            json_data = request.body
            loaded = json.loads(json_data)
            uuid = match.groupdict()["uuid"]
            self.params["config"][uuid] = json.loads(loaded["parameters"])
            update_creds(self.params["config"])
            self.logger.debug("Caught connections update. Test creds updated")
        elif url.path == "/execution/log/TEST_UUID":
            json_data = request.body
            # self.logger.debug("Caught log message {}".format(json_data))
            loaded = json.loads(json_data)
        elif url.path == "/task/TEST_UUID/update":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task update {}".format(pformat(loaded)))
        elif url.path == "/execution/update/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug(
                "Caught execution progress update {}".format(pformat(loaded))
            )
        elif url.path == "/execution/decode/TEST_UUID":
            return json.dumps(self.secrets)
        elif url.path == "/task/TEST_UUID/parameters":
            return json.dumps({"result": "success"})
        elif url.path == "/execution/checkout/TEST_UUID":
            return json.dumps({"parameters": self.params, "task_uuid": "TASK_UUID"})
        else:
            self.logger.info(
                "Unknown api endpoint called {}, \n Body {}".format(
                    url.path, request.body.decode("utf-8")
                )
            )
        self.api_calls.append((url, request))
        return '{"you_logged":"test"}'


class BaseNomTest(unittest.TestCase):
    def setUp(self):
        self.params = {"config": {"nothing": "nothing"}, "action_name": "nothing"}
        self.api_calls = []
        self.logger = logging.getLogger("nomigen_tests." + self.__class__.__name__)
        self._old_environ = os.environ.copy()
        os.environ["execution_uuid"] = "TEST_UUID"
        os.environ["nomnom_api"] = "http://127.0.0.1:9090"
        os.environ["project_uuid"] = "TEST_PROJECT"
        os.environ["token"] = "token"

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._old_environ)

    def run(self, result=None):
        with HTTMock(self.api_match):
            result = super().run(result)
        return result

    @urlmatch(netloc=r"(.*\.)?127.0.0.1:9090$")
    def api_match(self, url, request):
        match = re.match(r"/connection/(?P<uuid>.+)/update", url.path)
        if match:
            json_data = request.body
            loaded = json.loads(json_data)
            uuid = match.groupdict()["uuid"]
            self.params["config"][uuid] = json.loads(loaded["parameters"])
            update_creds(self.params["config"])
            self.logger.debug("Caught connections update. Test creds updated")
        elif url.path == "/execution/log/TEST_UUID":
            json_data = request.body
            self.logger.debug("Caught log message {}".format(json_data))
            loaded = json.loads(json_data)
        elif url.path == "/task/TEST_UUID/update":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug("Caught task update {}".format(pformat(loaded)))
        elif url.path == "/execution/update/TEST_UUID":
            json_data = request.body
            loaded = json.loads(json_data)
            self.logger.debug(
                "Caught execution progress update {}".format(pformat(loaded))
            )
        elif url.path == "/execution/decode/TEST_UUID":
            return json.dumps(self.params["config"])
        elif url.path == "/task/TEST_UUID/parameters":
            return json.dumps({"result": "success"})
        elif url.path == "/execution/checkout/TEST_UUID":
            return json.dumps({"parameters": self.params, "task_uuid": "TASK_UUID"})
        else:
            self.logger.info("Unknown api endpoint called {}".format(url.path))
            self.logger.info(request.body.decode("utf-8"))
        self.api_calls.append((url, request))
        return '{"you_logged":"test"}'
