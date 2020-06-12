# a Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Helper functions for interacting with the Windows registry
"""

from typing import Optional

import os
import sys
from portmod.io_guard import _check_call, IOType

if sys.platform == "win32":
    import winreg  # pylint: disable=import-error
    from winreg import (  # noqa  # pylint: disable=unused-import,import-error
        HKEY_LOCAL_MACHINE,
        HKEY_CLASSES_ROOT,
        HKEY_CURRENT_USER,
        HKEY_USERS,
        HKEY_CURRENT_CONFIG,
    )

    def read_reg(key: str, subkey: str, entry: Optional[str] = None):
        """
        Reads the given registry
        """
        # Registry reads should always be considered potentially dangerous reads
        _check_call(os.sep, IOType.Read)

        with winreg.ConnectRegistry(None, key) as reg:
            try:
                rawkey = winreg.OpenKey(
                    reg, subkey, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY
                )
            except FileNotFoundError:
                try:
                    rawkey = winreg.OpenKey(
                        reg, subkey, access=winreg.KEY_READ | winreg.KEY_WOW64_32KEY
                    )
                except FileNotFoundError:
                    return None
            try:
                i = 0
                while True:
                    name, value, _ = winreg.EnumValue(rawkey, i)
                    if entry is None:
                        return value
                    if name == entry:
                        return value
                    i += 1
            except WindowsError:  # pylint: disable=undefined-variable
                return None
