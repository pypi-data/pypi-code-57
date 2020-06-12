# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Displays filesystem conflicts between mods
"""

import shutil
import subprocess
from portmod.vfs import get_vfs_dirs


def main():
    """
    Main executable for openmw-conflicts executable
    """
    mod_dirs = get_vfs_dirs()

    args = ["omwcmd", "file-conflicts", "--ignore", "txt,md"]
    args.extend(mod_dirs)

    if shutil.which("omwcmd"):
        subprocess.Popen(args).wait()
    else:
        print('Error: Could not find "dcv"')
