# copyright 2003-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""Deprecation utilities."""

__docformat__ = "restructuredtext en"

import os
import sys
from warnings import warn
from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES


def lazy_wraps(wrapped):
    """
    This is the equivalent of the @wraps decorator of functools except it won't
    try to grabs attributes of the targeted function on decoration but on access.

    This is needed because of logilab.common.modutils.LazyObject.

    Indeed: if you try to decorate a LazyObject with @wraps, wraps will try to
    access attributes of LazyObject and this will trigger the attempt to import
    the module decorated by LazyObject which you don't want to do when you just
    want to mark this LazyObject has been a deprecated objet that you only
    wants to trigger if the user try to use it.

    Usage: like @wraps()

    >>> @lazy_wraps(function)
    >>> def wrapper(*args, **kwargs): ...
    """

    def update_wrapper_attributes(wrapper):
        def __getattribute__(self, attribute):
            if attribute in WRAPPER_ASSIGNMENTS:
                return getattr(wrapped, attribute)

            return super(self.__class__, self).__getattribute__(attribute)

        wrapper.__getattribute__ = __getattribute__

        for attribute in WRAPPER_UPDATES:
            getattr(wrapper, attribute).update(getattr(wrapped, attribute, {}))

        wrapper.__wrapped__ = wrapped

        return wrapper

    return update_wrapper_attributes


class DeprecationWrapper(object):
    """proxy to print a warning on access to any attribute of the wrapped object
    """

    def __init__(self, proxied, msg=None, version=None):
        self._proxied = proxied
        self._msg = msg
        self.version = version

    def __getattr__(self, attr):
        send_warning(self._msg, stacklevel=3, version=self.version)
        return getattr(self._proxied, attr)

    def __setattr__(self, attr, value):
        if attr in ("_proxied", "_msg"):
            self.__dict__[attr] = value
        else:
            send_warning(self._msg, stacklevel=3, version=self.version)
            setattr(self._proxied, attr, value)


def _get_module_name(number=1):
    """
    automagically try to determine the package name from which the warning has
    been triggered by loop other calling frames.

    If it fails to do so, return an empty string.
    """

    frame = sys._getframe()

    for i in range(number + 1):
        if frame.f_back is None:
            break

        frame = frame.f_back

    if frame.f_globals["__package__"]:
        return frame.f_globals["__package__"]

    file_name = os.path.split(frame.f_globals["__file__"])[1]

    if file_name.endswith(".py"):
        file_name = file_name[: -len(".py")]

    return file_name


def send_warning(reason, version=None, stacklevel=2, module_name=None):
    """Display a deprecation message only if the version is older than the
    compatible version.
    """
    if module_name and version:
        reason = "[%s %s] %s" % (module_name, version, reason)
    elif module_name:
        reason = "[%s] %s" % (module_name, reason)
    elif version:
        reason = "[%s] %s" % (version, reason)

    warn(reason, DeprecationWarning, stacklevel=stacklevel)


def callable_renamed(old_name, new_function, version=None):
    """use to tell that a callable has been renamed.

    It returns a callable wrapper, so that when its called a warning is printed
    telling what is the object new name.

    >>> old_function = renamed('old_function', new_function)
    >>> old_function()
    sample.py:57: DeprecationWarning: old_function has been renamed and is deprecated, uses
    new_function instead old_function()
    >>>
    """

    @lazy_wraps(new_function)
    def wrapped(*args, **kwargs):
        send_warning(
            (
                f"{old_name} has been renamed and is deprecated, uses {new_function.__name__} "
                f"instead"
            ),
            stacklevel=3,
            version=version,
            module_name=new_function.__module__,
        )
        return new_function(*args, **kwargs)

    return wrapped


renamed = callable_renamed(old_name="renamed", new_function=callable_renamed)


def argument_removed(old_argument_name, version=None):
    """
    callable decorator to allow getting backward compatibility for renamed keyword arguments.

    >>> @argument_removed("old")
    ... def some_function(new):
    ...     return new
    >>> some_function(old=42)
    sample.py:15: DeprecationWarning: argument old of callable some_function has been renamed and
    is deprecated, use keyword argument new instead some_function(old=42)
    42
    """

    def _wrap(func):
        @lazy_wraps(func)
        def check_kwargs(*args, **kwargs):
            if old_argument_name in kwargs:
                send_warning(
                    f"argument {old_argument_name} of callable {func.__name__} has been "
                    f"removed and is deprecated",
                    stacklevel=3,
                    version=version,
                    module_name=func.__module__,
                )
                del kwargs[old_argument_name]

            return func(*args, **kwargs)

        return check_kwargs

    return _wrap


@argument_removed("name")
@argument_removed("doc")
def callable_deprecated(reason=None, version=None, stacklevel=2):
    """Display a deprecation message only if the version is older than the
    compatible version.
    """

    def decorator(func):
        @lazy_wraps(func)
        def wrapped(*args, **kwargs):
            message = reason or 'The function "%s" is deprecated'
            if "%s" in message:
                message %= func.__name__

            send_warning(message, version, stacklevel + 1, module_name=func.__module__)
            return func(*args, **kwargs)

        return wrapped

    return decorator


deprecated = callable_renamed(old_name="deprecated", new_function=callable_deprecated)


def _generate_class_deprecated():
    class _class_deprecated(type):
        """metaclass to print a warning on instantiation of a deprecated class"""

        def __call__(cls, *args, **kwargs):
            message = getattr(cls, "__deprecation_warning__", "%(cls)s is deprecated") % {
                "cls": cls.__name__
            }
            send_warning(
                message,
                module_name=getattr(
                    cls, "__deprecation_warning_module_name__", _get_module_name(1)
                ),
                stacklevel=getattr(cls, "__deprecation_warning_stacklevel__", 4),
                version=getattr(cls, "__deprecation_warning_version__", None),
            )
            return type.__call__(cls, *args, **kwargs)

    return _class_deprecated


class_deprecated = _generate_class_deprecated()


def attribute_renamed(old_name, new_name, version=None):
    """
    class decorator to allow getting backward compatibility for renamed attributes.

    >>> @attribute_renamed(old_name="old", new_name="new")
    ... class SomeClass:
    ...     def __init__(self):
    ...         self.new = 42

    >>> some_class = SomeClass()
    >>> print(some_class.old)
    sample.py:15: DeprecationWarning: SomeClass.old has been renamed and is deprecated, use
    SomeClass.new instead
      print(some_class.old)
    42
    >>> some_class.old = 43
    sample.py:16: DeprecationWarning: SomeClass.old has been renamed and is deprecated, use
    SomeClass.new instead
      some_class.old = 43
    >>> some_class.old == some_class.new
    True
    """

    def _class_wrap(klass):
        reason = (
            f"{klass.__name__}.{old_name} has been renamed and is deprecated, use "
            f"{klass.__name__}.{new_name} instead"
        )

        def _get_old(self):
            send_warning(reason, stacklevel=3, version=version, module_name=klass.__module__)
            return getattr(self, new_name)

        def _set_old(self, value):
            send_warning(reason, stacklevel=3, version=version, module_name=klass.__module__)
            setattr(self, new_name, value)

        def _del_old(self):
            send_warning(reason, stacklevel=3, version=version, module_name=klass.__module__)
            delattr(self, new_name)

        setattr(klass, old_name, property(_get_old, _set_old, _del_old))

        return klass

    return _class_wrap


def argument_renamed(old_name, new_name, version=None):
    """
    callable decorator to allow getting backward compatibility for renamed keyword arguments.

    >>> @argument_renamed(old_name="old", new_name="new")
    ... def some_function(new):
    ...     return new
    >>> some_function(old=42)
    sample.py:15: DeprecationWarning: argument old of callable some_function has been renamed and
    is deprecated, use keyword argument new instead
      some_function(old=42)
    42
    """

    def _wrap(func):
        @lazy_wraps(func)
        def check_kwargs(*args, **kwargs):
            if old_name in kwargs and new_name in kwargs:
                raise ValueError(
                    f"argument {old_name} of callable {func.__name__} has been "
                    f"renamed to {new_name} but you are both using {old_name} and "
                    f"{new_name} has keyword arguments, only uses {new_name}"
                )

            if old_name in kwargs:
                send_warning(
                    f"argument {old_name} of callable {func.__name__} has been renamed "
                    f"and is deprecated, use keyword argument {new_name} instead",
                    stacklevel=3,
                    version=version,
                    module_name=func.__module__,
                )
                kwargs[new_name] = kwargs[old_name]
                del kwargs[old_name]

            return func(*args, **kwargs)

        return check_kwargs

    return _wrap


@argument_renamed(old_name="modpath", new_name="module_path")
@argument_renamed(old_name="objname", new_name="object_name")
def callable_moved(module_name, object_name, version=None, stacklevel=2):
    """use to tell that a callable has been moved to a new module.

    It returns a callable wrapper, so that when its called a warning is printed
    telling where the object can be found, import is done (and not before) and
    the actual object is called.

    NOTE: the usage is somewhat limited on classes since it will fail if the
    wrapper is use in a class ancestors list, use the `class_moved` function
    instead (which has no lazy import feature though).
    """
    message = "object %s has been moved to module %s" % (object_name, module_name)

    def callnew(*args, **kwargs):
        from logilab.common.modutils import load_module_from_name

        send_warning(
            message, version=version, stacklevel=stacklevel + 1, module_name=_get_module_name(1)
        )

        m = load_module_from_name(module_name)
        return getattr(m, object_name)(*args, **kwargs)

    return callnew


moved = callable_renamed(old_name="moved", new_function=callable_moved)


def class_renamed(old_name, new_class, message=None, version=None, module_name=None):
    """automatically creates a class which fires a DeprecationWarning
    when instantiated.

    >>> Set = class_renamed('Set', set, 'Set is now replaced by set')
    >>> s = Set()
    sample.py:57: DeprecationWarning: Set is now replaced by set
    s = Set()
    >>>
    """
    class_dict = {}
    if message is None:
        message = "%s is deprecated, use %s instead" % (old_name, new_class.__name__)

    class_dict["__deprecation_warning__"] = message
    class_dict["__deprecation_warning_version__"] = version
    class_dict["__deprecation_warning_stacklevel__"] = 3

    if module_name:
        class_dict["__deprecation_warning_module_name__"] = module_name
    else:
        class_dict["__deprecation_warning_module_name__"] = _get_module_name(1)

    try:
        return class_deprecated(old_name, (new_class,), class_dict)
    except (NameError, TypeError):
        # in case of conflicting metaclass situation
        class DeprecatedClass(new_class):
            def __init__(self, *args, **kwargs):
                msg = class_dict.get("__deprecation_warning__", f"{old_name} is deprecated")
                send_warning(
                    msg,
                    stacklevel=class_dict.get("__deprecation_warning_stacklevel__", 3),
                    version=class_dict.get("__deprecation_warning_version__", None),
                )
                super(DeprecatedClass, self).__init__(*args, **kwargs)

        return DeprecatedClass


def class_moved(new_class, old_name=None, message=None, version=None):
    """nice wrapper around class_renamed when a class has been moved into
    another module
    """
    if old_name is None:
        old_name = new_class.__name__

    if message is None:
        message = "class %s is now available as %s.%s" % (
            old_name,
            new_class.__module__,
            new_class.__name__,
        )

    module_name = _get_module_name(1)

    return class_renamed(old_name, new_class, message=message, module_name=module_name)
