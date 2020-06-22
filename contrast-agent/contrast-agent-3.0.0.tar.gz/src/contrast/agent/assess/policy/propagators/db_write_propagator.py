# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.utils import cs__apply_tags, get_properties
from contrast.agent.assess.policy.propagators.base_propagator import BasePropagator


class DBWritePropagator(BasePropagator):
    """
    Propagator to handle stored XSS. This propagator assumes the database
    column names are passed in via ALL_KWARGS.

    For each column name, patch the getter/setter property for the column name
    and create dynamic sources for these properties.
    """

    @property
    def needs_propagation(self):
        return True

    def track_target(self):
        """
        This propagator does not track the target because the target is
        an instance of an ORM model, such as django's Model class. If it
        were a string instead, we would track it.
        """
        pass

    def add_tags_and_properties(self, ret, frame):
        """
        Because the target is an instance of an ORM model,
        such as django's Model class, and not a string, we do this
        work inside self.propagate(). Later on we could refactor
        to move the work here.
        """
        pass

    def propagate(self):
        from contrast.agent.assess.policy.policy_applicator import (
            apply_patch_to_dynamic_property,
            save_original_method,
            build_method_name,
        )

        cls = self.preshift.obj.__class__

        source = self.sources[0]

        for col_name, value in source.items():
            if not value:
                continue

            cs_method_name = build_method_name(col_name)
            if hasattr(cls, cs_method_name):
                continue

            old_property = getattr(cls, col_name)
            if not save_original_method(cls, cs_method_name, old_property):
                continue

            cs__apply_tags(self.node, value)
            col_value_properties = get_properties(value)

            tags = [tag for tag in col_value_properties.tags]
            apply_patch_to_dynamic_property(cls, col_name, tags)

            col_value_properties.build_event(
                self.node,
                value,
                self.preshift.obj,
                self.target,
                self.preshift.args,
                self.preshift.kwargs,
                [],
                0,
                None,
            )
