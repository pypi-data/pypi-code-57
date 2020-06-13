#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `berhoel.helper.check_args`.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Third party libraries.
import pytest

from berhoel.helper.check_args import ArgError, CheckArgs, check_args

__date__ = "2020/04/25 21:06:15 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


class Samp(CheckArgs):
    default = (("A", "A"), ("B", "B"), ("C", ("C", 1, 2)))

    def __init__(self, *data, **kw):
        CheckArgs.__init__(self, *data, **kw)

    def __call__(self):
        return (self.args["A"], self.args["B"], self.args["C"])


def test_samp_1():
    probe = Samp(A=34)
    assert probe() == (34, "B", ("C", 1, 2))


def test_samp_2():

    probe = Samp(34, "HALLO")
    assert probe() == (34, ("HALLO"), ("C", 1, 2))


def test_samp_3():
    with pytest.raises(ArgError):
        Samp(D=34)


def tst(*data, **kw):
    default = (("A", "A"), ("B", "B"), ("C", ("C", 1, 2)))
    return check_args(default, data, kw, "tst")


def test_tst_0():
    assert tst() == {"A": "A", "B": "B", "C": ("C", 1, 2)}


def test_tst_1():
    assert tst(A=34) == {"A": 34, "B": "B", "C": ("C", 1, 2)}


def test_tst_2():
    tst(34, B=22) == {"A": 34, "B": 22, "C": ("C", 1, 2)}


def test_tst_3():
    tst(34) == {"A": 34, "B": "B", "C": ("C", 1, 2)}


def test_tst_4():
    with pytest.raises(ArgError):
        tst(D=34)


def test_tst_5():
    with pytest.raises(ArgError):
        tst(34, 35, B=36)


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
