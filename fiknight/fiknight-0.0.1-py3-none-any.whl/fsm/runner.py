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

class Runner(object):
    '''Runner for taking logic changes and executing them on the display.'''
    
    def __init__(self, machine: object, display: object, **kwargs) -> None:
        self.machine = machine
        self.display = display
        self.__dict__.update((key, value) for key, value in kwargs.items())
        self.execution_stack = []
    
    def executeEvent(self, event: object) -> int:
        '''
        If the list is empty, just executes the single event. Otherwise, there is a chain of events, in which case behavior is to append and call executeChain().
        '''
        try:
            event.body()
            logging.debug(f"Executed event {self.name}")
            return 0
        except Exception as e:
                logging.debug(f"Error resolving {event.name} in the execution stack. Error encountered: {e}.")
                return -1


    def executeChain(self) -> int:
        '''
        Decides the order and executes the events sequentially, first sorting the events being triggered by priority level.
        '''
        for event in self.execution_stack[:]:
            try:
                event.trigger()
                self.execution_stack.pop(0)
            except Exception as e:
                logging.debug(f"Error resolving {event.name} in the execution stack. Error encountered: {e}.")
                return -1

        return 0

    def resolvePriority(self) -> int:
        '''
        Given a chain of events, helper function to decide the resolution order of the events.
        '''
        raise NotImplementedError
        return 0

