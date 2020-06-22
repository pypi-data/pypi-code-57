# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import integer_types

from contrast.agent.assess import policy_constants
from contrast.agent.assess.assess_exceptions import ContrastAssessException
from contrast.agent.assess.policy_constants import ALL_ARGS, ALL_KWARGS, OBJECT
from contrast.agent.assess.policy.policy_node import PolicyNode
from contrast.utils.decorators import cached_property


class PropagationNode(PolicyNode):
    TAGGER = "Tagger"
    PROPAGATOR = "Propagator"

    def __init__(
        self,
        module,
        class_name,
        instance_method,
        method_name,
        source,
        target,
        action,
        tags=None,
        untags=None,
        policy_patch=True,
        python2_only=False,
        python3_only=False,
    ):
        """
        :param class_name: class of the hook
        :param instance_method: if the method is an instance method vs static/bound/unbound
        :param method_name: method name to hook
        :param source: from where the tainted data flows, cannot be None
        :param target: to where the tainted data flows, cannot be None
        :param action: how the tainted data flows from source to target, should not be None
        :param tags: array of tags to apply to the target, can be None if no tags are added
        :param untags: array of tags to remove from the target, can be None if not tags are removed
        """
        super(PropagationNode, self).__init__(
            module,
            class_name,
            instance_method,
            method_name,
            source,
            target,
            tags,
            policy_patch=policy_patch,
            python2_only=python2_only,
            python3_only=python3_only,
        )

        self.action = action
        self.untags = set(untags) if untags else set()

        self.validate()

    @property
    def node_class(self):
        return self.TAGGER if self.is_tagger else self.PROPAGATOR

    @property
    def node_type(self):
        return "TYPE_TAG" if self.is_tagger else "PROPAGATOR"

    @cached_property
    def is_tagger(self):
        return bool(self.tags) or bool(self.untags)

    def validate(self):

        super(PropagationNode, self).validate()

        if not (self.targets and len(self.targets) != 0):
            raise ContrastAssessException(
                "Propagator {} did not have a proper target. Unable to create.".format(
                    self.method_name
                )
            )

        if not (self.sources and len(self.sources) != 0):
            raise ContrastAssessException(
                "Propagator {} did not have a proper source. Unable to create.".format(
                    self.method_name
                )
            )

        if not self.action:
            raise ContrastAssessException(
                "Propagator {} did not have a proper action. Unable to create.".format(
                    self.method_name
                )
            )

        self.validate_untags()

    def validate_untags(self):
        if not self.untags:
            return

        for item in self.untags:
            if item not in policy_constants.VALID_TAGS:
                raise ContrastAssessException(
                    "{} {} did not have a valid untag. {} is not a known value.".format(
                        self.node_type, self.id, item
                    )
                )

            if self.tags and item in self.tags:
                raise ContrastAssessException(
                    "{} {} had the same tag and untag, {}.".format(
                        self.node_type, self.id, item
                    )
                )

    def get_matching_sources(self, preshift):
        sources = []

        for source in self.sources:
            if source == OBJECT:
                sources.append(preshift.obj)
            elif source == ALL_ARGS:
                sources.extend(preshift.args)
            elif source == ALL_KWARGS:
                sources.append(preshift.kwargs)
            elif isinstance(source, integer_types) and len(preshift.args) > source:
                sources.append(preshift.args[source])
            elif preshift.kwargs and source in preshift.kwargs:
                sources.append(preshift.kwargs[source])

        return sources

    @staticmethod
    def from_dict(obj):
        return PropagationNode(
            obj[policy_constants.JSON_MODULE],
            obj.get(policy_constants.JSON_CLASS_NAME, ""),
            obj.get(policy_constants.JSON_INSTANCE_METHOD, True),
            obj[policy_constants.JSON_METHOD_NAME],
            obj[policy_constants.JSON_SOURCE],
            obj[policy_constants.JSON_TARGET],
            obj[policy_constants.JSON_ACTION],
            obj.get(policy_constants.JSON_TAGS, []),
            obj.get(policy_constants.JSON_UNTAGS, []),
            policy_patch=obj.get(policy_constants.JSON_POLICY_PATCH, True),
            python2_only=obj.get(policy_constants.JSON_PY2_ONLY, False),
            python3_only=obj.get(policy_constants.JSON_PY3_ONLY, False),
        )
