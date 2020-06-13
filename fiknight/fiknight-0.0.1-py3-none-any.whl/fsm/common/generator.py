#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (C) 2020  Trijeet Sethi
#This project is written under the GPL license. For the full GPL license, please see the base directory COPYING file or visit <https://www.gnu.org/licenses/>.

##Std Lib Imports:
import itertools

##Internal Imports:
from fiknight.fsm.core import *

def fullyConnected(machine_name: str, n_states: int, link_event: object = None) -> object:
    '''
    Function to build a fully connected state machine.

    The default behavior is to name states in arbitrary numerically ascending order, all linked with one default event.

    returns:
    a fully connected state machine with n states and 2-of-n transition events.

    '''

    ##Machine definition:
    fsm = Machine(name=machine_name)

    ##Define the states:
    states = [State(f"Stage_{i}", machine=fsm) for i in range(1,n_states+1)]

    ##Cycle through all of the states, putting transitions to every other state:
    for i in itertools.permutations(states, 2):
        i[0].addEvent(Event(name="baseTransition", destinations=i[1]))
    
    ##Cycle through all of the states, adding to the machine:
    for state in states:
        fsm.addState(state)

    return fsm

def sequentialMachine(machine_name: str, n_states: int, link_event: object = None) -> object:
    '''
    Function to build a fully connected state machine.

    The default behavior is to name states in arbitrary numerically ascending order, all linked with one default event.

    returns:
    a fully connected state machine with n states and 2-of-n transition events.

    '''

    ##Machine definition:
    fsm = Machine(name=machine_name)

    ##Define the states:
    states = [State(f"Stage_{i}", machine=fsm) for i in range(1,n_states+1)]        
    
    ##Cycle through all of the states, adding to the machine:
    for counter in range(len(states)):
        try:
            states[counter].addEvent(Event(name="baseTransition", destinations=states[counter+1]))
        except IndexError:
            states[counter].addEvent(Event(name="baseTransition", destinations=states[0]))
        fsm.addState(states[counter])

    return fsm