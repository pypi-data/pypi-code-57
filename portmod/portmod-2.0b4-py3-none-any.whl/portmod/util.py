# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Optional
import os
import stat
import sys
from shutil import copy2, copystat, Error


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise  # pylint: disable=misplaced-bare-raise


def patch_dir(src, dst, *, symlinks=False, ignore=None, case_insensitive=False):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst):
        os.makedirs(dst)

    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        if case_insensitive:
            dstname = ci_exists(os.path.join(dst, name)) or os.path.join(dst, name)
        else:
            dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                patch_dir(
                    srcname,
                    dstname,
                    symlinks=symlinks,
                    ignore=ignore,
                    case_insensitive=case_insensitive,
                )
            else:
                copy2(srcname, dstname)
        except Error as err:
            errors.extend(err.args[0])
        except (IOError, OSError) as why:
            errors.append((srcname, dstname, str(why)))
    if sys.platform == "win32":
        try:
            copystat(src, dst)
        except WindowsError:  # pylint: disable=undefined-variable
            pass
        except OSError as why:
            errors.append((src, dst, str(why)))
    else:
        try:
            copystat(src, dst)
        except OSError as why:
            errors.append((src, dst, str(why)))

        if errors:
            raise Error(errors)


def ci_exists(path: str) -> Optional[str]:
    """
    Checks if a path exists, ignoring case.

    If the path exists but is ambiguous the result is not guaranteed
    """
    partial_path = "/"
    for component in os.path.normpath(os.path.abspath(path)).split(os.sep)[1:]:
        found = False
        for entryname in os.listdir(partial_path):
            if entryname.lower() == component.lower():
                partial_path = os.path.join(partial_path, entryname)
                found = True
                break
        if not found:
            return None

    if os.path.exists(partial_path):
        return partial_path

    return None


def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total
