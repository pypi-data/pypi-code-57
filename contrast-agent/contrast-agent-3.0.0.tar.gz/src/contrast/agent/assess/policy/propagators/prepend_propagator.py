# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.propagators.base_propagator import BasePropagator
from contrast.agent.assess.utils import cs__copy_from


class PrependPropagator(BasePropagator):
    def _propagate(self):
        try:
            original_start_index = self.target.rindex(self.first_source)
        except Exception:
            original_start_index = 0

        # find original in the target, copy tags to the new position in target
        cs__copy_from(
            self.target, self.first_source, original_start_index, self.node.untags
        )
