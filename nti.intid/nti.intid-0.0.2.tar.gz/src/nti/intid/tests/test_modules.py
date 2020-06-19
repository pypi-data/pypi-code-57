#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import sys
import types
import unittest

from zope.dottedname import resolve as dottedname


class TestModules(unittest.TestCase):

    def test_import_interfaces(self):
        dottedname.resolve('nti.intid.interfaces')

    def test_import_containers(self):
        location = 'nti.containers'
        if location not in sys.modules:
            for name in ('', '.datastructures'):
                new_loc = location + name
                sys.modules[new_loc] = types.ModuleType(new_loc, "Created module")
        dottedname.resolve('nti.intid.containers')
