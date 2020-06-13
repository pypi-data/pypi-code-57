#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `berhoel.helper`.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
import time

# Third party libraries.
import toml
import pytest

from berhoel import helper

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

__date__ = "2020/05/09 12:49:50 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


@pytest.fixture
def base_path():
    "Return path to project base."
    return Path(__file__).parents[3]


@pytest.fixture
def py_project(base_path):
    "Return path of project `pyproject.toml`."
    return base_path / "pyproject.toml"


@pytest.fixture
def toml_inst(py_project):
    "Return `toml` instance of project `pyproject.toml`"
    return toml.load(py_project.open("r"))


def test_version(toml_inst):
    "Test for consistent version numbers."
    assert helper.__version__ == toml_inst["tool"]["poetry"]["version"]


def test_swirl(capsys):
    "Test swirler."
    swirl = helper.swirl()
    for expected in r"\|/-\|":
        next(swirl)
        res = capsys.readouterr()
        assert res.out == "{}\r".format(expected)


def test_count_with_message_1(capsys):
    "Test counter with life message."
    count = helper.count_with_msg()
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i == j
        assert res.out == "loop {} \r".format(i + 1)
        if i > 5:
            break


def test_count_with_message_2(capsys):
    "Test counter with life message."
    count = helper.count_with_msg(start=10)
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i + 10 == j
        assert res.out == "loop {} \r".format(i + 1)
        if i > 5:
            break


def test_count_with_message_3(capsys):
    "Test counter with life message."
    count = helper.count_with_msg(msg="msg")
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i == j
        assert res.out == "msg {} \r".format(i + 1)
        if i > 5:
            break


def test_count_with_message_4(capsys):
    "Test counter with life message."
    count = helper.count_with_msg("alt", 5)
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i + 5 == j
        assert res.out == "alt {} \r".format(i + 1)
        if i > 5:
            break


def test_process_msg_context(capsys):
    "Test process context."
    with helper.process_msg_context("do something"):
        res = capsys.readouterr()
        assert res.out == "do something...\r"
    res = capsys.readouterr()
    assert res.out == "do something...done\n"


def test_timed_process_msg_context_1(capsys):
    "Test timed process context."
    with helper.timed_process_msg_context("do something"):
        res = capsys.readouterr()
        time.sleep(1)
        assert res.out == "do something...\r"
    res = capsys.readouterr()
    assert res.out == "do something...done (0:00:01)\n"


def test_timed_process_msg_context_2(capsys):
    "Test timed process context."
    with helper.timed_process_msg_context(
        "do something", lambda t: "{:d}s".format(int(t))
    ):
        res = capsys.readouterr()
        time.sleep(1)
        assert res.out == "do something...\r"
    res = capsys.readouterr()
    assert res.out == "do something...done (1s)\n"


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
