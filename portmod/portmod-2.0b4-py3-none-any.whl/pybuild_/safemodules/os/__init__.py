# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
A wrapper around os that provides safe versions of its functions for use within pybuilds
"""
import os
import importlib
from portmod.io_guard import (
    _check_call,
    IOType,
    _wrap_path_read,
    _wrap_path_write,
    _wrap_path_write_2,
    _wrap_path_read_write,
)

path = importlib.import_module("pybuild_.safemodules.os.path")
from os import (  # noqa  # pylint: disable=unused-import
    environ,
    chdir,
    getcwd,
    getenv,
    get_exec_path,
    getlogin,
    get_terminal_size,
    terminal_size,
    F_OK,
    R_OK,
    W_OK,
    X_OK,
    getcwdb,
    supports_dir_fd,
    supports_fd,
    supports_follow_symlinks,
    cpu_count,
    curdir,
    pardir,
    sep,
    altsep,
    extsep,
    pathsep,
    defpath,
    linesep,
    devnull,
    urandom,
)

# Unavailable on OSX:
#    getresuid,
#    getresgid,
#    XATTR_SIZE_MAX,
#    XATTR_CREATE,
#    XATTR_REPLACE,
#    getrandom,
#    GRND_NONBLOCK,
#    GRND_RANDOM,


def access(filepath, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True):
    if mode in (os.F_OK, os.R_OK):
        try:
            _check_call(filepath, IOType.Read)
        except PermissionError:
            return False
    elif mode == os.W_OK:
        try:
            _check_call(filepath, IOType.Write)
        except PermissionError:
            return False
    elif mode == os.X_OK:
        try:
            _check_call(filepath, IOType.Exec)
        except PermissionError:
            return False
    else:
        return False
    return os.access(
        filepath,
        mode,
        dir_fd=dir_fd,
        effective_ids=effective_ids,
        follow_symlinks=follow_symlinks,
    )


chmod = _wrap_path_write(os.chmod)
link = _wrap_path_read_write(os.link)
listdir = _wrap_path_read(os.listdir, ".")
lstat = _wrap_path_read(os.lstat)
mkdir = _wrap_path_write(os.mkdir)
makedirs = _wrap_path_write(os.makedirs)
readlink = _wrap_path_read(os.readlink)
remove = _wrap_path_write(os.remove)
rename = _wrap_path_write_2(os.rename)
# Note: Banned as they may write to parent directories
# removedirs(name):
# renames(old, new):
replace = _wrap_path_write_2(os.replace)
rmdir = _wrap_path_write(os.rmdir)
scandir = _wrap_path_read(os.scandir, ".")
stat = _wrap_path_read(os.stat)
symlink = _wrap_path_read_write(os.symlink)
truncate = _wrap_path_write(os.truncate)
unlink = _wrap_path_write(os.unlink)
utime = _wrap_path_write(os.utime)
walk = _wrap_path_read(os.walk)

# Unavailable on OSX:
# fwalk = _wrap_path_read(os.fwalk)
# getxattr = _wrap_path_read(os.getxattr)
# listxattr = _wrap_path_read(os.listxattr)
# removexattr = _wrap_path_write(os.removexattr)
# setxattr = _wrap_path_write(os.setxattr)
