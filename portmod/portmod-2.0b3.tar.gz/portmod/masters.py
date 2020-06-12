# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import shutil
import subprocess
import shlex
import re
import sys
from pkg_resources import parse_version
from functools import lru_cache


@lru_cache()
def check_dependency():
    omwcmd = shutil.which("omwcmd")
    if not omwcmd:
        raise Exception("Cannot find omwcmd executable")

    try:
        if sys.platform == "win32":
            cmd = "{} --version".format(omwcmd)
        else:
            cmd = shlex.split("{} --version".format(omwcmd))
        output = subprocess.check_output(cmd)
        version = parse_version(re.sub(r"^[^\d]*", "", output.decode("ascii")))

        if version < parse_version("0.2"):
            raise Exception(
                "this version of Portmod requires omwcmd version >= 0.2. "
                f"Currently installed: {version}"
            )
    except subprocess.CalledProcessError:
        raise Exception("this version of Portmod requires omwcmd version >= 0.2")


def get_masters(file):
    """
    Detects masters for the given file
    """
    check_dependency()

    _, ext = os.path.splitext(file)
    if re.match(r"\.(esp|esm|omwaddon|omwgame)", ext, re.IGNORECASE):
        omwcmd = shutil.which("omwcmd")

        if sys.platform == "win32":
            cmd = '{} masters "{}"'.format(omwcmd, file)
        else:
            cmd = shlex.split('{} masters "{}"'.format(omwcmd, file))

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, err) = process.communicate()
        if err:
            raise Exception(err)

        result = output.decode("utf-8", errors="ignore").rstrip("\n")
        if result:
            return set(result.split("\n"))
    return set()
