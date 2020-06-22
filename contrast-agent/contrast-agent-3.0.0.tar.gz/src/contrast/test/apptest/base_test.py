# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import subprocess

import mock

from contrast.agent.assess import patch_manager
from contrast.agent.assess.utils import clear_properties
from contrast.agent.request_context import RequestContext
from contrast.test.settings_builder import SettingsBuilder

SETTINGS_STATE_PATCH_LOC = "contrast.agent.middlewares.base_middleware.SettingsState"


class BaseContrastTest(object):
    @property
    def middleware_name(self):
        raise NotImplementedError

    @property
    def middleware_request_context(self):
        return "contrast.agent.middlewares.{}.RequestContext".format(
            self.middleware_name
        )

    def patch_request_context(self):
        class PatchedRequestContext(RequestContext):
            def __init__(*args, **kwargs):
                super(PatchedRequestContext, args[0]).__init__(*args[1:], **kwargs)
                # This "self" belongs to the test class, not the request context
                self.request_context = args[0]

        return PatchedRequestContext

    def build_settings(self):
        """Override in subclasses to use different settings."""
        return SettingsBuilder().build()

    def build_app(self):
        """
        Override to configure the app for each middleware.
        """
        pass

    @classmethod
    def setup_class(cls):
        """
        Patch locations that are used by both assess and protect tests need to be
        reversed here.
        """
        patch_manager.reverse_patches_by_owner(os)
        patch_manager.reverse_patches_by_owner(subprocess)
        patch_manager.reverse_patches_by_owner(subprocess.Popen)

    def setup_method(self):
        self.settings = self.build_settings()
        self.settings.is_agent_enabled = mock.MagicMock(return_value=True)
        mock_settings = mock.MagicMock(return_value=self.settings)
        self.settings_patch = mock.patch(SETTINGS_STATE_PATCH_LOC, mock_settings)

        self.request_context_patch = mock.patch(
            self.middleware_request_context, self.patch_request_context()
        )

        self.settings_patch.start()
        self.request_context_patch.start()

        self.build_app()

    def teardown_method(self):
        self.settings_patch.stop()
        self.request_context_patch.stop()
        clear_properties()
