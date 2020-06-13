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