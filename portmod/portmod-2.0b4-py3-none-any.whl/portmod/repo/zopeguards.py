#############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################

# Note: All code (except comments) in this file was Originally taken from
#   https://github.com/zopefoundation/AccessControl
# Given that we need so little of AccessControl, we reproduce what is needed
# here rather than depend on it, given the size of both it and its dependency tree.

# flake8: noqa
# pylint: disable=all

valid_inplace_types = (list, set)


inplace_slots = {
    "+=": "__iadd__",
    "-=": "__isub__",
    "*=": "__imul__",
    "/=": (1 / 2 == 0) and "__idiv__" or "__itruediv__",
    "//=": "__ifloordiv__",
    "%=": "__imod__",
    "**=": "__ipow__",
    "<<=": "__ilshift__",
    ">>=": "__irshift__",
    "&=": "__iand__",
    "^=": "__ixor__",
    "|=": "__ior__",
}


def __iadd__(x, y):
    x += y
    return x


def __isub__(x, y):
    x -= y
    return x


def __imul__(x, y):
    x *= y
    return x


def __idiv__(x, y):
    x /= y
    return x


def __ifloordiv__(x, y):
    x //= y
    return x


def __imod__(x, y):
    x %= y
    return x


def __ipow__(x, y):
    x **= y
    return x


def __ilshift__(x, y):
    x <<= y
    return x


def __irshift__(x, y):
    x >>= y
    return x


def __iand__(x, y):
    x &= y
    return x


def __ixor__(x, y):
    x ^= y
    return x


def __ior__(x, y):
    x |= y
    return x


inplace_ops = {
    "+=": __iadd__,
    "-=": __isub__,
    "*=": __imul__,
    "/=": __idiv__,
    "//=": __ifloordiv__,
    "%=": __imod__,
    "**=": __ipow__,
    "<<=": __ilshift__,
    ">>=": __irshift__,
    "&=": __iand__,
    "^=": __ixor__,
    "|=": __ior__,
}


def protected_inplacevar(op, var, expr):
    """Do an inplace operation
    If the var has an inplace slot, then disallow the operation
    unless the var is a list.
    """
    if hasattr(var, inplace_slots[op]) and not isinstance(var, valid_inplace_types):
        try:
            cls = var.__class__
        except AttributeError:
            cls = type(var)
        raise TypeError(
            "Augmented assignment to %s objects is not allowed"
            " in untrusted code" % cls.__name__
        )
    return inplace_ops[op](var, expr)
