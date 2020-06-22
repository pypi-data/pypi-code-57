# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import copy
import mock

import pytest
from contrast.extern import six

import contrast
from contrast.agent.assess import policy_constants
from contrast.agent.assess.policy import source_policy
from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.api.dtm_pb2 import Library, TraceEvent
from contrast.api.settings_pb2 import AgentSettings
from contrast.test.settings_builder import SettingsBuilder
from contrast.utils import patch_utils


@pytest.fixture(autouse=True)
def disable_service_client(mocker):
    """Prevent the test suite from inadvertently starting the service"""
    mocker.patch("contrast.agent.service_client.ServiceClient.start_service")
    mocker.patch(
        "contrast.agent.service_client.ServiceClient.send_dtm",
        return_value=AgentSettings(),
    )


@pytest.fixture(autouse=True)
def modified_modules_to_ignore_prefixes(monkeypatch):
    """
    In most uses of the agent we ignore module such as contrast...
    so we don't bother patching them, but since our apptests often start
    with contrast., we need to make sure these modules are not in the
    modules to ignore.
    """
    new_prefixes = list(patch_utils.MODULES_TO_IGNORE_PREFIXES[:])
    new_prefixes.remove("contrast.")
    new_prefixes = tuple(new_prefixes)

    monkeypatch.setattr(patch_utils, "MODULES_TO_IGNORE_PREFIXES", new_prefixes)


@pytest.fixture(autouse=True)
def reset_base_middleware():
    BaseMiddleware._loaded = False
    yield


@pytest.fixture(autouse=True, scope="module")
def disable_heartbeat():
    patch_heartbeat = mock.patch(
        "contrast.agent.settings_state.SettingsState.establish_heartbeat"
    )

    patch_heartbeat.start()
    yield
    patch_heartbeat.stop()


def assert_django_sqli_finding_events(finding, source_class_name):
    assert len(finding.events) == 5

    check_event(
        finding.events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.CREATION_TYPE),
        class_name=source_class_name,
        method_name="__getitem__",
        source_types=[source_policy.PARAMETER_TYPE],
        first_parent=None,
    )

    # TODO: this needs to be updated when urllib.parse.unquote is added
    # as a propagator

    check_event(
        finding.events[1],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.PARAMETER
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="django.utils.safestring",
        method_name="mark_safe",
        source_types=[],
        first_parent=finding.events[0],
    )

    check_event(
        finding.events[2],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
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
        method_name="concat",
        source_types=[],
        first_parent=finding.events[2],
    )

    # TODO: currently there is an fstring propagation inside of the django
    # ORM that has no effect. We are currently not recording events for
    # propagation actions that have no effect

    check_event(
        finding.events[4],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.TRIGGER_TYPE),
        class_name="SQLite3",
        method_name="execute",
        source_types=[],
        first_parent=finding.events[3],
    )


def assert_xss_cookie_finding_events(finding):
    import django

    legacy_django = django.__version__ < "1.11"

    assert len(finding.events) == 9

    check_event(
        finding.events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.CREATION_TYPE),
        class_name="django.http.request.HttpRequest",
        method_name="__getattribute__",
        source_types=[source_policy.COOKIE_TYPE],
        first_parent=None,
    )

    check_event(
        finding.events[1],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[0],
    )

    check_event(
        finding.events[2],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="cformat",
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
        method_name="join",
        source_types=[],
        first_parent=finding.events[2],
    )

    check_event(
        finding.events[8],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.TRIGGER_TYPE),
        class_name="django.core.handlers.base" if not legacy_django else "app",
        method_name="_get_response" if not legacy_django else "app",
        source_types=[],
        first_parent=finding.events[7],
    )


def assert_subprocess_popen_finding_events(findings):
    events = findings[0].events
    assert len(events) == 8

    check_event(
        events[0],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.CREATION_TYPE),
        class_name="wsgi.environ",
        method_name="QUERY_STRING",  # TODO PYT-865: wrong?
        source_types=[source_policy.QUERYSTRING_TYPE],  # TODO PYT-865: wrong?
        first_parent=None,
        source="",
        target=policy_constants.RETURN,
    )

    check_event(
        events[1],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="encode" if six.PY3 else "split",
        source_types=[],
        first_parent=events[0],
        source=policy_constants.OBJECT,
        target=policy_constants.RETURN,
    )

    check_event(
        events[2],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        )
        if six.PY3
        else TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="decode" if six.PY3 else "replace",
        source_types=[],
        first_parent=events[1],
        source=policy_constants.OBJECT if six.PY3 else "OBJ,P1",
        target=policy_constants.RETURN,
    )

    check_event(
        events[3],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str",
        method_name="split",
        source_types=[],
        first_parent=events[2],
        source=policy_constants.OBJECT,
        target=policy_constants.RETURN,
    )

    check_event(
        events[4],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="str" if six.PY3 else "urllib",
        method_name="replace" if six.PY3 else "unquote",
        source_types=[],
        first_parent=events[3],
        source="OBJ,P1" if six.PY3 else "P0,KWARG:s",
        target=policy_constants.RETURN,
    )

    check_event(
        events[5],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            policy_constants.ALL_TYPE
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        )
        if six.PY3
        else TraceEvent.Action.Value(
            policy_constants.OBJECT_KEY
            + policy_constants.TO_MARKER
            + policy_constants.RETURN_KEY
        ),
        class_name="urllib.parse" if six.PY3 else "str",
        method_name="unquote" if six.PY3 else "decode",
        source_types=[],
        first_parent=events[4],
        source="P0,KWARG:string" if six.PY3 else policy_constants.OBJECT,
        target=policy_constants.RETURN,
    )

    check_event(
        events[6],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.CREATION_TYPE),
        class_name="django.utils.datastructures.MultiValueDict",
        method_name="__getitem__",
        source_types=[source_policy.PARAMETER_TYPE],
        first_parent=None,  # TODO PYT-865: wrong?
        source="",  # TODO PYT-865: wrong?
        target=policy_constants.RETURN,
    )

    check_event(
        events[7],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(policy_constants.TRIGGER_TYPE),
        class_name="subprocess.Popen",
        method_name="__init__",
        source_types=[],
        first_parent=events[6],
        source="P0,KWARG:args",
        target="",
    )


def check_event(
    event,
    event_type,
    action,
    class_name,
    method_name,
    source_types,
    first_parent,
    source=None,
    target=None,
):
    assert event.type == event_type
    assert event.action == action
    assert event.signature.class_name == class_name
    assert event.signature.method_name == method_name

    assert all([s.type in source_types for s in event.event_sources])

    assert (
        event.parent_object_ids[0].id == first_parent.object_id
        if first_parent
        else True
    )

    if source:
        assert event.source == source

    if target:
        assert event.target == target


def _build_lxml_lib():
    fake_lxml = Library()
    fake_lxml.version = "1.11.1"
    fake_lxml.manifest = "test"
    fake_lxml.class_count = 100
    fake_lxml.used_class_count = 50
    fake_lxml.file_path = "lxml"
    fake_lxml.url = "lxml.com"
    fake_lxml.hash_code = "123499789"
    fake_lxml.external_ms = 1
    fake_lxml.internal_ms = 1

    return fake_lxml


def _build_django_lib():
    fake_django = Library()
    fake_django.version = "7.7.7"
    fake_django.manifest = "test"
    fake_django.class_count = 100
    fake_django.used_class_count = 50
    fake_django.file_path = "django"
    fake_django.url = "djangoproject.com"
    fake_django.hash_code = "987654321"
    fake_django.external_ms = 1
    fake_django.internal_ms = 1

    return fake_django


def _build_yaml_lib():
    fake_yaml = Library()
    fake_yaml.version = "1.11.1"
    fake_yaml.manifest = "test"
    fake_yaml.class_count = 100
    fake_yaml.used_class_count = 50
    fake_yaml.file_path = "pyyaml"
    fake_yaml.url = "yaml.org"
    fake_yaml.hash_code = "123456789"
    fake_yaml.external_ms = 1
    fake_yaml.internal_ms = 1

    return fake_yaml


def _build_sqlalchemy_lib():
    fake_sqlalchemy = Library()
    fake_sqlalchemy.version = "1.3.1"
    fake_sqlalchemy.manifest = "test"
    fake_sqlalchemy.class_count = 100
    fake_sqlalchemy.used_class_count = 50
    fake_sqlalchemy.file_path = "sqlalchemy"
    fake_sqlalchemy.url = "sqlalchemy.org"
    fake_sqlalchemy.hash_code = "123456789"
    fake_sqlalchemy.external_ms = 1
    fake_sqlalchemy.internal_ms = 1

    return fake_sqlalchemy


def _build_markupsafe_lib():
    fake_markupsafe = Library()
    fake_markupsafe.version = "1.1.1"
    fake_markupsafe.manifest = "test"
    fake_markupsafe.class_count = 100
    fake_markupsafe.used_class_count = 50
    fake_markupsafe.file_path = "markupsafe"
    fake_markupsafe.url = "markupsafe.org"
    fake_markupsafe.hash_code = "123456789"
    fake_markupsafe.external_ms = 1
    fake_markupsafe.internal_ms = 1

    return fake_markupsafe


def build_extra_libs():
    """
    When adding a vulnerability that requires a 3rd party library, make sure to add the library here!

    This is used to mimic actual libraries being found on pip
    """
    return [
        _build_django_lib(),
        _build_lxml_lib(),
        _build_yaml_lib(),
        _build_markupsafe_lib(),
    ]


def param_is_tracked(param_val):
    for props in contrast.STRING_TRACKER.values():
        if props.origin == param_val:
            return True
    return False


def _validate(response, tracked_param, mocked_build_finding):
    assert response is not None
    assert param_is_tracked(tracked_param)
    assert mocked_build_finding.called


def validate_finding(
    findings,
    response,
    tracked_param,
    result,
    mocked_build_finding,
    rule_id,
    num_findings,
):
    _validate(response, tracked_param, mocked_build_finding)

    args = mocked_build_finding.call_args[0]  # [1] is kwargs

    assert args[1].name == rule_id
    assert args[3] == result

    assert len(findings) == num_findings


def validate_any_finding(
    findings,
    response,
    tracked_param,
    possible_results,
    mocked_build_finding,
    rule_id,
    num_findings,
):
    _validate(response, tracked_param, mocked_build_finding)

    args = mocked_build_finding.call_args[0]

    assert args[1].name == rule_id
    assert args[3] in possible_results

    assert len(findings) == num_findings


def validate_nondataflow_finding(
    findings, response, mocked_build_finding, rule_id, call_count, num_findings
):
    assert response is not None

    assert mocked_build_finding.called
    assert mocked_build_finding.call_count == call_count

    args, _ = mocked_build_finding.call_args

    assert args[1].name == rule_id

    assert len(findings) == num_findings


def validate_observed_route(request_context, method, url, source_name, source_type):
    observed_route = request_context.observed_route

    assert observed_route.verb == method
    assert observed_route.url == url

    sources = observed_route.sources
    matching_source = [src for src in sources if src.name == source_name][0]

    assert matching_source.name == source_name
    assert matching_source.type == source_type


def assert_route_appended(findings, url, verb):
    """
    Asserts that 1 route with the url and verb are in the findings

    Fail if we never found a matching route
    """
    for finding in findings:
        for route in finding.routes:
            if route.url == url and route.verb == verb:
                return True

    routes_message = " Routes: {}".format(findings[0].routes) if findings else ""
    pytest.fail("Unable to find route in findings;" + routes_message)


def build_assess_settings():
    features = copy.deepcopy(SettingsBuilder.DEFAULT_FEATURES)
    features["defend"]["enabled"] = False
    features["assess"] = {"enabled": True}

    settings = SettingsBuilder().build_assess()

    # disable non dataflow rules
    settings.application_settings.disabled_assess_rules.append("crypto-weak-randomness")
    settings.application_settings.disabled_assess_rules.append("crypto-bad-mac")
    settings.application_settings.disabled_assess_rules.append("crypto-bad-ciphers")

    settings.libraries = build_extra_libs()

    return settings


def find_routes_by_verb(routes, verb):
    return [x for x in routes if x.verb == verb]


def current_routes_by_url(routes, url):
    return [x for x in routes.values() if x.url == url]


def assert_routes_count(routes, routes_count):
    assert len(routes) == routes_count


def assert_ssrf_finding(module, request_context, mocked):
    assert mocked.called
    assert mocked.call_args[0][1].name == "ssrf"

    # This case results in multiple findings for reasons that are not entirely understood
    num_findings = 2 if module == "urllib2_obj" else 1

    assert len(request_context.activity.findings) == num_findings
    assert request_context.activity.findings[0].rule_id == six.u("ssrf")


# These request part values must match the TYPE parameter for source nodes in policy.json, which are
# a best effort at translating the types in this document:
# https://bitbucket.org/contrastsecurity/teamserver/src/862d499227e8eac42b6eb7c6b03f10b7f1556218/teamserver-agent-messages/src/main/java/contrast/agent/messages/finding/trace/EventSourceTypeDTM.java#lines-8
SOURCE_OPTIONS = {
    "parameter": "PARAMETER",
    "cookies": "COOKIE",
    "body": "BODY",
    "full_path": "URI",
    "full_path_info": "URI",
    "raw_uri": "URI",
    "host": "URI",
    "port": "URI",
    "scheme": "OTHER",
    "encoding": "OTHER",
    "files": "MULTIPART_CONTENT_DATA",
    "form": "MULTIPART_FORM_DATA",
    "header": "HEADER",
    "referer_header": "HEADER",
    "header_key": "HEADER_KEY",
    "wsgi.input": "MULTIPART_CONTENT_DATA",
}


def validate_source_finding(
    findings,
    response,
    mocked_build_finding,
    source_name,
    rule_id,
    num_findings,
    source_map=None,
):
    assert response is not None
    assert mocked_build_finding.called

    args, _ = mocked_build_finding.call_args

    assert args[1].name == rule_id

    assert len(findings) == num_findings

    assert_event_sources(findings, source_name, source_map or SOURCE_OPTIONS)


def validate_header_sources(findings, source_name):
    assert len(findings) == 1
    assert findings[0].rule_id == "cmd-injection"
    assert_event_sources(
        findings, source_name, {"header": "HEADER", "header_key": "HEADER_KEY"}
    )


def validate_cookies_sources(findings):
    assert len(findings) == 1
    assert findings[0].rule_id == "cmd-injection"
    assert_event_sources(findings, "cookies", {"cookies": "COOKIE"})


def assert_event_sources(findings, source_name, source_options):
    all_event_sources = _get_event_sources(findings)
    # for now all we care is that the source name appears in TYPE at least once
    assert source_options[source_name] in [source.type for source in all_event_sources]


def _get_event_sources(findings):
    """
    Get all trace event sources from all finding.events

    :param findings: a list of Finding objects
    :return: a list of TraceEventSource objects
    """
    event_sources = []

    for finding in findings:
        for event in finding.events:
            if event.event_sources:
                for trace_event in event.event_sources:
                    event_sources.append(trace_event)

    return event_sources
