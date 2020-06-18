# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Callback for tracing anything
"""
import logging

from ..binding_accessor import BindingAccessor
from ..rules import RuleCallback
from ..samplers import ScopedTracingSampler

LOGGER = logging.getLogger(__name__)


class Trace(RuleCallback):

    def __init__(self, *args, **kwargs):
        super(Trace, self).__init__(*args, **kwargs)
        self.payload_template = {}
        options = self.data.get("options", {})
        self.scope = options.get("scope")
        sampler_definition = options.get("sampler_definition")
        self.sampler = ScopedTracingSampler(sampler_definition) \
            if sampler_definition is not None else None
        for key, template in options.get("payload_template", {}).items():
            self.payload_template[key] = BindingAccessor(template)

    def pre(self, instance, args, kwargs, **options):
        binding_eval_args = {
            "request": self.storage.get_current_request(),
            "response": self.storage.get_current_response(),
            "inst": instance,
            "args": self.storage.get_current_args(args),
            "kwargs": kwargs,
            "data": self.data,
            "extra": options,
        }
        payload = {}
        try:
            for key, ba in self.payload_template.items():
                payload[key] = ba.resolve(**binding_eval_args)
        except Exception:
            LOGGER.debug("ignore this trace as the payload template cannot be filled", exc_info=True)
        else:
            if self.sampler is None or self.sampler.should_sample(scope=self.scope, payload=payload):
                # if there is a callback level sampler, use it then delegates the decision to the agent
                # to send or not the trace
                self.record_trace(scope=self.scope, payload=payload)
