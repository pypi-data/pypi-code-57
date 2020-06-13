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

class TransitionTable(object):
    '''
    A state table is an attribute of a state.
    The logic is organized as follows:
    Machine organizes transitions and states.
    A transition belongs to a state.
    A state has many transitions.
    Each transition has a governing event.
    '''
    def __init__(self, state_ref: object) -> None:
        self.state_ref = state_ref
        self.next_states = {}
        self.destination_state = None
        ##Every state is endowed with two events: the enter and exit.
        
    
    def addEventTransition(self, event: object) -> int:
        '''
        Adds an Event to the transition list. 
        Each event must have a transition destination.
        The default behavior is for an Event to point to the table's State.
        '''
        if not event.destination:
            self.next_states[event.name] = self.state_ref
            return 0
        else:
            self.next_states[event.name] = event.destination
            return 1
            
    def transitionOverride(self, event: object, destination: object) -> int:
        '''Override the destination for a given event.'''
        try:
            #and check that it lives in the machine.
            assert destination.__class__==self.state_ref.__class__, "Destination must be a valid State" 
            self.next_states[event.name] = destination
            return 0
        except Exception as e:
            print(e)
            return -1
    
    def getTable(self) -> Dict[str, str]:
        return {k: v.name for k,v in self.next_states.items()}
    
    def showTable(self, max_display: int = 20) -> None:
        '''
        Shows a prettified table with destinations. 
        Max display controls length of both event and destination output.
        '''
        display_bar = " "*max_display
        print(f"\tEvent table for {self.state_ref.name}")
        print(f"Event{' '*(max_display-5)}\tDestination")
        for e, d in self.next_states.items():
            print(f"{e[:max_display]}{' '*(max_display-len(e))}\t{d.name[:max_display]}")
        return
    
    def setNextStates(self, destinations: List[object]) -> int:
        '''For each event in the handler, specify a destination; this behavior is one-to-one.'''
        if len(destinations) != len(self.event_list):
            j = "Expected %s Got %s."%(len(self.event_list), len(destinations))
            raise RuntimeError("Wrong number of states in transition list.\n%s"%j)
        for trigger, destination in zip(self.eventList, destinations):
            self.next_states[trigger] = destination
    
    def setState(self) -> None:
        self.state_ref.machine.current_state = self
