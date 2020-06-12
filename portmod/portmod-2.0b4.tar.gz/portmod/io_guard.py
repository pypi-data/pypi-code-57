# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module that provides a function to aid construction of safe
wrapper libraries around unsafe system libraries
"""
import inspect
import sys
from typing import List
from types import SimpleNamespace
from enum import Enum
from pathlib import Path


class Permissions(SimpleNamespace):
    def __init__(
        self,
        *,
        rw_paths: List[str] = [],
        ro_paths: List[str] = [],
        global_read: bool = False,
        network: bool = False,
    ):
        self.rw_paths = rw_paths
        self.ro_paths = ro_paths
        self.global_read = global_read
        self.network = network


class InvalidPermissions(PermissionError):
    def __init__(self, message, paths):
        self.message = message
        self.paths = paths

    def __str__(self):
        paths_string = "\n".join(self.paths)
        return f"{self.message}\nValid paths are:\n{paths_string}"


def get_permissions() -> Permissions:
    """Returns file permissions from within the context of this call"""
    for frame in inspect.stack(0):
        perms = frame.frame.f_locals.get("__PERMS")
        if perms is not None and isinstance(perms, Permissions):
            return perms

    return Permissions()


def _is_relative_to(path: Path, otherpath: Path) -> bool:
    """
    Returns true if and only if path is relative to otherpath
    (i.e. within the subtree)
    """
    try:
        path.relative_to(otherpath)
    except ValueError:
        return False

    return True


class IOType(Enum):
    """Enumerated type indicating type of file IO operation"""

    Read = 1
    Write = 2
    Exec = 3  # Note that in general we allow execution when we allow reads


def _check_call(path: str, operation: IOType):
    """
    Determines if the given IO operation is valid given the context of the function call
    """
    # Pathlib on windows may not resolve nonexistant paths properly
    # See https://bugs.python.org/issue38671
    if sys.platform == "win32" and hasattr(Path, "absolute"):
        realpath = Path(path).resolve().absolute()
    else:
        realpath = Path(path).resolve()

    # Default permissions prevent all file I/O
    permissions = get_permissions()

    displayed_path = path
    if str(realpath) != str(path):
        displayed_path = f"{path} (resolves to {realpath})"

    # We treat Exec and Read the same.
    if operation in (IOType.Read, IOType.Exec):
        if not permissions.global_read and not any(
            _is_relative_to(realpath, Path(allowed_path))
            for allowed_path in permissions.ro_paths + permissions.rw_paths
        ):
            raise InvalidPermissions(
                f"Path {displayed_path} is not readable!",
                permissions.ro_paths + permissions.rw_paths,
            )
    elif operation == IOType.Write:
        if not any(
            _is_relative_to(realpath, Path(allowed_path))
            for allowed_path in permissions.rw_paths
        ):
            raise InvalidPermissions(
                f"Path {displayed_path} is not writeable!", permissions.rw_paths
            )


def _wrap_path_read(func, default=None):
    if default is None:

        def wrapper(path, *args, **kwargs):
            _check_call(path, IOType.Read)
            return func(path, *args, **kwargs)

    else:

        def wrapper(path=default, *args, **kwargs):
            _check_call(path, IOType.Read)
            return func(path, *args, **kwargs)

    return wrapper


def _wrap_path_read_2(func):
    def wrapper(path1, path2, *args, **kwargs):
        _check_call(path1, IOType.Read)
        _check_call(path2, IOType.Read)
        return func(path1, path2, *args, **kwargs)

    return wrapper


def _wrap_path_write(func):
    def wrapper(path, *args, **kwargs):
        _check_call(path, IOType.Write)
        return func(path, *args, **kwargs)

    return wrapper


def _wrap_path_write_2(func):
    def wrapper(path1, path2, *args, **kwargs):
        _check_call(path1, IOType.Write)
        _check_call(path2, IOType.Write)
        return func(path1, path2, *args, **kwargs)

    return wrapper


def _wrap_path_read_write(func):
    def wrapper(src, dst, *args, **kwargs):
        _check_call(src, IOType.Read)
        _check_call(dst, IOType.Write)
        return func(src, dst, *args, **kwargs)

    return wrapper
