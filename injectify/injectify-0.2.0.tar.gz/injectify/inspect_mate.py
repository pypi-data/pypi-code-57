"""
``inspect_mate`` provides more methods to get information about class attribute
than the standard library ``inspect``.

Includes tester function to check:

- is regular attribute
- is property style method
- is regular method, example: ``def method(self, *args, **kwargs)``
- is static method
- is class method

These are 5-kind class attributes.

and getter function to get each kind of class attributes of a class.
"""

import ast
import inspect
import functools
import linecache
from collections import deque
from types import FunctionType

from .exceptions import ClassFoundException


def is_attribute(klass, attr, value=None):
    """Test if a value of a class is attribute. (Not a @property style
    attribute)

    Args:
        klass: The class.
        attr: Attribute name.
        value: Attribute value.
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    if not inspect.isroutine(value):
        if not isinstance(value, property):
            return True
    return False


def is_property_method(klass, attr, value=None):
    """Test if a value of a class is @property style attribute.

    Args:
        klass: The class.
        attr: Attribute name.
        value: Attribute value.
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    if not inspect.isroutine(value):
        if isinstance(value, property):
            return True
    return False


def is_regular_method(klass, attr, value=None):
    """Test if a value of a class is regular method.

    Args:
        klass: The class.
        attr: Attribute name.
        value: Attribute value.
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    if inspect.isroutine(value):
        if not is_static_method(klass, attr, value) \
                and not is_class_method(klass, attr, value):
            return True

    return False


def is_static_method(klass, attr, value=None):
    """Test if a value of a class is static method.

    Args:
        klass: The class.
        attr: Attribute name.
        value: Attribute value.
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    for cls in inspect.getmro(klass):
        if inspect.isroutine(value):
            if attr in cls.__dict__:
                binded_value = cls.__dict__[attr]
                if isinstance(binded_value, staticmethod):
                    return True
    return False


def is_class_method(klass, attr, value=None):
    """Test if a value of a class is class method.

    Args:
        klass: The class.
        attr: Attribute name.
        value: Attribute value.
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    for cls in inspect.getmro(klass):
        if inspect.isroutine(value):
            if attr in cls.__dict__:
                binded_value = cls.__dict__[attr]
                if isinstance(binded_value, classmethod):
                    return True
    return False


def _get_members(klass, tester_func, return_builtin):
    """

    Args:
        klass: The class.
        tester_func: Function to test.
        allow_builtin: If ``False``, built-in variable or method such as
            ``__name__``, ``__init__`` will not be returned.
    """
    if not inspect.isclass(klass):
        raise ValueError

    pairs = list()
    for attr, value in inspect.getmembers(klass):
        if tester_func(klass, attr, value):
            if return_builtin:
                pairs.append((attr, value))
            else:
                if not (attr.startswith('__') or attr.endswith('__')):
                    pairs.append((attr, value))

    return pairs


get_attributes = functools.partial(
    _get_members, tester_func=is_attribute, return_builtin=False)
get_attributes.__doc__ = 'Get all class attributes members.'

get_property_methods = functools.partial(
    _get_members, tester_func=is_property_method, return_builtin=False)
get_property_methods.__doc__ = 'Get all property style attributes members.'

get_regular_methods = functools.partial(
    _get_members, tester_func=is_regular_method, return_builtin=False)
get_regular_methods.__doc__ = 'Get all non static and class method members'

get_static_methods = functools.partial(
    _get_members, tester_func=is_static_method, return_builtin=False)
get_static_methods.__doc__ = 'Get all static method attributes members.'

get_class_methods = functools.partial(
    _get_members, tester_func=is_class_method, return_builtin=False)
get_class_methods.__doc__ = 'Get all class method attributes members.'


def get_all_attributes(klass):
    """Get all attribute members (attribute, property style method)."""
    if not inspect.isclass(klass):
        raise ValueError

    pairs = list()
    for attr, value in inspect.getmembers(
            klass, lambda x: not inspect.isroutine(x)):
        if not (attr.startswith('__') or attr.endswith('__')):
            pairs.append((attr, value))
    return pairs


def get_all_methods(klass):
    """Get all method members (regular, static, class method)."""
    if not inspect.isclass(klass):
        raise ValueError

    pairs = list()
    for attr, value in inspect.getmembers(
            klass, lambda x: inspect.isroutine(x)):
        if not (attr.startswith('__') or attr.endswith('__')):
            pairs.append((attr, value))
    return pairs


def extract_wrapped(decorated):
    """Extract a wrapped method."""
    try:
        closure = (c.cell_contents for c in decorated.__closure__)
        return next((c for c in closure if isinstance(c, FunctionType)), None)
    except (TypeError, AttributeError):
        return


class _ClassFinder(ast.NodeVisitor):

    def __init__(self, qualname):
        self.stack = deque()
        self.qualname = qualname

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        self.stack.append('<locals>')
        self.generic_visit(node)
        self.stack.pop()
        self.stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        if self.qualname == '.'.join(self.stack):
            # Return the decorator for the class if present
            if node.decorator_list:
                line_number = node.decorator_list[0].lineno
            else:
                line_number = node.lineno

            # decrement by one since lines starts with indexing by zero
            line_number -= 1
            raise ClassFoundException(line_number)
        self.generic_visit(node)
        self.stack.pop()


def getsource(obj):
    """Get the source code of an object."""
    if inspect.isclass(obj):
        # From Python 3.9 inspect library
        obj = inspect.unwrap(obj)
        file = inspect.getsourcefile(obj)
        if file:
            # Invalidate cache if needed.
            linecache.checkcache(file)
        else:
            file = inspect.getfile(obj)
            # Allow filenames in form of "<something>" to pass through.
            # `doctest` monkeypatches `linecache` module to enable
            # inspection, so let `linecache.getlines` to be called.
            if not (file.startswith('<') and file.endswith('>')):
                raise OSError('source code not available')

        module = inspect.getmodule(obj, file)
        if module:
            lines = linecache.getlines(file, module.__dict__)
        else:
            lines = linecache.getlines(file)
        if not lines:
            raise OSError('could not get source code')

        qualname = obj.__qualname__
        source = ''.join(lines)
        tree = ast.parse(source)
        class_finder = _ClassFinder(qualname)
        try:
            class_finder.visit(tree)
        except ClassFoundException as e:
            line_number = e.args[0]
            return ''.join(inspect.getblock(lines[line_number:]))
        else:
            raise OSError('could not find class definition')
    else:
        return getattr(obj, '__inject_code__', inspect.getsource(obj))
