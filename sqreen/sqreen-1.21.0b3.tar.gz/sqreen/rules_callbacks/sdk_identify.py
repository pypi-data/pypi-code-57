# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Enforce user actions with SDK callbacks
"""
import logging

from ..rules import RuleCallback
from ..utils import now

LOGGER = logging.getLogger(__name__)


class SDKIdentify(RuleCallback):

    def pre(self, instance, args, kwargs, **options):
        """Associate the current request with a user."""
        traits = kwargs.get("traits") or {}
        user_identifiers = {}
        if args:
            user_identifiers.update(args[0])

        self.storage.observe(
            "sdk", ["identify", now(), user_identifiers, traits],
            report=False
        )
