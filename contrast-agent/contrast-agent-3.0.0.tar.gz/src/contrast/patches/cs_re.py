# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implementation of proxy classes for `re.Match` (`_sre.SRE_Match`)

In order to implement string propagation for the results of regular expression
matches, we need to patch the `re.Match` class. However, since this is a
built-in we can't patch it directly. Instead, we patch the methods of `re` that
return match objects and cause them to return proxied `re.Match` objects.
Since we require the use of an object proxy, we can't use policy for patching.
Instead, these patches are installed explicitly when assess is enabled.
This module implements the object proxy and also applies the patches to the
appropriate methods.

Other methods of the `re` module such as `split` and `escape` can be patched
directly, so they are implemented in policy.
"""
import functools

from contrast.extern import six
from contrast.extern.wrapt import ObjectProxy, register_post_import_hook

import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.propagators import regex_propagator
from contrast.utils.patch_utils import patch_cls_or_instance


MATCH = "match"
SEARCH = "search"
FULLMATCH = "fullmatch"
FINDITER = "finditer"
SUB = "sub"
SUBN = "subn"


class MatchObjectProxy(ObjectProxy):
    def _call_propagator(self, method, propagator, *args, **kwargs):
        context = contrast.CS__CONTEXT_TRACKER.current()
        result = method(*args, **kwargs)
        if context is not None and context.propagate_assess:
            with scope.propagation_scope():
                # TODO: catch exceptions here?
                propagator(self.__wrapped__, result, *args)
        return result

    def group(self, *args, **kwargs):
        method = self.__wrapped__.group
        propagator = regex_propagator.propagate_group
        return self._call_propagator(method, propagator, *args, **kwargs)

    def groups(self, *args, **kwargs):
        method = self.__wrapped__.groups
        propagator = regex_propagator.propagate_groups
        return self._call_propagator(method, propagator, *args, **kwargs)

    def groupdict(self, *args, **kwargs):
        method = self.__wrapped__.groupdict
        propagator = regex_propagator.propagate_groupdict
        return self._call_propagator(method, propagator, *args, **kwargs)


def single_match_hook(original_func, patch_policy=None, *args, **kwargs):
    result = original_func(*args, **kwargs)
    return MatchObjectProxy(result) if result is not None else None


def iterable_match_hook(original_finditer, patch_policy=None, *args, **kwargs):
    result = original_finditer(*args, **kwargs)
    return [MatchObjectProxy(x) for x in result] if result is not None else None


def wrap_repl(repl):
    repl_results = []

    def new_repl(match):
        # Wrap the match in our proxied object so that we propagate any
        # calls that are made by the custom repl function.
        result = repl(MatchObjectProxy(match))
        repl_results.append(result)
        return result

    functools.update_wrapper(new_repl, repl)
    return new_repl, repl_results


def sub_hook(original_sub, patch_policy, pattern, repl, string, count=0, flags=0):
    """
    Hook for re.sub and re.subn used for propagation in assess

    The following explains why we can't simply patch these methods using
    policy.

    It is possible for the repl argument to be a callable. In this case, the
    callable is passed a Match object, and it returns the string to be used for
    the replacement. In order to correctly propagate the substitution
    operation, we need to keep track of the results of calling the replacement
    function.

    It might seem like we should just call the replacement function again
    during our propagation action. But this is not practicable for several
    reasons:

      1. We're in scope at the time, so any propagation that needs to occur
         within the replacement callable itself will be missed.
      2. Related to above, but methods of Match do not return the same object
         even when called multiple times with the same arguments, so we would
         not be tracking the strings that actually get used in the substitution
         result.
      3. There's no guarantee that the replacement function does not cause any
         side effects or rely on any state in application code. We definitely
         don't want to mess around with this.

    The solution is to wrap the replacement callable with our own function that
    records the results of each call. We then pass our wrapped callable to the
    original function, and we pass the accumulated results to the propagator.
    This has the additional benefit of allowing us to wrap the match object
    that is passed to the repl function with our proxied object so that we
    propagate any calls that are made within this function if necessary.
    """
    # Get the non-propagation case out of the way here
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None or not context.propagate_assess:
        return original_sub(pattern, repl, string, count, flags)

    new_repl, repl_results = wrap_repl(repl) if callable(repl) else (repl, None)

    result = original_sub(pattern, new_repl, string, count, flags)
    with scope.propagation_scope():
        regex_propagator.propagate_sub(
            result, repl_results, pattern, new_repl, string, count, flags, "sub"
        )
    return result


def subn_hook(original_subn, patch_policy, pattern, repl, string, count=0, flags=0):
    """See docstring for sub_hook above"""
    # Get the non-propagation case out of the way here
    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None or not context.propagate_assess:
        return original_subn(pattern, repl, string, count, flags)

    new_repl, repl_results = wrap_repl(repl) if callable(repl) else (repl, None)

    result, result_count = original_subn(pattern, new_repl, string, count, flags)
    with scope.propagation_scope():
        # Since we know exactly how many replacements occurred, pass this as
        # the count parameter to the propagator
        regex_propagator.propagate_sub(
            result, repl_results, pattern, new_repl, string, result_count, flags, "subn"
        )
    return result, result_count


def patch_re(re_module):
    patch_cls_or_instance(re_module, MATCH, single_match_hook)
    patch_cls_or_instance(re_module, SEARCH, single_match_hook)
    if six.PY3:
        patch_cls_or_instance(re_module, FULLMATCH, single_match_hook)
    patch_cls_or_instance(re_module, FINDITER, iterable_match_hook)
    patch_cls_or_instance(re_module, SUB, sub_hook)
    patch_cls_or_instance(re_module, SUBN, subn_hook)


def register_patches():
    register_post_import_hook(patch_re, "re")
