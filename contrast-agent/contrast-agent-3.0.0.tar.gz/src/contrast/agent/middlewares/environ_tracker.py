# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import iteritems

from contrast.agent import scope
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.policy.source_policy import cs__apply_source
from contrast.utils.assess.stream_utils import ContrastWsgiStreamProxy
from contrast.utils.decorators import fail_safely


# a best effort at translating the types in this document:
# https://bitbucket.org/contrastsecurity/teamserver/src/862d499227e8eac42b6eb7c6b03f10b7f1556218/teamserver-agent-messages/src/main/java/contrast/agent/messages/finding/trace/EventSourceTypeDTM.java#lines-8
ENVIRON_SOURCES = {
    "CONTENT_LENGTH": "HEADER",
    "CONTENT_TYPE": "HEADER",
    "PATH_INFO": "URI",
    "QUERY_STRING": "QUERYSTRING",
    "REMOTE_ADDR": "URI",
    "REMOTE_HOST": "URI",
    "REMOTE_USER": "URI",
    "REQUEST_METHOD": "HEADER",
    "SCRIPT_NAME": "HEADER",
    "SERVER_NAME": "HEADER",
    "SERVER_PORT": "HEADER",
    "SERVER_PROTOCOL": "HEADER",
    "wsgi.url_scheme": "OTHER",
    "webob.adhoc_attrs": "OTHER",
    "webob.url_encoding": "OTHER",
}

SOURCE_TAGS = {"HEADER": ["NO_NEWLINES"], "PARAMETER": ["CROSS_SITE"]}

SOURCE_DICT = {"module": "wsgi.environ", "instance_method": False, "target": "RETURN"}

WEBOB_KEYS = {
    "webob._parsed_query_vars",
    "webob._parsed_post_vars",
    "webob._body_file",
    "webob.is_body_seekable",
    "webob._parsed_cookies",
    "webob._cache_control",
}


def _track_keys_and_values(
    framework, context, mapping, key_type, value_type, no_cross_site=False
):
    for key, value in mapping.items():
        if key:
            key_node = build_source_node(framework, key, key_type, no_cross_site)
            cs__apply_source(
                context, key_node, key, mapping, key, (), {}, source_name=key
            )

        if value:
            value_node = build_source_node(framework, value, value_type, no_cross_site)
            cs__apply_source(
                context, value_node, value, mapping, value, (), {}, source_name=key
            )


@fail_safely("failed to track cookie sources")
def track_cookie_sources(framework, context, cookies):
    """track cookie keys and values"""
    if skip_analysis(context):
        return

    with scope.contrast_scope():
        _track_keys_and_values(
            framework, context, cookies, "COOKIE_KEY", "COOKIE", no_cross_site=True
        )


@fail_safely("Failed to track environ sources")
def track_environ_sources(framework, context, environ, skip_wsgi_input=False):
    """
    This method will track necessary information in the environ

    For wsgi frameworks, this is the one true source of (stateless) untrusted data

    :param framework: current application's framework
    :param context: current request context
    :param environ: WSGI environ dict
    :param skip_wsgi_input: If True, do not track the wsgi.input stream.

    :return: None
    """
    if skip_analysis(context):
        return

    with scope.contrast_scope():
        for key, value in iteritems(environ):
            source_type = ""
            if key in ENVIRON_SOURCES:
                source_type = ENVIRON_SOURCES[key]

                node = build_source_node(framework, key, source_type, False)

                cs__apply_source(
                    context, node, value, environ, value, (), {}, source_name=key
                )
            elif key.startswith("HTTP_"):
                # This is to track custom headers we may not know about
                source_type = "COOKIE" if key == "HTTP_COOKIE" else "HEADER"

                node = build_source_node(framework, key, source_type, "COOKIE" in key)

                cs__apply_source(
                    context, node, value, environ, value, (), {}, source_name=key
                )

            # Track HTTP header keys as well
            if key.startswith("HTTP_") or source_type == "HEADER":
                no_cross_site = (source_type == "HEADER") or (key == "HTTP_COOKIE")

                key_node = build_source_node(
                    framework, key, "HEADER_KEY", no_cross_site
                )
                cs__apply_source(
                    context, key_node, key, environ, key, (), {}, source_name=key
                )

        if "wsgi.input" in environ and not skip_wsgi_input:
            if not hasattr(environ["wsgi.input"], "cs__source"):
                environ["wsgi.input"] = ContrastWsgiStreamProxy(environ["wsgi.input"])

            environ["wsgi.input"].cs__source = True
            environ["wsgi.input"].cs__source_type = "BODY"
            environ["wsgi.input"].cs__source_tags = ["UNTRUSTED", "CROSS_SITE"]

        remove_webob_environ_vars(environ)


@fail_safely("Failed to remove webob environ variables")
def remove_webob_environ_vars(environ):
    """
    webob adds several variables to the environ for efficiency. For example, if webob
    ever parses wsgi.input to extract request body parameters, it stores them in a
    MultiDict under environ['webob._parsed_post_vars']. This way, if a future middleware
    or application using webob tries to access the post params again, it doesn't need to
    re-parse the request body.

    This is a good idea, but it's really a pain for us. It means that it's not enough
    to simply track wsgi.input, because if it has already been parsed once by the time
    we call the environ tracker, data stored under these special webob.* keys won't be
    tracked. Here, we delete these variables, forcing webob to re-parse any necessary
    info using our now-tracked environ values. In the future, we should instead iterate
    over these entries and track their values explicitly, for the sake of performance.

    Another consequence of deleting these variables is that their values will necessarily
    be webob types for which we have patches. Since our request wrapper is a subclass of
    contrast.extern.webob.BaseRequest, we were ending up with _our_ externed webob objects
    in the application's environ. We don't have or want patches for our own externed webob,
    so this ensures that all of webob's cached environ values will have patches.

    We should always check to see if these values are present, even if we're inside
    of a framework that doesn't explicitly use webob. This is because it's possible that
    an earlier middleware used webob, causing the values to be added to environ.

    To the best of our current understanding, the following extra environ items are
    of interest:

    webob._parsed_query_vars
        A 2-tuple
        - first element is a MultiDict of parsed GET parameters
        - second element is the query string that was parsed

    webob._parsed_post_vars
        A 2-tuple
        - the first element is a MultiDict of parsed POST parameters
        - the second is the body stream that was parsed

    webob.adhoc_attrs
        A custom dictionary of arbitrary data passed between middlewares. We make a best
        effort to patch this, and we don't delete it, because we can't know much about it

    webob._body_file
        A 2-tuple
        - first element is a double-wrapper for the raw wsgi.input stream
            BufferedReader(webob.LimitedLengthFile(wsgi.input))
        - second element is the underlying raw wsgi.input stream
            It should be PEP-333 compliant

    webob.is_body_seekable
        A boolean
        - Created/set to True once webob replaces wsgi.input with a seekable file-like object
        - Assumed to be False if missing

    webob._parsed_cookies
        A 2-tuple
        - first element is a dict of cookie keys to cookie values (parsed from HTTP_COOKIE)
        - second element is the HTTP_COOKIE string that was parsed to produce element #1

    TODO: webob._cache_control

    webob.url_encoding
        A string
        - Used to store the string encoding of the URL. We don't delete it because it's easy
        to track directly. In the future we might want to look into whether we need to track
        this at all.

    :param environ: WSGI environ dict
    :return: None
    """
    for key in WEBOB_KEYS:
        if key in environ:
            del environ[key]


def build_source_node(framework, method_name, source_type, no_cross_site=False):
    """
    Builds a new SourceNode based on the method name and source type

    Since cookie sources are not tagged with CROSS_SITE, callers must indicate whether
    the given source corresponds to a cookie or not.

    :param framework: str framework name for node
    :param method_name: name of the environ key
    :param source_type: type of the source
    :param no_cross_site: boolean indicating whether source tags include CROSS_SITE
    :return: SourceNode for cs__apply_source
    """

    source_dict = SOURCE_DICT.copy()

    tags = [] if no_cross_site else SOURCE_TAGS.get(source_type, ["CROSS_SITE"])

    source_dict["method_name"] = method_name
    source_dict["type"] = source_type
    source_dict["tags"] = tags

    return SourceNode.from_dict(framework, source_dict)
