# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:08:33 2020

This all needs testing
@author: fergal
"""

import traceback
import datetime
import logging
import persist
import pdb
import sys
import os

def handle_exceptions(func):
    """Wrapper to handle exceptions differently in debug/production mode.

    If _debug=True is passed to the wrapped function as a keyword argument,
    and the function then throws an exception, the wrapper fires up the
    debugger to let you figure out the problem.

    If _debug is False (or not provided), the error is logged, then converted
    to a RuntimeError, to simplify the handling of the exception.

    Syntax errors are always thrown because they are "compile" time errors,
    not run time errors.

    Additional Arguments
    ------------
    When a function is decorated with @handle_exceptions, it accepts
    the following additional arguments, not included in the signatute.

    _debug
        (bool) If True, drop into the debugger when an exception is caught.
        Default is to save the state and throw an RuntimeError

    _outpath
        (str) Where to save state files

    _metadata_stack_level
        (int) Control where in the stack to collect the machine state from.
        The default value makes sense in most cases. Higher values allow
        you to save the state of functions that are higher in the stack.
        Typically you don't want to adjust this.

    Usage
    -----
    ::

        @handle_exceptions
        def foo(a, b):
            ...


        foo(a, b, _debug=True, _outpath="/path/to/debug/files")


    Note
    ----
    This function does introduce some confusion because wrapped functions
    accept arguments (_debug and _outpath) that aren't part of their signatude.
    I haven't found a clearer way to implement the desired behaviour.
    """

    def wrapper(*args, **kwargs):
        debug_mode = kwargs.pop('_debug', False)
        out_path = kwargs.pop('_outpath', '.')

        try:
            return func(*args, **kwargs)
        except SyntaxError as e:
            raise e
        except Exception as e:
            if debug_mode:
                print("Runtime Exception Thrown: %s: %s" %(type(e), e))
                pdb.post_mortem(sys.exc_info()[2])
                raise e
            else:
                logger = logging.getLogger(__name__)
                log_msg = create_log_message(func)
                logger.error(log_msg)

                kwargs['_metadata_stack_level'] = 4
                persist_state(logger, out_path, func, *args, **kwargs)
                raise RuntimeError(e)

    wrapper.__name__ == func.__name__
    return wrapper


def create_log_message(func):
    funcname = func.__name__
    exc_type, exc_value = sys.exc_info()[:2]
    msg = "Function %s raised %s: %s" %(funcname, exc_type, exc_value)
    return msg


def persist_state(logger, out_path, func,  *args, **kwargs):
    exc_type = sys.exc_info()[0]

    vals = dict()
    for i, val in enumerate(args):
        vals['arg%i' %(i)] = val
    vals.update(**kwargs)
    vals['exception'] = exc_type
    vals['backtrace'] = traceback.format_exc()

    per_file = pick_persistable_filename(out_path, func)
    try:
        logger.error("Persisting state to %s" %(per_file))
        persist.persist_to_file(per_file, **vals)
    except Exception:
        try:
            logger.error("Failed to persist. Setting strict to false")
            persist.persist_to_file(per_file, **vals, strict=False)
        except Exception as e:
            logger.critical("Failed to persist with strict=False")
            raise IOError(str(e))


def pick_persistable_filename(out_path, func):

    try:
        module = func.__module__
        filename = module.split('.')[-1]
    except AttributeError:
        filename = "nofile"

    funcname = func.__name__
    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fn = "%s_%s_%s.per" %(filename, funcname, ts)
    return os.path.join(out_path, fn)
