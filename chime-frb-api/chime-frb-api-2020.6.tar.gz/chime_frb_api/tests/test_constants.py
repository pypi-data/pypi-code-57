#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chime_frb_api import constants


def test_constants():
    assert isinstance(constants.k_DM, float)


def test_fpga_constants():
    assert isinstance(constants.FPGA_COUNTS_PER_SECOND, int)
