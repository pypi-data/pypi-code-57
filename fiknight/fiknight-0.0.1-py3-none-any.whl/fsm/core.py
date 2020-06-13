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


class Event(object):
    '''
    Base class for any state-dependent behaviors.
    '''
    
    def __init__(self, name: str, destinations: Union[object, List[object]] = None, weights: List[float] = None, priority: int = 1, **kwargs) -> None:
        self.name = name
        self.destinations = destinations
        self.destination_weights = weights
        self.priority = priority
        self.destination = self.resolveDestination()
        self.__dict__.update((key, value) for key, value in kwargs.items())
    
    
    def bindBody(self, new_body: object) -> None:
        '''
        Wrapper function that inserts the new body into the event.
        '''
        self.body = types.MethodType(new_body, self)

    def body(self) -> int:
        '''Template for actual event body.'''
        try:
            return -1
        except Exception as e:
            print(f"Encountered error {e} during execution of {self.name}")
    
    def resolveDestination(self) -> Union[None, object]:
        '''
        Each Event must have a single destination.
        If there are multiple possible destinations, the random element is removed here.
        Choice is default uniform over the choices, the Event accepts a weighted decision.
        '''
        if not self.destinations:
            return None
        if type(self.destinations)!=list:
            return self.destinations
        else:
            return random.choices(self.destinations, weights=self.destination_weights, k=1)[0]

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

class Display(object):
    '''Generic use object to hold the state of what is human facing. Acts as both a display and a controller for changing the inputs'''
    
    def __init__(self, machine: object) -> None:
        self.machine = machine

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