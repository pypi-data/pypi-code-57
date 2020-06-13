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

##Internal imports:
from .transition import TransitionTable
from .event import Event, onEnter, onExit

class State(object):
    '''
    Main object maintaining each state and its corresponding events.
    '''
    
    def __init__(self, name: str, machine: object, **kwargs) -> None:
        self.name = name
        self.events = {}
        self.transitions = TransitionTable(self)
        self.machine = machine
        self.belonging = machine.__class__
        self.n_events = 0
        self.__dict__.update((key, value) for key, value in kwargs.items())
        self.addEvent(onEnter(name="onEntry"))
        self.addEvent(onExit(name="onExit"))
    
    def addEvent(self, event: object) -> int:
        '''
        Takes an Event (defined in module) and attaches it to the State.
        Events must have a unique identifier for a name.
        '''
        ##Give it an internal name if not supplied:
        if not hasattr(event, "name"):
            event.name = f"{self.name}_{self.n_events}"
        self.events[event.name] = event
        self.n_events += 1
        
        self.transitions.addEventTransition(event)
        
        return 0
    
    def changeDestination(self, event_name: object) -> int:
        '''
        Internal function for changing the destination of the machine.
        '''
        self.machine.destination_state = self.transitions.next_states[event_name]
        if self.machine.destination_state is not self.machine.current_state:
            logging.debug(f"Transitioning to state {self.machine.destination_state.name}")
            self.machine.transition()

        return 0

    def setCycle(self) -> int:
        self.machine.state_stack.append(self)
        raise NotImplementedError
        return 0
    
    def resolveEvent(self, event_name: str) -> int:
        '''
        Resolve a state-dependent event.
        '''
        if event_name in self.events.keys():
            self.machine.runner.executeEvent(self.events[event_name])
            return 0
        else:
            logging.debug(f"No event with name {event_name} found")
            return -1

    def resolveEventTransition(self, event_name: str) -> int:
        '''
        Resolve a state-dependent event.
        '''
        if event_name in self.events.keys():
            self.machine.runner.executeEvent(self.events[event_name])
            self.changeDestination(event_name)
            return 0
        else:
            logging.debug(f"No event with name {event_name} found")
            return -1
