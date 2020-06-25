# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017, 2018, 2019, 2020 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
"""
__docformat__ = 'restructuredtext'

__all__ = [
    'bind',
]

import types

from .memory import *
from .message import *
from .runtime import *

#from routine import *
#from point import *
#from machine import *

class Point: pass
class Dispatch: pass
class Stateless: pass
class StateMachine: pass

def bind(object_type, *args, **kw_args):
    '''The function that registers the specified class.

    :param object_type: the application class to be registered
    :type object_type: ``Message``-derived class
    :param args: optional positional args 
    :type args: list
    :param kw_args: optional key-word args 
    :type kw_args: dict
    '''
    # Damn line length constraint.
    cp1 = 'Cannot bind class "%s"; unknown machine type.'
    cp2 = 'Cannot bind; not a routine, machine, point or message.'
    if isinstance(object_type, types.FunctionType):
        pass    # bind_routine(object_type, *args, **kw_args)
    elif issubclass(object_type, Point):
        if issubclass(object_type, Dispatch):
            if issubclass(object_type, Stateless):
                pass #bind_stateless(object_type, *args, **kw_args)
            elif issubclass(object_type, StateMachine):
                pass #bind_statemachine(object_type, *args, **kw_args)
            else:
                raise MessageRegistrationError(object_type.__name__, 'unknown machine')
        else:
            pass # bind_point(object_type, *args, **kw_args)
    elif issubclass(object_type, Message):
        bind_message(object_type, *args, **kw_args)
    else:
        raise MessageRegistrationError(object_type.__name__, 'unknown')
