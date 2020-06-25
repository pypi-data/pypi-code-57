import re
import copy
import uuid
import json
import unittest
import requests
import responses
from platkit import auth
from http import HTTPStatus
from unittest.mock import patch
from platkit.config import Config

config = Config()
local_password = "LOCAL"


class PlatkitTestCase(unittest.TestCase):
    """
    Base test case for endpoints which uses some tricks to add a
    requests-interface
    """

    headers = {}
    token = None
    current_user = {}
    endpoints = {}
    player_id = None
    user_id = None

    def initialize(self, app):
        self.host = "http://localhost"
        self.client = app.test_client()
        app.testing = True
        self.app = app

        # make sure debug and skipauth are false in decouple for platkit
        # we also need to set these in the flask config because we are using
        # flask for config in the service layer but decouple config in platkit (arg!)
        config.set({"DEBUG": 0, "SKIPAUTH": 0})
        app.config["SKIPAUTH"] = 0
        app.config["DEBUG"] = 0

    @staticmethod
    def mock(func):
        @responses.activate
        def wrapped(self, *args, **kwargs):
            self._setup_mocking()
            return func(self, *args, **kwargs)

        return wrapped

    def _do_request(self, method, endpoint, data=None, params=None, headers=None, *args, **kw):
        @PlatkitTestCase.mock
        def inner(self, method, endpoint, data, params, added_headers, *args, **kw):
            check = kw.pop("check", True)
            expected_status_code = kw.pop("status", HTTPStatus.OK)
            # backwards compatibility
            expected_status_code = kw.pop("expected_status_code", expected_status_code)
            headers = copy.copy(self.headers)
            if "Accept" not in headers:
                headers["Accept"] = "application/json"

            if data:
                headers["Content-Type"] = "application/json"
                if not isinstance(data, list) and not isinstance(data, dict):
                    raise Exception("Data must be a list or a dict: %s" % data)

            # override headers with any that were passed in
            if added_headers:
                headers.update(added_headers)

            if not endpoint.startswith(self.host):
                endpoint = self.host + endpoint

            public_key = auth.get_public_key()
            with patch("platkit.auth.get_public_key") as patched_get_public_key:
                patched_get_public_key.return_value = public_key
                r = getattr(requests, method)(endpoint, json=data, headers=headers, params=params)
            if check:
                self.assertEqual(
                    r.status_code,
                    expected_status_code,
                    u"Status code should be {} but is {}: {}".format(
                        expected_status_code, r.status_code, r.text.replace("\\n", "\n")
                    ),
                )
            return r

        return inner(self, method, endpoint, data, params, headers, *args, **kw)

    def _setup_mocking(self):
        def _mock_callback(request):
            method_name = request.method.lower()
            url = request.path_url
            handler = getattr(self.client, method_name)
            r = handler(url, data=request.body, headers=dict(request.headers))
            return r.status_code, r.headers, r.data

        pattern = re.compile("{}/(.*)".format(self.host))
        methods = [responses.GET, responses.POST, responses.PUT, responses.DELETE, responses.PATCH]
        for method in methods:
            responses.add_callback(method, pattern, callback=_mock_callback)

    def get(self, *args, **kw):
        return self._do_request("get", *args, **kw)

    def put(self, *args, **kw):
        return self._do_request("put", *args, **kw)

    def post(self, *args, **kw):
        return self._do_request("post", *args, **kw)

    def delete(self, *args, **kw):
        return self._do_request("delete", *args, **kw)

    def patch(self, *args, **kw):
        return self._do_request("patch", *args, **kw)

    def auth(self, user_name="testuser", client_id="api-key-client", roles=None):
        """
        If payload is supplied we JWT encode it using the current
        app's secret and add it to the headers.
        If payload is not supplied we do an auth call against the
        current app's /auth endpoint
        """
        # TODO 1: Assumes anyone can log in with any password
        # Needs to be refactored when we have real auth

        # JWT generation for testing purposes.

        auth_payload = auth.get_auth_payload(user_name, client_id, roles)

        token = auth_payload["access_token"]

        self.token = token
        self.headers = {"Authorization": "Bearer " + token}

        self.endpoints = self.get_endpoints()

    def get_endpoints(self):
        resp = self.get("/")
        return resp.json()["endpoints"]

    def links(self, resource):
        return resource.get("links", {})

    def uuid(self):
        return str(uuid.uuid4())

    def pretty(self, obj):
        if isinstance(obj, requests.models.Response):
            print("Response from %s with status code %s" % (obj.url, obj.status_code))
            try:
                obj = obj.json()
            except Exception:
                obj = obj.text
        formatted_json = json.dumps(obj, sort_keys=True, indent=4)
        try:
            from pygments import highlight, lexers, formatters

            colorful_json = highlight(
                formatted_json, lexers.JsonLexer(), formatters.Terminal256Formatter()
            )
        except ImportError:
            colorful_json = formatted_json
        print(colorful_json)
