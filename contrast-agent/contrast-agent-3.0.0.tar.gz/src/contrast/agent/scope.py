# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Controller for global scope state

Basically we use scoping to prevent us from assessing our own code. Scope
improves performance but it also prevents us from accidentally recursing
inside our analysis code. For example, we don't want to inadvertently cause
string propagation events while we're doing string building for reporting
purposes.

Currently there are several types of scope that we use. However, it is
likely that these are redundant and we should consolidate them into a
single contrast scope. This would be in line with changes that the Ruby
agent recently made.
"""
from contextlib import contextmanager

from contrast.assess_extensions import cs_str


def enter_contrast_scope():
    """
    Enter contrast scope

    Contrast scope is global. It should prevent us from taking *any*
    further analysis action, whether it be propagation or evaluating
    triggers.
    """
    cs_str.enter_scope(cs_str.CONTRAST_SCOPE)


def exit_contrast_scope():
    cs_str.exit_scope(cs_str.CONTRAST_SCOPE)


def enter_propagation_scope():
    """
    Enter propagation scope

    While in propagation scope, prevent any further propagation actions.
    Basically this means that no string propagation should occur while in
    propagation scope.
    """
    cs_str.enter_scope(cs_str.PROPAGATION_SCOPE)


def exit_propagation_scope():
    cs_str.exit_scope(cs_str.PROPAGATION_SCOPE)


def enter_trigger_scope():
    """
    Enter trigger scope

    While in trigger scope, prevent analysis inside of any other trigger
    methods that get called.
    """
    cs_str.enter_scope(cs_str.TRIGGER_SCOPE)


def exit_trigger_scope():
    cs_str.exit_scope(cs_str.TRIGGER_SCOPE)


@contextmanager
def contrast_scope():
    """Context manager for contrast scope"""
    enter_contrast_scope()
    try:
        yield
    finally:
        exit_contrast_scope()


@contextmanager
def propagation_scope():
    """Context manager for propagation scope"""
    enter_propagation_scope()
    try:
        yield
    finally:
        exit_propagation_scope()


@contextmanager
def trigger_scope():
    """Context manager for trigger scope"""
    enter_trigger_scope()
    try:
        yield
    finally:
        exit_trigger_scope()


def in_contrast_scope():
    return cs_str.in_scope(cs_str.CONTRAST_SCOPE)


def in_propagation_scope():
    return cs_str.in_scope(cs_str.PROPAGATION_SCOPE)


def in_trigger_scope():
    return cs_str.in_scope(cs_str.TRIGGER_SCOPE)


def in_scope():
    """Indicates we are in either contrast scope or propagation scope"""
    return in_contrast_scope() or in_propagation_scope()


@contextmanager
def pop_contrast_scope():
    """
    Context manager that pops contrast scope level and restores it when it exits

    Scope is implemented as a stack. If the thread is in contrast scope at the time
    this is called, the scope level will be reduced by one for the lifetime of the
    context manager. If the prior scope level was 1, this has the effect of temporarily
    disabling contrast scope. The original scope level will be restored when the
    context manager exits. If the thread is **not** already in contrast scope when this
    is called, it has no effect.
    """
    in_scope = in_contrast_scope()
    # This has no effect if we're not already in scope
    exit_contrast_scope()
    try:
        yield
    finally:
        # For safety, only restore scope if we were in it to begin with
        if in_scope:
            enter_contrast_scope()
