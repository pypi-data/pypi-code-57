# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.mixins.path_traversal_sink_features import (
    PathTraversalSinkFeatures,
)
from contrast.agent.protect.rule.base_rule import BaseRule


class PathTraversal(BaseRule, PathTraversalSinkFeatures):
    NAME = "path-traversal"

    def __init__(self, settings):
        BaseRule.__init__(self, settings)

    def find_attack(self, context, candidate_string, **kwargs):
        """
        Finds the attacker in the original string if present
        """
        attack = super(PathTraversal, self).find_attack(
            context, candidate_string, **kwargs
        )
        if self.in_infilter:
            attack = self.check_sink_features(context, candidate_string, attack)

        return attack

    def build_sample(self, context, evaluation, path, **kwargs):
        sample = self.build_base_sample(context, evaluation)
        if path is not None:
            sample.path_traversal.path = path
        return sample
