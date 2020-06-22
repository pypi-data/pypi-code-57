# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import logging

logger = logging.getLogger("contrast")

from contrast.agent import scope
from contrast.agent.assess.policy.policy_applicator import register_import_hooks
from contrast.agent.settings_state import SettingsState
from contrast.assess_extensions import cs_str
from contrast.patches import (
    cs_str as cs_str_patches,
    register_assess_patches,
    register_common_patches,
    register_protect_patches,
)
from contrast.utils.namespace import Namespace
from contrast.utils.patch_utils import repatch_imported_modules


class module(Namespace):
    hook = None
    enabled = False


def enable_assess_patches():
    """
    Enables extension hooks and other string patches.

    Has no effect if these patches are already enabled.
    """
    if module.enabled:
        return

    module.hook = cs_str.enable(logger)

    # Enable any string patches that need to be applied through Python
    cs_str_patches.patch_strtype_methods()

    module.enabled = True


def disable_assess_patches():
    """
    Disables extension hooks and other string patches.

    Has no effect if these patches are not already enabled.
    """
    if not module.enabled:
        return

    cs_str.disable(module.hook)

    # Disable any string patches that were applied through Python
    cs_str_patches.unpatch_strtype_methods()

    module.enabled = False


def _enable_patches():
    settings = SettingsState()

    if settings.is_protect_enabled():
        register_common_patches()
        register_protect_patches()

        # This has no effect if the patches are not enabled
        disable_assess_patches()

    if settings.is_assess_enabled():
        enable_assess_patches()

        logger.debug("enabled assess string patches")
        register_common_patches()
        register_assess_patches()

        logger.debug("adding assess policy")
        register_import_hooks()

    logger.debug("revisiting imported modules to apply patches")
    repatch_imported_modules()


def enable_patches():
    """
    Enable all patches for agent based on current settings
    """
    # Being in scope here prevents us from inadvertantly propagating while we are
    # applying patches and navigating policy. This has a fairly significant performance
    # impact for assess initialization, and also promotes correctness/safety.
    with scope.contrast_scope():
        _enable_patches()
