# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import cgi

from contrast.extern.six import iteritems, PY2
from contrast.extern.six.moves.collections_abc import Mapping

import contrast
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.properties import Properties
from contrast.agent.assess.utils import (
    get_properties,
    get_last_event_ids_from_sources,
    track_string,
    update_properties,
    value_of_source,
)
from contrast.utils.assess.duck_utils import is_iterable, safe_iterator
from contrast.utils.decorators import fail_safely
from contrast.utils.string_utils import truncated_signature
from contrast.agent.settings_state import SettingsState

import logging

logger = logging.getLogger("contrast")

try:
    # We only need this if werkzeug is actually installed
    # It is necessary since this is not a subclass of dict/Mapping
    from werkzeug.datastructures import EnvironHeaders

    werkzeug_headers = (EnvironHeaders,)
except ImportError:
    werkzeug_headers = ()


class SourcePolicy(object):
    @staticmethod
    def apply(source_nodes, self_obj, ret, args, kwargs=None):
        """
        Apply node into all sources to track all new strings coming in from a request
        """
        context = contrast.CS__CONTEXT_TRACKER.current()
        if context is None or not SettingsState().is_assess_enabled():
            return

        for node in source_nodes:

            # args[0] is `self` for instance methods
            args = args[1:] if node.instance_method else args

            target = node.get_matching_first_target(self_obj, ret, args, kwargs)
            if hasattr(target, "cs__source"):
                # Target is already a source, nothing to do
                if target.cs__source:
                    return

                target.cs__source = True
                target.cs__source_type = node.type
                target.cs__source_tags = node.tags
                target.cs__properties = Properties(target)

            cs__apply_source(context, node, target, self_obj, ret, args, kwargs)

        return ret


def adjust_source_tags(tags, source_type, source_name):
    """
    Update source tags to account for Referer header

    The XSS spec dictates that, with a single exception, no HTTP headers (or keys)
    should trigger XSS due to a high rate of false positives. The one exception is the
    'Referer' header. In order to account for this, we add the CROSS_SITE tag if the
    given source appears to correspond to this header value.
    """
    is_header = source_type == "HEADER"
    # This accounts for various representations of referer header keys, including
    # 'Referer' and 'HTTP_REFERER'
    is_referer = is_header and source_name and source_name.lower().endswith("referer")

    # According to XSS spec, the only header that should have CROSS_SITE is Referer.
    return (
        list(tags) + ["CROSS_SITE"]
        if (is_referer and "CROSS_SITE" not in tags)
        else list(tags)
    )


@fail_safely("Error in apply_stream_source")
def apply_stream_source(method_name, target, self_obj, ret, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None or not SettingsState().is_assess_enabled():
        return

    module = self_obj.__class__.__module__
    class_name = self_obj.__class__.__name__

    source_type = getattr(self_obj, "cs__source_type", None) or "BODY"
    source_tags = getattr(self_obj, "cs__source_tags", None) or ["UNTRUSTED"]

    node = SourceNode(
        module,
        class_name,
        True,
        method_name,
        "RETURN",
        source_type,
        None,
        tags=source_tags,
    )

    cs__apply_source(context, node, target, self_obj, ret, args, kwargs)


NAMED_SOURCE_TYPES = [
    "PARAMETER",
    "PARAMETER_KEY",
    "HEADER",
    "HEADER_KEY",
    "COOKIE",
    "COOKIE_KEY",
    "MULTIPART_HEADER",
    "MULTIPART_HEADER_KEY",
    "MULTIPART_PARAMETER",
    "MULTIPART_PARAMETER_KEY",
]


def _get_source_name(node, self_obj, args):
    """
    Determine name for source

    Some sources require a source name since there can potentially be multiple values
    for that given source type (e.g. multiple headers, cookies, etc.).

    If no source name is explicitly given, but we have a dict/mapping object, then we
    try to use the dict/mapping key as the source name. This assumes that the
    instrumented dict/mapping method is something like __getitem__.

    Otherwise, use the method name (e.g. for `flask.wrappers.Request.full_path`, the
    source name will be "full_path").
    """
    if args and isinstance(self_obj, (dict, Mapping) + werkzeug_headers):
        return args[0]

    return node.method_name


def cs__apply_source(
    context, node, target, self_obj, ret, args, kwargs, source_name=None
):
    # target: {param: test} / QueryDict
    # self_obj: QueryDict
    # ret: test
    # args: param
    # TODO swap target for self_obj

    logger.debug("In cs__apply_source for %r", node)

    if node.type in NAMED_SOURCE_TYPES and not source_name:
        source_name = _get_source_name(node, self_obj, args)

    _cs__apply_source(
        context, node, target, self_obj, ret, node.type, source_name, True, args, kwargs
    )


@fail_safely("Unable to apply source for node")
def _cs__apply_source(
    context,
    node,
    target,
    self_obj,
    ret,
    source_type,
    source_name,
    use_source_key,
    args,
    kwargs,
):

    if not context or not node or target is None:
        return

    if hasattr(target, "cs__properties"):
        target_properties = target.cs__properties
    else:
        target_properties = get_properties(target)
        if target_properties is None:
            target_properties = track_string(target)

    if target_properties is not None:
        if not getattr(target, "cs__source", False):
            for tag in adjust_source_tags(node.tags, source_type, source_name):
                length = len(target)

                target_properties.add_tag(tag, AdjustedSpan(0, length))
                target_properties.add_properties(node.properties)

                logger.debug(
                    "Source %s detected: %s tagged with %s",
                    node.name,
                    truncated_signature(target),
                    str(tag),
                )

        parent_ids = get_parent_ids(node, self_obj, ret, args, kwargs)
        target_properties.build_event(
            node,
            target,
            self_obj,
            ret,
            args,
            kwargs,
            parent_ids,
            possible_key=None,
            source_type=source_type,
            source_name=source_name,
        )

        if hasattr(target, "cs__properties"):
            target.cs__properties = target_properties
        else:
            update_properties(target, target_properties)

    elif isinstance(target, dict):
        # This logic is intended to handle the case where the source is a dict
        # that happens to represent request parameters, headers, or cookies.
        # In these cases we want the top-level keys of this dictionary to be
        # labeled with the appropriate data type (e.g. PARAMETER_KEY). This
        # behavior should not apply to recursive calls, however.
        source_key_type = key_type(source_type) if use_source_key else source_type
        for key, value in iteritems(target):
            _cs__apply_source(
                context,
                node,
                key,
                self_obj,
                ret,
                source_key_type,
                key,
                False,
                args,
                kwargs,
            )
            _cs__apply_source(
                context,
                node,
                value,
                self_obj,
                ret,
                source_type,
                key,
                False,
                args,
                kwargs,
            )

    elif isinstance(target, cgi.FieldStorage):
        # circular import
        from contrast.utils.assess.stream_utils import (  # noqa
            ContrastFileProxy,
            ContrastRawIOProxy,
            BaseStreamProxy,
        )

        if hasattr(target, "filename"):
            _cs__apply_source(
                context,
                node,
                target.filename,
                self_obj,
                ret,
                source_type,
                source_name,
                False,
                args,
                kwargs,
            )
        if hasattr(target, "file") and not isinstance(target.file, BaseStreamProxy):
            # In PY2, FieldStorage.file has type `file`. In PY3, it has type FileIO.
            if hasattr(target.file, "cs__source"):
                target.file.cs__source = True
            elif PY2:
                target.file = ContrastFileProxy(target.file)
            else:
                target.file = ContrastRawIOProxy(target.file)

            # TODO: fix so we get the proper source type for Pyramid files (PYT-621)
            # target.file.cs__source_type = node.type
            target.file.cs__source_tags = node.tags

    elif is_iterable(target):
        for value in safe_iterator(target):
            _cs__apply_source(
                context,
                node,
                value,
                self_obj,
                ret,
                source_type,
                source_name,
                False,
                args,
                kwargs,
            )


def get_parent_ids(node, self_obj, ret, args, kwargs):
    if isinstance(node, SourceNode):
        return []

    sources = [
        value_of_source(source, self_obj, ret, args, kwargs) for source in node.sources
    ]
    return get_last_event_ids_from_sources(sources)


KEY_MAPPING = {
    "PARAMETER": "PARAMETER_KEY",
    "HEADER": "HEADER_KEY",
    "COOKIE": "COOKIE_KEY",
}

PARAMETER_TYPE = "PARAMETER"
PARAMETER_KEY_TYPE = "PARAMETER_KEY"
HEADER_TYPE = "HEADER"
HEADER_KEY_TYPE = "HEADER_KEY"
COOKIE_TYPE = "COOKIE"
COOKIE_KEY_TYPE = "COOKIE_KEY"
QUERYSTRING_TYPE = "QUERYSTRING"


def key_type(source_type):
    return KEY_MAPPING.get(source_type, source_type)
