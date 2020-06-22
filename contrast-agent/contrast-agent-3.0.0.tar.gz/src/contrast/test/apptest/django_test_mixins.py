# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
# pylint: disable=too-many-lines
import copy
import os
import six  # pylint: disable=did-not-import-extern

import pytest
from app import settings
from app.urls import urlpatterns

from django import __version__ as django_version
from django.utils.html import escape
from django.test import Client
from django.http import HttpResponseForbidden
from contrast.agent.middlewares.django_middleware import DjangoMiddleware
from contrast.api.dtm_pb2 import AttackResult, ObservedRoute

from contrast.api.settings_pb2 import ProtectionRule
from contrast.test import mocks
from contrast.test.apptest_utils import (
    assert_event_sources,
    assert_route_appended,
    assert_routes_count,
    assert_ssrf_finding,
    current_routes_by_url,
    param_is_tracked,
    validate_observed_route,
    validate_finding,
    validate_any_finding,
    validate_source_finding,
    validate_header_sources,
    validate_cookies_sources,
    assert_subprocess_popen_finding_events,
)

from contrast.test.helper import (
    mock_build_update_messages,
    mock_send_messages,
    python2_only,
    skip_no_mongo_db,
)

URLPATTERNS_COPY = copy.copy(urlpatterns)
BASE_DIR = os.path.abspath(os.curdir)


SOURCE_OPTIONS = (
    "parameter",
    "host",
    "port",
    "raw_uri",
    "scheme",
    "referer_header",
)

# full_path_info is only in newer versions of django. We do not test it for POST
# requests since in this case the path does not contain a query, and so the entire path
# is actually sanitized.
GET_SOURCES = SOURCE_OPTIONS + (("full_path", "full_path_info",) if six.PY3 else ())
POST_SOURCES = ("files", "body",) + SOURCE_OPTIONS + (("full_path",) if six.PY3 else ())


class DjangoProtectTestMixinBlock(object):
    """
    Provides test cases to be used across all django protect apptests
    """

    PROTECT_RULES_MODE_BLOCK = [
        {
            "id": "cmd-injection",
            "name": "Command Injection",
            "mode": ProtectionRule.BLOCK,
        },
        {
            "id": "path-traversal",
            "name": "Path Traversal",
            "mode": ProtectionRule.BLOCK,
        },
    ]

    def test_cmdi(self):
        c = Client()
        response = c.get("/cmdi/", {"user_input": "; echo /etc/passwd | nc"})
        assert isinstance(response, HttpResponseForbidden)
        assert six.ensure_str(response.content) == DjangoMiddleware.OVERRIDE_MESSAGE
        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "cmd-injection"


class DjangoAssessTestMixin(object):
    """
    Provides test cases to be used across all django assess apptests
    """

    def test_track_django_sources(self):
        param_val = "; echo /etc/passwd | nc"
        response = self.client.get("/cmdi/", {"user_input": param_val})

        assert response is not None
        assert param_is_tracked(param_val)

    @mocks.build_finding
    def test_xss_django_autoescape(self, mocked):
        """Autoescaping is enabled by default and should not lead to a finding"""
        param_val = "im an attack!"
        response = self.client.get("/xss-autoescape/", {"user_input": param_val})
        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 0
        assert not mocked.called

    @mocks.build_finding
    def test_xss_django_autoescape_safe(self, mocked):
        """
        Autoescaping is enabled but the value is marked as safe in the template
        which prevents it from being escaped. This should result in a finding.
        """
        param_val = "im an attack!"
        response = self.client.get("/xss-autoescape-safe/", {"user_input": param_val})
        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 1

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"

    @mocks.build_finding
    def test_xss_django_no_autoescape(self, mocked):
        """Autoescaping is disabled so we should get a finding"""
        param_val = "im an attack!"
        response = self.client.get("/xss-no-autoescape/", {"user_input": param_val})
        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 1

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"

    def test_byte_file_contents_are_tracked(self):
        filename = "logo.png"
        file_path = os.path.join(BASE_DIR, "..", "data", filename)

        with open(file_path, "rb") as fp:
            self.client.post("/file-contents/", {"upload": fp})

        assert param_is_tracked(filename)

        contents = open(file_path, "rb").read()
        file_start = contents[:6]
        file_end = contents[-18:]

        # we cannot simply assert param_is_tracked(contents) because the contents
        # are split up into chunks in the string tracker and tracked in these chunks
        assert param_is_tracked(file_start)
        assert param_is_tracked(file_end)

    @mocks.build_finding
    def test_cmdi_base64_encoded(self, mocked):
        # this string is "__import__('os').system('echo hacked')" b64 encoded
        encoded_input = "X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJ2VjaG8gaGFja2VkJyk="
        response = self.client.get(
            "/cmdi-base64-encoded/", {"user_input": encoded_input}
        )

        assert response.status_code == 200
        assert len(self.request_context.activity.findings) == 1
        assert mocked.called
        args, _ = mocked.call_args
        orig_args = args[-2]
        orig_kwargs = args[-1]

        assert args[1].name == "unsafe-code-execution"
        assert orig_args == (b"__import__('os').system('echo hacked')",)
        assert orig_kwargs == {}

    @skip_no_mongo_db
    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_find(self, mocked, with_kwarg):
        param_val = "book title"
        response = self.client.post(
            "/nosqli/",
            {"user_input": param_val, "with_kwarg": with_kwarg},
            method_to_test="find",
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_insert_one(self, mocked, with_kwarg):
        values = ("Record One", "PyMongo is fun!", "Dani")
        param_val = (
            '{"title": "'
            + values[0]
            + '", "content": "'
            + values[1]
            + '", "author": "'
            + values[2]
            + '"}'
        )

        response = self.client.post(
            "/nosqli/",
            {"user_input": param_val, "with_kwarg": with_kwarg},
            method_to_test="insert_one",
        )

        validate_any_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            values,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_insert_many(self, mocked, with_kwarg):
        param_val = (
            '{{"title": "Record One", "content": "PyMongo is fun!", "author":'
            ' "Dani"},{"title": "Record Two", "content": "PyMongo is alright",'
            ' "author": "Dani"}}'
        )

        response = self.client.post(
            "/nosqli/",
            {"user_input": param_val, "with_kwarg": with_kwarg},
            method_to_test="insert_many",
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    def test_nosqli_rule_post_update(self, mocked):
        param_val = "New Title"

        response = self.client.post(
            "/nosqli/", {"user_input": param_val}, method_to_test="update"
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    def test_nosqli_rule_post_delete(self, mocked):
        param_val = (
            '{"title": "Record One", "content": "PyMongo is fun!", "author": "Dani"}'
        )

        response = self.client.post(
            "/nosqli/", {"user_input": param_val}, method_to_test="delete"
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @mocks.build_finding
    def test_cmdi_os_system(self, mocked):
        param_val = "echo attack"
        response = self.client.get("/cmdi/", {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "cmd-injection",
            1,
        )
        assert_subprocess_popen_finding_events(self.request_context.activity.findings)

    @pytest.mark.parametrize("method_name", ["get", "post"])
    @mocks.build_finding
    def test_ud_pickle(self, mocked, method_name):
        param_val = "(dp0\nS'lion'\np1\nS'yellow'\np2\nsS'kitty'\np3\nS'red'\np4\ns."

        params = dict(user_input=param_val)

        method = getattr(self.client, method_name)
        method("/untrusted-pickle/", params)

        assert (
            self.request_context.activity.findings[0].rule_id
            == "untrusted-deserialization"
        )

    @mocks.build_finding
    def test_ud_yaml(self, mocked):
        param_val = '!!map {\n  ? !!str "goodbye"\n}'
        response = self.client.get("/untrusted-yaml/", {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "untrusted-deserialization",
            1,
        )

    @mocks.build_finding
    def test_ud_yaml_all(self, mocked):
        param_val = '!!map {\n  ? !!str "goodbye"\n}'
        response = self.client.get(
            "/untrusted-yaml/", {"user_input": param_val}, load_all=True
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "untrusted-deserialization",
            1,
        )

    @mocks.build_finding
    def test_xss_escaped_no_vuln(self, mocked):
        param_val = "<script>alert(1)</script>"
        response = self.client.get(
            "/xss/", {"user_input": param_val}, django_escape=True
        )

        assert response is not None
        assert param_is_tracked(param_val)
        assert param_is_tracked(escape(param_val))

        assert not mocked.called
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("xml_url", ["/xxe-pulldom/", "/xxe-lxml/", "/xxe-sax/"])
    @mocks.build_finding
    def test_xxe_urls(self, mocked, xml_url):
        param_val = "<root>attack</root>"

        response = self.client.get(xml_url, {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "xxe",
            1,
        )

    @mocks.build_finding
    def test_xss_jinja(self, mocked):
        param_val = "im an attack!"
        response = self.client.get("/xss-jinja/", {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            response.content,
            mocked,
            "reflected-xss",
            1,
        )

    @mocks.build_finding
    def test_xss_mako(self, mocked):
        if django_version.startswith("3"):
            pytest.xfail("djangomako is broken in Django 3")

        param_val = "im an attack!"
        response = self.client.get("/xss-mako/", {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            response.content,
            mocked,
            "reflected-xss",
            1,
        )

    @pytest.mark.parametrize("route", ["/raw-xss/", "/raw-xss-streaming/"])
    @mocks.build_finding
    def test_xss_raw(self, mocked, route):
        param_val = "im an attack!"

        response = self.client.get(route, {"user_input": param_val})
        assert response.status_code == 200

        if "streaming" in route:
            # Make sure that our middleware doesn't consume streaming content
            content = list(response.streaming_content)
            assert content
            assert content[0] == b"<p>Looks like xss: im an attack!</p>"
        else:
            assert response.content == b"<p>Looks like xss: im an attack!</p>"

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"
        assert len(self.request_context.activity.findings) == 1

    @mocks.build_finding
    def test_xss_csv_does_not_send_finding(self, mocked):
        param_val = "im an attack!"
        response = self.client.get("/xss-csv/", {"user_input": param_val})

        assert response.status_code == 200

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"
        # even though build_finding is called, middleware later removes the finding from activity
        assert len(self.request_context.activity.findings) == 0

    @mocks.build_finding
    def test_cmdi_from_filename_and_contents(self, mocked):
        filename = "testfile.txt"
        file_path = os.path.join(BASE_DIR, "..", "data", filename)

        with open(file_path) as fp:
            response = self.client.post("/cmdi-file/", {"upload": fp})

        data_path = os.path.join(settings.MEDIA_ROOT, "data")
        result = "cp {0}/testfile.txt {0}/testfile.txt.bak".format(data_path)
        validate_finding(
            self.request_context.activity.findings,
            response,
            filename,
            result,
            mocked,
            "cmd-injection",
            1,
        )

        file_contents = (
            b"This file contains extremely dangerous data. Use at your own risk!\n"
        )
        param_is_tracked(file_contents)

    @mocks.build_finding
    def test_stream_source(self, mocked):
        response = self.client.get("/stream-source/")
        assert response.status_code == 200

        assert mocked.called
        assert mocked.call_args[0][1].name == "untrusted-deserialization"
        assert len(self.request_context.activity.findings) == 1

    def _build_ssrf_request(self, module, with_kwarg, use_https=None):
        data = {
            "url": "http://example.com/?q=foobar",
            "path": "/index.html",
            "hostname": "example.com",
            "module": module,
            "method": "GET",
            "with_kwarg": with_kwarg,
        }
        if use_https is not None:
            data["use_https"] = use_https
        return data

    @pytest.mark.parametrize(
        "module",
        (
            ["urllib", "urllib2_str", "urllib2_obj"]
            if six.PY2
            else ["urllib.request_str", "urllib.request_obj"]
        ),
    )
    @pytest.mark.parametrize("with_kwarg", [False, True])
    @mocks.build_finding
    def test_ssrf_dynamic_urllib(self, mocked, with_kwarg, module):
        response = self.client.post(
            "/ssrf-dynamic/", self._build_ssrf_request(module, with_kwarg)
        )
        assert response.status_code == 200
        assert_ssrf_finding(module, self.request_context, mocked)

    @pytest.mark.parametrize(
        "module",
        ["HTTPConnection.__init__"]
        + ["HTTPConnection.request-method", "HTTPConnection.putrequest-method"],
    )
    @pytest.mark.parametrize("use_https", [False, True])
    @pytest.mark.parametrize("with_kwarg", [False, True])
    @mocks.build_finding
    def test_ssrf_dynamic_httpclient(self, mocked, with_kwarg, use_https, module):
        response = self.client.post(
            "/ssrf-dynamic/", self._build_ssrf_request(module, with_kwarg, use_https)
        )
        assert response.status_code == 200
        assert_ssrf_finding(module, self.request_context, mocked)

    @pytest.mark.parametrize(
        "module", ["HTTPConnection.request", "HTTPConnection.putrequest"]
    )
    @pytest.mark.parametrize("use_https", [False, True])
    @pytest.mark.parametrize("with_kwarg", [False, True])
    @mocks.build_finding
    def test_ssrf_dynamic_safe(self, mocked, with_kwarg, use_https, module):
        """
        These triggers aren't vulnerable to SSRF, because they only accept
        path/querystring as the URL argument, which can't trigger SSRF.
        """
        response = self.client.post(
            "/ssrf-dynamic/", self._build_ssrf_request(module, with_kwarg, use_https)
        )
        assert response.status_code == 200
        assert not mocked.called
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("permanent_redirect", [True, False])
    @mocks.build_finding
    def test_unvalidated_redirect(self, mocked, permanent_redirect):
        """
        By passing a permanent redirect bool flag, we can test that both
        HttpResponsePermanentRedirect and HttpResponseRedirect are patched
        because they inherit from HttpResponseRedirectBase
        """
        redirect_route = "/cmdi/"
        response = self.client.get(
            "/unvalidated-redirect/",
            {"user_input": redirect_route, "permanent": permanent_redirect},
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            redirect_route,
            redirect_route,
            mocked,
            "unvalidated-redirect",
            1,
        )

    def test_preflight_hash_same_request(self):
        """
        Two requests that look exactly the same should generate the same hash
        """
        # This test will pass in isolation on django-1.10.8, but when the full test
        # suite runs, it will not. The findings are both present, but the first one
        # has way more events than the second one for some reason. It seems like
        # something in the test environment is polluting this test state somehow.
        if django_version.startswith("1.10"):
            pytest.xfail("Known weirdness with events on django-1.10.8 apptest")

        self.client.get("/cmdi/", {"user_input": "first attack"})

        assert len(self.request_context.activity.findings) == 1
        first_finding = self.request_context.activity.findings[0]

        self.client.get("/cmdi/", {"user_input": "second attack"})
        assert len(self.request_context.activity.findings) == 1
        second_finding = self.request_context.activity.findings[0]

        assert second_finding is not first_finding
        assert second_finding.hash_code == first_finding.hash_code
        assert second_finding.preflight == first_finding.preflight

    def test_preflight_hash_different_requests(self):
        """
        Two different requests that find the same vuln should have different hashes

        In this case, the two requests are the same except one uses GET and the
        other uses POST. Since the HTTP method contributes to the hash, we
        should get different preflight values.
        """
        param_val = "im an attack!"
        self.client.get("/cmdi/", {"user_input": param_val})

        assert len(self.request_context.activity.findings) == 1
        first_finding = self.request_context.activity.findings[0]

        self.client.post("/cmdi/", {"user_input": param_val})
        assert len(self.request_context.activity.findings) == 1
        second_finding = self.request_context.activity.findings[0]

        assert second_finding is not first_finding
        assert second_finding.hash_code != first_finding.hash_code
        assert second_finding.preflight != first_finding.preflight

    def test_preflight_hash_same_request_different_vulns(self):
        """
        The same request that generates two different vulns should have different hashes
        """
        param_val = "im an attack!"
        self.client.get("/two-vulns/", {"user_input": param_val})

        assert len(self.request_context.activity.findings) == 2

        first_finding = self.request_context.activity.findings[0]
        second_finding = self.request_context.activity.findings[1]

        assert second_finding.hash_code != first_finding.hash_code
        assert second_finding.preflight != first_finding.hash_code

    def test_untrusted_exec(self):
        user_input = "x = 1 + 2 + 3"
        self.client.get("/untrusted-exec/", dict(user_input=user_input))

        assert len(self.request_context.activity.findings) == 2
        assert (
            self.request_context.activity.findings[0].rule_id
            == u"unsafe-code-execution"
        )

    @python2_only
    def test_untrusted_execfile(self):
        user_input = "fake_filename.py"
        self.client.get("/untrusted-execfile/", dict(user_input=user_input))

        assert len(self.request_context.activity.findings) == 2
        assert self.request_context.activity.findings[0].rule_id == u"path-traversal"

    @pytest.mark.parametrize(
        "test_type",
        [
            "create_method",
            "init_direct",
            "filter",
            "multi-column",  # TODO: PYT-583 still need to test multi-trigger / multi findings
        ],
    )
    @pytest.mark.django_db(transaction=False)
    @mocks.build_finding
    def test_stored_xss(self, mocked, test_type):
        param_val = "hello"
        response = self.client.get(
            "/stored-xss/", {"user_input": param_val, "test_type": test_type}
        )

        findings = self.request_context.activity.findings

        validate_finding(
            findings, response, param_val, response.content, mocked, "reflected-xss", 1
        )

        assert_event_sources(findings, "database", {"database": "TAINTED_DATABASE"})


class DjangoRouteCoverageTestMixin(object):
    @pytest.mark.xfail(
        django_version.startswith("3"),
        reason="TODO: PYT-821 fix route coverage for Django 3",
    )
    @mock_build_update_messages
    def test_finds_app_routes(self, build_update_message):
        self.client.get("/cmdi/", {"user_input": "; echo /etc/passwd | nc"})

        routes = build_update_message.call_args[0][0]
        cmdi_routes = current_routes_by_url(routes, "cmdi/")
        assert_routes_count(cmdi_routes, 2)

    @pytest.mark.xfail(
        django_version.startswith("3"),
        reason="TODO: PYT-821 fix route coverage for Django 3",
    )
    @mock_build_update_messages
    def test_reports_dynamic_route_in_discovery(self, build_update_message):
        """
        Tests that a dynamically-created route is found because the first request
        made is to the endpoint that creates this route. The dynamically-created
        route is not visited.
        """
        new_view = "new_dynamic"
        original_url_names = [x.name for x in URLPATTERNS_COPY[1:]]
        assert new_view not in original_url_names

        self.client.get("/dynamic_url_view/", {"user_input": new_view})

        routes = build_update_message.call_args[0][0]
        dynamic_routes = current_routes_by_url(routes, new_view + "/")
        assert_routes_count(dynamic_routes, 2)

    @pytest.mark.xfail(
        django_version.startswith("3"),
        reason="TODO: PYT-821 fix route coverage for Django 3",
    )
    @mock_send_messages
    @mock_build_update_messages
    def test_reports_dynamic_route_by_observed_route(
        self, build_update_message, send_messages
    ):
        """
        Tests that a dynamically-created route is found because it is visited. The
        endpoint that created this route was not the first request to the app.
        """
        new_view = "new_dynamic"
        original_url_names = [x.name for x in URLPATTERNS_COPY[1:]]
        assert new_view not in original_url_names

        self.client.get("/")

        routes = build_update_message.call_args[0][0]
        current_routes = current_routes_by_url(routes, "/" + new_view)
        # new_dynamic has not been created so it is not found
        assert_routes_count(current_routes, 0)

        assert len(send_messages.call_args[0][0]) == 4

        self.client.get("/dynamic_url_view/?user_input=" + new_view)

        assert len(send_messages.call_args[0][0]) == 3

        self.client.get("/" + new_view + "/")
        call_args = send_messages.call_args[0][0]
        assert len(call_args) == 3

        observed_route = call_args[2]
        assert isinstance(observed_route, ObservedRoute)
        assert observed_route.url == new_view + "/"
        assert observed_route.signature == "app.view_definitions.new_dynamic(request,)"

    @pytest.mark.xfail(
        django_version.startswith("3"),
        reason="TODO: PYT-821 fix route coverage for Django 3",
    )
    def test_route_appended_to_xss_vuln(self):
        param_val = "im an attack!"
        response = self.client.get("/xss/", {"user_input": param_val})

        assert response
        assert len(self.request_context.activity.findings) > 0
        assert_route_appended(self.request_context.activity.findings, "xss/", "GET")

    @pytest.mark.xfail(
        django_version.startswith("3"),
        reason="TODO: PYT-821 fix route coverage for Django 3",
    )
    @pytest.mark.django_db(transaction=False)
    def test_observed_route_appended(self):
        param_val = "im an attack!"
        param_name = "user_input"
        url = "/sqli/"
        response = self.client.get(url, {param_name: param_val})

        assert response
        assert len(self.request_context.activity.findings) == 1
        validate_observed_route(
            self.request_context, "GET", url[1:], param_name, "PARAMETER"
        )

    @pytest.mark.xfail(
        django_version.startswith("3"),
        reason="TODO: PYT-821 fix route coverage for Django 3",
    )
    # We should get a finding whether or not the input is valid
    @pytest.mark.parametrize("param_val", ["0 + 1 + 2", "garbage"])
    @mocks.build_finding
    def test_unsafe_code_execution_eval(self, mocked, param_val):
        response = self.client.get(
            "/unsafe-code-exec/", {"user_input": param_val, "with_eval": True}
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "unsafe-code-execution",
            1 if six.PY3 else 2,
        )


class DjangoAssessTestDynamicSources(object):

    ATTACK_VALUE = "im an attack!"
    DYNAMIC_SOURCE_RULE_ID = "cmd-injection"

    def set_dangerous_cookie(self):
        self.client.cookies["user_input"] = self.ATTACK_VALUE

    @mocks.build_finding
    def test_xss_from_cookie(self, mocked):
        self.set_dangerous_cookie()
        self.client.get("/xss-cookie/")

        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("source", GET_SOURCES)
    @mocks.build_finding
    def test_all_get_sources(self, mocked, source):
        self.set_dangerous_cookie()
        response = self.client.get(
            "/dynamic-sources/",
            {"user_input": self.ATTACK_VALUE, "source": source},
            HTTP_REFERER="www.python.org",
            **{source: self.ATTACK_VALUE}
        )

        validate_source_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            source,
            self.DYNAMIC_SOURCE_RULE_ID,
            1,
        )

    @pytest.mark.parametrize("source", POST_SOURCES)
    @mocks.build_finding
    def test_all_post_sources(self, mocked, source):
        self.set_dangerous_cookie()
        if source == "files":
            file_path = os.path.join(BASE_DIR, "..", "data", "testfile.txt")
            with open(file_path, "rb") as fp:
                response = self.client.post(
                    "/dynamic-sources/",
                    {"source": source, "user_input": fp},
                    HTTP_REFERER="www.python.org",
                )

        else:
            response = self.client.post(
                "/dynamic-sources/",
                {"user_input": self.ATTACK_VALUE, "source": source},
                HTTP_REFERER="www.python.org",
                **{source: self.ATTACK_VALUE}
            )

        validate_source_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            source,
            self.DYNAMIC_SOURCE_RULE_ID,
            1,
        )

    @mocks.build_finding
    def test_cookie_get(self, mocked):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.set_dangerous_cookie()
        self.client.get("/cookie-source/")
        validate_cookies_sources(self.request_context.activity.findings)

    @mocks.build_finding
    def test_cookie_post(self, mocked):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.set_dangerous_cookie()
        self.client.post("/cookie-source/")
        validate_cookies_sources(self.request_context.activity.findings)

    @pytest.mark.parametrize(
        "route,source_name",
        [("/header-source/", "header"), ("/header-key-source/", "header_key")],
    )
    @pytest.mark.parametrize("method_name", ["get", "post"])
    @pytest.mark.parametrize("use_environ", [False, True])
    @mocks.build_finding
    def test_header_source(self, mocked, use_environ, method_name, route, source_name):
        method = getattr(self.client, method_name)
        method(route, HTTP_TEST_HEADER="whatever", use_environ=use_environ)

        validate_header_sources(self.request_context.activity.findings, source_name)
