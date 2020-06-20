#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `solvate_step` package."""

import solvate_step
import pytest
import re


@pytest.fixture
def instance():
    instance = solvate_step.Solvate()
    instance._id = (1,)
    return instance


def test_construction():
    """Simplest test that we can make a SOLVATE object"""
    instance = solvate_step.Solvate()
    assert str(type(instance)) == "<class 'solvate_step.solvate.Solvate'>"


def test_version():
    """Test that the object returns a version"""
    instance = solvate_step.Solvate()
    result = instance.version
    assert isinstance(result, str) and len(result) > 0


def test_git_revision():
    """Test that the object returns a git revision"""
    instance = solvate_step.Solvate()
    result = instance.git_revision
    assert isinstance(result, str) and len(result) > 0


def test_description_text_default(instance):
    """Test the default description text"""

    P = solvate_step.SolvateParameters()
    text = instance.description_text(P.values_to_dict())
    print(text)

    assert re.fullmatch(
        (
            r'Step 1: Solvate  [-+.0-9a-z]+\n'
            r'    Solvate the system making it a periodic system filled with '
            r'water, using the\n'
            r'    SPC model. The cell volume is fixed and will be filled to a '
            r'density of 1.0\n'
            r'    g/ml.'
        ),
        text
    ) is not None
