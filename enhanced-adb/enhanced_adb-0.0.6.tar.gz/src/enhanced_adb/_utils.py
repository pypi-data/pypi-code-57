import os
import platform
import sys
import subprocess
from pkg_resources import resource_filename

import whichcraft


def get_adb_exe():
    # 1. find in $PATH
    exe = whichcraft.which("adb")
    if exe and _is_valid_exe(exe):
        return exe

    plt = platform.system()

    if plt == "Windows":
        name = 'adb.exe'
    elif plt == "Linux":
        name = 'adb'
    elif plt == "Darwin":
        name = 'adb'

    # 2. use buildin adb
    bin_dir = resource_filename("enhanced_adb", "bin")
    exe = os.path.join(bin_dir, name)
    if os.path.isfile(exe) and _is_valid_exe(exe):
        return exe

    raise RuntimeError("No adb exe could be found. Install adb on your system")


def get_aapt_exe():
    # 1. find in $PATH
    exe = whichcraft.which("aapt")
    if exe and _is_valid_exe(exe):
        return exe

    # 2. use buildin adb
    bin_dir = resource_filename("enhanced_adb", "bin")

    plt = platform.system()

    if plt == "Windows":
        name = 'aapt.exe'
    elif plt == "Linux":
        name = 'aapt'
    elif plt == "Darwin":
        name = 'aapt_darwin'

    exe = os.path.join(bin_dir, name)
    if os.path.isfile(exe) and _is_valid_exe(exe):
        return exe

    raise RuntimeError("No aapt exe could be found. Install aapt on your system")


def _popen_kwargs(prevent_sigint=False):
    startupinfo = None
    preexec_fn = None
    creationflags = 0
    if sys.platform.startswith("win"):
        # Stops executable from flashing on Windows (see imageio/imageio-ffmpeg#22)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if prevent_sigint:
        # Prevent propagation of sigint (see imageio/imageio-ffmpeg#4)
        # https://stackoverflow.com/questions/5045771
        if sys.platform.startswith("win"):
            creationflags = 0x00000200
        else:
            preexec_fn = os.setpgrp  # the _pre_exec does not seem to work
    return {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "preexec_fn": preexec_fn,
    }


def _is_valid_exe(exe: str):
    cmd = [exe, "version"]
    try:
        with open(os.devnull, "w") as null:
            subprocess.check_call(
                cmd, stdout=null, stderr=subprocess.STDOUT, **_popen_kwargs()
            )
        return True
    except (OSError, ValueError, subprocess.CalledProcessError):
        return False


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


class SingletonMetaClass(type):
    def __init__(cls, name, bases, dic):
        super(SingletonMetaClass, cls) \
            .__init__(name, bases, dic)
        original_new = cls.__new__

        def my_new(clz, *args, **kwargs):
            if clz.instance is None:
                clz.instance = \
                    original_new(cls, *args, **kwargs)
            return cls.instance

        cls.instance = None
        cls.__new__ = staticmethod(my_new)
