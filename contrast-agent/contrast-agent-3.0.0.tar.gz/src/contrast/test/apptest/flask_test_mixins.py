# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from os import path

import pytest
import six  # pylint: disable=did-not-import-extern

from contrast.agent.assess import policy_constants
from contrast.agent.assess.utils import get_properties
from contrast.api.dtm_pb2 import TraceEvent
from contrast.test import mocks
from contrast.test.apptest_utils import (
    check_event,
    validate_finding,
    validate_source_finding,
    validate_header_sources,
    validate_cookies_sources,
)


SOURCE_OPTIONS_MAP = {
    "args": "QUERYSTRING",
    "base_url": "URI",
    "full_path": "URI",
    "referer_header": "HEADER",
    "host": "URI",
    "host_url": "URI",
    "path": "URI",
    "query_string": "QUERYSTRING",
    "scheme": "OTHER",
    "url": "URI",
    "url_root": "URI",
    "values": "PARAMETER",
    "values_get_item": "PARAMETER",
}
# REMOTE_ADDR does not appear to be present in environ in Py27
SOURCE_OPTIONS_MAP.update({"remote_addr": "URI"} if six.PY3 else {})


POST_OPTIONS_MAP = {
    "files": "MULTIPART_CONTENT_DATA",
    "form": "MULTIPART_FORM_DATA",
    "wsgi.input": "BODY",
}

MULTIDICT_GET_OPTIONS_MAP = {
    "items": "QUERYSTRING",  # args.items()
    "lists": "QUERYSTRING",  # args.lists()
    "listvalues": "QUERYSTRING",  # args.listvalues()
    "values": "QUERYSTRING",  # args.values()
}

MULTIDICT_POST_OPTIONS_MAP = {
    "items": "MULTIPART_FORM_DATA",  # form.items()
    "lists": "MULTIPART_FORM_DATA",  # form.lists()
    "listvalues": "MULTIPART_FORM_DATA",  # form.listvalues()
    "values": "MULTIPART_FORM_DATA",  # form.values()
}


ALL_OPTIONS_MAP = {}
ALL_OPTIONS_MAP.update(SOURCE_OPTIONS_MAP)
ALL_OPTIONS_MAP.update(POST_OPTIONS_MAP)


SOURCE_OPTIONS = tuple(SOURCE_OPTIONS_MAP.keys())
POST_OPTIONS = tuple(POST_OPTIONS_MAP.keys())


def assert_flask_sqli_finding_events(finding, source_class_name):
    assert len(finding.events) == 16

    # TODO: this needs to be updated when urllib.parse.unquote is added as a propagator

    check_event(
        finding.events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.CREATION_TYPE),
        class_name=source_class_name,
        method_name="QUERY_STRING",
        source_types=["QUERYSTRING"],
        first_parent=None,
    )
    check_event(
        finding.events[1],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="encode",
        source_types=[],
        first_parent=finding.events[0],
    )
    check_event(
        finding.events[2],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="split",
        source_types=[],
        first_parent=finding.events[1],
    )
    check_event(
        finding.events[3],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[2],
    )
    check_event(
        finding.events[4],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[3],
    )
    check_event(
        finding.events[5],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="decode",
        source_types=[],
        first_parent=finding.events[4],
    )
    check_event(
        finding.events[9],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[8],
    )
    check_event(
        finding.events[10],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[9],
    )

    # There are a few f-string propagation events here that previously were
    # omitted because they have no effect (i.e. the resulting string is
    # identical to the input). They are now showing up because we had to make a
    # fix to join propagation, which affects f-strings as well.

    check_event(
        finding.events[14],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        # TODO: for some reason this event doesn't have any parent_object_ids
        first_parent=None,
    )
    check_event(
        finding.events[15],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.TRIGGER_TYPE),
        class_name="sqlite3.Cursor",
        method_name="execute",
        source_types=[],
        first_parent=finding.events[14],
    )


class FlaskAssessTestMixin(object):
    def validate_source_finding(self, response, mocked, source, options_map=None):
        validate_source_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            source,
            "reflected-xss",
            1,
            options_map or ALL_OPTIONS_MAP,
        )

    def assert_propagation_happened(self, apply_trigger):
        """
        This tests that apply_trigger was called with the "ret" argument
        that has an HTML_ENCODED tag, indicating that propagation did occur.
        """
        assert apply_trigger.called
        call_args = apply_trigger.call_args
        ret_arg = call_args[0][2]
        assert "HTML_ENCODED" in get_properties(ret_arg).tags

    @mocks.build_finding
    def test_xss_raw(self, mocked):
        user_input = "whatever"
        response = self.client.post("/raw-xss?user_input=" + user_input)

        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 1
        finding = self.request_context.activity.findings[0]
        assert finding.rule_id == "reflected-xss"

        trigger_event = finding.events[-1]
        assert trigger_event.signature.class_name == "flask.app.Flask"
        assert trigger_event.signature.method_name == "wsgi_app"

    @pytest.mark.parametrize("user_input", ["something <> dangerous", "something safe"])
    @mocks.apply_trigger
    @mocks.build_finding
    def test_jinja_sanitized_xss(self, build_finding, apply_trigger, user_input):
        response = self.client.post("/sanitized-xss?user_input=" + user_input)

        assert response.status_code == 200

        self.assert_propagation_happened(apply_trigger)
        assert not build_finding.called
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("source", SOURCE_OPTIONS)
    @mocks.build_finding
    def test_all_get_sources(self, mocked, source):
        self.client.set_cookie("localhost", "user_input", "attack_cookie")
        response = self.client.get(
            "/dynamic-sources/?user_input={}&source={}".format(
                self.ATTACK_VALUE, source
            ),
            headers={"Referer": "www.python.org"},
            data={"attack": self.ATTACK_VALUE},
        )

        self.validate_source_finding(response, mocked, source)

    @pytest.mark.parametrize("source", SOURCE_OPTIONS + POST_OPTIONS)
    @mocks.build_finding
    def test_all_post_sources(self, mocked, source):
        self.client.set_cookie("test", "user_input", "attack_cookie")
        with open(
            path.join(self.app.root_path, "..", "..", "data", "testfile.txt"), "rb"
        ) as f:
            fileobj = (f, "user_input.txt")
            response = self.client.post(
                "/dynamic-sources/?user_input={}&source={}".format(
                    self.ATTACK_VALUE, source
                ),
                headers={"Referer": "www.python.org"},
                data={"user_input": self.ATTACK_VALUE, "file_upload": fileobj},
            )

        self.validate_source_finding(response, mocked, source)

    @pytest.mark.parametrize("source", MULTIDICT_GET_OPTIONS_MAP.keys())
    @mocks.build_finding
    def test_all_get_multidict(self, mocked, source):
        response = self.client.get(
            "/multidict-sources",
            query_string={"user_input": self.ATTACK_VALUE, "source": source},
            headers={"user_input": self.ATTACK_VALUE},
        )

        self.validate_source_finding(
            response, mocked, source, MULTIDICT_GET_OPTIONS_MAP
        )

    @pytest.mark.parametrize("source", MULTIDICT_POST_OPTIONS_MAP.keys())
    @mocks.build_finding
    def test_all_post_multidict(self, mocked, source):
        response = self.client.post(
            "/multidict-sources",
            query_string={"source": source},
            headers={"user_input": self.ATTACK_VALUE},
            data={"user_input": self.ATTACK_VALUE},
        )

        self.validate_source_finding(
            response, mocked, source, MULTIDICT_POST_OPTIONS_MAP
        )

    def test_cookie_get(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.client.set_cookie("test", "user_input", "attack_cookie")
        self.client.get("/cookie-source")
        validate_cookies_sources(self.request_context.activity.findings)

    def test_cookie_post(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.client.set_cookie("test", "user_input", "attack_cookie")
        self.client.post("/cookie-source")
        validate_cookies_sources(self.request_context.activity.findings)

    @pytest.mark.parametrize(
        "route,source_name",
        [
            ("/header-source/", "header"),
            ("/header-key-source/", "header_key"),
            ("/method-source/", "header"),
        ],
    )
    @pytest.mark.parametrize("method_name", ["get", "post"])
    def test_non_xss_sources(self, method_name, route, source_name):
        method = getattr(self.client, method_name)
        method(route, headers={"Test-Header": "whatever"})

        validate_header_sources(self.request_context.activity.findings, source_name)

    @mocks.build_finding
    def test_sqli_rule_get(self, mocked):
        param_val = "doesnt matter"
        response = self.client.get("/sqli/?user_input=" + param_val)

        query = "SELECT * FROM user WHERE user.email = 'doesnt matter'"

        findings = self.request_context.activity.findings
        validate_finding(
            findings, response, param_val, query, mocked, "sql-injection", 1
        )
        # TODO: Update so that the events can be validated for the PY2 case as
        # well For the time being it only matters that we get a finding at all.
        if six.PY3:
            assert_flask_sqli_finding_events(findings[0], "wsgi.environ")

    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_unvalidated_redirect(self, mocked, with_kwarg):
        redirect_route = "/cmdi"
        response = self.client.get(
            "/unvalidated-redirect?user_input={}&with_kwarg={}".format(
                redirect_route, with_kwarg
            )
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
