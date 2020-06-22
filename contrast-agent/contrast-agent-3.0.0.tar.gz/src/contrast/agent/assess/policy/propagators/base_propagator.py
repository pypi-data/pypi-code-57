# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import binary_type, string_types, text_type

from contrast.agent.assess.policy.source_policy import get_parent_ids
from contrast.utils.assess import tracking_util
from contrast.utils.decorators import cached_property
from contrast.agent.assess.utils import (
    cs__apply_tags,
    cs__apply_untags,
    cs__tracked,
    get_properties,
    track_string,
    update_properties,
)

SUPPORTED_TYPES = string_types + (text_type, binary_type, bytearray)


class BasePropagator(object):
    def __init__(self, node, preshift, target):
        """
        :param node: instance of PropagationNode
        """
        self.node = node
        self.preshift = preshift
        self.target = target
        self.target_properties = None

    @cached_property
    def sources(self):
        """
        Get all the sources for the propagation node.
        """
        return self.node.get_matching_sources(self.preshift)

    @property
    def any_source_tracked(self):
        return any(tracking_util.is_tracked(s) for s in self.sources)

    @property
    def needs_propagation(self):
        if not isinstance(self.target, SUPPORTED_TYPES):
            return False

        if tracking_util.is_tracked(self.target):
            return True

        if not self.preshift:
            return False

        return self.inputs_require_propagation

    @property
    def inputs_require_propagation(self):
        return self.any_source_tracked

    def track_target(self):
        for source in self.sources:
            if cs__tracked(source):
                track_string(self.target)
                return True

        return False

    def propagate(self):
        """
        Any propagators that inherit from BasePropagator and are able to follow
        this same propagation pattern should define _propagate.

        Some propagators continue to define their own propagate method.
        """
        target_properties = get_properties(self.target)
        if target_properties is None:
            return

        self.first_source = self.sources[0]
        self._propagate()
        target_properties.cleanup_tags()

    def get_parent_ids(self, ret):
        """Some derived classes may need to override this method"""
        return get_parent_ids(
            self.node, self.preshift.obj, ret, self.preshift.args, self.preshift.kwargs
        )

    def build_event(self, target_properties, ret, frame):
        parent_ids = self.get_parent_ids(ret)
        target_properties.build_event(
            self.node,
            self.target,
            self.preshift.obj,
            ret,
            self.preshift.args,
            self.preshift.kwargs,
            parent_ids,
            None,
            frame=frame,
        )

    def add_tags(self):
        if self.node.tags:
            cs__apply_tags(self.node, self.target)

        if self.node.untags:
            cs__apply_untags(self.node, self.target)

    def add_tags_and_properties(self, ret, frame):
        self.add_tags()

        target_properties = get_properties(self.target)

        # ignore un-tracked targets; possible interning
        if target_properties is None:
            return

        target_properties.add_properties(self.node.properties)

        self.build_event(target_properties, ret, frame)
        update_properties(self.target, target_properties)

    def reset_tags(self):
        """
        Some propagators will store the original set of tags but then restore them.
        This is because PropagationNode are only initialized once (for the entire server-startup cycle)
        from their policy.json representation, so if a propagator has to add/delete a tag, we need
        to restore the original tags.

        In the future, we could avoid doing this reset by re-instantiating nodes
        every time, albeit with a cost to performance.
        """
        pass

    def track_and_propagate(self, ret, frame):
        self.track_target()
        self.propagate()
        self.add_tags_and_properties(ret, frame)
