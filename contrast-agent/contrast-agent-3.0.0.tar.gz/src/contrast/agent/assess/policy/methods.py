# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.wrapt import ObjectProxy

import contrast
from contrast.agent import scope
from contrast.agent.settings_state import SettingsState
from contrast.agent.assess.policy.propagation_policy import (
    PropagationPolicy,
    build_preshift,
)
from contrast.agent.assess.policy.policy_utils import build_method_name
from contrast.agent.assess.policy.source_policy import SourcePolicy
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.agent.assess.utils import get_self_for_method


import logging

logger = logging.getLogger("contrast")


def perform_analysis(context, patch_policy, result, args, kwargs):
    if skip_analysis(context):
        return

    with scope.contrast_scope():
        self_obj = get_self_for_method(patch_policy, args)
        preshift = build_preshift(self_obj, args, kwargs)
        apply_nodes(patch_policy, preshift, self_obj, result, args, kwargs)


def classmethod_assess_method(original_method, patch_policy, *args, **kwargs):
    """
    Patching method to replace old method and call our assess code with the original method
    :param original_method: method to call for result
    :param patch_policy: PatchLocationPolicy containing all policy nodes for this patch
    :param args: method args
    :param kwargs: method kwargs
    :return: result of original method

    A separate method was required for classmethod patch because we need to remove
    argument 1. arg 1 is the class. This is something that is automatically passed to
    the function so passing it again will cause a TypeError.
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    try:
        result = original_method(*args[1:], **kwargs)
    except Exception:
        result = None
        raise
    finally:
        perform_analysis(context, patch_policy, result, args, kwargs)

    return result


def _assess_method(original_method, patch_policy, *args, **kwargs):
    """
    Patching method to replace old method and call our assess code with the original method
    :param original_method: method to call for result
    :param patch_policy: PatchLocationPolicy containing all policy nodes for this patch
    :param args: method args
    :param kwargs: method kwargs
    :return: result of original method
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    try:
        result = original_method(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        perform_analysis(context, patch_policy, result, args, kwargs)

    return result


def _property_assess_method(original_property_name, patch_policy, *args, **kwargs):
    """
    Calls the original property by looking for it in in the cs_assess_{property} location
    to return the property value, and run assess analysis.
    """
    context = contrast.CS__CONTEXT_TRACKER.current()
    try:
        cls_instance = args[0]
        cs_method_name = build_method_name(original_property_name)
        result = getattr(cls_instance, cs_method_name)
    except Exception:
        result = None
        raise
    finally:
        perform_analysis(context, patch_policy, result, args, kwargs)

    return result


class CachedPropertyProxy(ObjectProxy):
    cs__attr_name = None
    cs__patch_policy = None

    def __init__(self, wrapped, attr_name, patch_policy):
        super(CachedPropertyProxy, self).__init__(wrapped)
        self.cs__patch_policy = patch_policy
        self.cs__attr_name = attr_name

    def __get__(self, *args, **kwargs):
        context = contrast.CS__CONTEXT_TRACKER.current()
        result = self.__wrapped__.__get__(*args, **kwargs)

        try:
            # Self is the only arg that seems to be relevant for policy/reporting
            args = (self.__wrapped__,)
            perform_analysis(context, self.cs__patch_policy, result, args, {})
        except Exception:
            logger.exception("Failed to apply policy for %s", self.cs__attr_name)

        return result


def apply_cached_property(cls_or_module, patch_policy, property_name, orig_property):
    """
    Older werkzeug versions implement cached_property that does not inherit from property.
    This causes us to have to use a workaround for patching to avoid errors.

    Instead of replacing the cached_property with a new property, we replace it with
    and object proxy with a custom __get__ method.
    """
    proxied_property = CachedPropertyProxy(orig_property, property_name, patch_policy)

    try:
        setattr(cls_or_module, property_name, proxied_property)
    except Exception:
        logger.exception("Failed to apply patch to cached_property: %s", property_name)

    return True


def skip_analysis(context):
    """
    Skip analysis if there is no context, scope, or configuration is False
    :param context: RequestContext
    :return:
    """
    if not context:
        return True
    if scope.in_contrast_scope():
        return True
    return not SettingsState().is_assess_enabled()


def apply_nodes(patch_policy, preshift, self_obj, ret, args, kwargs=None):
    if not patch_policy:
        return

    replaced_return = None
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    if patch_policy.trigger_nodes:
        # Each node may potentially correspond to a different rule
        for node in patch_policy.trigger_nodes:
            if not scope.in_trigger_scope():
                with scope.trigger_scope():
                    # TODO: pass all trigger nodes here, sort the rules out later
                    TriggerPolicy.apply(node.rule, [node], ret, args, kwargs)

    if patch_policy.source_nodes:
        replaced_return = SourcePolicy.apply(
            patch_policy.source_nodes, self_obj, ret, args, kwargs
        )
    if not scope.in_propagation_scope():
        if patch_policy.propagator_nodes:
            with scope.propagation_scope():
                PropagationPolicy.apply(
                    patch_policy.propagator_nodes, preshift, self_obj, ret, args, kwargs
                )

    safe_return = replaced_return if replaced_return is not None else ret

    # rewind if necessary for io

    return safe_return
