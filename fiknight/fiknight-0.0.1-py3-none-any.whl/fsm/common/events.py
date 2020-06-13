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

from ..core import Event

class onEnter(Event):
    '''
    Event that describes every state when it moves to active.
    '''
    def __init__(self, **kwargs):
        super(onEnter, self).__init__(**kwargs)
    
    def body(self) -> None:
        print("Entering state...")

class onExit(Event):
    '''
    Event that describes every state when it goes dormant.
    '''
    def __init__(self, **kwargs):
        super(onExit, self).__init__(**kwargs)
    
    def body(self) -> None:
        print("Leaving state...")

class clickEvent(Event):
        '''
        Event that describes every state when it moves to active.
        '''
        def __init__(self, **kwargs):
            super(clickEvent, self).__init__(**kwargs)
        
        def body(self) -> None:
            print("Button clicked. Beginning transition")

