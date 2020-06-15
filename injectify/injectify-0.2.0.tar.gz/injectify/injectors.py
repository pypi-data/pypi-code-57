"""This module contains the model objects that power Injectify."""

import ast
import inspect
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import wraps

import astunparse

from .inspect_mate import extract_wrapped, getsource
from .structures import listify
from .utils import (
    parse_object,
    tryattrs,
    get_defining_class,
    caninject,
)


def count_visit(f):
    """Count objnumber of times a method has been called."""

    @wraps(f)
    def wrapper(self, node):
        if not hasattr(self, '_visit_counter'):
            self._visit_counter = defaultdict(int)

        if f.__name__ not in self._visit_counter:
            # B/c increment happens before function call,
            # initialize at -1
            self._visit_counter[f.__name__] = -1

        self._visit_counter[f.__name__] += 1
        r = f(self, node, self._visit_counter[f.__name__])
        return r

    return wrapper


class BaseInjector(ABC, ast.NodeTransformer):
    """An abstract class that identifies an injection point.

    Args:
        save_state: Whether or not the target object should allow multiple
            injections.
    """

    def __init__(self, save_state=True):
        self.save_state = save_state

    def prepare(self, target, handler):
        """Prepares the injector with the given parameters."""
        self.prepare_target(target)
        self.prepare_handler(handler)

    def prepare_target(self, target):
        """Prepares the given target object."""
        if caninject(target):
            raise TypeError('cannot inject to type {!r}', type(target))

        wrapped = extract_wrapped(target)
        self.target = wrapped or target

    def prepare_handler(self, handler):
        """Prepares the given handler function."""
        node = parse_object(handler)
        self.handler = node.body[0].body

    def visit_target(self):
        """Visit the AST node of the target object."""
        return self.visit(parse_object(self.target))

    def is_target_module(self):
        """Check whether the target object is a module."""
        return inspect.ismodule(self.target)

    def compile(self, tree):
        """Recompile the target object with the handler."""

        def inject_code(f):
            # Used to allow injection multiple times in a
            # single object, b/c inject.findsource() reads
            # the actual source file
            f.__inject_code__ = code if self.save_state else target_src

        target_name = self.target.__name__
        target_file = inspect.getfile(self.target)
        target_src = getsource(self.target)

        # Find the ast node with the same name as our target object and get the
        # source code
        node = next(x for x in tree.body if getattr(x, 'name', None) == target_name)
        if hasattr(node, 'decorator_list'):
            # Don't want to compile the decorators
            node.decorator_list = []
        code = astunparse.unparse(node)

        # Compile the new object
        _locals = {}
        exec(compile(code, target_file, 'exec'), _locals)
        compiled_obj = _locals[target_name]

        # Replace the old code with the new code
        try:
            # If function has code object, simply replace it
            self.target.__code__ = compiled_obj.__code__
            inject_code(self.target)
        except AttributeError:
            # Attempt to the class that the function is defined in
            meth_mod = get_defining_class(self.target)
            if not meth_mod:
                # If function is not defined in a class, or the target is not a function
                meth_mod = inspect.getmodule(self.target)

            inject_code(compiled_obj)
            setattr(meth_mod, target_name, compiled_obj)

    @abstractmethod
    def inject(self, node):
        """Abstract method that merges the handler into the target."""
        pass


class HeadInjector(BaseInjector):
    """An injector that injects code at the top of the object.

    **Usage**
        .. code-block::

            from injectify import inject, HeadInjector

            def file_write(filename, data):
                with open(filename, 'w') as f:
                    f.write(data)

            @inject(target=target, injector=HeadInjector())
            def handler():
                data = 'injected'

        After the injection happens, the function ``file_write`` has code that is
        equivalent to

        .. code-block::

            def file_write(filename, data):
                data = 'injected'
                with open(filename, 'w') as f:
                    f.write(data)
    """

    def visit_Module(self, node):
        """Visit a ``Module`` node.

        If the target object is a module then inject the handler in this node,
        else keep traversing. This is because the root of the AST will be this
        node for code parsed using the `exec` mode.
        """
        if self.is_target_module():
            return self._visit(node)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        """Visit a ``ClassDef`` node."""
        return self._visit(node)

    def visit_FunctionDef(self, node):
        """Visit a ``FunctionDef`` node."""
        return self._visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _visit(self, node):
        return ast.fix_missing_locations(self.inject(node))

    def inject(self, node):
        """Inject the handler at the top of the target object."""
        node.body.insert(0, self.handler)
        return node


class TailInjector(BaseInjector):
    """An injector that injects code at the bottom of the object.

    **Usage**
        .. code-block:: python

            import os.path
            from injectify import inject, TailInjector

            def file_read(filename):
                if os.path.exists(filename):
                    with open(filename_, 'r') as f:
                        return f.read()

            @inject(target=target, injector=TailInjector())
            def handler():
                raise FileNotFoundError('File does not exist')

        After the injection happens, the function ``file_open`` has code that is
        equivalent to

        .. code-block::

            def file_read(filename):
                if os.path.exists(filename):
                    with open(filename, 'r') as f:
                        return f.read()
                raise FileNotFoundError('File does not exist')
    """

    def visit_Module(self, node):
        """Visit a ``Module`` node.

        If the target object is a module then inject the handler in this node,
        else keep traversing. This is because the root of the AST will be this
        node for code parsed using the `exec` mode.
        """
        if self.is_target_module():
            return self._visit(node)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        """Visit a ``ClassDef`` node."""
        return self._visit(node)

    def visit_FunctionDef(self, node):
        """Visit a ``FunctionDef`` node."""
        return self._visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _visit(self, node):
        return ast.fix_missing_locations(self.inject(node))

    def inject(self, node):
        """Inject the handler at the bottom of the target object."""
        node.body.append(self.handler)
        return node


class ReturnInjector(BaseInjector):
    """An injector that injects code before a return statement.

    Note: The ``ReturnInjector`` can only be used when the target is a
    `function` or `method`.

    Args:
        ordinal: Optional zero-based index to choose specific point of injection.
            Multiple indices can be given in the form of a list.

    **Usage**
        .. code-block:: python

            import statistics
            from injectify import inject, ReturnInjector

            def stat(operation, seq):
                if operation == 'mean':
                    return statistics.mean(seq)
                elif operation == 'median':
                    return statistics.median(seq)
                elif operation == 'mode':
                    return staistics.mode(seq)

            @inject(target=target, injector=ReturnInjector(ordinal=[1,2]))
            def handler():
                seq = list(seq)
                seq.append(10)

        After the injection happens, the function ``stat`` has code that is
        equivalent to

        .. code-block::

            def stat(operation, seq):
                if operation == 'mean':
                    return statistics.mean(seq)
                elif operation == 'median':
                    seq = list(seq)
                    seq.append(10)
                    return statistics.median(seq)
                elif operation == 'mode':
                    seq = list(seq)
                    seq.append(10)
                    return staistics.mode(seq)
    """

    def __init__(self, ordinal=None, *args, **kwargs):
        self.ordinal = listify(ordinal)

        super().__init__(*args, **kwargs)

    @count_visit
    def visit_Return(self, node, visit_count):
        """Visit a ``Return`` node."""
        if not self.ordinal or visit_count in self.ordinal:
            return ast.copy_location(self.inject(node), node)
        self.generic_visit(node)
        return node

    def inject(self, node):
        """Inject the handler before each return statement in the target object."""
        return ast.Module(body=[self.handler, node])


class FieldInjector(BaseInjector):
    """An injector that injects code at a field's assignment.

    Args:
        field: The field to inject at.
        ordinal: Zero-based index to choose specific point of injection.
        insert: Where to insert the handler's code relative to the target.
            Options include 'before' and 'after'.

    **Usage**
        .. code-block:: python

            from injectify import inject, FieldInjector

            def get_rank(year):
                if year == 1:
                    rank = 'Freshman'
                elif year == 2:
                    rank = 'Sophomore'
                elif year == 3:
                    rank = 'Junior'
                else:
                    rank = 'Senor'
                return rank

            @inject(target=target,
                    injector=FieldInjector('rank', ordinal=3, insert='after'))
            def handler():
                rank = 'Senior'

        After the injection happens, the function ``stat`` has code that is
        equivalent to

        .. code-block::

            def get_rank(year):
                if year == 1:
                    rank = 'Freshman'
                elif year == 2:
                    rank = 'Sophomore'
                elif year == 3:
                    rank = 'Junior'
                else:
                    rank = 'Senor'
                    rank = 'Senior'
                return rank
    """

    def __init__(self, field, ordinal=None, insert=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.field = field
        self.ordinal = listify(ordinal)
        self.insert = insert
        self._field_counter = defaultdict(int)

    def visit_Assign(self, node):
        """Visit an ``Assign`` node."""
        field = self.field or self.target

        if any(field == tryattrs(t, 'id', 'attr') for t in node.targets):
            field_count = self._field_counter[field]
            self._field_counter[field] += 1
            if not self.ordinal or field_count in self.ordinal:
                return ast.copy_location(self.inject(node), node)
        self.generic_visit(node)
        return node

    def inject(self, node):
        """Inject the handler at the assignment of the given field in the
        target object."""
        if self.insert == 'after':
            return ast.Module(body=[node, self.handler])
        else:
            return ast.Module(body=[self.handler, node])


class NestedInjector(BaseInjector):
    """An injector that injects code in a nested function.

    Note: The ``NestedInjector`` can only be used when the target is a
    `function` or `method`.

    Args:
        nested: Name of the nested function.
        injector: Injector to use in the nested function.

    **Usage**
        .. code-block:: python

            from time import time
            from injectify import inject, FieldInjector

            def timing(f):
                def wrapper(*args, **kwargs):
                    ts = time()
                    result = f(*args, **kwargs)
                    te = time()
                    return result

            @inject(target=target,
                    injector=NestedInjector('wrapper', ReturnInjector()))
            def handler():
                print('func:{!r} args:[{!r}, {!r}] took: {:2.f} sec'.format(
                        f.__name__, args, kwargs, te-ts))

        After the injection happens, the function ``stat`` has code that is
        equivalent to

        .. code-block::

            def timing(f):
                def wrapper(*args, **kwargs):
                    ts = time()
                    result = f(*args, **kwargs)
                    te = time()
                    print('func:{!r} args:[{!r}, {!r}] took: {:2.f} sec'.format(
                        f.__name__, args, kwargs, te-ts))
                    return result
    """

    def __init__(self, nested, injector, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nested = nested
        self.injector = injector

    def prepare(self, target, handler):
        """Prepares the injector and the nested injector with the given
        parameters."""
        super().prepare(target, handler)
        self.injector.prepare(target, handler)

    def visit_FunctionDef(self, node):
        """Visit a ``FunctionDef`` node."""
        if node.name == self.nested:
            return ast.fix_missing_locations(self.inject(node))
        self.generic_visit(node)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def inject(self, node):
        """Inject the handler into the nested function with the given injector."""
        return self.injector.inject(node)
