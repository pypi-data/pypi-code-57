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
from .display import Display
from .event import Event, onEnter, onExit
from .runner import Runner
from .state import State
from .transition import TransitionTable

class Machine(object):
    '''Organizer for all of the states and transitions.'''
    
    def __init__(self, **kwargs) -> None:
        self.log_path = "./fsm_info.log"
        self.initial_state = None
        self.current_state = None
        self.destination_state = None
        self.__dict__.update((key, value) for key, value in kwargs.items())
        self.display = Display(machine=self)
        self.runner = Runner(machine=self, display=self.display)
        self.state_stack = []
        self.history = []
    
    def addState(self, state: object = None) -> int:
        
        if not state:
            state_number = len(self.state_stack)
            self.state_stack.append(State(name=f"state_{state_number}", machine=self))
        self.state_stack.append(state)
        
        if not self.current_state:
            self.current_state = self.state_stack[-1]
    
    def buildDiagram(self) -> int:
        raise NotImplementedError
    
    def getCurrentState(self) -> None:
        if not self.state:
            print("Machine has not been started.")
        print(self.state.name)
    
    def getHistory(self) -> str:
        print(f"There have been {len(history)} transitions. The most recent five states are:")
        print(self.history[-5:])
        return self.log_path

    def revertState(self) -> int:
        self.history.append(self.current_state.name)
        self.current_state = self.state_stack[-1]
        return 0
        
    def overrideTransition(self, destination: object) -> None:
        '''
        Only way to force move through a state that does not operate through the usual state transition.
        '''
        pass
    
    def transition(self) -> int:
        '''
        Move the machine from this state to the next.
        Events of onExit and onEntry trigger as warranted.
        '''
        self.current_state.resolveEvent('onExit')
        self.history.append(self.current_state.name)
        self.current_state = self.destination_state
        self.current_state.resolveEvent('onEntry')
        return 0