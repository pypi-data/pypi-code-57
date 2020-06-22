# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.propagators.base_propagator import BasePropagator
from contrast.agent.assess.utils import (
    copy_events,
    copy_tags_to_offset,
    cs__copy_from,
    get_properties,
)

import logging

logger = logging.getLogger("contrast")


class AppendPropagator(BasePropagator):
    def _propagate(self):
        second_source = None

        if len(self.sources) > 1:
            second_source = self.sources[1]

        target_properties = get_properties(self.target)

        # if the object and the return are the same length just copy the tags
        # from the object(since nothing from args was added to return)
        if len(self.first_source) == len(self.target):
            cs__copy_from(self.target, self.first_source, 0, self.node.untags)
        else:
            # find original in the target, copy tags to the new position in target
            try:
                original_start_index = self.target.index(self.first_source)
            except Exception:
                logger.debug(
                    "%s was not found in the target %s", self.first_source, self.target
                )
                return

            cs__copy_from(
                self.target, self.first_source, original_start_index, self.node.untags
            )

            start = original_start_index + len(self.first_source)
            if second_source is not None:
                source_properties = get_properties(second_source)
                if source_properties is not None:
                    copy_tags_to_offset(
                        target_properties, source_properties.tags, start
                    )
                    copy_events(target_properties, source_properties)
