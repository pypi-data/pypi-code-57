#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (C) 2020  Trijeet Sethi
#This project is written under the GPL license. For the full GPL license, please see the base directory COPYING file or visit <https://www.gnu.org/licenses/>.

##Std Lib Imports:
from functools import wraps
import itertools
import logging
import random
import types

##Non Std Imports:
from typing import Dict, List, Tuple, Union

class Display(object):
    '''Generic use object to hold the state of what is human facing. Acts as both a display and a controller for changing the inputs'''
    
    def __init__(self, machine: object) -> None:
        self.machine = machine
