'''python_net.py

Utility module for importing python net modules.
'''


import sys
from typing import Optional


def python_net_import(module: str, class_name: Optional[str] = None):
    ''' Dynamically imports a Python.NET module

    Args:
        module (str): Module path
        class_name (str, optional): class name
    '''

    try:
        # PythonNet only works if you use __import__ for dynamic imports.
        # It does not work for importlib.import_module. Also for some reason,
        # __import__ is not working properly. Providing fromlist=[None] still
        # returns the root package. Instead I am looping getattr until we're
        # at the right-most module.
        path = list(filter(None, module.split('.')))
        m = __import__(path[0])
        for p in path[1:]:
            m = getattr(m, p)
        if class_name:
            m = getattr(m, class_name)
    except ImportError:
        raise Exception((
            'MastaPy has not been initialised. Call \'mastapy.init()\' '
            'with the path to your MastaAPI.dll file.'))
    except Exception:
        raise Exception(
            'Failed to load {} from {}.'.format(class_name, module))

    return m
