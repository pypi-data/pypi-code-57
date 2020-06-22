# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Propagator used for flask.helpers.safe_join

Tests for this propagator are found in
test/agent/assess/sanitizers/test_flask_sanitizers.py
"""
import posixpath

from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy.propagators import JoinPropagator
from contrast.agent.assess.utils import cs__apply_tags, cs__apply_untags
from contrast.utils.decorators import cached_property


class SafeJoinPropagator(JoinPropagator):
    """
    Sanitizing propagator for flask.helpers.safe_join

    The safe_join function is used to join path components to a base directory in such
    a way that a path traversal attack is not possible. The tag propagation from
    sources to target is the same as the basic str.join propagation. Unlike str.join,
    in the case of safe_join, the separator is not given as a source. Instead, we
    simply set it to posixpath.sep since that is what is used by safe_join under the
    hood.

    The most important difference between str.join and safe_join is the tags that are
    applied. The safe_join propagator adds sanitizing tags since the path components
    passed to safe_join can't contribute to a path traversal attack. However, safe_join
    _assumes_ that the base directory is trusted. We can't make that same assumption
    since it actually can come from anywhere, including an untrusted source. Since the
    base directory isn't validated by safe_join in any way, we do not apply safe tags
    to the corresponding range in the target.
    """

    def __init__(self, node, preshift, target):
        super(SafeJoinPropagator, self).__init__(node, preshift, target)
        # safe_join looks like '/'.join(directory, *pathnames)
        # Under the hood, safe_join uses posixpath.sep as the separator, so we use it
        # as the separator here as well. However, the value of the separator doesn't
        # actually matter for the purposes of propagation, as long as len(sep) == 1
        self.separator = posixpath.sep
        self.strings_to_join = self.sources
        self.directory = self.preshift.args[0] or ""

    @cached_property
    def sources(self):
        """
        Use all arguments as sources: safe_join(directory, *pathnames)
        """
        # We want to use BasePropagator.sources, not JoinPropagator.sources
        return super(JoinPropagator, self).sources

    def add_tags(self):
        """
        Add sanitizing tags to entire result excluding the base directory
        """
        tag_span = AdjustedSpan(len(self.directory), len(self.target))

        if self.node.tags:
            cs__apply_tags(self.node, self.target, tag_span)

        if self.node.untags:
            cs__apply_untags(self.node, self.target, tag_span)
