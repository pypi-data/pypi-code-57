# -*- coding: utf-8 -*-
"""rackio/state.py

This module implements all state machine classes.
"""
import logging

from inspect import ismethod

from statemachine import StateMachine, State

from .models import FloatField, IntegerField, BooleanField, StringField

from .engine import CVTEngine
from .logger import QueryLogger, LoggerEngine

FLOAT = "float"
INTEGER = "int"
BOOL = "bool"
STRING = "str"

READ = "read"
WRITE = "write"

def detailed_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    message =  'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

    return message


class TagBinding:

    tag_engine = CVTEngine()

    def __init__(self, tag, direction="read"):
        
        self.tag = tag
        self.direction = direction
        self.value = None

    def update(self):

        if self.direction == WRITE:

            self.tag_engine.write_tag(self.tag, self.value)

        if self.direction == READ:

            self.value = self.tag_engine.read_tag(self.tag)
    

class RackioStateMachine(StateMachine):

    tag_engine = CVTEngine()
    logger_engine = LoggerEngine()
    query_logger = QueryLogger()

    def __init__(self, name, **kwargs):
        
        super(RackioStateMachine, self).__init__()
        self.name = name
        self._tag_bindings = list()

        attrs = self.get_attributes()

        for key, value in attrs.items():

            try:

                if isinstance(value, TagBinding):
                    self._tag_bindings.append((key, value))
                    _value = self.tag_engine.read_tag(value.tag)

                    setattr(self, key, 0.0)

                if key in kwargs:
                    default = kwargs[key]
                else:
                    default = value.default
                    _type = value._type

                if default:
                    setattr(self, key, default)
                else:
                    if _type == FLOAT:
                        setattr(self, key, 0.0)
                    elif _type == INTEGER:
                        setattr(self, key, 0)
                    elif _type == BOOL:
                        setattr(self, key, False)
                    elif _type == STRING:
                        setattr(self, key, "")
            except:
                continue

        self.attrs = attrs
    
    def get_states(self):

        return [state.identifier for state in self.states]
    
    @classmethod
    def get_attributes(cls):

        result = dict()
        
        props = cls.__dict__

        for key, value in props.items():

            if key in ["states", "transitions", "states_map", "_loop", "get_attributes", "_tag_bindings"]:
                continue
            if hasattr(value, '__call__'):
                continue
            if isinstance(value, cls):
                continue
            if isinstance(value, State):
                continue
            if not ismethod(value):

                if not "__" in key:
                    result[key] = value

        return result

    def _update_tags(self, direction=READ):

        for attr, _binding in self._tag_bindings:

            try:
                if direction == READ and _binding.direction == READ:
                
                    tag = _binding.tag
                    value = self.tag_engine.read_tag(tag)
                    value = setattr(self, attr, value)
                
                elif direction == WRITE and _binding.direction == WRITE:
                    tag = _binding.tag
                    value = getattr(self, attr)
                    self.tag_engine.write_tag(tag, value)
            
            except Exception as e:
                error = str(e)
                logging.error("Machine - {}:{}".format(self.name, error))


    def _loop(self):

        try:
            state_name = self.current_state.identifier.lower()
            method_name = "while_" + state_name

            if method_name in dir(self):
                update = getattr(self, '_update_tags')
                method = getattr(self, method_name)
                
                # update tag read bindings
                update()

                # loop machine
                try:
                    method()
                except Exception as e:
                    error = str(e)
                    logging.error("Machine - {}:{}".format(self.name, error))
                    logging.error("Machine - {}:{}".format(self.name, detailed_exception()))

                #update tag write bindings
                update("write")

        except Exception as e:
            error = str(e)
            logging.error("Machine - {}:{}".format(self.name, error))
    
    def serialize(self):

        def is_serializable(value):

            if isinstance(value, float):
                return True

            if isinstance(value, int):
                return True

            if isinstance(value, bool):
                return True

            if isinstance(value, str):
                return True

            return False

        def ismodel_instance(obj):

            for cls in [FloatField, IntegerField, BooleanField, StringField]:
                if isinstance(obj, cls):
                    return True
            return False

        result = dict()

        result["state"] = self.current_state.identifier

        states = self.get_states()
        checkers = ["is_" + state for state in states]
        methods = ["while_" + state for state in states]

        attrs = self.get_attributes()
        
        for key in attrs.keys():
            if key in checkers:
                continue
            if key in methods:
                continue
            if not ismodel_instance(attrs[key]):
                continue
            
            value = getattr(self, key)

            if not is_serializable(value):
                try:
                    obj = attrs[key]

                    if isinstance(obj, FloatField):
                        value = float(value)
                    elif isinstance(obj, IntegerField):
                        value = int(value)
                    elif isinstance(obj, BooleanField):
                        value = bool(value)
                    else:
                        value = str(value)

                except Exception as e:
                    
                    error = str(e)

                    logging.error("Machine - {}:{}".format(self.name, error))
                    value = None

            result[key] = value

        return result


class StateMachineManager:

    def __init__(self):

        self._machines = list()

    def append_machine(self, machine, interval=1):
        
        self._machines.append((machine, interval,))

    def get_machines(self):

        result = [_machine for _machine in self._machines]
        
        return result

    def get_machine(self, name):

        for _machine, interval in self._machines:

            if name == _machine.name:

                return _machine

    def start_machine(self, name):

        for _machine, interval in self._machines:

            if name == _machine.name:

                _machine.start()
                break

    def summary(self):

        result = dict()

        machines = [_machine.name for _machine, interval in self.get_machines()]

        result["length"] = len(machines)
        result["state_machines"] = machines

        return result
