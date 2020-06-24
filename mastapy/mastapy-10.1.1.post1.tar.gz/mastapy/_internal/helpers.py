'''helpers.py

This is the main utility module for the Masta Python API. This module is
required to be imported by users to interact with Masta.

Examples:
    The following code demonstrates how to initialise Masta for use with
    external Python scripts:

        >>> import mastapy as mp
        >>> mp.init('my_path_to_dll_folder')

    The following code demonstrates how to define a Masta property:

        >>> import mastapy as mp
        >>> from mp.system_model import Design
        >>> @masta_property(name='my_masta_property')
            def my_function(design:Design) -> int:
                return 0

    The following demonstrates how to start debugging a script launched
    from Masta:

        >>> import mastapy as mp
        >>> mp.start_debugging()

Attributes:
    _MASTA_PROPERTIES (dict): Internal use only. Contains property information
'''


import inspect
import sys
import os
import errno
import importlib
import warnings
import types

import clr
import ptvsd

from typing import Optional

from mastapy._internal.python_net import python_net_import
from mastapy._internal.custom_warnings import VersionWarning
from mastapy._internal.version import __api_version__


__all__ = (
    'masta_property', 'masta_before', 'masta_after', 'init',
    'start_debugging', 'load_mastafile')


_MASTA_PROPERTIES = dict()
_MASTA_SETTERS = dict()
_HOOK_NAME_TO_METHOD_DICT = dict()
_HAS_ATTEMPTED_MASTAFILE_LOAD = False

warnings.formatwarning = (
    lambda m, c, f, n, line=None:
    '{}:{}:\n{}: {}\n'.format(f, n, c.__name__, m))


class MastaPropertyException(Exception):
    '''MastaPropertyException

    Exception raised when there is an issue with a defined Masta property.
    '''


def _masta_property_setter(func):
    '''Setter for the MASTA property.

    Args:
        func: Wrapped function.
    '''

    func_spec = inspect.getfullargspec(func)
    annotations = func_spec.annotations
    arg_names = func_spec.args
    num_arguments = len(arg_names)
    num_typed_parameters = len(list(
        filter(lambda x: x != 'return', annotations)))

    if func.__name__ not in _MASTA_PROPERTIES:
        raise MastaPropertyException((
            'MASTA property setters must share the same name as their '
            'accompanying getter. No getter found called \'{}\'.').format(
                func.__name__))

    if num_arguments != 2:
        end = 'was' if num_arguments == 1 else 'were'
        raise MastaPropertyException((
            'MASTA property setters require 2 '
            'arguments, but {} {} found.').format(num_arguments, end))

    if num_typed_parameters != 2:
        raise MastaPropertyException(
            'Both MASTA property setter parameters must be typed.')

    setter_type = annotations[arg_names[0]]
    getter_type = _MASTA_PROPERTIES[func.__name__][1]
    if setter_type != getter_type:
        raise MastaPropertyException((
            'MASTA property setters and getters must have their first '
            'parameters defined with the same type.\n'
            'Got: {}\nExpected: {}').format(
                setter_type.__qualname__, getter_type.__qualname__))

    setter_value_type = annotations[arg_names[1]]
    getter_value_type = _MASTA_PROPERTIES[func.__name__][6]

    if not getter_value_type:
        raise MastaPropertyException((
            'MASTA property getter does not have a specified '
            'return type. Setter not expected.'))

    if setter_value_type != getter_value_type:
        raise MastaPropertyException((
            'MASTA property setters and getters must match their setting '
            'and returning types.\nGot: {}\nExpected: {}').format(
                setter_value_type.__qualname__,
                getter_value_type.__qualname__
            ))

    _MASTA_SETTERS[func.__name__] = func
    return func


def masta_property(
        name: str, *, description: Optional[str] = '',
        symbol: Optional[str] = '', measurement: Optional[str] = ''):
    '''Decorator method for creating MASTA properties in Python

    Args:
        name (str): The name of the property displayed in Masta
        description (str, optional): The description of what the property does.
        symbol (str, optional): The symbol for the property displayed in Masta.
        measurement (str, optional): Unit the property displayed in, in Masta.
    '''

    def _masta_property_decorator(func):
        func_spec = inspect.getfullargspec(func)
        args = func_spec.args
        annotations = func_spec.annotations
        num_typed_parameters = len(list(
            filter(lambda x: x != 'return', annotations)))

        if len(args) < 1 or num_typed_parameters < 1:
            raise MastaPropertyException((
                'MASTA property found without a typed parameter. '
                'MASTA properties must include one typed parameter.'))

        if len(args) > 1:
            raise MastaPropertyException((
                'Too many parameters found in MASTA property description. '
                'Only one is supported.'))

        parameter = annotations.get(args[0], None)
        returns = annotations.get('return', None)

        # If a function is made into a masta property, add the setter
        # decorator to the function spec.
        func.setter = _masta_property_setter

        if parameter:
            is_old_type = not parameter.__module__.startswith('mastapy')
            _MASTA_PROPERTIES[func.__name__] = (
                func, parameter, name, description, symbol,
                measurement, returns, is_old_type)

        return func

    return _masta_property_decorator


def load_mastafile():
    '''Executes a mastafile.py file from the local directory if found.'''

    global _HAS_ATTEMPTED_MASTAFILE_LOAD, _HOOK_NAME_TO_METHOD_DICT

    if 'mastafile' not in sys.modules and not _HAS_ATTEMPTED_MASTAFILE_LOAD:
        _HAS_ATTEMPTED_MASTAFILE_LOAD = True

        try:
            path_to_mastafile = os.path.realpath('mastafile.py')

            if not os.path.exists(path_to_mastafile):
                path_to_mastafile = next(
                    filter(
                        lambda x: os.path.exists(x),
                        map(
                            lambda x: os.path.join(x, 'mastafile.py'),
                            sys.path)),
                    None)

            os.chdir(os.path.dirname(path_to_mastafile))
            mastafile_loader = importlib.machinery.SourceFileLoader(
                'mastafile_module', path_to_mastafile)
            mastafile_module = types.ModuleType(mastafile_loader.name)
            mastafile_loader.exec_module(mastafile_module)
            _HOOK_NAME_TO_METHOD_DICT = dict(inspect.getmembers(
                mastafile_module, predicate=inspect.isfunction))
        except (IOError, OSError, TypeError):
            # No mastafile.py file has been found.
            # This is an optional feature, so ignore the error!
            pass


def masta_before(name: str):
    '''Decorator method for adding hooks to properties that are called before
    the property is called. Hooking methods must be defined in a mastafile.py
    file.

    Args:
        name (str): The name of the hooking method in mastafile.py
    '''

    def _masta_before_decorator(func):

        def _decorator(*args, **kwargs):
            hook = _HOOK_NAME_TO_METHOD_DICT.get(name, None)

            if not hook:
                raise MastaPropertyException(
                    'Failed to find hooking method \'{}\'.'.format(name))

            hook(*args, **kwargs)
            return func(*args, **kwargs)
        return _decorator

    return _masta_before_decorator


def masta_after(name: str):
    '''Decorator method for adding hooks to properties that are called after
    the property is called. Hooking methods must be defined in a mastafile.py
    file.

    Args:
        name (str): The name of the hooking method in mastafile.py
    '''

    def _masta_after_decorator(func):

        def _decorator(*args, **kwargs):
            hook = _HOOK_NAME_TO_METHOD_DICT.get(name, None)

            if not hook:
                raise MastaPropertyException(
                    'Failed to find hooking  method \'{}\'.'.format(name))

            x = func(*args, **kwargs)
            hook(*args, **kwargs)
            return x
        return _decorator

    return _masta_after_decorator


def _match_versions():
    utility_methods = python_net_import('SMT.MastaAPI', 'UtilityMethods')

    api_version = utility_methods.ReleaseVersionString.split(' ')[0]
    if api_version != __api_version__:
        warning_str = ('The mastapy and MASTA API versions do not match. '
                       'Please update either mastapy or MASTA.\n\n'
                       'Expected: {}\n'
                       'Actual  : {}\n').format(__api_version__, api_version)

        warnings.warn(warning_str, VersionWarning)


def init(path_to_dll_folder: str):
    '''Initialises the Python to MASTA API interop

    Args:
        path_to_dll_folder (str): Path to your MASTA folder that includes the
            MastaAPI.dll file
    '''

    if not path_to_dll_folder.endswith('MastaAPI.dll'):
        full_path = os.path.join(path_to_dll_folder, 'MastaAPI.dll')

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), full_path)

    clr.AddReference(full_path)
    utility_methods = python_net_import('SMT.MastaAPI', 'UtilityMethods')
    utility_methods.InitialiseApiAccess(path_to_dll_folder)

    _match_versions()


def start_debugging(
    host: Optional[str] = 'localhost', port: Optional[int] = 5678,
        timeout: Optional[int] = 10):
    '''Starts Python debugging using PTVSD

    Args:
        host (str, optional): Debug server IP address. Defaults to 'localhost'
        port (int, optional): Debug server port. Defaults to 5678
        timeout (int, optional): How long the program will wait for a debugger
            to attach in seconds. Defaults to 10

    Note:
        Execution will pause until either a debugger is attached to the Python
        process, or the timout expires.
    '''

    print((
        'Waiting for debugger to attach at {}:{} (execution will time out '
        'in {} seconds)...').format(host, port, timeout))
    ptvsd.enable_attach(address=(host, port), redirect_output=True)
    ptvsd.wait_for_attach(timeout)
