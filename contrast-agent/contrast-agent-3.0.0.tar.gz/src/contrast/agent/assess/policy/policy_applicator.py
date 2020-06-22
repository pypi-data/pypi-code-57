# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six.moves import builtins
from contrast.extern.wrapt import register_post_import_hook

# only bother with cached_property if we have access to Werkzeug
try:
    from werkzeug.utils import cached_property
except ImportError:
    cached_property = None

from contrast.agent.assess.policy import Policy
from contrast.agent.assess.policy.methods import (
    apply_cached_property,
    _assess_method,
    classmethod_assess_method,
    _property_assess_method,
)
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.policy.policy_utils import build_method_name
from contrast.utils.patch_utils import (
    patch_cls_or_instance,
    patch_property,
    repatch_module,
)


import logging

logger = logging.getLogger("contrast")


# Maintains a record of all patch locations that have been applied
PATCH_LOCATIONS = set()


def save_original_method(cls_or_module, cs_method_name, old_method):
    """
    Attempt to save old_method with the name cs_method_name on the
    class or module
    """
    try:
        # set old function to "cs_assess_{name}"
        setattr(cls_or_module, cs_method_name, old_method)
    except Exception:
        logger.debug("failed to patch %s.%s", cls_or_module, old_method)
        return False

    return True


def apply_assess_patch(patch_site, patch_policy):
    """
    Store the original method implementation under our custom "cs_assess_{name}" so we
    can call the old method from the new method in order to return the same result

    :param cls_or_module: Class or module to patch
    :param patch_policy: PatchLocationPolicy containing all policy nodes for this patch
    :param methods: methods in cls_or_module
    :param node_method: tuple of string and actual method
        ('get_raw_uri', <unbound method django.http.request.HttpRequest.get_raw_uri>)

    Static methods and class methods are implemented as descriptors. When one of these
    methods is called on the parent object, it uses the descriptor protocol, which
    means that the underlying function objects are not seen directly by the caller.

    In order to access the staticmethod/classmethod objects directly, they must be
    accessed via the parent object's __dict__ attribute.

    For example,

    class D:
        @staticmethod
        def sm():
            pass

    If I do this:
    D.sm will call __get__ under the hood to get the function definition (this is
    what's wrapped inside the staticmethod or classmethod obj in this case)

    If we do this:
    D.__dict__['sm'] we get the underlying staticmethod/classmethod object. This is
    required because we need to do a type check in order to replace the original obj
    with our own function of the correct type.

    This shows examples of C code re-written in python for the __get__ desc
    implementation for classmethod, staticmethod and function
    https://docs.python.org/2.7/howto/descriptor.html#functions-and-methods

    For additional details on PY3:
    https://docs.python.org/3/howto/descriptor.html#functions-and-methods
    """
    logger.debug("Applying patch to %s", patch_policy.name)

    method_name = patch_policy.method_name
    cs_method_name = build_method_name(method_name)
    has_key = hasattr(patch_site, "__dict__") and method_name in patch_site.__dict__

    static_method = has_key and isinstance(
        patch_site.__dict__[method_name], staticmethod
    )
    class_method = has_key and isinstance(patch_site.__dict__[method_name], classmethod)

    # Need to make sure we get original static/class function
    if static_method or class_method:
        old_method = patch_site.__dict__[method_name]
    else:
        # get old function/property/method
        old_method = getattr(patch_site, patch_policy.method_name)

    if not save_original_method(patch_site, cs_method_name, old_method):
        return False

    if isinstance(old_method, property):
        # newer versions of werkzeug cached_property inherit from property
        # so these are handled here
        new_method = _property_assess_method
    elif cached_property is not None and isinstance(old_method, cached_property):
        # Handle the case in older versions of werkzeug where cached_propery does
        # not inherit from property.
        return apply_cached_property(patch_site, patch_policy, method_name, old_method)
    elif class_method:
        new_method = classmethod_assess_method
    else:
        new_method = _assess_method

    try:
        patch_cls_or_instance(
            patch_site,
            method_name,
            new_function=new_method,
            patch_policy=patch_policy,
            static_method=static_method,
            class_method=class_method,
            assess_patch=True,
        )
        logger.debug("added patch to %s.%s", patch_site, method_name)
    except Exception as e:
        logger.debug(
            "unable to patch %s method of %s: %s", method_name, patch_site, str(e)
        )
        return False

    return True


def apply_module_patches(module):
    """
    Apply patches to all methods and functions in a module as dictated by policy
    """
    global PATCH_LOCATIONS

    logger.debug("Running import hook for %s", module.__name__)

    module_name = "BUILTIN" if module is builtins else module.__name__

    policy = Policy()

    if module_name not in policy.policy_by_module:
        logger.debug("WARNING: No module policy found for %s", module_name)
        return

    for patch_policy in policy.policy_by_module[module_name]:
        if patch_policy.name in PATCH_LOCATIONS:
            continue

        # If the module has no policy nodes, or if none of the nodes are policy
        # patches, then there's nothing to do here.
        if not patch_policy.has_patches:
            continue

        if patch_policy.class_name:
            patch_site = getattr(module, patch_policy.class_name, None)
            if patch_site is None:
                continue
        else:
            patch_site = module

        try:
            apply_assess_patch(patch_site, patch_policy)
        except Exception:
            logger.debug("Failed to apply patch for %s", patch_policy.name)

        PATCH_LOCATIONS.add(patch_policy.name)

    # It's possible that the current module contains multiple references to the
    # function we replaced, but that only one of them is represented in policy. We do a
    # quick repatching pass over the current module here to make sure we cover all of
    # the references that may have been missed.
    repatch_module(module)


def register_import_hooks():
    """
    Use policy to register import hooks for each module that requires patches
    """
    policy = Policy()

    for module_name in policy.policy_by_module:
        # BUILTIN is a stand-in in policy for the builtins/__builtin__ module
        module_name = builtins.__name__ if module_name == "BUILTIN" else module_name
        logger.debug("Registering import hook for %s", module_name)
        register_post_import_hook(apply_module_patches, module_name)


def apply_patch_to_dynamic_property(class_to_patch, property_name, tags):
    """
    Take the property of a class we want to patch and:
        1. create a source node to store in policy
        2. patch the original property with our own code, including
            the policy instance with the new dynamic source.

    This means that the next time the cls.property is called,
    we will inject ourselves and run source policy.

    NOTE: adding the dynamic source to Policy() BEFORE calling patch_property
    is critical order, given that we have to patch with the policy instance
    that has this dynamic source. This could later be modified to not need
    this requirement.
    """
    module = class_to_patch.__module__
    class_name = class_to_patch.__name__

    dynamic_source_node = SourceNode.create_source_node(
        module, class_name, property_name, tags, policy_patch=False
    )

    policy = Policy()
    patch_policy = policy.add_node(dynamic_source_node, "dynamic_source")

    patch_property(class_to_patch, property_name, _property_assess_method, patch_policy)

    return True
