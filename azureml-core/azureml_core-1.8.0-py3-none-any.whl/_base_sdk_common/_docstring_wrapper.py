# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import functools
import logging
import inspect


module_logger = logging.getLogger(__name__)
_experimental_link_msg = "and may change at any time. For more information, see (https://aka.ms/azuremlexperimental)."
_docstring_template = ".. note::" \
                      "    {0} {1}\n\n"
_class_msg = "This is an experimental class,"
_method_msg = "This is an experimental method,"


def _add_class_docstring(cls):
    """Add experimental tag to the class doc string"""
    def _add_class_warning(func=None):
        """Add warning message for class init"""
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            module_logger.warning("{0} {1}".format(_class_msg, _experimental_link_msg))
            return func(*args, **kwargs)
        return wrapped

    doc_string = _docstring_template.format(_class_msg, _experimental_link_msg)
    if cls.__doc__:
        cls.__doc__ = doc_string + cls.__doc__
    else:
        cls.__doc__ = doc_string + '>'
    cls.__init__ = _add_class_warning(cls.__init__)
    return cls


def _add_method_docstring(func=None):
    """Add experimental tag to the method doc string"""
    doc_string = _docstring_template.format(_method_msg, _experimental_link_msg)
    if func.__doc__:
        func.__doc__ = doc_string + func.__doc__
    else:
        # '>' is required. Otherwise the note section can't be generated
        func.__doc__ = doc_string + '>'

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        module_logger.warning("method {0}: {1} {2}".format(func.__name__, _method_msg, _experimental_link_msg))
        return func(*args, **kwargs)
    return wrapped


def experimental(wrapped):
    """Add experimental tag to a class or a method"""
    if inspect.isclass(wrapped):
        return _add_class_docstring(wrapped)
    elif inspect.isfunction(wrapped):
        return _add_method_docstring(wrapped)
    else:
        return wrapped
