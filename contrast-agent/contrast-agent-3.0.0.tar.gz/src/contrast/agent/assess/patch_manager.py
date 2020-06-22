# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections import defaultdict

from contrast.extern.six import PY2

from contrast.assess_extensions.cs_str import set_attr_on_type
from contrast.utils import Namespace

import logging

logger = logging.getLogger("contrast")


class module(Namespace):
    # map from id(orig_attr) -> patch
    patch_map = {}
    # map from id(patch) -> orig_attr
    inverse_patch_map = {}
    # list of modules we've visited, whose relevant
    # attributes we've at least initially patched
    visited_modules = set()
    patches_by_owner = defaultdict(set)


def patch(owner, name, patch=None, force=False):
    """
    Set attribute `name` of `owner` to `patch`.

    If `patch` is not provided, we look up the appropriate existing patch in
    the patch book and apply it. This behavior is used during repatching.

    :param owner: module or class that owns the original attribute
    :param name: str name of the attribute being patched
    :param patch: object replacing owner.name, or None to use an existing patch
    :param force: use set_attr_on_type instead of setattr to force the patch to succeed
    """
    orig_attr = _get_underlying_function(getattr(owner, name, None))

    if orig_attr is None:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: failed to patch %s of %s: no such attribute", name, owner
        )
        return
    if patch is None:
        patch = module.patch_map.get(id(orig_attr))
        if patch is None:
            # TODO: PYT-692 investigate unexpected patching
            logger.debug(
                "WARNING: failed to repatch %s of %s: no entry in the patch map",
                name,
                owner,
            )
            return

    if id(orig_attr) in module.inverse_patch_map:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: patching over already patched method %s of %s", name, owner
        )

    if id(orig_attr) in module.patch_map and id(patch) != id(
        module.patch_map[id(orig_attr)]
    ):
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: patching method %s of %s with an attribute "
            "that differs from its patch map entry. This is almost "
            "certainly unintended.",
            name,
            owner,
        )

    # TODO: PYT-696 this is a hack that only definitely works for sqlite3.
    # It is not a satisfactory resolution to PYT-696 without at least some more investigation.
    # This should be investigated for cases like `open`, or cases where `owner` is a module.
    setattr(owner, name, patch) if not force else set_attr_on_type(owner, name, patch)
    register_patch(owner, name, orig_attr)


def reverse_patch(owner, name, force=False):
    """
    Restore a patched attribute back to its original

    :param owner: module or class that owns the attribute being reverse patched
    :param name: name of the attribute as a string
    :param force: use set_attr_on_type instead of setattr to force the reverse patch to succeed
    """
    patch = _get_underlying_function(getattr(owner, name, None))

    if patch is None:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: failed to reverse patch %s of %s: no such attribute", name, owner
        )
        return

    if not is_patched(patch):
        return

    orig_attr = module.inverse_patch_map.get(id(patch))

    if orig_attr is None:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: failed to reverse patch %s of %s: it isn't patched", name, owner
        )
        return

    # TODO: PYT-696 - see note above, in `patch`
    setattr(owner, name, orig_attr) if not force else set_attr_on_type(
        owner, name, orig_attr
    )

    module.patches_by_owner[id(owner)].discard(name)


def reverse_patches_by_owner(owner, force=False):
    """
    Restore all patched attributes that belong to the owning module/class

    If the owner is a module, any patched classes in this module will not be
    automatically reversed by this method. For example, if the following are patched:

        foo.a
        foo.b
        foo.FooClass.foo_method

    in order to reverse the patches, it will be necessary to call this method twice:

        reverse_patches_by_owner(foo)
        reverse_patches_by_owner(foo.FooClass)

    :param owner: module or class that owns the attribute being reverse patched
    :param force: use set_attr_on_type instead of setattr to force the reverse patch to succeed
    """
    for name in list(module.patches_by_owner[id(owner)]):
        reverse_patch(owner, name, force=force)


def register_patch(owner, name, orig_attr):
    """
    Register patch in the patch map to prevent us from patching twice

    :param owner: module or class that owns the original function
    :param name: name of the patched attribute
    :param orig_attr: original attribute, which is being replaced
    """
    mark_visited(owner)

    patch = _get_underlying_function(getattr(owner, name))
    orig_attr = _get_underlying_function(orig_attr)

    if id(module.patch_map.get(id(orig_attr))) == id(patch):
        return
    if module.patch_map.get(id(orig_attr)) is not None:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug("WARNING: overwriting existing patch map entry for %s", orig_attr)
    if patch is orig_attr:
        # TODO: PYT-692 investigate unexpected patching
        logger.debug(
            "WARNING: attempt to register %s as a patch for itself - "
            "skipping patch map registration",
            orig_attr,
        )
        return

    module.patch_map[id(orig_attr)] = patch
    module.inverse_patch_map[id(patch)] = orig_attr
    module.patches_by_owner[id(owner)].add(name)


def is_patched(attr):
    """
    If the given attribute is a key in the inverse patch map, it means that it is being
    used as a patch.

    :param attr: attribute in question
    :return: True if the attribute is a key in the inverse patch map, False otherwise
    """
    return id(_get_underlying_function(attr)) in module.inverse_patch_map


def has_associated_patch(attr):
    """
    If we come across an attribute that's a value in the patch_map (a key in
    the inverse patch map), it should be patched. This is most useful during
    re-patching, where we might see an old reference to the unpatched original
    attribute.

    :param attr: attribute in question
    :return: True if the attribute is a key in the patch map, False otherwise
    """
    return id(_get_underlying_function(attr)) in module.patch_map


def is_visited(module_):
    """
    Check if we've visited a given module.

    :param module_: module object in question
    :return: True if we've visited this module in the context of patching,
        False otherwise
    """
    return id(module_) in module.visited_modules


def mark_visited(module_):
    """
    Mark a module as visited.

    :param module_: module object in question
    """
    module.visited_modules.add(id(module_))


def clear_visited_modules():
    """
    Clear the set of visited modules.
    """
    module.visited_modules.clear()


def _get_underlying_function(attr):
    """
    In python 2, we can't trust the id of unbound methods. For example, if we have
    class Foo with instance method bar, Foo.bar returns a wrapper around the actual
    function object, and that wrapper may change between accesses to Foo.bar.

    This is due to the descriptor protocol; in python2 methods are descriptors,
    like properties.

    However, unbound methods should have a __func__ attribute, which references the
    raw underlying function. This value does not change, so we want to enter its id
    in the patch map.
    """
    if PY2 and hasattr(attr, "__func__"):
        return attr.__func__
    return attr
