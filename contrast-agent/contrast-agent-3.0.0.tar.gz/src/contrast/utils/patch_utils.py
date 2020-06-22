# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import OrderedDict
import inspect
import sys

from contrast.extern.six import iteritems

from contrast.agent.assess import patch_manager
from contrast.utils.ignored_modules import (
    ALL_MODULES_TO_IGNORE,
    MODULES_TO_IGNORE_PREFIXES,
)
from contrast.utils.object_share import ObjectShare

import logging

logger = logging.getLogger("contrast")


def module_is_ignored(module_name):
    return module_name in ALL_MODULES_TO_IGNORE or module_name.startswith(
        MODULES_TO_IGNORE_PREFIXES
    )


def call_patch(
    new_function, original_function, patch_policy, *orig_func_args, **orig_func_kwargs
):
    return new_function(
        original_function, patch_policy, *orig_func_args, **orig_func_kwargs
    )


def curry(new_function, original_func, patch_policy):
    def _curried(*orig_func_args, **orig_func_kwargs):
        return call_patch(
            new_function,
            original_func,
            patch_policy,
            *orig_func_args,
            **orig_func_kwargs
        )

    return _curried


def patch_cls_or_instance(
    patch_target,
    method_name,
    new_function=None,
    patch_policy=None,
    static_method=False,
    class_method=False,
    assess_patch=False,
):
    """
    Apply a patch to given module, class, or object instance

    :param patch_target: The class, module, or object instance to be patched
    :param method_name: The name of the method (or function) that is being replaced
    :param patch_policy: patch policy location instance
    :param new_function: The function that will replace the original function
    :param static_method: Indicates whether method being replaced is a staticmethod
    :param class_method: Indicates whether method being replaced is a classmethod
    """
    cs_method_name = (
        ObjectShare.CONTRAST_ASSESS_METHOD_START + method_name
        if assess_patch
        else method_name
    )

    original_func = getattr(patch_target, cs_method_name)
    if patch_manager.is_patched(original_func):
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING! Method %s is not getting patched - already patched", method_name
        )
        return

    curried = curry(new_function, original_func, patch_policy)

    if static_method:
        curried_function = staticmethod(curried)
    elif class_method:
        curried_function = classmethod(curried)
    elif callable(new_function) or hasattr(new_function, "__call__"):
        if isinstance(original_func, property):
            curried_function = property(curry(new_function, method_name, patch_policy))
        else:
            curried_function = curried
    else:
        logger.debug(
            "WARNING! Method %s is not getting patched - unrecognized object type: %s",
            method_name,
            type(original_func),
        )
        return

    patch_manager.patch(patch_target, method_name, curried_function)


def patch_property(
    class_to_patch, property_name, new_property_method, patch_policy=None
):
    """
    Patch properties which require both fget and fset to be set.
    This currently supports the case for the DjangoORM. Column name attributes
    for the model that defines database operations operate as properties.
    While in patch_cls_or_instance we handle properties, here we handle this special
    case that fails if fset is not defined.

    Note the definition of fset is the most basic definition of a setter, which is
    sufficient to make the getter/setter implementation of the property patching work.
    """
    original_prop = getattr(class_to_patch, property_name)
    if patch_manager.is_patched(original_prop):
        return

    fget = curry(new_property_method, property_name, patch_policy)

    def fset(cls_instance, value):
        # while good instinct would lead us to use setattr here instead of __dict__,
        # doing so does not work because we are in fact within a setter!
        cls_instance.__dict__[property_name] = value

    new_property = property(fget=fget, fset=fset)
    patch_manager.patch(class_to_patch, property_name, new_property)


CONTRAST_MODULE = "contrast."
INTELLIJ_MODULE = "pydevd"


def get_loaded_modules(use_for_patching=False):
    """
    Retrieves and filters all loaded modules

    The parameter `use_for_patching` indicates that this function is being
    called to enable patching. In this case the modules are sorted (to
    provide deterministic behavior) and also the modules_to_ignore list is used.

    :return: dict of name and module as value
    """
    if not use_for_patching:
        return {k: v for k, v in iteritems(sys.modules) if inspect.ismodule(v)}

    filtered = OrderedDict()
    filtered.update(
        dict(
            (name, module)
            for name, module in sorted(iteritems(sys.modules))
            if inspect.ismodule(module) and not module_is_ignored(name)
        )
    )

    # TODO: PYT-683 filter out .so modules

    return filtered


def is_patchable(obj):
    if inspect.ismodule(obj):
        return False
    if inspect.isclass(obj):
        return True

    # cython methods look like unpatchable builtins, but they can be patched normally
    # an example of this is lxml.etree.fromstring
    # for additional info, see https://groups.google.com/forum/#!topic/cython-users/v5dXFOu-DNc
    is_unpatchable_builtin_method = inspect.ismethoddescriptor(
        obj
    ) and not obj.__class__.__name__.startswith("cython")

    return inspect.isroutine(obj) and not is_unpatchable_builtin_method


def repatch_module(module):
    """Repatch a single module. See docstring for repatch_imported_modules"""
    for attr_name, attr in vars(module).items():
        try:
            if not is_patchable(attr):
                continue
        except Exception as e:
            # TODO: is this even worth logging?
            logger.debug(
                "exception occurred while checking whether to patch %s in %s",
                attr_name,
                module.__name__,
                exc_info=e,
            )
            continue

        if not patch_manager.has_associated_patch(attr):
            continue

        logger.debug("applying repatch to %s in %s", attr_name, module.__name__)
        patch_manager.patch(module, attr_name)


def repatch_imported_modules():
    """
    Applies patches to modules that were already imported prior to agent startup

    Here's the problem: our patches don't get applied until after our
    middleware class is initialized. At this point it's likely that most (or
    all) application modules will have already been imported.

    If we patch the function `foo.bar.baz`, and an application module that was
    loaded prior to our patches imports it as `from foo.bar import baz`, then
    our patch will have no effect within that application module. This is
    because the application module has a reference to the *original* function,
    and that reference remains unchanged even after we apply a patch to the
    `foo.bar` module.

    On the other hand, if the application imports it as `from foo import bar`
    and uses it as `bar.baz()`, then our patches will work just fine. In this
    case, the application module has a reference to the *module itself*, which
    is where we apply our patch. This means that when the application calls
    `bar.baz()`, it will be calling the updated (patched) function.

    Incidentally, if the application imports as `from foo.bar import baz`, but
    this module is not loaded until *after* our patches have been applied, our
    patch will be effective. However, we have no control over the order of
    imports in an application.

    This function is designed to remedy the former case in order to make sure
    that our patches are effective regardless of how they are imported or the
    order in which they are imported by the application.

    Prior to calling this function, we make a record of every function that
    gets patched. After all patches are applied, this function iterates
    through all imported modules, which includes all modules that may have been
    imported before our patches were applied. We look for any instances of the
    original functions that need to be patched, and we replace them with the
    patches in those modules.
    """
    for _, module in get_loaded_modules(use_for_patching=True).items():

        if patch_manager.is_visited(module):
            continue

        repatch_module(module)

        # Prevent us from re-repatching =D
        patch_manager.mark_visited(module)
